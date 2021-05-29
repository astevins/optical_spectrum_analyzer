import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets


class PlotWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QGridLayout()
        self.graphWidget = pg.PlotWidget()
        self.line_pen = pg.mkPen(color='g', width=1)
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.layout)
        self.graphWidget.setContentsMargins(40, 40, 40, 40)
        self.layout.addWidget(self.graphWidget)
        self.graphWidget.showGrid(x=True, y=True)

    def set_labels(self, x_label: str, y_label: str):
        self.graphWidget.setLabels(bottom=x_label, left=y_label)

    def update_data(self, data: list[float], x_start: float, x_increment: float):
        x_end = x_start + x_increment * len(data)
        x = np.arange(x_start, x_end, x_increment)
        self.graphWidget.plot(x=x, y=data, pen=self.line_pen)
        self.graphWidget.setXRange(x_start, x_end)
