from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject


class Signals(QObject):
    start_clicked = pyqtSignal()
    stop_clicked = pyqtSignal()
    single_clicked = pyqtSignal()

class Controller(QtWidgets.QWidget):
    """
    Controller box for requesting traces.
    Includes 'start/stop' button for continuous acquisition,
    'single' button for getting and displaying a single trace.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Components
        self.layout = QtWidgets.QGridLayout()
        self.start_stop_button = QtWidgets.QPushButton('Start')
        self.single_button = QtWidgets.QPushButton('Single')

        # Signals
        self.signals = Signals()

        # Init
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
        self.single_button.clicked.connect(self.single_clicked)
        self.layout.addWidget(self.single_button)

    @pyqtSlot(bool)
    def start_stop_clicked(self, checked):
        if checked:
            self.start_stop_button.setText('Stop')
            self.single_button.setEnabled(False)
            self.signals.start_clicked.emit()
        else:
            self.start_stop_button.setText('Start')
            self.single_button.setEnabled(True)
            self.signals.stop_clicked.emit()

    @pyqtSlot()
    def single_clicked(self):
        print("Single clicked")
        self.signals.single_clicked.emit()
