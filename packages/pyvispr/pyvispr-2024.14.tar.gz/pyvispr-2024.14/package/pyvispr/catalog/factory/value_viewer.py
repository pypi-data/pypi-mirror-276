"""
Copyright CNRS/Inria/UniCA
Contributor(s): Eric Debreuve (eric.debreuve@cnrs.fr) since 2017
SEE COPYRIGHT NOTICE BELOW
"""

from __future__ import annotations

import pprint as pprt
import typing as h

import numpy
import PyQt6.QtCore as core
import PyQt6.QtGui as qtui
import PyQt6.QtWidgets as wdgt
from PyQt6.QtCore import QRunnable as task_base_t
from PyQt6.QtCore import QThreadPool as thread_manager_t
from pyvispr.interface.window.runner import runner_wdw_t
from pyvispr.runtime.backend import SCREEN_BACKEND

_MANAGER: dict[str, viewer_t] = {}


def pyVisprValueViewer(value: h.Any, /, *, pyvispr_name: str | None = None) -> None:
    """"""
    if pyvispr_name in _MANAGER:
        viewer = _MANAGER[pyvispr_name]
        viewer.Update(value)
    else:
        value_viewer = viewer_t(value, pyvispr_name)
        value_viewer.show()
        # TODO: Solve the following error:
        #     QBasicTimer::stop: Failed. Possibly trying to stop from a different thread
        #     The code below makes it disappear, but the table is not correctly populated then.
        # if value_viewer.thread_manager is not None:
        #     value_viewer.thread_manager.waitForDone()
        # Test also somewhere (not here though; it does not work):
        # value_viewer.thread_manager.moveToThread(wdgt.QApplication.instance().thread())


class viewer_t(wdgt.QMainWindow):
    def __init__(self, value: h.Any, name: str | None, /) -> None:
        """"""
        wdgt.QMainWindow.__init__(self, runner_wdw_t.Instance())
        self.setAttribute(core.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setWindowTitle("pyVispr Value Viewer")
        if name is None:
            self.name = f"Unknown Node {id(self)}"
        else:
            self.name = name
        _MANAGER[self.name] = self

        name_wgt = wdgt.QLabel(f'<span style="font-weight:bold">{self.name}</span>')
        name_wgt.setContentsMargins(6, 0, 0, 0)

        as_array = _ValueAsArray(value)
        if as_array is None:
            as_str = pprt.pformat(value, width=120, compact=True, sort_dicts=False)
            self.value_container = wdgt.QTextEdit(as_str)
        else:
            self.value = as_array
            self.value_container, self.model = _NewContainerAndModel(self.value)
            self.filling_task = task_t(self.value_container, self.model, self.value)
            thread_manager_t.globalInstance().start(self.filling_task)

        done = wdgt.QPushButton("Done")

        layout = wdgt.QVBoxLayout()
        layout.addWidget(name_wgt)
        layout.addWidget(self.value_container)
        layout.addWidget(done)

        central = wdgt.QWidget()
        central.setLayout(layout)
        self.setCentralWidget(central)

        SCREEN_BACKEND.CreateMessageCanal(done, "clicked", self.close)

    def Update(self, value: h.Any, /) -> None:
        """"""
        as_array = _ValueAsArray(value)
        if as_array is None:
            if not isinstance(self.value_container, wdgt.QTextEdit):
                container = wdgt.QTextEdit()
                layout = self.centralWidget().layout()
                _ = layout.replaceWidget(self.value_container, container)
                self.value_container = container

            as_str = pprt.pformat(value, width=120, compact=True, sort_dicts=False)
            self.value_container.setText(as_str)
        else:
            self.value = as_array

            if isinstance(self.value_container, wdgt.QTableView):
                self.value_container.selectAll()
                self.value_container.clearSelection()
                self.model.clear()
                self.value_container.setEnabled(False)
            else:
                container, model = _NewContainerAndModel(self.value)
                layout = self.centralWidget().layout()
                _ = layout.replaceWidget(self.value_container, container)
                self.value_container = container
                self.model = model

            self.filling_task = task_t(self.value_container, self.model, self.value)
            thread_manager_t.globalInstance().start(self.filling_task)

    def closeEvent(self, event: qtui.QCloseEvent, /) -> None:
        """"""
        del _MANAGER[self.name]
        wdgt.QMainWindow.closeEvent(self, event)


class task_t(task_base_t):
    def __init__(
        self,
        viewer: wdgt.QTableView,
        model: qtui.QStandardItemModel,
        value: numpy.ndarray,
        /,
    ) -> None:
        """"""
        task_base_t.__init__(self)
        self.viewer = viewer
        self.model = model
        self.value = value

    @core.pyqtSlot()
    def run(self) -> None:
        """"""
        min_value, max_value = numpy.amin(self.value), numpy.amax(self.value)
        if max_value > min_value:
            color = qtui.QColor()
            if (min_value, max_value) != (0, 255):
                factor = 255.0 / (max_value - min_value)
            else:
                factor = None
        else:
            color = factor = None

        for row in self.value:
            cells = map(str, row)
            cells = tuple(map(qtui.QStandardItem, cells))
            if color is None:
                for cell in cells:
                    cell.setTextAlignment(core.Qt.AlignmentFlag.AlignRight)
            else:
                for cell, value in zip(cells, row):
                    if factor is None:
                        gray = value
                    else:
                        gray = int(round(factor * (value - min_value)))
                    color.setRgb(255 - gray, 255, 255 - gray, 255)
                    cell.setData(
                        core.QVariant(qtui.QBrush(color)),
                        core.Qt.ItemDataRole.BackgroundRole,
                    )
                    cell.setTextAlignment(core.Qt.AlignmentFlag.AlignRight)
            self.model.appendRow(cells)

        self.viewer.resizeRowsToContents()
        self.viewer.resizeColumnsToContents()

        self.viewer.setEnabled(True)

        self.value = None


def _ValueAsArray(value: h.Any, /) -> numpy.ndarray | None:
    """"""
    try:
        output = numpy.array(value)
    except:
        output = None

    if (
        (output is not None)
        and (output.ndim < 3)
        and (output.size > 1)
        and (
            numpy.issubdtype(output.dtype, numpy.integer)
            or numpy.issubdtype(output.dtype, numpy.floating)
        )
    ):
        return output

    return None


def _NewContainerAndModel(
    value: numpy.ndarray, /
) -> tuple[wdgt.QTableView, qtui.QStandardItemModel]:
    """"""
    container = wdgt.QTableView()
    container.setEnabled(False)

    model = qtui.QStandardItemModel(container)
    model.setColumnCount(max(_elm.__len__() for _elm in value))

    container.setModel(model)

    return container, model


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
