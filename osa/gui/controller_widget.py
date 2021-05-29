from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot


class Controller(QtWidgets.QWidget):
    '''
    Controller box for updating plot with new traces.
    Includes 'start/stop' button for continuous acquisition,
    'single' button for getting and displaying a single trace.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QtWidgets.QGridLayout()
        self.start_stop_button = QtWidgets.QPushButton('Start')
        self.single_button = QtWidgets.QPushButton('Single')

        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)
        self.init_start_stop_button()
        self.init_single_button()

    def init_start_stop_button(self):
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.toggled.connect(self.start_stop_clicked)
        self.layout.addWidget(self.start_stop_button)

    def init_single_button(self):
        self.start_stop_button.clicked.connect(self.single_clicked)
        self.layout.addWidget(self.single_button)

    @pyqtSlot(bool)
    def start_stop_clicked(self, checked):
        self.start_stop_button.setText('Stop' if checked else 'Start')
        self.single_button.setEnabled(False if checked else True)
        # TODO send signal to app

    @pyqtSlot(bool)
    def single_clicked(self, checked):
        return
        # TODO send signal to app
