from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFrame, QGridLayout, QLineEdit, QHBoxLayout, QSizePolicy, QComboBox, QTimeEdit, QCheckBox, QTableWidget, QHeaderView, QStackedWidget, QMenuBar, QToolBar, QTabWidget, QWidgetAction
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QAction
import sys

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.setWindowTitle('CTC Office')
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet('background-color: #8f97a3;')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QGridLayout(central_widget)

        ######################################################################
        # Block View Layout
        ######################################################################

        # Create header label
        self.header = QLabel('CTC - Block View', self)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet('background-color: #2B78E4; color: white; font-size: 40px; padding: 10px;')
        self.header.setMaximumHeight(60)
        self.main_layout.addWidget(self.header, 0, 0, 1, -1) # Row 0, Column 0, Span 1 row, Span all columns
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        ######################################################################
        # Dispatch Rectangle
        ######################################################################

        # Create an empty rectangle using QFrame
        self.maintanence = QFrame(self)
        self.maintanence.setFrameShape(QFrame.Shape.Box)
        self.maintanence.setMaximumHeight(200)
        self.maintanence.setLineWidth(2)
        self.maintanence.setMaximumWidth(410)

        # Create a grid layout for the maintanence rectangle
        self.maintanence_layout = QGridLayout(self.maintanence)
        self.maintanence_layout.setContentsMargins(20, 20, 20, 20)  # Remove margins
        self.maintanence_layout.setSpacing(10)

        # Box Title
        self.maintanence_title = QLabel('Place Block in Maintenance', self.maintanence)
        self.maintanence_title.setStyleSheet('font-size: 30px; padding: 0px;')
        self.maintanence_layout.addWidget(self.maintanence_title, 0, 0, 1, 1)

        # Block Infro
        self.block_info = QLabel("Block Info...", self.maintanence)
        self.block_info.setStyleSheet('font-size: 35px; padding: 0px; border: 2px solid #000000;')
        self.maintanence_layout.addWidget(self.block_info, 1, 0, 1, 1)
        
        # Maintenance Button
        self.maintanence_button = QPushButton("Maintanence Mode", self.maintanence)
        self.maintanence_button.setStyleSheet('background-color: #FFFF00; color: black; font-size: 15px; padding: 10px;')
        self.maintanence_button.clicked.connect(self.on_click)
        self.maintanence_layout.addWidget(self.maintanence_button, 2, 0, 1, 1)




        ######################################################################
        # Throughput Rectangle
        ######################################################################

        self.throughput_rect = QFrame(self)
        self.throughput_rect.setFrameShape(QFrame.Shape.Box)
        self.throughput_rect.setMaximumHeight(160)
        self.throughput_rect.setLineWidth(2)
        self.throughput_rect.setMaximumWidth(175)

        self.throughput_rect_layout = QVBoxLayout(self.throughput_rect)
        self.throughput_rect_layout.setContentsMargins(20, 20, 20, 20)

        self.time = QLabel(f"15:40", self.throughput_rect)
        self.time.setStyleSheet('color: white; font-size: 40px; padding: 0px;')
        self.time.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.throughput_display = QLabel(f"X Trains/hr/line", self.throughput_rect)
        self.throughput_display.setStyleSheet('background-color: #2B78E4; color: white; font-size: 15px; padding: 0px; border: 2px solid #000000;')
        self.throughput_display.setMinimumWidth(120)
        self.throughput_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.throughput_label = QLabel('Throughput', self.throughput_rect)
        self.throughput_label.setStyleSheet('font-size: 20px; padding: 0px;')

        self.throughput_rect_layout.addWidget(self.time, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.throughput_rect_layout.addWidget(self.throughput_display, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.throughput_rect_layout.addWidget(self.throughput_label, 2, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

        ######################################################################
        # Train Table 1
        ######################################################################

        self.train_table1 = QTableWidget(4, 5, self)
        self.train_table1.setHorizontalHeaderLabels(["  Train  ", "  Current Block  ", "  Departure Station  ", "  Destination Station  ", "  Departure Time  ", "  Arrival Time  "])
        self.train_table1.setFixedHeight(200)
        self.train_table1.setFixedWidth(800)
        self.train_table1.resizeColumnsToContents()
        self.train_table1.resizeRowsToContents()
        self.train_table1.verticalHeader().setVisible(False)
        self.train_table1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.train_table1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #self.table1.horizontalHeader().setStretchLastSection(True)


        ######################################################################
        # Layout
        ######################################################################

        self.main_layout.addWidget(self.maintanence, 1, 0, 1, 1)
        self.main_layout.addWidget(self.throughput_rect, 1, 1, 1, 1)
        self.main_layout.addWidget(self.train_table1, 2, 0, 1, 2)


    def on_click(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
