import pyqtgraph as pg
from PyQt5 import QtWidgets


class PlotWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_ui()

    def build_ui(self):
        self.layout = QtWidgets.QGridLayout()
        self.setLayout(self.layout)

        self.graphWidget = pg.PlotWidget()
        self.layout.addWidget(self.graphWidget)

    def update_data(self, data: list[float]):
        # plot data: x, y values
        self.graphWidget.plot(y=data)
