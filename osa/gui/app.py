import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer

from osa.gui.controller_widget import Controller
from osa.gui.plot_widget import PlotWidget
from osa.services.server_requests import get_trace, get_x_lims


class MainWindow(QtWidgets.QMainWindow):
    """
    Main GUI interface for OSA app
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        # Components
        self.layout = QtWidgets.QGridLayout()
        self.window = QtWidgets.QWidget()
        self.plot_widget = PlotWidget()
        self.controller = Controller()
        self.update_data_timer = QTimer()

        # Init
        self.init_window()
        self.init_plot()
        self.init_controller()
        self.init_timer()

    def init_window(self):
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

    def init_plot(self):
        self.layout.addWidget(self.plot_widget)

    def init_controller(self):
        self.layout.addWidget(self.controller)
        self.controller.signals.single_clicked.connect(self.update_plot_data)
        self.controller.signals.start_clicked.connect(self.start_acquisition)
        self.controller.signals.stop_clicked.connect(self.stop_acquisition)

    def init_timer(self):
        self.update_data_timer.timeout.connect(self.update_plot_data)

    def init_plot_data(self):
        """
        Gets first trace for plot and sets axis labels
        """

        print("Requesting initial plot data.")
        trace_data = get_trace()

        self.plot_widget.set_labels(
            f"{trace_data.x_label} ({trace_data.x_units})",
            trace_data.y_label)
        self.update_plot_data(trace_data)

    def start_acquisition(self):
        print("Starting continuous acquisition at 1 Hz.")
        self.update_data_timer.start(1000)

    def stop_acquisition(self):
        print("Stopping continuous acquisition.")
        self.update_data_timer.stop()

    @pyqtSlot()
    def update_plot_data(self, trace_data=None):
        """
        Plots new trace
        :param trace_data:
            Uses previously acquired trace data if trace_data
            is provided, otherwise requests new data.
        """

        # Request new trace
        if not trace_data:
            print("Requesting new plot data.")
            trace_data = get_trace()
        x_lims = get_x_lims()

        # Update plot title
        self.plot_widget.set_title(
            f"{trace_data.instrument} :: {trace_data.time}")

        # Update data
        self.plot_widget.update_data(
            trace_data.data,
            x_lims[0],
            trace_data.x_increment)
        print("Set new plot data.")


def run():
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.show()
    win.init_plot_data()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
