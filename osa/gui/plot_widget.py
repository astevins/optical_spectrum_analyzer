import numpy as np
import pyqtgraph as pg
from PyQt5 import QtWidgets

from osa.utils.unit_conversions import wavelength_to_frequency


class PlotWidget(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Components
        self.layout = QtWidgets.QGridLayout()
        self.graphWidget = pg.PlotWidget()
        self.line_pen = pg.mkPen(color='g', width=1)
        self.line = None

        # State
        self.display_frequency = False
        self.data = []
        self.x_start = 0
        self.x_increment = 1

        # Init
        self.build_ui()

    def build_ui(self):
        self.setLayout(self.layout)
        self.layout.addWidget(self.graphWidget)
        self.graphWidget.showGrid(x=True, y=True)

    def set_labels(self, x_label: str, y_label: str):
        self.graphWidget.setLabels(bottom=x_label, left=y_label)

    def set_title(self, title: str):
        self.graphWidget.setTitle(title)

    def set_x_units(self, frequency: bool):
        """
        Sets x units to display frequency or wavelength
        :param frequency:
            - If true, plot will display frequency on x-axis
            - If false, plot will display wavelength on x-axis
        """
        self.display_frequency = frequency
        if frequency:
            self.set_labels(
                x_label=f"Frequency (THz)", y_label="dBm")
            self.graphWidget.invertX(True)
        else:
            self.set_labels(
                x_label=f"Wavelength (nm)", y_label="dBm")
            self.graphWidget.invertX(False)

        self.update_data(self.data, self.x_start, self.x_increment)

    def update_data(self, data: list[float], x_start: float, x_increment: float):
        """
        Updates plot data.
        :param data: List of y-values to plot
        :param x_start: Starting x value (wavelength) in nm
        :param x_increment: Increment in x between each y-value in nm
        """
        self.data = data
        self.x_start = x_start
        self.x_increment = x_increment

        # Create x data from range
        x_end = x_start + x_increment * len(data)
        x = np.arange(x_start, x_end, x_increment)

        if self.display_frequency:
            x = [wavelength_to_frequency(x_point) for x_point in x]

        # Clear past line
        if self.line:
            self.line.clear()

        # Draw new line
        self.line = self.graphWidget.plot(x=x, y=data, pen=self.line_pen)
