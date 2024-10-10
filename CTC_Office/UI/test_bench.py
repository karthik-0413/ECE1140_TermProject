from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QVBoxLayout, QFrame, QGridLayout, QLineEdit, QHBoxLayout, QSizePolicy, QComboBox, QTimeEdit, QCheckBox, QTableWidget, QHeaderView, QStackedWidget, QMenuBar, QToolBar, QTabWidget, QWidgetAction
from PyQt6.QtCore import Qt, QTime
from PyQt6.QtGui import QAction
import sys
import os

cur_dir = os.path.dirname(__file__)
lib_dir = os.path.join(cur_dir, '../backend/')
sys.path.append(lib_dir)

from backend import CTC_Controller
from communicationSignals import Communicate

class TB(QMainWindow):
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
        self.header = QLabel('CTC - Test Benech', self)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet('background-color: #2B78E4; color: white; font-size: 40px; padding: 10px;')
        self.header.setMaximumHeight(60)
        self.main_layout.addWidget(self.header, 0, 0, 1, -1) # Row 0, Column 0, Span 1 row, Span all columns
        self.header.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)


        self.block_info = QFrame(self)
        self.block_info.setFrameShape(QFrame.Shape.Box)
        self.block_info.setMaximumHeight(150)
        self.block_info.setLineWidth(2)
        self.block_info.setMaximumWidth(200)

        self.block_info_layout = QVBoxLayout(self.block_info)
        self.block_info_layout.setContentsMargins(20, 20, 20, 20)
        self.block_info_layout.setSpacing(10)

        self.block_info_label = QLabel('Block Info', self)
        self.block_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignBottom)
        self.block_info_layout.addWidget(self.block_info_label, 0)

        ###########
        # Output box
        ###########

        self.output_box = QFrame(self)
        self.output_box.setFrameShape(QFrame.Shape.Box)
        self.output_box.setMaximumHeight(100)
        self.output_box.setLineWidth(2)
        self.output_box.setMaximumWidth(450)

        self.output_box_layout = QGridLayout(self.output_box)
        self.output_box_layout.setContentsMargins(20, 20, 20, 20)
        self.output_box_layout.setSpacing(10)

        # Line Selector
        self.choose_line = QComboBox(self.output_box)
        self.choose_line.addItems(['Line...', 'Blue'])
        #self.choose_line.currentIndexChanged.connect(self.update_line)
        self.choose_line.setFixedWidth(80)
        self.output_box_layout.addWidget(self.choose_line, 0, 0, 1, 1)
        
        # Train Selector
        self.choose_train = QComboBox(self.output_box)
        self.choose_train.addItems(['Train #', 'Train 1'])
        self.choose_train.setFixedWidth(80)
        self.output_box_layout.addWidget(self.choose_train, 0, 1, 1, 1)

        # Box Label
        self.output_box_label = QLabel('Outputs to Train', self.output_box)
        self.output_box_label.setStyleSheet('font-size: 20px;')
        self.output_box_layout.addWidget(self.output_box_label, 0, 2, 1, 2)

        # Speed Label
        self.speed_label = QLabel('Suggested Speed:', self.output_box)
        self.speed_label.setStyleSheet('font-size: 15px;')
        self.output_box_layout.addWidget(self.speed_label, 1, 0, 1, 1)

        # Speed Display
        self.speed_display = QLabel('0 mph', self.output_box)
        self.speed_display.setStyleSheet('font-size: 15px; padding: 0px; border: 2px solid #000000;')
        self.output_box_layout.addWidget(self.speed_display, 1, 1, 1, 1)

        # Authority Label
        self.authority_label = QLabel('Authority:', self.output_box)
        self.authority_label.setStyleSheet('font-size: 15px;')
        self.output_box_layout.addWidget(self.authority_label, 1, 2, 1, 1)

        # Authority Display
        self.authority_display = QLabel('0 m', self.output_box)
        self.authority_display.setStyleSheet('font-size: 15px; padding: 0px; border: 2px solid #000000;')
        self.output_box_layout.addWidget(self.authority_display, 1, 3, 1, 1)


        ###########

        # Input Box
        self.input_box = QFrame(self)
        self.input_box.setFrameShape(QFrame.Shape.Box)
        self.input_box.setMaximumHeight(150)
        self.input_box.setLineWidth(2)
        self.input_box.setMaximumWidth(500)
        
        # input layout
        self.input_layout = QGridLayout(self.input_box)
        self.input_layout.setContentsMargins(20, 20, 20, 20)
        self.input_layout.setSpacing(10)

        # Occupancy Checkbox
        self.occupancy_checkbox = QCheckBox(self.input_box)
        self.occupancy_checkbox.setFixedSize(20, 20)
        self.occupancy_checkbox.setStyleSheet('QCheckBox::indicator { width: 40px; height: 40px; }')
        self.occupancy_checkbox.stateChanged.connect(self.toggle_occupied)
        self.input_layout.addWidget(self.occupancy_checkbox, 0, 0, 1, 1)

        # occupancy label
        self.occupancy_label = QLabel('Block Occupied', self.input_box)
        self.occupancy_label.setStyleSheet('font-size: 15px;')
        self.input_layout.addWidget(self.occupancy_label, 0, 1, 1, 2)

        # Damage Checkbox
        self.damage_checkbox = QCheckBox(self.input_box)
        self.damage_checkbox.setFixedSize(20, 20)
        self.damage_checkbox.setStyleSheet('QCheckBox::indicator { width: 40px; height: 40px; }')
        self.input_layout.addWidget(self.damage_checkbox, 1, 0, 1, 1)

        # Track damaged label
        self.damage_label = QLabel('Track Damaged', self.input_box)
        self.damage_label.setStyleSheet('font-size: 15px; padding: 0px;')
        self.input_layout.addWidget(self.damage_label, 1, 1, 1, 2)

        # Crossing Checkbox
        self.crossing_checkbox = QCheckBox(self.input_box)
        self.crossing_checkbox.setFixedSize(20, 20)
        self.crossing_checkbox.setStyleSheet('QCheckBox::indicator { width: 40px; height: 40px; }')
        self.input_layout.addWidget(self.crossing_checkbox, 2, 0, 1, 1)

        # Crossing label
        self.crossing_label = QLabel('Crossing Closed', self.input_box)
        self.crossing_label.setStyleSheet('font-size: 15px; padding: 0px;')
        self.input_layout.addWidget(self.crossing_label, 2, 1, 1, 2)

        # Maintenance label
        self.maintanence_label = QLabel('Block Under Maintenance: ', self.input_box)
        self.maintanence_label.setStyleSheet('font-size: 15px;')
        self.input_layout.addWidget(self.maintanence_label, 3, 0, 1, 2)

        # Maintenance display
        self.maintanence_display = QLabel('No', self.input_box)
        self.maintanence_display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.maintanence_display.setStyleSheet('font-size: 15px; padding: 0px; border: 2px solid #000000;')
        self.input_layout.addWidget(self.maintanence_display, 3, 2, 1, 1)


        # Switch Label
        self.switch_position = QLabel("Switch Position", self.input_box)
        self.switch_position.setStyleSheet('font-size: 15px; padding: 0px;')
        self.input_layout.addWidget(self.switch_position, 0, 2, 1, 1)

        # Switch Position Selector
        self.switch_selector = QComboBox(self.input_box)
        self.switch_selector.addItems(["Block", "Block 6", "Block 11"])
        self.switch_selector.setMinimumWidth(60)
        self.input_layout.addWidget(self.switch_selector, 1, 2, 1, 1)

        # Signal Label
        self.signal_state = QLabel("Signal State", self.input_box)
        self.signal_state.setStyleSheet('font-size: 15px; padding: 0px;')
        self.input_layout.addWidget(self.signal_state, 0, 3, 1, 1)

        # Signal Selector
        self.signal_selector = QComboBox(self.input_box)
        self.signal_selector.addItems(["Green", "Yellow", "Red"])
        self.signal_selector.currentIndexChanged.connect(self.signal_change)
        self.input_layout.addWidget(self.signal_selector, 1, 3, 1, 1)


        ############




        self.main_layout.addWidget(self.block_info, 1, 0, 1, 1)
        self.main_layout.addWidget(self.output_box, 1, 1, 1, 2)
        self.main_layout.addWidget(self.input_box, 2, 0, 1, -1)


    def toggle_occupied(self):
        if self.communicator.blockOccupied:
            self.communicator.blockOccupied.emit(False)
        else:
            self.communicator.blockOccupied.emit(True)

    def toggle_crossing(self):
        if self.communicator.crossingState:
            self.communicator.crossingState.emit(False)
        else:
            self.communicator.crossingState.emit(True)
        
    def signal_change(self, index):
        self.communicator.signalColor.emit(index)





if __name__ == '__main__':
    app = QApplication(sys.argv)
    comm = Communicate()
    ex = TB(comm)
    ex.show()
    sys.exit(app.exec())
