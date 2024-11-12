import sys, os
import csv
import re
from typing import List, Dict
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import (Qt, QObject, pyqtSignal)
from Track_Model_UI import Ui_TrackModel
import random

from TrackTrainCommunicate import TrackTrainComms as TrainComms
from WaysideTrackCommunicate import WaysideTrackComms as WaysideComms

cmdSpeed: List[int] = []
cmdAuthority: List[int] = []
gradeValue: List[float] = []
elevationValue: List[float] = []
polarityValue: List[bool] = []
numPassengersEmbarking: List[int] = []
numPassengersDisembarking: List[int] = []
positions: List[float] = [50, 1000, 2000, 7000]
direction: bool = False
vacancy: int = 0
switchCmds: List[bool] = []
crossingCmds: List[bool] = []
signalCmds: List[bool] = []

defaultRedPath = [
    0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75,
    74, 73, 72, 33, 34, 35, 36, 37, 38, 71, 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51,
    52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46,
    45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24,
    23, 22, 21, 20, 19, 18, 17, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
]
defaultGreenPath = [
    0, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
    85, 84, 83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
    125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 29, 28, 27, 26, 25, 24, 23,
    22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
    32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 0
]

switchDict = {
    "green": {
        "13": [["1", "12"]],
        "28": [["150", "29"]],
        "57": [["58", "0"]],
        "63": [["0", "62"]],
        "77": [["76", "101"]],
        "85": [["100", "86"]]
    }
}

class Track(QObject):
    def __init__(self):
        super().__init__()
        self.heater = False
        self.switches = []
        self.stations = []
        self.blocks = []
        self.path = {}
        self.layoutData = []
        self.lenghtArray = []
        self.occupancies = []

class Passenger(QObject):
    def __init__(self, communicator: TrainComms):
        super().__init__()
        self.num_passengers_at_station = []
        self.num_passengers_embarking = []
        self.num_passengers_disembarking = []
        self.open_train_seats = []
        self.communicator = communicator

    # generate a random number of passengers at the station between 1 and 
    def gen_num_passengers_at_station(self):
        self.num_passengers_at_station = random.randint(1, 222)

    # return the value of the number of passengers at the station
    def get_num_passengers_at_station(self):
        return self.num_passengers_at_station

    # update the number of passengers at the station according to people boarding and leaving the train
    def update_num_passengers_at_station(self):
        self.num_passengers_at_station -= self.num_passengers_embarking
        self.num_passengers_at_station += self.num_passengers_disembarking

    # get the number of passengers leaving the train from the train model
    def get_num_passengers_leaving(self):
        self.communicator.number_passenger_leaving_signal.connect(self.handle_num_passenger_leaving_signal)

    # store the number of passengers leaving the train
    def handle_num_passenger_leaving_signal(self, num_people: list):
        self.num_passengers_disembarking = num_people

    # generate a random number between 0 and the number of people at station, send this value to the train model
    def get_num_passengers_boarding(self):
        self.num_passengers_embarking = random.randint(0, min(self.num_passengers_at_station, self.open_train_seats))
        self.communicator.number_passenger_boarding_signal.emit(self.num_passengers_embarking)
    
    # store the number of passengers leaving the train
    def handle_seat_vacancy_signal(self, train_vacancy: list): 
        self.open_train_seats = train_vacancy

    # get the number of open seats on the train from the train model
    def get_seat_vacancy(self):
        self.communicator.seat_vacancy_signal.connect(self.handle_seat_vacancy_signal)

class Station(QObject):
    def __init__(self, communicator: WaysideComms):
        self.station_status = []
        self.communicator = communicator

class Switch(QObject):
    def __init__(self, communicator: WaysideComms):
        self.switch_status = []
        self.signal_status = []
        self.communicator = communicator

    # def get_switch_cmds(self, switch_state):
    #     self.switch_status = switch_state

    # def get_signal_cmds(self, signal_state):
    #     self.signal_status = signal_state

    def handle_switch_cmds(self, switch_state):
        self.switch_status = switch_state
        

class Crossing(QObject):
    crossing_cmd_signal = pyqtSignal(list)

    def __init__(self, communicator: WaysideComms):
        self.crossing_status = []

class Block(QObject):
    commanded_speed_signal = pyqtSignal(list)
    commanded_authority_signal = pyqtSignal(list)
    block_occupancies_signal = pyqtSignal(list)
    block_grade_signal = pyqtSignal(list)
    block_elevation_signal = pyqtSignal(list)
    polarity_signal = pyqtSignal(list)
    position_signal = pyqtSignal(list)

    def __init__(self, line, section: str, number: int, length: float, grade: float, speedLimit: float, infrastructure: str, elevation: float, cumulativeElevation: float, side, polarity: bool = False, functional: bool = True, occupied: bool = False):
        super().__init__()
        self.line = line
        self.section = section
        self.number = number
        self.length = length
        self.grade = grade
        self.speedLimit = speedLimit
        self.infrastructure = infrastructure
        self.side = side
        self.elevation = elevation
        self.cumulativeElevation = cumulativeElevation
        self.polarity = polarity
        self.functional = functional
        self.occupied = occupied

        self.postion_list = []

        self.position_signal.connect(self.get_positions)

    def get_positions(self, positions):
        self.position_list = positions

    def set_positions(self):
        positions = [50, 1000, 2000, 7000]
        self.position_signal.emit(positions)

    def checkFailure(ui) -> bool:
        return any(toggle.isChecked() for toggle in [ui.breakStatus1, ui.breakStatus2, ui.breakStatus3])

    @classmethod
    def createBlocks(cls, ui, layoutData: List[List[str]], lengthArray: List[float], position: int) -> Dict[str, List['Block']]:
        sections = {row[1]: [] for row in layoutData}
        for row in layoutData:
            line, section, number, length, grade, speedLimit, infrastructure, side, elevation, cumulativeElevation = row[:10]
            block = cls(
                line=line,
                section=section,
                number=int(number),
                length=float(length),
                grade=float(grade),
                speedLimit=float(speedLimit),
                infrastructure=infrastructure,
                side=side,
                elevation=float(elevation),
                cumulativeElevation=float(cumulativeElevation)
            )
            sections[section].append(block)
        allBlocks = [block for blocks in sections.values() for block in blocks]
        cls.setOccupancy(ui, allBlocks, lengthArray, position)
        cls.setPolarity(allBlocks)
        return sections

    # def setPath(blocks: Dict[str, List['Block']], pathOrder: List[int]) -> Dict[int, 'Block']:
    #     path = {}
    #     for num in pathOrder:
    #         for blockList in blocks.values():
    #             for block in blockList:
    #                 if block.number == num:
    #                     path[block.number] = block
    #                     break
    #     return path

    @staticmethod
    def setOccupancy(ui, blocks: List['Block'], lengthArray: List[float], x: int) -> List[bool]:
        occupancies = []
        blockStart = 0
        for i, (length, block) in enumerate(zip(lengthArray, blocks)):
            blockEnd = blockStart + length
            if block.functional:
                occupied = blockStart <= x < blockEnd
            else:
                occupied = Block.checkFailure(ui) or (blockStart <= x < blockEnd)
            blocks[i].occupied = occupied
            occupancies.append(occupied)
            blockStart = blockEnd

        return occupancies

    @staticmethod
    def setPolarity(blocks: List['Block']) -> None:
        for i, block in enumerate(blocks):
            if block.number in defaultGreenPath:
                block.polarity = defaultGreenPath.index(block.number) % 2 == 0

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, Communicator: WaysideComms):
        super().__init__()
        self.ui = Ui_TrackModel()
        self.communicator = Communicator
        self.ui.setupUi(self)
        self.setupConnections()
        self.blocks = {}
        self.layoutData = []
        self.lengthArray = []
        self.occupancies = []
        self.switchStatus = False
        self.switchArray = []
        self.switchLightArray = []
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.recurring)
        self.timer.start(1000)
        self.tempIncreaseTimer = QtCore.QTimer(self)
        self.tempIncreaseTimer.timeout.connect(self.increaseTemp)
        # Block.setPath(self.blocks, defaultGreenPath)


    def read_wayside(self):
        pass

    def write_wayside(self):
        pass

    def read_train(self):
        Passenger.get_num_passengers_leaving()
        Passenger.get_seat_vacancy()

    def write_train(self):
        pass

    def setupConnections(self) -> None:
        self.ui.uploadButton.clicked.connect(self.uploadFile)
        self.ui.tempStepper.valueChanged.connect(self.checkTemp)
        self.ui.applyChangesButton.clicked.connect(self.applyChanges)
        self.ui.breakStatus1.toggled.connect(self.breakToggle1)
        self.ui.breakStatus2.toggled.connect(self.breakToggle2)
        self.ui.breakStatus3.toggled.connect(self.breakToggle3)
        self.ui.switchToggle.toggled.connect(self.checkSwitch)
        self.ui.blockTable.itemSelectionChanged.connect(self.printBlockInfo)

    def uploadFile(self) -> None:
        self.switchArray.clear()
        self.switchLightArray.clear()
        fileDialog = QtWidgets.QFileDialog()
        filePath, _ = fileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv)")
        if filePath:
            try:
                self.readLayoutFile(filePath)
                self.initializeBlocks()
            except Exception as e:
                print(f"Error reading file: {e}")

    def readLayoutFile(self, filePath: str) -> None:
        with open(filePath, newline='') as layoutFile:
            reader = csv.reader(layoutFile, delimiter=',', quotechar='|')
            next(reader)
            self.layoutData = []
            self.lengthArray = []
            for row in reader:
                self.layoutData.append(row)
                self.lengthArray.append(float(row[3]))

    def initializeBlocks(self) -> None:
        totLen = sum(self.lengthArray)
        self.ui.positionValue.setMaximum(totLen)
        position = self.ui.positionValue.value()
        self.blocks = Block.createBlocks(self.ui, self.layoutData, self.lengthArray, position)
        # self.path = Block.setPath(self.blocks, self.path)
        self.occupancies = Block.setOccupancy(self.ui, [block for blocks in self.blocks.values() for block in blocks], self.lengthArray, position)
        self.updateBlockTable()
        self.setSwitches()
        self.createCrossings()
        self.createStaions()


    def checkTemp(self) -> None:
        temp = self.ui.tempStepper.value()
        if temp <= 32:
            self.ui.heaterStatus.setStyleSheet("font: 10pt \"Times New Roman\";\nbackground-color: yellow;\ncolor: rgb(0, 0, 0);")
            QtCore.QTimer.singleShot(2000, self.initiateTempIncrease)
        else:
            self.ui.heaterStatus.setStyleSheet("font: 10pt \"Times New Roman\";\nbackground-color: rgb(68, 68, 68);\ncolor: rgb(0, 0, 0);")
            self.tempIncreaseTimer.stop()

    def initiateTempIncrease(self) -> None:
        self.tempIncreaseTimer.start(500)

    def increaseTemp(self) -> None:
        temp = self.ui.tempStepper.value()
        if temp <= 32:
            self.ui.tempStepper.setValue(temp + 1)
        else:
            self.tempIncreaseTimer.stop()

    def applyChanges(self) -> None:
        self.printPassInfo()

    def createStaions(self) -> None:
        self.stations = []
        for blocks in self.blocks.values():
            for block in blocks:
                if "STATION" in block.infrastructure:
                    self.stations.append(block.number)
        print(self.stations)

    @staticmethod
    def getSwitchNums(infrastructure: str) -> List[int]:
        return list(map(int, re.findall(r'\d+', infrastructure)))
    
    def setSwitches(self) -> None:
        for blocks in self.blocks.values():
            for block in blocks:
                if "SWITCH" in block.infrastructure:
                    switchNums = self.getSwitchNums(block.infrastructure)
                    joint = block.number
                    leg1 = min(num for num in switchNums if num != joint)
                    leg2 = max(num for num in switchNums if num != joint)
                    self.switchArray.append({'joint': joint, 'leg1': leg1, 'leg2': leg2})
                    self.switchLightArray.append({'joint': joint, 'leg1': leg1, 'leg2': leg2})
        self.ui.switches.clear()
        for switch in self.switchArray:
            self.ui.switches.addItem(f"Switch at Block {switch['joint']}")

    def checkSwitch(self) -> str:
        switchText = self.ui.switches.currentText()
        if switchText:
            joint = int(re.search(r'\d+', switchText).group())
            switch = next((b for blocks in self.blocks.values() for b in blocks if b.number == joint), None)
            if switch is None:
                return "Switch not found"
            switch_numbers = [num for num in self.getSwitchNums(switch.infrastructure) if num != joint]
            if switch_numbers:
                leg1 = min(switch_numbers)
                leg2 = max(switch_numbers)
            else:
                leg1 = leg2 = None
            if self.ui.switchToggle.isChecked():
                self.setLightColor(leg2, 'green')
                self.setLightColor(leg1, 'red')
                return f"{joint} to {leg2}"
            else:
                self.setLightColor(leg2, 'red')
                self.setLightColor(leg1, 'green')
                return f"{joint} to {leg1}"
        return "No switch selected"

    def setLightColor(self, blockNum: int, color: str) -> None:
        for light in self.switchLightArray:
            if light['leg1'] == blockNum or light['leg2'] == blockNum:
                if color == 'green':
                    self.ui.blockTable.item(blockNum , 2).setBackground(QtGui.QColor('green'))
                elif color == 'red':
                    self.ui.blockTable.item(blockNum , 2).setBackground(QtGui.QColor('red'))

    def createCrossings(self) -> None:
        self.crossingArray = []
        for blocks in self.blocks.values():
            for block in blocks:
                if "RAILWAY CROSSING" in block.infrastructure:
                    self.crossingArray.append(block.number)
                    self.setCrossingLights(block.number, 'green')
        self.ui.crossings.clear()
        for crossing in self.crossingArray:
            self.ui.crossings.addItem(f"Crossing at Block {crossing}")

    def checkCrossing(self) -> None:
        crossingText = self.ui.crossings.currentText()
        if crossingText:
            crossing = int(re.search(r'\d+', crossingText).group())
            if self.ui.crossingStatus.isChecked():
                self.setCrossingLights(crossing, 'red')
                return (f"Crossing at Block {crossing} is active.") 
            else:
                self.setCrossingLights(crossing, 'green')
                return (f"Crossing at Block {crossing} is clear.") 
            
    def setCrossingLights(self, blockNum: int, color: str) -> None:
        crossingText = self.ui.crossings.currentText()
        if crossingText:
            crossing = int(re.search(r'\d+', crossingText).group())
            if color == 'red':
                self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('red'))
            else:
                self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('green'))

    def printPassInfo(self) -> None:
        rowCount = self.ui.passInfoTable.rowCount()
        colCount = self.ui.passInfoTable.columnCount()
        for row in range(rowCount):
            data = [self.ui.passInfoTable.item(row, column).text() if self.ui.passInfoTable.item(row, column) else "" for column in range(colCount)]
            print(data)

    def breakToggle1(self) -> None:
        self.handleBreakToggle(self.ui.breakStatus1, self.ui.murphyBlockNumber1.value(), "Circuit")

    def breakToggle2(self) -> None:
        self.handleBreakToggle(self.ui.breakStatus2, self.ui.murphyBlockNumber2.value(), "Power")

    def breakToggle3(self) -> None:
        self.handleBreakToggle(self.ui.breakStatus3, self.ui.murphyBlockNumber3.value(), "Rail")

    def handleBreakToggle(self, toggle, blockNum: int, failureType: str) -> None:
        if toggle.isChecked():
            self.fail(blockNum)
            print(f"{failureType} failure on Block {blockNum}.")
        else:
            self.fix(blockNum)
        self.updateBlockTable()

    def fail(self, blockNum: int) -> None:
        for blocks in self.blocks.values():
            for block in blocks:
                if block.number == blockNum:
                    block.functional = False
                    block.occupied = True
                    allBlocks = [block for blocks in self.blocks.values() for block in blocks]
                    block.occupied = Block.setOccupancy(self.ui, allBlocks, self.lengthArray, self.ui.positionValue.value())[allBlocks.index(block)]
                    return

    def fix(self, blockNum: int) -> None:
        for blocks in self.blocks.values():
            for block in blocks:
                if block.number == blockNum:
                    block.functional = True
                    block.occupied = False
                    allBlocks = [block for blocks in self.blocks.values() for block in blocks]
                    block.occupied = Block.setOccupancy(self.ui, allBlocks, self.lengthArray, self.ui.positionValue.value())[allBlocks.index(block)]
                    print(f"Block {blockNum} is fixed.")
                    return

    def updateBlockTable(self) -> None:
        allBlocks = [block for blocks in self.blocks.values() for block in blocks]
        self.ui.blockTable.setRowCount(len(allBlocks))

        headers = ["Functional", "Occupied", "Switch State"]
        self.ui.blockTable.setColumnCount(len(headers))
        self.ui.blockTable.setHorizontalHeaderLabels(headers)

        for row, block in enumerate(allBlocks):
            functional_item = QtWidgets.QTableWidgetItem(str(block.functional))
            occupancy_item = QtWidgets.QTableWidgetItem(str(block.occupied))
            switch_item = QtWidgets.QTableWidgetItem("")
            passeneger_item = QtWidgets.QTableWidgetItem("")

            for switch in self.switchArray:
                if block.number == switch['joint']:
                    switch_item.setText(self.checkSwitch())

            for station in self.stations:
                if block.number == station:
                    passeneger_item.setText("Passenger Station")

            self.ui.blockTable.setItem(row, 0, functional_item)
            self.ui.blockTable.setItem(row, 1, occupancy_item)
            self.ui.blockTable.setItem(row, 2, switch_item)
            self.ui.blockTable.setItem(row, 3, passeneger_item)

            if block.occupied:
                for col in range(len(headers)-2):
                    self.ui.blockTable.item(row, col).setBackground(QtGui.QColor('lightblue'))
            if not block.functional:
                for col in range(len(headers)-2):
                    self.ui.blockTable.item(row, col).setBackground(QtGui.QColor('lightcoral'))

        self.ui.blockTable.cellClicked.connect(self.handleCellClick)

    def handleCellClick(self, row: int, column: int) -> None:
        if column == 2: 
            allBlocks = [block for blocks in self.blocks.values() for block in blocks]
            selectedBlock = allBlocks[row]
            for switch in self.switchArray:
                if selectedBlock.number == switch['joint']:
                    self.ui.switches.setCurrentText(f"Switch at Block {switch['joint']}")
                    self.ui.switchToggle.setChecked(not self.ui.switchToggle.isChecked())
                    switch_state = self.checkSwitch()
                    self.ui.blockTable.item(row, column).setText(switch_state)
                    break

    def printBlockInfo(self) -> None:
        selectedItems = self.ui.blockTable.selectedItems()
        if not selectedItems:
            return
        selectedRow = selectedItems[0].row()
        allBlocks = [block for blocks in self.blocks.values() for block in blocks]
        selectedBlock = allBlocks[selectedRow]

        self.ui.blockInfo.setRowCount(11)
        self.ui.blockInfo.setColumnCount(1)
        self.ui.blockInfo.setVerticalHeaderLabels([
            "Line", "Section", "Number", "Length", "Grade", "Speed Limit", 
            "Infrastructure", "Elevation", "Cumulative Elevation", "Side", "Polarity"
        ])
        self.ui.blockInfo.setItem(0, 0, QtWidgets.QTableWidgetItem(selectedBlock.line))
        self.ui.blockInfo.setItem(1, 0, QtWidgets.QTableWidgetItem(selectedBlock.section))
        self.ui.blockInfo.setItem(2, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.number)))
        self.ui.blockInfo.setItem(3, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.length)))
        self.ui.blockInfo.setItem(4, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.grade)))
        self.ui.blockInfo.setItem(5, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.speedLimit)))
        self.ui.blockInfo.setItem(6, 0, QtWidgets.QTableWidgetItem(selectedBlock.infrastructure))
        self.ui.blockInfo.setItem(7, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.elevation)))
        self.ui.blockInfo.setItem(8, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.cumulativeElevation)))
        self.ui.blockInfo.setItem(9, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.side)))
        self.ui.blockInfo.setItem(10, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.polarity)))

    def updateOccupancy(self) -> None:
        position = self.ui.positionValue.value()
        self.occupancies = Block.setOccupancy(self.ui, [block for blocks in self.blocks.values() for block in blocks], self.lengthArray, position)
        self.updateBlockTable()

    def recurring(self) -> None:
        self.updateOccupancy()
        self.checkSwitch()
        self.checkCrossing()
        self.checkTemp()
        

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())