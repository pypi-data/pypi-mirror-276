"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from typing import Any, Callable

import PyQt6.QtWidgets as wdgt
from PyQt6.QtGui import QAction
from pyvispr.runtime.backend import SCREEN_BACKEND

action_h = Callable[[bool], None]
action_optional_h = action_h | None
entry_h = tuple[str, action_optional_h]
entry_args_h = tuple[str, action_optional_h, tuple[Any, ...]]
entry_kwargs_h = tuple[str, action_optional_h, dict[str, Any]]
entry_full_h = tuple[str, action_optional_h, tuple[Any, ...], dict[str, Any]]
entry_any_h = entry_h | entry_args_h | entry_kwargs_h | entry_full_h


def NewMenuWithEntries(
    text: str,
    entries: tuple[entry_any_h | wdgt.QMenu | None, ...],
    manager: wdgt.QWidget,
    /,
    *,
    parent: wdgt.QMenuBar | wdgt.QMenu | None = None,
) -> wdgt.QMenu:
    """"""
    if parent is None:
        output = wdgt.QMenu(text)
    else:
        output = parent.addMenu(text)

    AddEntriesToMenu(entries, output, manager)

    return output


def AddEntriesToMenu(
    entries: tuple[entry_any_h | wdgt.QMenu | None, ...],
    menu: wdgt.QMenu,
    manager: wdgt.QWidget,
) -> None:
    """"""
    for entry in entries:
        if entry is None:
            menu.addSeparator()
        elif isinstance(entry, wdgt.QMenu):
            menu.addMenu(entry)
        else:
            text, action, *args = entry
            if (n_args := args.__len__()) > 0:
                if (n_args == 1) and isinstance(args[0], (tuple, dict)):
                    if isinstance(args[0], tuple):
                        args, kwargs = args[0], {}
                    else:
                        args, kwargs = (), args[0]
                elif (
                    (n_args == 2)
                    and isinstance(args[0], tuple)
                    and isinstance(args[1], dict)
                ):
                    args, kwargs = args
                else:
                    raise ValueError(
                        f"Invalid entry specification: Actual={args}; Expected=a(n optional) arg tuple and a(n optional) kwarg dictionary."
                    )
            else:
                args, kwargs = (), {}
            AddEntryToMenu(text, action, menu, manager, *args, **kwargs)


def AddEntryToMenu(
    text: str,
    action: action_h | None,
    menu: wdgt.QMenu,
    manager: wdgt.QWidget,
    /,
    *args,
    status_tip: str | None = None,
    shortcut: str | None = None,
    disabled: bool = False,
    checkable: bool = False,
    checked: bool = False,
    **kwargs,
) -> None:
    """"""
    entry = QAction(text, parent=manager)
    if action is None:
        entry.setEnabled(False)
    else:
        SCREEN_BACKEND.CreateMessageCanal(entry, "triggered", action, *args, **kwargs)
    if status_tip is not None:
        entry.setStatusTip(status_tip)
    if shortcut is not None:
        entry.setShortcut(shortcut)
    if disabled:
        entry.setEnabled(False)
    if checkable:
        entry.setCheckable(True)
        entry.setChecked(checked)

    menu.addAction(entry)


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
