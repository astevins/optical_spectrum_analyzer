import os
import sys
from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtWidgets import QMessageBox, QFileDialog

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
        self.menu_bar = self.menuBar()
        self.controller = Controller()
        self.update_data_timer = QTimer()
        self.alert_box = QtWidgets.QMessageBox()

        # State
        self.file_save_directory = os.getcwd()

        # Init
        self.init_window()
        self.init_plot()
        self.init_controller()
        self.init_save_action()
        self.init_menu_bar()
        self.init_timer()
        self.init_failed_connection_alert_box()

    def init_window(self):
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)
        self.setWindowTitle('Optical Spectrum Analyzer')

    def init_plot(self):
        self.layout.addWidget(self.plot_widget)

    def init_menu_bar(self):
        file_menu = self.menu_bar.addMenu('&File')
        file_menu.addAction(self.init_save_action())
        file_menu.addAction(self.init_set_directory_action())
        file_menu.setToolTipsVisible(True)

    def init_save_action(self):
        save_action = QtWidgets.QAction('&Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setToolTip('Save image of current plot view')
        save_action.triggered.connect(self.save_plot_image)
        return save_action

    def init_set_directory_action(self):
        set_directory_action = QtWidgets.QAction('Set directory', self)
        set_directory_action.setToolTip('Save location to save plot images')
        set_directory_action.triggered.connect(self.set_image_save_directory)
        return set_directory_action

    def init_controller(self):
        self.layout.addWidget(self.controller)
        signals = self.controller.signals
        signals.single_clicked.connect(
            lambda: self.update_plot_data(retry_on_error=True))
        signals.start_clicked.connect(self.start_acquisition)
        signals.stop_clicked.connect(self.stop_acquisition)
        signals.wavelength_toggled.connect(self.set_plot_units_wavelength)
        signals.frequency_toggled.connect(self.set_plot_units_frequency)

    def init_timer(self):
        self.update_data_timer.timeout.connect(self.update_plot_data)

    def init_failed_connection_alert_box(self):
        """
        Inits popup alert box for failed connection to server.
        This does not show the alert, only prepares it for future use.
        """
        self.alert_box.setIcon(QMessageBox.Critical)
        self.alert_box.setText("Multiple consecutive requests for trace data failed.")
        self.alert_box.setInformativeText("The OSA server may be down. Check console logs for details.")
        self.alert_box.setWindowTitle("Failed to update plot")
        self.alert_box.setStandardButtons(QMessageBox.Ok)

    def populate_plot(self):
        """
        Init plot x-units to wavelength and update plot data.
        """
        self.plot_widget.set_x_units(frequency=False)
        self.update_plot_data(retry_on_error=True)

    @pyqtSlot()
    def start_acquisition(self):
        """
        Starts automatic calls to update plot data at 1 Hz
        """
        print("Starting continuous acquisition at 1 Hz.")
        self.update_data_timer.start(1000)

    @pyqtSlot()
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
        """
        Sets plot data from trace data and x limits retrieved from server.
        Updates plot title to reflect time trace was taken.
        """

        # Update plot title
        self.plot_widget.set_title(
            f"{trace_data.instrument}::{trace_data.time}")

        # Update data
        self.plot_widget.update_data(
            trace_data.data,
            x_lims[0],
            trace_data.x_increment)
        print("Set new plot data.")

    @pyqtSlot()
    def set_plot_units_wavelength(self):
        """ Set plot to display x-axis as wavelength """
        self.plot_widget.set_x_units(frequency=False)

    @pyqtSlot()
    def set_plot_units_frequency(self):
        """ Set plot to display x-axis as frequency """
        self.plot_widget.set_x_units(frequency=True)

    def show_failed_connection_alert(self):
        """ Shows popup alert for failed connection to server."""
        self.alert_box.exec_()

    def set_image_save_directory(self):
        """ Opens file select dialog to choose directory for plot images. """
        self.file_save_directory = str(QFileDialog.getExistingDirectory(self, 'Select Directory'))

    def save_plot_image(self):
        """ Saves plot image as png. """
        self.plot_widget.export_plot(self.file_save_directory)


def run():
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.show()
    win.populate_plot()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
