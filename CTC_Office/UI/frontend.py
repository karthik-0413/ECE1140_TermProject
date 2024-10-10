from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFrame, QGridLayout, QLineEdit, QHBoxLayout, QSizePolicy, QComboBox, QTimeEdit, QCheckBox, QTableWidget, QHeaderView, QStackedWidget, QMenuBar, QToolBar, QTabWidget, QWidgetAction, QFileDialog
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QAction
import sys
import os

cur_dir = os.path.dirname(__file__)
lib_dir = os.path.join(cur_dir, '../backend/')
sys.path.append(lib_dir)

from backend import CTC_Controller
from communicationSignals import Communicate

class App(QMainWindow):
    def __init__(self, communicator):
        super().__init__()
        self.communicator = communicator
        self.initUI()

    def initUI(self):

        self.ctc = CTC_Controller()

        self.setWindowTitle('CTC Office')
        self.setGeometry(100, 100, 300, 200)
        self.setStyleSheet('background-color: #8f97a3;')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.main_layout = QVBoxLayout(central_widget)

        self.train_view_layout = QGridLayout()
        self.block_view_layout = QGridLayout()

        self.menuBar = QMenuBar(self)
        self.setMenuBar(self.menuBar)
        self.setVisible(True)

        self.toolbar = QToolBar(self)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolbar)
        self.toolbar.setVisible(True)
        self.toolbar.setFixedHeight(25)
        self.toolbar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        
        self.tab_widget = QTabWidget(self)
        self.tab_widget.addTab(QWidget(), "Train View")
        self.tab_widget.addTab(QWidget(), "Block View")

        self.tab_widget.currentChanged.connect(self.on_tab_changed)

        self.tab_action = QWidgetAction(self)
        self.tab_action.setDefaultWidget(self.tab_widget)

        self.toolbar.addAction(self.tab_action)

        self.view_trains = QAction("Train View", self)
        self.view_blocks = QAction("Block View", self)

        self.menuBar.addAction(self.view_trains)
        self.menuBar.addAction(self.view_blocks)

        self.view_trains.triggered.connect(self.show_train_view)
        self.view_blocks.triggered.connect(self.show_block_view)


        ######################################################################
        # Train View Layout
        ######################################################################

        # Create header label
        self.header = QLabel('CTC - Train View', self)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet('background-color: #2B78E4; color: white; font-size: 40px; padding: 10px;')
        self.header.setMaximumHeight(60)
        self.train_view_layout.addWidget(self.header, 0, 0, 1, -1) # Row 0, Column 0, Span 1 row, Span all columns
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
        self.throughput_rect.setMaximumHeight(160)
        self.throughput_rect.setLineWidth(2)
        self.throughput_rect.setMaximumWidth(200)

        self.throughput_rect_layout = QVBoxLayout(self.throughput_rect)
        self.throughput_rect_layout.setContentsMargins(20, 20, 20, 20)

        self.time = QLabel(self.ctc.time_string(), self.throughput_rect)
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


        self.upload_schedule_button = QPushButton("Upload Schedule", self)
        self.upload_schedule_button.setStyleSheet('background-color: #FF00FF; font-size: 15px; padding: 10px;')
        self.upload_schedule_button.clicked.connect(self.upload_schedule)

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
        # Train Table 2
        ######################################################################

    




        ######################################################################
        # Block View Layout
        ######################################################################

        self.maintanence_box = QFrame(self)
        self.maintanence_box.setFrameShape(QFrame.Shape.Box)
        self.maintanence_box.setMaximumHeight(200)
        self.maintanence_box.setLineWidth(2)
        self.maintanence_box.setMaximumWidth(500)

        self.maintanence_box_layout = QGridLayout(self.maintanence_box)
        self.maintanence_box_layout.setContentsMargins(20, 20, 20, 20)

        self.maintanence_box_label = QLabel('Maintanence', self.maintanence_box)
        self.maintanence_box_label.setStyleSheet('font-size: 40px; padding: 0px;')






        self.track_button = QPushButton("Upload Track Layout", self)
        self.track_button.setStyleSheet('background-color: #2B78E4; font-size: 15px; padding: 10px;')
        self.track_button.clicked.connect(self.upload_layout)
        self.train_view_layout.addWidget(self.track_button, 4, 0, 1, 1)


        ######################################################################
        # Layout
        ######################################################################

        self.train_view_layout.addWidget(self.dispatch, 1, 0, 2, 1)
        self.train_view_layout.addWidget(self.throughput_rect, 1, 1, 1, 1)
        self.train_view_layout.addWidget(self.upload_schedule_button, 2, 1, 1, 1)
        self.train_view_layout.addWidget(self.train_table1, 3, 0, 1, 2)

        self.main_layout.addLayout(self.train_view_layout)



        ####
        # Vars
        ####

        self.selected_line = None
        self.tab_index = 0
        

    def show_train_view(self):
        self.clear_layout(self.main_layout)
        self.tab_index = 0
        self.main_layout.addLayout(self.train_view_layout)

    def show_block_view(self):
        self.clear_layout(self.main_layout)
        self.tab_index = 1
        self.main_layout.addLayout(self.block_view_layout)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_tab_changed(self, index):
        if self.tab_index == 0:
            self.show_train_view()
        elif self.tab_index == 1:
            self.show_block_view()

    def on_line_change(self):
        self.selected_line = self.line_select.currentText()

    def change_page(self, layout):
        self.setLayout(layout)
        pass


    def time_step(self):
        self.ctc.increment_time(self)

        self.time.setText(self.ctc.time_string())



    def upload_layout(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Layout File", os.getcwd(), "Excel File (*.xlsx *.xls)")
        if file_name:
            print(f"Selected file: {file_name}")
            self.ctc.upload_layout(file_name)

    def upload_schedule(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Schedule File", os.getcwd(), "Excel File (*.xlsx *.xls)")
        if file_name:
            print(f"Selected file: {file_name}")
            self.ctc.upload_schedule(file_name)

    def on_click(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec())
