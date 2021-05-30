import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QMessageBox

from osa.exceptions.invalid_response import InvalidResponse
from osa.exceptions.osa_server_exception import OsaServerException
from osa.gui.controller_widget import Controller
from osa.gui.plot_widget import PlotWidget
from osa.services.request_error_manager import request_until_success
from osa.services.server_requests import get_trace, get_x_lims, TraceData


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
        self.alert_box = QtWidgets.QMessageBox()

        # Init
        self.init_window()
        self.init_plot()
        self.init_controller()
        self.init_timer()
        self.init_failed_connection_alert_box()

    def init_window(self):
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
        self.setWindowTitle('Optical Spectrum Analyzer')

    def init_plot(self):
        self.layout.addWidget(self.plot_widget)

    def init_controller(self):
        self.layout.addWidget(self.controller)
        self.controller.signals.single_clicked.connect(
            lambda: self.update_plot_data(retry_on_error=True))
        self.controller.signals.start_clicked.connect(self.start_acquisition)
        self.controller.signals.stop_clicked.connect(self.stop_acquisition)

    def init_timer(self):
        self.update_data_timer.timeout.connect(self.update_plot_data)

    def init_failed_connection_alert_box(self):
        """
        Inits popup alert box for failed connection to server.
        This does not show the alert, only prepares it for future use.
        """
        # self.alert_box.hide()
        self.alert_box.setIcon(QMessageBox.Critical)
        self.alert_box.setText("Multiple consecutive requests for trace data failed.")
        self.alert_box.setInformativeText("The OSA server may be down. Check console logs for details.")
        self.alert_box.setWindowTitle("Failed to update plot")
        self.alert_box.setStandardButtons(QMessageBox.Ok)

    def show_failed_connection_alert(self):
        """ Shows popup alert for failed connection to server."""
        # self.alert_box.show()
        self.alert_box.exec_()

    def start_acquisition(self):
        """
        Starts automatic calls to update plot data at 1 Hz
        """
        print("Starting continuous acquisition at 1 Hz.")
        self.update_data_timer.start(1000)

    def stop_acquisition(self):
        """
        Stops automatically updating plot data
        """
        print("Stopping continuous acquisition.")
        self.update_data_timer.stop()

    @pyqtSlot()
    def update_plot_data(self, retry_on_error=False):
        """
        Requests and plots new trace.
        :param retry_on_error:
            - If True, will repeat requests up to 5 times until a valid response is received.
                If still no valid response is received, displays popup alert and skips update.
            - If false, will log errors and skip plot data update.
        """

        # Request new trace
        print("Requesting new plot data.")
        num_attempts = 5
        if retry_on_error:
            try:
                trace_data = request_until_success(get_trace, num_attempts)
                x_lims = request_until_success(get_x_lims, num_attempts)
            except InvalidResponse as e:
                print(str(e))
                self.show_failed_connection_alert()
                return
        else:
            try:
                trace_data = get_trace()
                x_lims = get_x_lims()
            except OsaServerException as e:
                print(str(e))
                print("Skipping plot update due to server error.")
                return

        self.set_plot_data(trace_data, x_lims)

    def set_plot_data(self, trace_data: TraceData, x_lims: list[float]):
        # Update plot labels
        self.plot_widget.set_title(
            f"{trace_data.instrument} :: {trace_data.time}")
        self.plot_widget.set_labels(
            f"{trace_data.x_label} ({trace_data.x_units})",
            trace_data.y_label)

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
    win.update_plot_data(retry_on_error=True)

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
