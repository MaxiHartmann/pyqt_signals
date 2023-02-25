import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import uic
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Ui(qtw.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi("layout.ui", self)
        self.show()

        self.sc = MplCanvas(self, width=8, height=6, dpi=100)
        self.sc.axes.plot()

        self.horizontal_layout = qtw.QHBoxLayout(self.frame_plot)
        self.horizontal_layout.addWidget(self.sc)

        # Connect to functions
        self.doubleSpinBox_f.valueChanged.connect(self.update_plot)
        self.doubleSpinBox_t0.valueChanged.connect(self.update_plot)
        self.doubleSpinBox_t1.valueChanged.connect(self.update_plot)
        self.spinBox_n.valueChanged.connect(self.update_plot)

        self.btn_reset.clicked.connect(self.reset_plot)

    def get_inputs(self):
        self.f = self.doubleSpinBox_f.value()
        self.t0 = self.doubleSpinBox_t0.value()
        self.t1 = self.doubleSpinBox_t1.value()
        self.n = self.spinBox_n.value()

    def calc_data(self):
        self.get_inputs()
        n = self.n
        t0 = self.t0
        t1 = self.t1
        f = self.f
        x = np.linspace(t0, t1, n)
        y = np.sin(2 * np.pi * f * x)
        self.data_x = x
        self.data_y = y

    def update_plot(self):
        self.calc_data()

        self.sc.axes.cla()
        self.sc.axes.plot(self.data_x, self.data_y, "*-")

        self.sc.draw()

    def reset_plot(self):
        self.sc.axes.cla()
        self.sc.draw()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
