"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import dataclasses as dtcl
import traceback as tbck
import typing as h
from enum import Enum as enum_t

from logger_36 import LOGGER
from pyvispr.constant.function import UNIQUE_NAME_INPUT
from pyvispr.constant.uid import UNIQUE_NAME_SEPARATOR, UNIQUE_OUTPUT_NAME_SEPARATOR
from pyvispr.constant.value import (
    MSG_OUTPUT_SET,
    MSG_OUTPUT_UNSET,
    VALUE_LOOP_DONE,
    VALUE_NOT_SET,
)
from pyvispr.flow.descriptive.node import node_t as description_t
from pyvispr.flow.functional.socket import input_t, output_t
from sio_messenger.instance import MESSENGER


class state_e(enum_t):
    disabled = 0
    todo = 1
    doing = 2
    done = 3


@dtcl.dataclass(slots=True, repr=False, eq=False)
class node_t:
    """
    The description is shared among all the functional nodes.

    links[idx]: Outbound links of node of index idx in list "nodes":
        - None if node has no outbound links.
        - If not None, dictionary with:
            - key=name of output and...
            - value=list of alternating target nodes and name of target inputs.
    """

    description: description_t
    inputs: dict[str, input_t]
    outputs: dict[str, output_t]
    unique_name: str | None = None
    state: state_e = state_e.todo

    @classmethod
    def NewForDescription(
        cls, description: description_t, names_already_used: h.Sequence[str], /
    ) -> node_t:
        """"""
        description.Activate()

        inputs = {_nme: input_t() for _nme in description.inputs}
        outputs = {_nme: output_t() for _nme in description.outputs}

        output = cls(
            description=description,
            inputs=inputs,
            outputs=outputs,
        )
        output.SetUniqueName(names_already_used)

        return output

    def SetUniqueName(self, already_used: h.Sequence[str], /) -> None:
        """"""
        if self.unique_name is None:
            unique_name = self.description.name
        else:
            unique_name = self.unique_name
        if unique_name in already_used:
            version = 1
            while f"{unique_name}{UNIQUE_NAME_SEPARATOR}{version}" in already_used:
                version += 1

            self.unique_name = f"{unique_name}{UNIQUE_NAME_SEPARATOR}{version}"
        else:
            self.unique_name = unique_name

    def UniqueOutputName(self, output_name: str, /) -> str:
        """"""
        return f"{self.unique_name}{UNIQUE_OUTPUT_NAME_SEPARATOR}{output_name}"

    @property
    def needs_running(self) -> bool:
        """"""
        return self.state is state_e.todo

    @property
    def can_run(self) -> bool:
        """
        It must have been checked that the state is not disabled.

        This method is meant to be called from functional.graph.Run,
        i.e., after visual.Run has read the ii_values
        to set the corresponding node input values if appropriate.
        Appropriate means: the corresponding inputs have mode "full" (actually,
        not "link") and they are not linked to outputs.
        """
        description = self.description
        return (description.n_inputs == 0) or all(
            self.inputs[_nme].has_value or _rcd.has_default
            for _nme, _rcd in description.inputs.items()
        )

    def Run(
        self,
        /,
        *,
        script_accessor: h.TextIO | None = None,
        values_script: dict[str, str] | None = None,
    ) -> None:
        """
        It must have been checked that the state is not disabled.
        """
        self.state = state_e.doing
        MESSENGER.Transmit(self.state, self)

        should_save_as_script = script_accessor is not None

        if should_save_as_script:
            if self.description.n_outputs > 1:
                output_assignments = (
                    self.UniqueOutputName(_elm) for _elm in self.outputs
                )
                output_assignments = ", ".join(output_assignments) + " = "
            else:
                output_assignments = ""
        else:
            output_assignments = None

        if self.description.n_inputs > 0:
            anonymous_args = []
            named_args = {}
            anonymous_args_script = []
            named_args_script = []

            for name, description in self.description.inputs.items():
                input_ = self.inputs[name]
                if input_.has_value:
                    value = input_.value
                else:
                    value = description.default_value
                    assert description.has_default

                if description.has_default:
                    named_args[name] = value
                    if should_save_as_script:
                        named_args_script.append(f"{name}={values_script[name]}")
                else:
                    anonymous_args.append(value)
                    if should_save_as_script:
                        anonymous_args_script.append(values_script[name])

            if should_save_as_script:
                arguments = ", ".join(anonymous_args_script + named_args_script)
                script_accessor.write(
                    f"{output_assignments}{self.description.module.__name__}_"
                    f"{self.description.actual.name}({arguments})\n"
                )
                output_values = _FakeOutputs(self.description.n_outputs, "Done")
            else:
                if self.description.wants_unique_name:
                    named_args[UNIQUE_NAME_INPUT] = self.unique_name
                output_values = self._SafelyRun(anonymous_args, named_args)
        elif should_save_as_script:
            script_accessor.write(
                f"{output_assignments}{self.description.module.__name__}_{self.description.actual.name}()\n"
            )
            output_values = _FakeOutputs(self.description.n_outputs, "Done")
        else:
            output_values = self._SafelyRun(None, None)

        # Since output values are computed here, it makes more sense to directly set them, as opposed to returning them
        # and letting the caller doing it. Hence, _SetOutputValue is meant for internal use, whereas SetInputValue is
        # meant for external use.
        output_names = self.description.output_names
        n_outputs = output_names.__len__()
        if n_outputs > 1:
            for name, value in zip(output_names, output_values):
                self._SetOutputValue(name, value)
        elif n_outputs > 0:
            self._SetOutputValue(output_names[0], output_values)

        self.state = state_e.done
        MESSENGER.Transmit(self.state, self)

    def _SafelyRun(
        self,
        anonymous_args: h.Sequence[h.Any] | None,
        named_args: dict[str, h.Any] | None,
        /,
    ) -> h.Any | None:
        """"""
        try:
            if anonymous_args is None:
                output = self.description.Function()
            else:
                output = self.description.Function(*anonymous_args, **named_args)
        except Exception as exception:
            output = _FakeOutputs(self.description.n_outputs, None)
            lines = tbck.format_exception(exception)
            as_str = "\n".join(lines[:1] + lines[2:])
            LOGGER.error(f"Error while running {self.unique_name}:\n{as_str}")

        return output

    def SetInputValue(self, name: str, value: h.Any, /) -> None:
        """"""
        self.inputs[name].value = value
        if value is not VALUE_LOOP_DONE:
            self.InvalidateOutputs()

    def _SetOutputValue(self, name: str, value: h.Any, /) -> None:
        """"""
        self.outputs[name].value = value
        if value is VALUE_NOT_SET:
            MESSENGER.Transmit(MSG_OUTPUT_UNSET, self)
        else:
            MESSENGER.Transmit(MSG_OUTPUT_SET, self)

    def InvalidateInput(self, /, *, name: str | None = None) -> None:
        """"""
        # "to do": already invalid.
        if self.state in (state_e.todo, state_e.disabled):
            return

        if name is None:
            for element in self.inputs.values():
                element.value = VALUE_NOT_SET
        else:
            self.inputs[name].value = VALUE_NOT_SET

        self.InvalidateOutputs(should_check_state=False)

    def InvalidateOutputs(self, /, *, should_check_state: bool = True) -> None:
        """"""
        # "to do": already invalid.
        if should_check_state and (self.state in (state_e.todo, state_e.disabled)):
            return

        for element in self.outputs.values():
            element.value = VALUE_NOT_SET

        self.state = state_e.todo

        MESSENGER.Transmit(self.state, self)
        MESSENGER.Transmit(MSG_OUTPUT_UNSET, self)


def _FakeOutputs(n_outputs: int, fake_value: h.Any, /) -> h.Any | tuple[h.Any, ...]:
    """"""
    if n_outputs > 1:
        return n_outputs * (fake_value,)
    return fake_value


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
