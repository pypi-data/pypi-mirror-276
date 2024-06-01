"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as dtcl
import math
import typing as h

import PyQt6.QtCore as core
import PyQt6.QtGui as qgui
import PyQt6.QtWidgets as wdgt
from pyvispr.config.appearance.color import GRID_PEN
from pyvispr.config.appearance.geometry import NODE_HEIGHT_TOTAL, NODE_WIDTH_TOTAL
from pyvispr.flow.functional.node import state_e
from pyvispr.flow.visual.graph import graph_t
from pyvispr.flow.visual.link import link_t
from pyvispr.flow.visual.node import node_t
from pyvispr.runtime.backend import SCREEN_BACKEND

constant_e = core.Qt


@dtcl.dataclass(slots=True, repr=False, eq=False)
class whiteboard_t(wdgt.QGraphicsView):
    zoom_factor: h.ClassVar[float] = 1.25

    grid: wdgt.QGraphicsItemGroup | None = dtcl.field(init=False, default=None)
    graph: graph_t | None = dtcl.field(init=False, default=None)

    _grid_update_comes_from_self: bool = dtcl.field(init=False, default=False)

    def __post_init__(self) -> None:
        """"""
        # Otherwise, complaint about super-init not having been called.
        wdgt.QGraphicsView.__init__(self)

        self.setRenderHint(qgui.QPainter.RenderHint.Antialiasing)
        # Used to not work in conjunction with selectable RectItems.
        self.setDragMode(wdgt.QGraphicsView.DragMode.RubberBandDrag)

        self.SetGraph(None)

    def AddOrUpdateGrid(self) -> None:
        """"""
        if self.graph is None:
            raise RuntimeError(
                "Whiteboard grid can be added only after a graph has been created."
            )

        if self._grid_update_comes_from_self:
            self._grid_update_comes_from_self = False
            return
        self._grid_update_comes_from_self = True

        if self.grid is not None:
            self.graph.removeItem(self.grid)
        grid = wdgt.QGraphicsItemGroup()
        grid.setZValue(0)

        geometry = []
        rectangle = self.graph.sceneRect()
        center = rectangle.center()
        for GetCenter, GetLength, node_length in (
            (center.x, rectangle.width, NODE_WIDTH_TOTAL),
            (center.y, rectangle.height, NODE_HEIGHT_TOTAL),
        ):
            center = GetCenter()
            length = GetLength()
            if length > 0.0:
                center_grid = 0.5 * round(2.0 * center / node_length) * node_length
            else:
                center_grid = 0.5 * node_length
            n_cells_half = max(math.ceil(round(length / node_length, 1)), 3) // 2
            geometry.append((center_grid, n_cells_half))

        for (
            (center_grid, n_cells_half),
            increment,
            increment_bnd,
            where,
            (center_grid_bnd, n_cells_half_bnd),
        ) in (
            (geometry[0], NODE_WIDTH_TOTAL, NODE_HEIGHT_TOTAL, 1, geometry[1]),
            (geometry[1], NODE_HEIGHT_TOTAL, NODE_WIDTH_TOTAL, 2, geometry[0]),
        ):
            position = center_grid - (n_cells_half + 0.5) * increment
            extent_bnd = (n_cells_half_bnd + 0.5) * increment_bnd
            bound_min = center_grid_bnd - extent_bnd
            bound_max = center_grid_bnd + extent_bnd
            for idx in range(2 * n_cells_half + 2):
                if where == 1:
                    line = wdgt.QGraphicsLineItem(
                        position, bound_min, position, bound_max
                    )
                else:
                    line = wdgt.QGraphicsLineItem(
                        bound_min, position, bound_max, position
                    )
                line.setPen(GRID_PEN)
                grid.addToGroup(line)
                position += increment

        self.grid = grid
        self.graph.addItem(grid)

    def ToggleGridVisibility(self) -> None:
        """"""
        self.grid.setVisible(not self.grid.isVisible())

    def AddNode(self, name: str, /) -> None:
        """"""
        self.graph.AddNode(name)

    def SetGraph(self, graph: graph_t | None, /, *, is_update: bool = False) -> None:
        """"""
        if graph is None:
            self.graph = graph_t()
        elif is_update:
            self.graph.MergeWith(graph)
        else:
            self.graph = graph

        if not is_update:
            self.setScene(self.graph)
            self.grid = None
            self._grid_update_comes_from_self = False
            SCREEN_BACKEND.CreateMessageCanal(
                self.graph, "sceneRectChanged", lambda _: self.AddOrUpdateGrid()
            )
        self.AddOrUpdateGrid()

    def AlignGraphOnGrid(self) -> None:
        """"""
        self.graph.AlignOnGrid()

    def InvalidateWorkflow(self) -> None:
        """"""
        self.graph.functional.Invalidate()

    def Clear(self) -> None:
        """"""
        self.graph.Clear()
        self.AddOrUpdateGrid()

    def Statistics(self) -> tuple[int, int, int]:
        """
        self.graph.nodes.__len__() and self.graph.functional.__len__() should be equal.
        """
        return (
            self.graph.nodes.__len__(),
            self.graph.functional.__len__(),
            self.graph.links.__len__(),
        )

    def Screenshot(self) -> qgui.QPixmap:
        """"""
        frame = self.viewport().rect()
        output = qgui.QPixmap(frame.size())
        painter = qgui.QPainter(output)
        self.render(painter, output.rect().toRectF(), frame)

        return output

    def RunWorkflow(self) -> None:
        """"""
        self.graph.Run()

    def mousePressEvent(self, event: qgui.QMouseEvent, /) -> None:
        """"""
        if event.buttons() != constant_e.MouseButton.LeftButton:
            wdgt.QGraphicsView.mousePressEvent(self, event)
            return

        view_position = event.pos()
        scene_position = self.mapToScene(view_position)
        item: node_t | link_t | None = None
        # Used to be: deviceTransform=self.graph.views()[0].transform()
        for current_item in self.graph.items(
            scene_position, deviceTransform=self.transform()
        ):
            if isinstance(current_item, (node_t, link_t)):
                item = current_item
                break
        if item is None:
            wdgt.QGraphicsView.mousePressEvent(self, event)
            return

        item: node_t | link_t
        if isinstance(item, node_t):
            item_position = item.mapFromScene(scene_position)
            if (item.in_btn is not None) and item.in_btn.contains(item_position):
                item_global_pos = self.mapToGlobal(view_position)
                self.graph.AddLinkMaybe(item, False, item_global_pos)
            elif (item.out_btn is not None) and item.out_btn.contains(item_position):
                item_global_pos = self.mapToGlobal(view_position)
                self.graph.AddLinkMaybe(item, True, item_global_pos)
            elif item.config_btn.contains(item_position):
                item.ToggleIIDialog(self.graph.functional.InvalidateNodeOutputs)
            elif item.state_btn.contains(item_position):
                pass
            elif item.remove_btn.contains(item_position):
                menu = wdgt.QMenu()
                cancel_action = menu.addAction("Close Menu")
                no_action = menu.addAction("or")
                no_action.setEnabled(False)
                invalidate_action = menu.addAction("Invalidate Node")
                if item.functional.state is state_e.disabled:
                    operation = "Enable"
                else:
                    operation = "Disable"
                disable_action = menu.addAction(f"{operation} Node")
                remove_action = menu.addAction("Remove Node")

                item_global_pos = self.mapToGlobal(view_position)
                selected_action = menu.exec(item_global_pos)

                if (selected_action is None) or (selected_action is cancel_action):
                    return
                if selected_action is invalidate_action:
                    self.graph.functional.InvalidateNodeOutputs(item.functional)
                elif selected_action is disable_action:
                    self.graph.functional.ToggleNodeAbility(item.functional)
                if selected_action is remove_action:
                    self.graph.RemoveNode(item)
            else:
                wdgt.QGraphicsView.mousePressEvent(self, event)
        else:
            links = item.LinksToBeRemoved(
                self.mapToGlobal(view_position), self.graph.functional
            )
            if isinstance(links, h.Sequence):
                if links[0] is None:
                    self.graph.RemoveLink(item)
                else:
                    self.graph.RemoveLink(
                        item, output_name=links[0][0], input_name=links[0][1]
                    )

    def wheelEvent(self, event, /) -> None:
        """"""
        if event.modifiers() == constant_e.KeyboardModifier.ControlModifier:
            scale_factor = (
                1 / whiteboard_t.zoom_factor
                if event.angleDelta().y() > 0
                else whiteboard_t.zoom_factor
            )
            self.scale(scale_factor, scale_factor)


# def _RoundedOddNGridCells() -> float:
#     """"""

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
