"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import dataclasses as dtcl
import typing as h
from datetime import datetime as date_time_t

import PyQt6.QtWidgets as wdgt
from conf_ini_g.phase.specification.parameter.type import type_t
from logger_36 import LOGGER
from PyQt6.QtCore import QCoreApplication, QPoint, QRectF
from pyvispr.config.appearance.color import (
    BUTTON_BRUSH_STATE_DISABLED,
    BUTTON_BRUSH_STATE_DOING,
    BUTTON_BRUSH_STATE_DONE,
    BUTTON_BRUSH_STATE_TODO,
    INOUT_BRUSH_ACTIVE,
    INOUT_BRUSH_INACTIVE,
    LINK_PEN_EMPTY,
    LINK_PEN_FULL,
    NODE_BRUSH_RESTING,
    NODE_BRUSH_RUNNING,
    QBrush,
    QPen,
)
from pyvispr.constant.function import UNIQUE_NAME_INPUT
from pyvispr.constant.value import MSG_OUTPUT_SET, MSG_OUTPUT_UNSET, VALUE_NOT_SET
from pyvispr.flow.functional.graph import graph_t as graph_functional_t
from pyvispr.flow.functional.node import node_t as functional_t
from pyvispr.flow.functional.node import state_e
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.flow.visual.socket import active_socket_t
from pyvispr.flow.visual.value_ii import invalid_ii_value_t
from pyvispr.runtime.backend import SCREEN_BACKEND
from pyvispr.runtime.catalog import NODE_CATALOG
from sio_messenger.instance import MESSENGER
from str_to_obj.task.comparison import TypesAreCompatible

_json_description_h = tuple[
    tuple[tuple[str, str, dict[str, h.Any], float, float], ...],
    tuple[tuple, ...],
]


@dtcl.dataclass(slots=True, repr=False, eq=False)
class graph_t(wdgt.QGraphicsScene):
    functional: graph_functional_t = dtcl.field(
        init=False, default_factory=graph_functional_t
    )
    nodes: list[node_t] = dtcl.field(init=False, default_factory=list)
    links: list[link_t] = dtcl.field(init=False, default_factory=list)

    # TODO: Better management is required.
    _active_socket: active_socket_t = dtcl.field(
        init=False, default_factory=active_socket_t
    )

    def __post_init__(self) -> None:
        """"""
        wdgt.QGraphicsScene.__init__(self)
        # TODO: Does not seem to have an effect:
        #     self.setSceneRect(QRectF(-500, -500, 1000, 1000))

        SCREEN_BACKEND.CreateMessageCanal(self, "changed", self.UpdateLinks)

        MESSENGER.AddCanal(state_e.disabled, self.AcknowledgeDisabled)
        MESSENGER.AddCanal(state_e.todo, self.AcknowledgeNeedsRunning)
        MESSENGER.AddCanal(state_e.doing, self.AcknowledgeRunningStarted)
        MESSENGER.AddCanal(state_e.done, self.AcknowledgeRunningEnded)
        MESSENGER.AddCanal(MSG_OUTPUT_SET, self.AcknowledgeLinkFull)
        MESSENGER.AddCanal(MSG_OUTPUT_UNSET, self.AcknowledgeLinkEmpty)

    @classmethod
    def __NewFromJsonDescription__(cls, description: _json_description_h, /) -> graph_t:
        """"""
        output = cls()

        nodes, links = description

        for name, unique_name, ii_values, position_x, position_y in nodes:
            output.AddNode(name)
            node = output.nodes[-1]
            node.functional.unique_name = unique_name
            node.SetUniqueNameFromFunctional()
            for input_name, value in ii_values.items():
                node.SetIIValue(input_name, value, output.functional.InvalidateNode)
            node.setPos(position_x, position_y)

        for source, target, *sockets in links:
            for node in output.nodes:
                if node.functional.unique_name == source:
                    source = node
                elif node.functional.unique_name == target:
                    target = node
                if isinstance(source, node_t) and isinstance(target, node_t):
                    break
            for output_name, input_name in sockets:
                output.AddLink(source, output_name, target, input_name)

        return output

    def __DescriptionForJSON__(self) -> _json_description_h:
        """"""
        return (
            tuple(
                (
                    _elm.functional.description.name,
                    _elm.functional.unique_name,
                    _elm.IIValue(self.functional),
                    _elm.x(),
                    _elm.y(),
                )
                for _elm in self.nodes
            ),
            tuple(
                (
                    _elm.source_node.functional.unique_name,
                    _elm.target_node.functional.unique_name,
                )
                + _elm.UnderlyingFunctionals(self.functional)
                for _elm in self.links
            ),
        )

    def AddNode(self, name: str, /) -> None:
        """"""
        try:
            description = NODE_CATALOG.NodeDescription(name)
        except ValueError:
            return

        if description.requires_completion:
            LOGGER.warning(f"Node {description.name} requires completion")

        node = functional_t.NewForDescription(
            description, self.functional.node_unique_names
        )
        self.functional.append(node)

        node = node_t.NewForFunctional(node)
        self.nodes.append(node)

        self.clearSelection()  # Otherwise the newly created visual node replaces the selection.
        self.addItem(node)
        self.addItem(node.ii_dialog)

    def AddLinkMaybe(
        self, node: node_t, node_is_source: bool, position: QPoint, /
    ) -> None:
        """"""
        if self._active_socket.node is None:
            functional = node.functional
            if node_is_source:
                sockets = functional.description.outputs
                possible_names = functional.description.output_names
                button = node.out_btn
            else:
                sockets = functional.description.inputs
                possible_names = tuple(
                    _nme
                    for _nme in functional.inputs
                    if self.functional.links.InputSocketIsFree(functional, _nme)
                )
                button = node.in_btn
            possible_names = tuple(
                filter(lambda _elm: _elm != UNIQUE_NAME_INPUT, possible_names)
            )
            if possible_names.__len__() > 1:
                selected = _SocketSelection(possible_names, position)
            elif possible_names.__len__() > 0:
                selected = possible_names[0]
            else:
                selected = None
            if selected is not None:
                stripe = sockets[selected]
                if not node_is_source:
                    stripe = stripe.type
                self._active_socket.node = node
                self._active_socket.is_source = node_is_source
                self._active_socket.name = selected
                self._active_socket.type = stripe
                button.setBrush(INOUT_BRUSH_ACTIVE)

            return

        same_kind = (node_is_source and self._active_socket.is_source) or not (
            node_is_source or self._active_socket.is_source
        )

        if node is self._active_socket.node:
            if same_kind:
                if node_is_source:
                    button = self._active_socket.node.out_btn
                else:
                    button = self._active_socket.node.in_btn
                self._active_socket.node = None
                button.setBrush(INOUT_BRUSH_INACTIVE)
            return

        if same_kind:
            return

        current = active_socket_t(node=node)
        current_functional = node.functional
        if node_is_source:
            source = current
            target = self._active_socket
            possible_names = tuple(
                _nme
                for _nme, _tpe in current_functional.description.outputs.items()
                if _TypesAreCompatible(_tpe, target.type)
            )
        else:
            source = self._active_socket
            target = current
            possible_names = tuple(
                _nme
                for _nme in current_functional.inputs
                if self.functional.links.InputSocketIsFree(current_functional, _nme)
                and _TypesAreCompatible(
                    current_functional.description.inputs[_nme].type,
                    source.type,
                )
            )
        possible_names = tuple(
            filter(lambda _elm: _elm != UNIQUE_NAME_INPUT, possible_names)
        )
        if (n_names := possible_names.__len__()) == 0:
            return

        if n_names > 1:
            selected = _SocketSelection(possible_names, position)
        else:
            selected = possible_names[0]
        if selected is None:
            return

        if node_is_source:
            source.name = selected
            button = target.node.in_btn
        else:
            target.name = selected
            button = source.node.out_btn
        self.AddLink(source.node, source.name, target.node, target.name)
        self._active_socket.node = None
        button.setBrush(INOUT_BRUSH_INACTIVE)

    def AddLink(
        self,
        source: node_t,
        output_name: str,
        target: node_t,
        input_name: str,
        /,
    ) -> None:
        """"""
        self.functional.AddLink(
            source.functional, output_name, target.functional, input_name
        )
        found = None
        for link in self.links:
            if (link.source_node is source) and (link.target_node is target):
                found = link
                break
        if found:
            found.SetTooltip(self.functional)
        else:
            link = link_t(
                source_node=source,
                source_point=source.output_anchor_coordinates,
                target_node=target,
                target_point=target.input_anchor_coordinates,
                graph=self.functional,
            )
            self.links.append(link)
            self.addItem(link)
            self.addItem(link.arrow)

    def UpdateLinks(self, _: h.Sequence[QRectF], /) -> None:
        """"""
        for node in self.items():
            if isinstance(node, node_t) and node.position_has_changed:
                for link in self.links:
                    link.SetPath(
                        link.source_node.output_anchor_coordinates,
                        link.target_node.input_anchor_coordinates,
                    )
                node.position_has_changed = False

    def MergeWith(self, other: graph_t, /) -> None:
        """"""
        already_present = list(self.functional.node_unique_names)
        for node in other.nodes:
            if node.functional.unique_name in already_present:
                node.functional.SetUniqueName(already_present)
                already_present.append(node.functional.unique_name)
            node.SetUniqueNameFromFunctional()

        self.functional.extend(other.functional)

        self.nodes.extend(other.nodes)
        self.links.extend(other.links)
        for item in other.nodes + other.links:
            self.addItem(item)
        for node in other.nodes:
            self.addItem(node.ii_dialog)
        for link in other.links:
            self.addItem(link.arrow)

    def RemoveNode(self, node: node_t, /) -> None:
        """"""
        if node.ii_dialog is not None:
            node.ii_dialog.close()

        # Do not iterate directly on the list since it can be modified in the process.
        for link in tuple(self.links):
            if (link.source_node is node) or (link.target_node is node):
                self.RemoveLink(link)

        self.functional.RemoveNode(node.functional)
        self.nodes.remove(node)
        self.removeItem(node)
        self.removeItem(node.ii_dialog)

    def RemoveLink(
        self,
        link: link_t,
        /,
        output_name: str | None = None,
        input_name: str | None = None,
    ) -> None:
        """"""
        if output_name is None:  # input_name must also be None.
            for output_name, input_name in link.UnderlyingFunctionals(self.functional):
                self.functional.RemoveLink(
                    link.source_node.functional,
                    output_name,
                    link.target_node.functional,
                    input_name,
                )
            should_be_actually_removed = True
        else:  # Both names are not None.
            self.functional.RemoveLink(
                link.source_node.functional,
                output_name,
                link.target_node.functional,
                input_name,
            )
            should_be_actually_removed = (
                link.UnderlyingFunctionals(self.functional).__len__() == 0
            )

        if should_be_actually_removed:
            self.links.remove(link)
            self.removeItem(link)
            self.removeItem(link.arrow)
        else:
            link.SetTooltip(self.functional)

    def Clear(self) -> None:
        """"""
        # Do not iterate directly on the list since it is modified in the process.
        while self.nodes.__len__() > 0:
            self.RemoveNode(self.nodes[0])

    def AlignOnGrid(self) -> None:
        """"""
        for node in self.nodes:
            node.AlignOnGrid()

    def Run(self, /, *, script_accessor: h.TextIO = None) -> None:
        """"""
        should_save_as_script = script_accessor is not None
        if should_save_as_script:
            script_accessor.write(
                "from importlib import util\n"
                "from pathlib import Path as path_t\n"
                "from json_any import JsonStringOf, ObjectFromJsonString\n\n"
            )

        for node in self.nodes:
            functional = node.functional
            if functional.state is not state_e.todo:
                continue

            if should_save_as_script:
                description = functional.description
                script_accessor.write(
                    f"""path = path_t("{description.actual.path}").expanduser()
spec = util.spec_from_file_location(path.stem, path)
module = spec.loader.load_module(spec.name)
{description.module.__name__}_{description.actual.name} = getattr(module, "{description.actual.name}")\n
"""
                )

            for input_name, value in node.IIValue(self.functional).items():
                if not isinstance(value, invalid_ii_value_t):
                    # Issues are stored in value.issues for invalid_ii_value_t.
                    functional.SetInputValue(input_name, value)

        un_run_nodes = self.functional.Run(script_accessor=script_accessor)

        if should_save_as_script:
            self.functional.Invalidate()
            if un_run_nodes.__len__() > 0:
                un_run_nodes = ", ".join(
                    sorted(_elm.unique_name for _elm in un_run_nodes)
                )
                wdgt.QMessageBox.warning(
                    None,
                    "Workflow Saving Warning",
                    f"Workflow saving was incomplete "
                    f"due to the following node(s) not being runnable:\n"
                    f"{un_run_nodes}",
                )

    def AcknowledgeDisabled(self, functional: functional_t, /) -> None:
        """"""
        self._AcknowledgeNodeState(
            functional, "Disabled", (NODE_BRUSH_RESTING, BUTTON_BRUSH_STATE_DISABLED)
        )

    def AcknowledgeNeedsRunning(self, functional: functional_t, /) -> None:
        """"""
        self._AcknowledgeNodeState(
            functional, "Needs Running", (NODE_BRUSH_RESTING, BUTTON_BRUSH_STATE_TODO)
        )

    def AcknowledgeRunningStarted(self, functional: functional_t, /) -> None:
        """"""
        self._AcknowledgeNodeState(
            functional,
            f"Running since {date_time_t.now()}",
            (NODE_BRUSH_RUNNING, BUTTON_BRUSH_STATE_DOING),
        )

    def AcknowledgeRunningEnded(self, functional: functional_t, /) -> None:
        """"""
        self._AcknowledgeNodeState(
            functional,
            f"Run Successfully ({date_time_t.now()})",
            (NODE_BRUSH_RESTING, BUTTON_BRUSH_STATE_DONE),
        )

    def _AcknowledgeNodeState(
        self, functional: functional_t, message: str, brushes: tuple[QBrush, QBrush], /
    ) -> None:
        """"""
        for node in self.nodes:
            if node.functional is functional:
                node.setBrush(brushes[0])
                node.state_btn.setBrush(brushes[1])
                node.state_btn.setToolTip(message)
                QCoreApplication.processEvents()
                break

    def AcknowledgeLinkEmpty(self, functional: functional_t, /) -> None:
        """"""
        self._AcknowledgeLinkState(functional, LINK_PEN_EMPTY)

    def AcknowledgeLinkFull(self, functional: functional_t, /) -> None:
        """"""
        self._AcknowledgeLinkState(functional, LINK_PEN_FULL)

    def _AcknowledgeLinkState(self, functional: functional_t, pen: QPen, /) -> None:
        """"""
        for link in self.links:
            if link.source_node.functional is functional:
                link.setPen(pen)
        QCoreApplication.processEvents()


def _SocketSelection(
    possible_names: tuple[str, ...], position: QPoint, /
) -> str | None:
    """"""
    menu = wdgt.QMenu()
    actions = [menu.addAction(_elm) for _elm in possible_names]
    selected_action = menu.exec(position)
    if selected_action is None:
        return None

    return possible_names[actions.index(selected_action)]


def _TypesAreCompatible(
    source: type_t | str,
    target: type_t | str,
    /,
) -> bool:
    """"""
    if isinstance(source, type_t):
        if isinstance(target, type_t):
            return TypesAreCompatible(
                source, target, strict_mode=False, second_should_be_wider=True
            )
        else:
            return str(source) == target
    else:
        if isinstance(target, type_t):
            return source == str(target)
        else:
            return source == target


"""
COPYRIGHT NOTICE

This software is governed by the CeCILL  license under French law and
abiding by the rules of distribution of free software.  You can  use,
modify and/ or redistribute the software under the terms of the CeCILL
license as circulated by CEA, CNRS and INRIA at the following URL
"http://www.cecill.info".

As a counterpart to the access to the source code and  rights to copy,
modify and redistribute granted by the license, users are provided only
with a limited warranty  and the software's author,  the holder of the
economic rights,  and the successive licensors  have only  limited
liability.

In this respect, the user's attention is drawn to the risks associated
with loading,  using,  modifying and/or developing or reproducing the
software by the user in light of its specific status of free software,
that may mean  that it is complicated to manipulate,  and  that  also
therefore means  that it is reserved for developers  and  experienced
professionals having in-depth computer knowledge. Users are therefore
encouraged to load and test the software's suitability as regards their
requirements in conditions enabling the security of their systems and/or
data to be ensured and,  more generally, to use and operate it in the
same conditions as regards security.

The fact that you are presently reading this means that you have had
knowledge of the CeCILL license and that you accept its terms.

SEE LICENCE NOTICE: file README-LICENCE-utf8.txt at project source root.

This software is being developed by Eric Debreuve, a CNRS employee and
member of team Morpheme.
Team Morpheme is a joint team between Inria, CNRS, and UniCA.
It is hosted by the Centre Inria d'Université Côte d'Azur, Laboratory
I3S, and Laboratory iBV.

CNRS: https://www.cnrs.fr/index.php/en
Inria: https://www.inria.fr/en/
UniCA: https://univ-cotedazur.eu/
Centre Inria d'Université Côte d'Azur: https://www.inria.fr/en/centre/sophia/
I3S: https://www.i3s.unice.fr/en/
iBV: http://ibv.unice.fr/
Team Morpheme: https://team.inria.fr/morpheme/
"""
