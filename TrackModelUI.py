import sys
import os
from PyQt6 import QtWidgets, QtCore, QtGui, uic
from Track_Model_UI import Ui_TrackModel
import pandas as pd
import csv
from typing import List

class Block:
    def __init__(self, line: str, section: str, number: int, length: float, grade: float, speedLimit: float, infrastructure: str, elevation: float, cumulativeElevation: float, polarity: bool = False, functional: bool = True, occupancy: bool = False):
        self.line = line
        self.section = section
        self.number = number
        self.length = length
        self.grade = grade
        self.speedLimit = speedLimit
        self.infrastructure = infrastructure
        self.elevation = elevation
        self.cumulativeElevation = cumulativeElevation
        self.polarity = polarity
        self.functional = functional
        self.occupancy = occupancy

    @staticmethod
    def setFailureMode(ui, block_number: int) -> bool:
        selected_values = [ui.comboBox1.currentText(), ui.comboBox2.currentText(), ui.comboBox3.currentText()]
        break_buttons = [ui.breakButton1, ui.breakButton2, ui.breakButton3]
        return not any(selected_value == str(block_number) and break_button.isChecked() for selected_value, break_button in zip(selected_values, break_buttons))

    @classmethod
    def create_blocks(cls, ui, layout_data: List[List[str]], lengthArray: List[float], position: int, switchStatus: bool) -> List['Block']:
        blocks = []
        sectionA = []
        sectionB = []
        sectionC = []
        for row in layout_data:
            line, section, number, length, grade, speedLimit, infrastructure, elevation, cumulativeElevation = row[:9]
            block = cls(
                line=line,
                section=section,
                number=int(number),
                length=float(length),
                grade=float(grade),
                speedLimit=float(speedLimit),
                infrastructure=infrastructure,
                elevation=float(elevation),
                cumulativeElevation=float(cumulativeElevation)
            )
            blocks.append(block)
            if section == "A":
                sectionA.append(block)
            elif section == "B":
                sectionB.append(block)
            elif section == "C":
                sectionC.append(block)
        
        if switchStatus:
            sectionA.extend(sectionB)
        else:
            sectionA.extend(sectionC)
        
        cls.setOccupancy(ui, blocks, lengthArray, position)
        cls.setPolarity(blocks)
        return blocks

    @staticmethod
    def setOccupancy(ui, blocks: List['Block'], lengthArray: List[float], x: int) -> List[bool]:
        occupancy_status = []
        blockStart = 0
        for i, length in enumerate(lengthArray):
            blockEnd = blockStart + length
            occupancy = blockStart <= x < blockEnd or not Block.setFailureMode(ui, blocks[i].number)
            blocks[i].occupancy = occupancy
            occupancy_status.append(occupancy)
            blockStart = blockEnd
        return occupancy_status

    @staticmethod
    def setPolarity(blocks: List['Block']) -> None:
        for i, block in enumerate(blocks):
            block.polarity = i % 2 == 0

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TrackModel()
        self.ui.setupUi(self)
        self.ui.fileUploadButton.clicked.connect(self.upload_file)
        self.ui.tempStepper.valueChanged.connect(self.check_temperature)
        self.ui.applyChangesButton.clicked.connect(self.apply_changes)
        self.ui.breakButton1.clicked.connect(self.break_button1_clicked)
        self.ui.breakButton2.clicked.connect(self.break_button2_clicked)
        self.ui.breakButton3.clicked.connect(self.break_button3_clicked)
        self.blocks = []
        self.layout_data = []
        self.lengthArray = []
        self.occupancy_status = []
        self.switchStatus = False 
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.on_timer_timeout)
        self.timer.start(1000) 
        self.temp_increase_timer = QtCore.QTimer(self)
        self.temp_increase_timer.timeout.connect(self.increase_temperature)

    def upload_file(self) -> None:
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if file_path:
            try:
                with open(file_path, newline='') as layoutFile:
                    spamreader = csv.reader(layoutFile, delimiter=',', quotechar='|')
                    next(spamreader)
                    self.layout_data = []
                    self.lengthArray = []
                    for row in spamreader:
                        self.layout_data.append(row)
                        self.lengthArray.append(float(row[3]))
                print("Imported Information:")
                for row in self.layout_data:
                    print(row)
                total_length = sum(self.lengthArray)
                self.ui.positionValue.setMaximum(total_length)
                position = self.ui.positionValue.value()
                self.blocks = Block.create_blocks(self.ui, self.layout_data, self.lengthArray, position, self.switchStatus)
                self.occupancy_status = Block.setOccupancy(self.ui, self.blocks, self.lengthArray, position)
                self.print_block_information()
            except Exception as e:
                print(f"Error reading file: {e}")

    def check_temperature(self) -> None:
        current_temp = self.ui.tempStepper.value()
        if current_temp <= 32:
            print("Turn on track heater")
            self.ui.label_2.setStyleSheet("font: 10pt \"Times New Roman\";\n"
                                          "background-color: yellow;\n"
                                          "color: rgb(0, 0, 0);")
            QtCore.QTimer.singleShot(2000, self.start_temp_increase_timer)
        else:
            self.ui.label_2.setStyleSheet("font: 10pt \"Times New Roman\";\n"
                                          "background-color: rgb(68, 68, 68);\n"
                                          "color: rgb(0, 0, 0);")
            self.temp_increase_timer.stop()

    def start_temp_increase_timer(self) -> None:
        self.temp_increase_timer.start(500) 

    def increase_temperature(self) -> None:
        current_temp = self.ui.tempStepper.value()
        if current_temp <= 32:
            self.ui.tempStepper.setValue(current_temp + 1)
        else:
            self.temp_increase_timer.stop()

    def apply_changes(self) -> None:
        print("Apply Changes Button pressed")
        self.print_pass_information()

    def checkSwitch(self) -> None:
        switch_state = self.ui.switchTable.item(0, 1).text()
        if switch_state == "(5 to 6)":
            self.switchStatus = True
            print(switch_state)
        elif switch_state == "(5 to 11)":
            self.switchStatus = False

    def print_pass_information(self) -> None:
        print("Pass Information:")
        row_count = self.ui.passInfoTable.rowCount()
        column_count = self.ui.passInfoTable.columnCount()
        for row in range(row_count):
            row_data = []
            for column in range(column_count):
                item = self.ui.passInfoTable.item(row, column)
                row_data.append(item.text() if item else "")
            print(row_data)

    def break_button1_clicked(self) -> None:
        self.set_block_non_functional(self.ui.comboBox1.currentText())
        self.print_block_information()

    def break_button2_clicked(self) -> None:
        self.set_block_non_functional(self.ui.comboBox2.currentText())
        self.print_block_information()

    def break_button3_clicked(self) -> None:
        self.set_block_non_functional(self.ui.comboBox3.currentText())
        self.print_block_information()

    def set_block_non_functional(self, block_number_str: str) -> None:
        try:
            block_number = int(block_number_str)
            for block in self.blocks:
                if block.number == block_number:
                    block.functional = False
                    block.occupancy = True
                    print(f"Block {block_number} set to non-functional and occupied")
                    QtCore.QTimer.singleShot(3000, lambda: self.set_block_functional(block_number))
                    return
            print(f"Block {block_number} not found")
        except ValueError:
            print(f"Invalid block number: {block_number_str}")

    def set_block_functional(self, block_number: int) -> None:
        for block in self.blocks:
            if block.number == block_number:
                block.functional = True
                block.occupancy = False
                print(f"Block {block_number} set back to functional")
                return

    def print_block_information(self) -> None:
        print("Block Information:")
        self.ui.tableWidget.setRowCount(len(self.blocks))
        headers = ["Line", "Section", "Number", "Length", "Grade", "Speed Limit", "Infrastructure", "Elevation", "Cumulative Elevation", "Polarity", "Functional", "Occupancy"]
        self.ui.tableWidget.setColumnCount(len(headers))
        self.ui.tableWidget.setHorizontalHeaderLabels(headers)
        
        for row, block in enumerate(self.blocks):
            self.ui.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(block.line))
            self.ui.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(block.section))
            self.ui.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(block.number)))
            self.ui.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(block.length)))
            self.ui.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(str(block.grade)))
            self.ui.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(str(block.speedLimit)))
            self.ui.tableWidget.setItem(row, 6, QtWidgets.QTableWidgetItem(block.infrastructure))
            self.ui.tableWidget.setItem(row, 7, QtWidgets.QTableWidgetItem(str(block.elevation)))
            self.ui.tableWidget.setItem(row, 8, QtWidgets.QTableWidgetItem(str(block.cumulativeElevation)))
            self.ui.tableWidget.setItem(row, 9, QtWidgets.QTableWidgetItem(str(block.polarity)))
            self.ui.tableWidget.setItem(row, 10, QtWidgets.QTableWidgetItem(str(block.functional)))
            self.ui.tableWidget.setItem(row, 11, QtWidgets.QTableWidgetItem(str(self.occupancy_status[row])))
            
            print(vars(block))

    def update_block_occupancy(self) -> None:
        position = self.ui.positionValue.value()
        self.occupancy_status = Block.setOccupancy(self.ui, self.blocks, self.lengthArray, position)
        self.print_block_information()

    def on_timer_timeout(self) -> None:
        self.check_temperature()
        self.update_block_occupancy()

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
