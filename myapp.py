import sys
import os
import pandas as pd
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")

from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtGui as qtg

class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.canvas, self)

        self.setGeometry(50, 50, 800, 600)

        self.directory_input = qtw.QLineEdit()

        self.open_button = qtw.QPushButton("Open ...")
        self.cancel_button = qtw.QPushButton("Cancel")
        self.plot_button = qtw.QPushButton("Plot")

        layout = qtw.QFormLayout()
        # layout.addRow('Directory:', self.directory_input, self.open_directory)
        layout.addRow("Directory:", self.directory_input)

        button_widget = qtw.QWidget()
        button_widget.setLayout(qtw.QHBoxLayout())
        button_widget.layout().addWidget(self.cancel_button)
        button_widget.layout().addWidget(self.open_button)
        button_widget.layout().addWidget(self.plot_button)
        layout.addRow("", button_widget)

        self.combobox1 = qtw.QComboBox()
        layout.addRow("", self.combobox1)

        plot_widget = qtw.QVBoxLayout()
        plot_widget.addWidget(toolbar)
        plot_widget.addWidget(self.canvas)

        layout.addRow("", plot_widget)

        self.setLayout(layout)

        # button events...
        self.cancel_button.clicked.connect(self.close)
        self.open_button.clicked.connect(self.open_directory_dialog)
        self.plot_button.clicked.connect(self.plot_selected_csv)

        # Your code ends here
        self.show()

    def open_directory_dialog(self, s):
        path = str(qtw.QFileDialog.getExistingDirectory(self, "Select Directory"))
        print("Choose path: ", path)
        self.directory_input.setText("{}".format(path))

        self.combobox1.clear()
        list_of_files = self.list_files_in_dir()
        self.combobox1.addItems(list_of_files)

    def list_files_in_dir(self):
        path = self.directory_input.text()
        print(path)

        filelist = []

        for (root, dirs, files) in os.walk(path):
            for f in files:
                if ".csv" in f:
                    filelist.append(f)

        return filelist

    def plot_selected_csv(self):
        self.canvas.axes.cla()  # Clear the canvas.

        currentpath = self.directory_input.text()
        csv_file = self.combobox1.currentText()

        df = pd.read_csv(f"{currentpath}/{csv_file}")
        xdata = df["t"]
        ydata = df["y"]

        self.canvas.axes.plot(xdata, ydata, 'r')
        self.canvas.draw()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
