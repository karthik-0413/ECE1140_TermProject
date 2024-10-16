import sys
import csv
import re
from typing import List, Dict
from PyQt6 import QtWidgets, QtCore, QtGui
from Track_Model_UI import Ui_TrackModel

class Block:
    def __init__(self, line: str, section: str, number: int, length: float, grade: float, speedLimit: float, infrastructure: str, elevation: float, cumulativeElevation: float, right: bool = False, left: bool = False, polarity: bool = False, functional: bool = True, occupied: bool = False):
        self.line = line
        self.section = section
        self.number = number
        self.length = length
        self.grade = grade
        self.speedLimit = speedLimit
        self.infrastructure = infrastructure
        self.right = right
        self.left = left
        self.elevation = elevation
        self.cumulativeElevation = cumulativeElevation
        self.polarity = polarity
        self.functional = functional
        self.occupied = occupied

    @staticmethod
    def checkFailure(ui) -> bool:
        return any(toggle.isChecked() for toggle in [ui.breakStatus1, ui.breakStatus2, ui.breakStatus3])

    @classmethod
    def createBlocks(cls, ui, layoutData: List[List[str]], lengthArray: List[float], position: int) -> Dict[str, List['Block']]:
        sections = {row[1]: [] for row in layoutData}
        for row in layoutData:
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
            sections[section].append(block)
        allBlocks = [block for blocks in sections.values() for block in blocks]
        cls.setOccupancy(ui, allBlocks, lengthArray, position)
        cls.setPolarity(allBlocks)
        for section, blocks in sections.items():
            print(f"Section: {section}")
            for block in blocks:
                print(f"Block {block.number}")
        return sections

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
            block.polarity = i % 2 == 0

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_TrackModel()
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
        self.occupancies = Block.setOccupancy(self.ui, [block for blocks in self.blocks.values() for block in blocks], self.lengthArray, position)
        self.updateBlockTable()
        self.createSwitches()
        self.createCrossings()

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
                    self.crossingArray.append(block.number)

    @staticmethod
    def extractSwitchNumbers(infrastructure: str) -> List[int]:
        return list(map(int, re.findall(r'\d+', infrastructure)))
    
    def createSwitches(self) -> None:
        for blocks in self.blocks.values():
            for block in blocks:
                if "SWITCH" in block.infrastructure:
                    switchNums = self.extractSwitchNumbers(block.infrastructure)
                    joint = next(num for num in switchNums if switchNums.count(num) == 2)
                    leg1 = min(num for num in switchNums if num != joint)
                    leg2 = max(num for num in switchNums if num != joint)
                    self.switchArray.append({'joint': joint, 'leg1': leg1, 'leg2': leg2})
                    self.switchLightArray.append({'leg1': leg1, 'leg2': leg2})
        self.ui.switches.clear()
        for switch in self.switchArray:
            self.ui.switches.addItem(f"Switch at Block {switch['joint']}")

    def checkSwitch(self) -> str:
        switchText = self.ui.switches.currentText()
        if switchText:
            joint = int(re.search(r'\d+', switchText).group())
            switch = next(b for blocks in self.blocks.values() for b in blocks if b.number == joint)
            leg1 = min(num for num in self.extractSwitchNumbers(switch.infrastructure) if num != joint)
            leg2 = max(num for num in self.extractSwitchNumbers(switch.infrastructure) if num != joint)
            if self.ui.switchToggle.isChecked():
                self.setLightColor(leg2, 'green')
                self.setLightColor(leg1, 'red')
                return f"{joint} to {leg2}"
            else:
                self.setLightColor(leg2, 'red')
                self.setLightColor(leg1, 'green')
                return f"{joint} to {leg1}"

    def setLightColor(self, blockNum: int, color: str) -> None:
        for light in self.switchLightArray:
            if light['leg1'] == blockNum or light['leg2'] == blockNum:
                if color == 'green':
                    self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('green'))
                elif color == 'red':
                    self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('red'))
                elif color == 'yellow':
                    self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('yellow'))

    def createCrossings(self) -> None:
        self.crossingArray = []
        for blocks in self.blocks.values():
            for block in blocks:
                if "RAILWAY CROSSING" in block.infrastructure:
                    self.crossingArray.append(block.number)
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
                self.setCrossingLights(crossing, 'lightgray')
                return (f"Crossing at Block {crossing} is clear.") 
            
    def setCrossingLights(self, blockNum: int, color: str) -> None:
        crossingText = self.ui.crossings.currentText()
        if crossingText:
            crossing = int(re.search(r'\d+', crossingText).group())
            if color == 'red':
                self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('red'))
            else:
                self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('lightgray'))

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

            for switch in self.switchArray:
                if block.number == switch['joint']:
                    switch_item.setText(self.checkSwitch())

            self.ui.blockTable.setItem(row, 0, functional_item)
            self.ui.blockTable.setItem(row, 1, occupancy_item)
            self.ui.blockTable.setItem(row, 2, switch_item)

            if block.occupied:
                for col in range(len(headers)-1):
                    self.ui.blockTable.item(row, col).setBackground(QtGui.QColor('lightblue'))
            if not block.functional:
                for col in range(len(headers)-1):
                    self.ui.blockTable.item(row, col).setBackground(QtGui.QColor('lightcoral'))

    def printBlockInfo(self) -> None:
        selectedItems = self.ui.blockTable.selectedItems()
        if not selectedItems:
            return
        selectedRow = selectedItems[0].row()
        allBlocks = [block for blocks in self.blocks.values() for block in blocks]
        selectedBlock = allBlocks[selectedRow]

        self.ui.blockInfo.setRowCount(12)
        self.ui.blockInfo.setColumnCount(1)
        self.ui.blockInfo.setVerticalHeaderLabels([
            "Line", "Section", "Number", "Length", "Grade", "Speed Limit", 
            "Infrastructure", "Elevation", "Cumulative Elevation", "Right", 
            "Left", "Polarity"
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
        self.ui.blockInfo.setItem(9, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.right)))
        self.ui.blockInfo.setItem(10, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.left)))
        self.ui.blockInfo.setItem(11, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.polarity)))

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
