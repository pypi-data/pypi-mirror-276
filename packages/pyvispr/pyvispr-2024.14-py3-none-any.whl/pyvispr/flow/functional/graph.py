"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

import dataclasses as dtcl
import typing as h

from pyvispr.flow.functional.link import links_t
from pyvispr.flow.functional.node import node_t, state_e
from pyvispr.flow.functional.value import EncodedValue
from sio_messenger.instance import MESSENGER


@dtcl.dataclass(repr=False, eq=False)
class graph_t(list[node_t]):
    """
    Cannot be sloted because of QThread issue with weak reference (see visual.graph).
    """

    links: links_t = dtcl.field(init=False, default_factory=links_t)

    @property
    def node_unique_names(self) -> tuple[str, ...]:
        """"""
        return tuple(_elm.unique_name for _elm in self)

    def ToggleNodeAbility(self, node: node_t, /) -> None:
        """"""
        if node.state is state_e.disabled:
            node.state = state_e.todo
        else:
            self.InvalidateNode(node)
            node.state = state_e.disabled
        MESSENGER.Transmit(node.state, node)

    def InvalidateNode(self, node: node_t) -> None:
        """"""
        node.InvalidateOutputs()

        for descendant in self.links.DescendantsOfNode(node):
            descendant, socket_pairs = descendant
            for _, input_name in socket_pairs:
                descendant.InvalidateInput(name=input_name)

    def RemoveNode(self, node: node_t, /) -> None:
        """"""
        self.InvalidateNode(node)

        self.RemoveLink(node, None, None, None)
        self.RemoveLink(None, None, node, None)

        self.remove(node)

    def AddLink(
        self, source: node_t, output_name: str, target: node_t, input_name: str, /
    ) -> None:
        """"""
        self.links.Add(
            source,
            output_name,
            target,
            input_name,
        )
        self.InvalidateNode(target)

    def RemoveLink(
        self,
        source: node_t | None,
        output_name: str | None,
        target: node_t | None,
        input_name: str | None,
        /,
    ) -> None:
        """
        Removes one or several links assuming that the link(s) exist(s).
        """
        if target is not None:
            self.InvalidateNode(target)

        self.links.Remove(source, output_name, target, input_name)

    def Invalidate(self) -> None:
        """"""
        for node in self:
            self.InvalidateNode(node)

    def Run(self, /, *, script_accessor: h.TextIO = None) -> tuple[node_t, ...]:
        """"""
        should_save_as_script = script_accessor is not None

        while True:
            needs_running = tuple(filter(lambda _elm: _elm.needs_running, self))
            if needs_running.__len__() == 0:
                break
            can_run = tuple(filter(lambda _elm: _elm.can_run, needs_running))
            if can_run.__len__() == 0:
                break

            for node in can_run:
                output_names = node.description.output_names
                n_outputs = output_names.__len__()

                if should_save_as_script and (n_outputs > 0):
                    if n_outputs > 1:
                        for idx in range(n_outputs - 1):
                            script_accessor.write(
                                node.UniqueOutputName(output_names[idx]) + ", "
                            )
                    script_accessor.write(
                        node.UniqueOutputName(output_names[-1]) + " = "
                    )

                if script_accessor is None:
                    values_script = None
                else:
                    values_script = {}
                    for name, input_ in node.inputs.items():
                        if input_.has_value:
                            attached = self.links.InputSocketIsFree(
                                node, name, should_return_socket=True
                            )
                            if attached is None:
                                value_script = EncodedValue(input_.value)
                            else:
                                predecessor, name_s_out = attached
                                value_script = predecessor.UniqueOutputName(name_s_out)
                        else:
                            default_value = node.description.inputs[name].default_value
                            value_script = EncodedValue(default_value)
                        values_script[name] = value_script

                node.Run(script_accessor=script_accessor, values_script=values_script)
                self.SendNodeOutputsToSuccessors(node)

        if should_save_as_script:
            if needs_running.__len__() > 0:
                script_accessor.write(
                    'print("Workflow saving was incomplete due to some nodes not being runnable.")'
                )

            return needs_running

        return ()

    def SendNodeOutputsToSuccessors(self, node: node_t, /) -> None:
        """"""
        for name_out, output in node.outputs.items():
            value = output.value
            successors = self.links.SuccessorsOfNode(node, output_name=name_out)
            for successor, socket_pairs in successors:
                for _, name_in in socket_pairs:
                    successor.SetInputValue(name_in, value)


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
