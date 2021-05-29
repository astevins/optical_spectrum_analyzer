import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from osa.gui.plot_widget import PlotWidget
from osa.services.server_requests import get_trace, get_x_lims


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_window()
        self.init_plot()

    def init_window(self):
        self.window = QtWidgets.QWidget()
        self.layout = QtWidgets.QGridLayout()
        self.setCentralWidget(self.window)
        self.window.setLayout(self.layout)

    def init_plot(self):
        self.plot_widget = PlotWidget()
        self.layout.addWidget(self.plot_widget)

    def set_plot_data(self):
        trace_data = get_trace()
        x_lims = get_x_lims()

        print("Setting plot data.")
        self.plot_widget.set_labels(
            f"{trace_data['x_label']} ({trace_data['x_units']})",
            trace_data['y_label'])
        self.plot_widget.update_data(
            trace_data['data'],
            x_lims[0],
            trace_data['x_increment'])


def run():
    app = QtWidgets.QApplication([])

    win = MainWindow()
    win.show()
    win.set_plot_data()

    sys.exit(app.exec_())


if __name__ == '__main__':
    run()
