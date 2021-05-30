from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QObject
from PyQt5.QtWidgets import QGroupBox


class Signals(QObject):
    wavelength_toggled = pyqtSignal()
    frequency_toggled = pyqtSignal()
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
        self.layout = QtWidgets.QHBoxLayout()
        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.radio_button_group = QtWidgets.QButtonGroup()
        self.start_stop_button = QtWidgets.QPushButton('Start')
        self.single_button = QtWidgets.QPushButton('Single')

        # Signals
        self.signals = Signals()

        # Init
        self.init_ui()

    def init_ui(self):
        self.setLayout(self.layout)
        self.init_radio_buttons()
        self.init_start_stop_button()
        self.init_single_button()
        self.layout.addLayout(self.buttons_layout)

    def init_start_stop_button(self):
        self.start_stop_button.setCheckable(True)
        self.start_stop_button.toggled.connect(self.start_stop_clicked)
        self.buttons_layout.addWidget(self.start_stop_button)

    def init_single_button(self):
        self.single_button.clicked.connect(self.single_clicked)
        self.buttons_layout.addWidget(self.single_button)

    def init_radio_buttons(self):
        wavelength_radio_button = QtWidgets.QRadioButton('Wavelength')
        frequency_radio_button = QtWidgets.QRadioButton('Frequency')

        # Create visual radio button group container
        radio_button_container = QtWidgets.QGroupBox()
        radio_button_container.setTitle('X Axis:')
        self.layout.addWidget(radio_button_container)
        radio_button_container_layout = QtWidgets.QVBoxLayout()
        radio_button_container.setLayout(radio_button_container_layout)
        radio_button_container_layout.addWidget(wavelength_radio_button)
        radio_button_container_layout.addWidget(frequency_radio_button)

        # Create abstract radio button group
        self.radio_button_group.setExclusive(True)
        self.radio_button_group.addButton(wavelength_radio_button, 1)
        self.radio_button_group.addButton(frequency_radio_button, 2)
        wavelength_radio_button.setChecked(True)
        self.radio_button_group.buttonClicked.connect(self.radio_button_clicked)

    def radio_button_clicked(self, button):
        button_id = self.radio_button_group.id(button)
        if button_id == 1:
            self.signals.wavelength_toggled.emit()
        else:
            self.signals.frequency_toggled.emit()

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
        self.signals.single_clicked.emit()
