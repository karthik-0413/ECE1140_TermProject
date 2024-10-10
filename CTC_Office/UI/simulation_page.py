from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFrame, QGridLayout, QLineEdit, QHBoxLayout, QSizePolicy, QComboBox, QTimeEdit, QCheckBox, QTableWidget, QHeaderView, QStackedWidget, QMenuBar, QToolBar, QTabWidget, QWidgetAction, QSlider
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QAction
from time import sleep as tsleep
import sys
import os

cur_dir = os.path.dirname(__file__)
lib_dir = os.path.join(cur_dir, '../backend/')
sys.path.append(lib_dir)

from backend import CTC_Controller
from communicationSignals import Communicate

class Simulate(QMainWindow):
    def __init__(self, communicator):
        super().__init__()
        self.communicator = communicator
        self.initUI()
        

    def initUI(self):

        self.setWindowTitle('CTC Office')
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet('background-color: #8f97a3;')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QGridLayout(central_widget)

        ######################################################################
        # Test Bench Layout
        ######################################################################

        # Create Block box and label
        self.header = QLabel('CTC - Simulation', self)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet('background-color: #2B78E4; color: white; font-size: 40px; padding: 10px;')
        self.header.setMaximumHeight(60)
        self.main_layout.addWidget(self.header, 0, 0, 1, -1) # Row 0, Column 0, Span 1 row, Span all columns
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


        # Simulation title
        self.simulation_title = QLabel('Simulation Speed', self)
        self.simulation_title.setStyleSheet('font-size: 30px')
        self.simulation_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.simulation_title, 1, 0, 1, -1)

        # Simulation speed Slider
        self.simulation_slider = QSlider(Qt.Orientation.Horizontal, self)
        self.simulation_slider.setMinimum(1)
        self.simulation_slider.setMaximum(100)
        self.simulation_slider.setValue(1)
        self.simulation_slider.valueChanged.connect(self.update_slider_value)
        self.main_layout.addWidget(self.simulation_slider, 2, 1, 1, 3)

        # Min and Max labels for the slider
        self.min_label = QLabel('1', self)
        self.min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.min_label, 2, 0)

        self.max_label = QLabel('100', self)
        self.max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.max_label, 2, 4)

        # Label to display the current value of the slider
        self.slider_value_label = QLabel('1x', self)
        self.slider_value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.slider_value_label, 3, 0, 1, -1)

        # Time title
        self.time_title = QLabel('Simulation Time', self)
        self.time_title.setStyleSheet('font-size: 30px')
        self.time_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.time_title, 4, 0, 1, -1)

         # Time display
        self.time_display = QLabel('00:00:00', self)
        self.time_display.setStyleSheet('font-size: 40px')
        self.time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.time_display, 5, 0, 1, -1)  

        # Label to display the time format
        self.time_format_label = QLabel('hr:min:sec', self)
        self.time_format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.addWidget(self.time_format_label, 6, 0, 1, -1) 

        self.time_step_button = QPushButton("Time step", self)
        self.time_step_button.setStyleSheet('background-color: #6AA84F; font-size: 15px; padding: 10px;')
        self.time_step_button.clicked.connect(self.time_step)
        self.main_layout.addWidget(self.time_step_button, 7, 0, 1, 1)


    def update_slider_value(self, value):
        self.slider_value_label.setText(str(value) + "x")
        self.communicator.time_speedup.emit(value)

    def time_step(self):
        self.communicator.time_step.emit(True)
        tsleep(1)
        self.communicator.time_step.emit(False)





if __name__ == '__main__':
    communicator = Communicate()
    app = QApplication(sys.argv)
    ex = Simulate(communicator)
    ex.show()
    sys.exit(app.exec())