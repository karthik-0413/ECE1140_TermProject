from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QFrame, QGridLayout, QLineEdit, QHBoxLayout, QSizePolicy, QComboBox, QTimeEdit, QCheckBox, QTableWidget, QHeaderView
from PyQt6.QtCore import Qt, QTime
import sys

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('PyQt6 Simple UI')
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet('background-color: #8f97a3;')

        self.layout = QGridLayout()

        # Create header label
        self.header = QLabel('CTC', self)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet('background-color: #2B78E4; color: white; font-size: 40px; padding: 10px;')
        self.header.setMaximumHeight(60)
        self.layout.addWidget(self.header, 0, 0, 1, -1) # Row 0, Column 0, Span 1 row, Span all columns
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        ######################################################################
        # Dispatch Rectangle
        ######################################################################

        # Create an empty rectangle using QFrame
        self.dispatch = QFrame(self)
        self.dispatch.setFrameShape(QFrame.Shape.Box)
        self.dispatch.setMaximumHeight(200)
        self.dispatch.setLineWidth(2)
        self.dispatch.setMaximumWidth(800)

        # Create a grid layout for the dispatch rectangle
        self.dispatch_layout = QGridLayout(self.dispatch)
        self.dispatch_layout.setContentsMargins(20, 20, 20, 20)  # Remove margins
        self.dispatch_layout.setSpacing(10)

        # Box Title
        self.dispatch_title = QLabel('Schedule New Train', self.dispatch)
        self.dispatch_title.setStyleSheet('font-size: 40px; padding: 0px;')
        self.dispatch_layout.addWidget(self.dispatch_title, 0, 0, 1, 2)

        # Train Line Label
        self.line_label = QLabel('Train Line', self.dispatch)
        self.line_label.setStyleSheet('font-size: 20px; padding: 0px;')
        self.dispatch_layout.addWidget(self.line_label, 0, 2, 1, 1, Qt.AlignmentFlag.AlignRight)

        # Train Line
        self.line_select = QComboBox(self.dispatch)
        self.line_select.addItems(["Blue", "Red", "Green"])
        self.line_select.currentIndexChanged.connect(self.on_line_change)
        self.line_select.setFixedWidth(80)

        self.dispatch_layout.addWidget(self.line_select, 0, 3, 1, 1)

        # Departure Station Label
        self.departure_station_label = QLabel('Departure Station', self.dispatch)
        self.departure_station_label.setStyleSheet('font-size: 20px; padding: 0px;')
        self.dispatch_layout.addWidget(self.departure_station_label, 1, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Departure Station
        self.departure_station = QComboBox(self.dispatch)
        self.departure_station.addItems(["Shadyside", "Station 2", "Station 3"])
        self.departure_station.setMinimumWidth(140)
        self.dispatch_layout.addWidget(self.departure_station, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Departure Time Label
        self.departure_time_label = QLabel('Departure Time', self.dispatch)
        self.departure_time_label.setStyleSheet('font-size: 20px; padding: 0px;')
        self.dispatch_layout.addWidget(self.departure_time_label, 1, 2, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Departure Time
        self.departure_time = QTimeEdit(self.dispatch)
        self.departure_time.setTime(QTime.currentTime())
        self.dispatch_layout.addWidget(self.departure_time, 1, 3, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        # Arrival Station Label
        self.arrival_station_label = QLabel('Arrival Station', self.dispatch)
        self.arrival_station_label.setStyleSheet('font-size: 20px; padding: 0px;')
        self.dispatch_layout.addWidget(self.arrival_station_label, 2, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Arrival Station
        self.arrival_station = QComboBox(self.dispatch)
        self.arrival_station.addItems(["Edgewood", "Station 2", "Station 3"])
        self.arrival_station.setMinimumWidth(140)
        self.dispatch_layout.addWidget(self.arrival_station, 2, 1, Qt.AlignmentFlag.AlignCenter)

        # Arrival Time Label
        self.arrival_time_label = QLabel('Arrival Time', self.dispatch)
        self.arrival_time_label.setStyleSheet('font-size: 20px; padding: 0px;')
        self.dispatch_layout.addWidget(self.arrival_time_label, 2, 2, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Arrival Time
        self.arrival_time = QTimeEdit(self.dispatch)
        self.arrival_time.setTime(QTime.currentTime())
        self.dispatch_layout.addWidget(self.arrival_time, 2, 3, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)

        # Dispatch Button
        self.button = QPushButton('Dispatch Train', self)
        self.button.setStyleSheet('background-color: #6AA84F; font-size: 15px; padding: 10px;')
        self.button.clicked.connect(self.on_click)
        self.dispatch_layout.addWidget(self.button, 3, 3, 1, 1, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        # Automatic Dispatch Label
        self.auto_mode_label = QLabel('Automatic Mode', self.dispatch)
        self.auto_mode_label.setStyleSheet('font-size: 30px; padding: 0px;')
        self.dispatch_layout.addWidget(self.auto_mode_label, 3, 0, 1, 2, Qt.AlignmentFlag.AlignCenter)

        # Automatic Dispatch Toggle Switch
        self.auto_mode_switch = QCheckBox(self.dispatch)
        self.auto_mode_switch.setFixedSize(200, 50)
        self.auto_mode_switch.setStyleSheet('QCheckBox::indicator { width: 40px; height: 40px; }')  # Adjust the size of the checkbox indicator   
        self.dispatch_layout.addWidget(self.auto_mode_switch, 3, 2, 1, 1)

        ######################################################################
        # Throughput Rectangle
        ######################################################################

        self.throughput_rect = QFrame(self)
        self.throughput_rect.setFrameShape(QFrame.Shape.Box)
        self.throughput_rect.setMaximumHeight(100)
        self.throughput_rect.setLineWidth(2)
        self.throughput_rect.setMaximumWidth(175)

        self.throughput_rect_layout = QVBoxLayout(self.throughput_rect)
        self.throughput_rect_layout.setContentsMargins(20, 20, 20, 20)

        self.throughput_display = QLabel(f"X Trains/hr/line", self.throughput_rect)
        self.throughput_display.setStyleSheet('background-color: #2B78E4; color: white; font-size: 15px; padding: 0px; border: 2px solid #000000;')
        self.throughput_display.setMinimumWidth(120)
        self.throughput_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.throughput_label = QLabel('Throughput', self.throughput_rect)
        self.throughput_label.setStyleSheet('font-size: 20px; padding: 0px;')

        self.throughput_rect_layout.addWidget(self.throughput_display, 0, Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignCenter)
        self.throughput_rect_layout.addWidget(self.throughput_label, 1, Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignCenter)

        ######################################################################
        # Table 1
        ######################################################################

        self.table1 = QTableWidget(4, 5, self)
        self.table1.setHorizontalHeaderLabels(["  Train  ", "  Current Block  ", "  Departure Station  ", "  Destination Station  ", "  Departure Time  ", "  Arrival Time  "])
        self.table1.setFixedHeight(200)
        self.table1.setFixedWidth(800)
        self.table1.resizeColumnsToContents()
        self.table1.resizeRowsToContents()
        self.table1.verticalHeader().setVisible(False)
        self.table1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table1.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        #self.table1.horizontalHeader().setStretchLastSection(True)

        ######################################################################
        # Layout
        ######################################################################

        self.layout.addWidget(self.dispatch, 1, 0, 1, 1)
        self.layout.addWidget(self.throughput_rect, 1, 1, 1, 1)
        self.layout.addWidget(self.table1, 2, 0, 1, 2)
        self.setLayout(self.layout)



        ####
        # Vars
        ####

        self.selected_line = None
        

    def on_line_change(self, index):
        self.selected_line = self.line_select.currentText()


    def on_click(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
