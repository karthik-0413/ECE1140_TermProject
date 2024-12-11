from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject
import csv

class Ui_TrackModel(QObject):
        def __init__(self):
                super().__init__()
                self.functional_list = []
                self.occupancy_list = []
                self.switch_list = []
                self.crossing_list = []
                self.lights_list = []
                self.num_people_at_station_list = []

                #initialize these lists with the proper values in order to display in the table
                self.block_line_list = []
                self.block_section_list = []
                self.block_number_list = []
                self.block_grade_list = []
                self.block_length_list = []
                self.block_elevation_list = []
                self.block_cumulative_elevation_list = []
                self.block_infrastructure_list = []
                self.block_speed_limit_list = []
                self.block_side_list = []

                self.toggle_circuit_failure = []
                self.toggle_power_failure = []
                self.toggle_rail_failure = []

                self.heater_status = False
                self.temperature = 0

                self.greenCoordinates = []
                self.all_blocks = []

        def update_block_table(self):
                self.update_occupancy_list()
                self.update_functional_list()
                self.update_station_list()
                # self.update_switch_list()
                # self.update_crossing_list()
                # self.update_lights_list()
                # self.update_num_people_at_station_list()
        
        def initialize_block_info_table(self):
                self.blockInfo.setRowCount(12)
                self.blockInfo.setColumnCount(1)
                self.blockInfo.setVerticalHeaderLabels([
                "Line", "Section", "Number", "Length", "Grade", "Speed Limit", 
                "Infrastructure", "Elevation", "Cumulative Elevation", "Side", "Switch State", "Failure"
                ])
                self.blockInfo.setItem(0, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(1, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(2, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(3, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(4, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(5, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(6, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(7, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(8, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(9, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(10, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(11, 0, QtWidgets.QTableWidgetItem(""))


        def update_block_info_table(self):
                selected_items = self.blockTable.selectedItems()
                if selected_items:
                        selected_block_number = selected_items[0].text()
                        for block in self.all_blocks:
                                if str(block.number) == selected_block_number:
                                        self.blockInfo.setItem(0, 0, QtWidgets.QTableWidgetItem(block.line))
                                        self.blockInfo.setItem(1, 0, QtWidgets.QTableWidgetItem(block.section))
                                        self.blockInfo.setItem(2, 0, QtWidgets.QTableWidgetItem(str(block.number)))
                                        self.blockInfo.setItem(3, 0, QtWidgets.QTableWidgetItem(str(block.length)))
                                        self.blockInfo.setItem(4, 0, QtWidgets.QTableWidgetItem(str(block.grade)))
                                        self.blockInfo.setItem(5, 0, QtWidgets.QTableWidgetItem(str(block.speedLimit)))
                                        self.blockInfo.setItem(6, 0, QtWidgets.QTableWidgetItem(block.infrastructure))
                                        self.blockInfo.setItem(7, 0, QtWidgets.QTableWidgetItem(str(block.elevation)))
                                        self.blockInfo.setItem(8, 0, QtWidgets.QTableWidgetItem(str(block.cumulativeElevation)))
                                        self.blockInfo.setItem(9, 0, QtWidgets.QTableWidgetItem(block.side))
                                        if "SWITCH" in block.infrastructure:
                                                for switch_state in self.switch_list:  
                                                        if switch_state[1] == block.number:                                        
                                                                self.blockInfo.setItem(10, 0, QtWidgets.QTableWidgetItem(switch_state[0]))
                                        else:
                                                self.blockInfo.setItem(10, 0, QtWidgets.QTableWidgetItem("N/A"))
                                        break

                
        def update_heater_status(self):
                """if the rail temperature drops below 32 degrees, the heater turns on. default is off"""
                self.update_temp()
                if self.temperature < 32:
                        self.heater_status = True
                        self.heaterStatus.setStyleSheet("font: 10pt \"Times New Roman\";\nbackground-color: yellow;\ncolor: rgb(0, 0, 0);")
                else:
                        self.heater_status = False
                        self.heaterStatus.setStyleSheet("font: 10pt \"Times New Roman\";\nbackground-color: rgb(68, 68, 68);\ncolor: rgb(0, 0, 0);")

        def update_temp(self):
                self.temperature = self.tempStepper.value()    

        def update_functional_list(self):
                """updates the ui with the functional status of each block"""
                for block in self.all_blocks:
                        if (block.functional == False):
                                self.blockTable.item(block.table_row, block.table_column).setBackground(QtGui.QColor("red"))
                        else:
                                self.blockTable.item(block.table_row, block.table_column).setBackground(QtGui.QColor("green"))
                        
        def update_occupancy_list(self):
                """updates the ui with the occupational status of each block"""
                for block in self.all_blocks:
                        if (block.occupied and block.functional):
                                self.blockTable.item(block.table_row, block.table_column).setBackground(QtGui.QColor("blue"))
                        # elif (not block.functional):
                        #         self.blockTable.item(block.table_row, block.table_column).setBackground(QtGui.QColor("red"))
                        else:
                                self.blockTable.item(block.table_row, block.table_column).setBackground(QtGui.QColor("green"))  

        # def update_crossing_list(self):
        #         for crossing_state in self.crossing_list:
        #                 self.blockTable.setItem(crossing_state[1], 3, QtWidgets.QTableWidgetItem(crossing_state[0])) # open or closed

        def update_station_list(self):
                for block in self.all_blocks:
                        if ("STATION" in block.infrastructure) and (not block.occupied) and (block.functional):
                                self.blockTable.item(block.table_row, block.table_column).setBackground(QtGui.QColor("violet")) 

        # def update_lights_list(self):
        #         for light_state in self.lights_list:
        #                 self.blockTable.setItem(light_state[1], 4, QtWidgets.QTableWidgetItem(None))
        #                 self.blockTable.item(light_state[1], 4).setBackground(QtGui.QColor(str(light_state[0]))) # red or green

        # def update_num_people_at_station_list(self):
        #         for people in self.num_people_at_station_list:
        #                 self.blockTable.setItem(people[1], 5, QtWidgets.QTableWidgetItem(str(people[0])))
                
        # def initialize_block_table(self, num_blocks: int):
        #         self.blockTable.setRowCount(num_blocks)
        #         # glorious king zach changing the headers of the rows
        #         labels = []
        #         for i in range(num_blocks):
        #                 if i == 0:
        #                         labels.append("Yard")

        #                 else:
        #                         labels.append(f"{i}")

        #         self.blockTable.setVerticalHeaderLabels(labels)

        def initialize_map(self):
                self.blockTable.setColumnCount(38)
                self.blockTable.setRowCount(40)
                self.blockTable.horizontalHeader().setDefaultSectionSize(25)
                self.blockTable.verticalHeader().setDefaultSectionSize(25)
                self.blockTable.setStyleSheet("font: 10pt \"Times New Roman\";\ncolor: rgb(255, 255, 255);\ntext-align: center;")
                for i in range(38):
                        for j in range(40):
                                self.blockTable.setItem(j, i, QtWidgets.QTableWidgetItem())
                                self.blockTable.item(j, i).setBackground(QtGui.QColor("white"))
                for coord in self.greenCoordinates:
                        num, col, row = coord
                        self.blockTable.setItem(row, col, QtWidgets.QTableWidgetItem(str(num)))
                        self.blockTable.item(row, col).setBackground(QtGui.QColor("green"))      

        def setupUi(self, TrackModel):
                TrackModel.setObjectName("TrackModel")
                TrackModel.setWindowModality(QtCore.Qt.WindowModality.WindowModal)
                TrackModel.resize(890, 860)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
                sizePolicy.setHorizontalStretch(0)
                sizePolicy.setVerticalStretch(0)
                sizePolicy.setHeightForWidth(TrackModel.sizePolicy().hasHeightForWidth())
                TrackModel.setSizePolicy(sizePolicy)
                self.centralwidget = QtWidgets.QWidget(parent=TrackModel)
                self.centralwidget.setObjectName("centralwidget")
                self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
                self.gridLayout.setObjectName("gridLayout")
                self.verticalLayout = QtWidgets.QVBoxLayout()
                self.verticalLayout.setObjectName("verticalLayout")
                self.tabs = QtWidgets.QTabWidget(parent=self.centralwidget)
                self.tabs.setAutoFillBackground(False)
                self.tabs.setStyleSheet("font: 14pt \"Times New Roman\";\n"
                "color: rgb(0, 0, 0);\n"
                "background-color: rgb(204, 204, 204);")
                self.tabs.setDocumentMode(True)
                self.tabs.setTabsClosable(False)
                self.tabs.setTabBarAutoHide(False)
                self.tabs.setObjectName("tabs")
                self.tab = QtWidgets.QWidget()
                self.tab.setObjectName("tab")
                self.gridLayout_14 = QtWidgets.QGridLayout(self.tab)
                self.gridLayout_14.setObjectName("gridLayout_14")
                self.trackLayout_header = QtWidgets.QFrame(parent=self.tab)
                self.trackLayout_header.setObjectName("trackLayout_header")
                self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.trackLayout_header)
                self.verticalLayout_3.setObjectName("verticalLayout_3")
                self.blockInfo = QtWidgets.QTableWidget(parent=self.trackLayout_header)
                self.blockInfo.setObjectName("blockInfo")
                self.verticalLayout_3.addWidget(self.blockInfo)
                self.murphyControls = QtWidgets.QGroupBox(parent=self.trackLayout_header)
                self.murphyControls.setObjectName("murphyControls")
                self.gridLayout_3 = QtWidgets.QGridLayout(self.murphyControls)
                self.gridLayout_3.setObjectName("gridLayout_3")
                self.verticalLayout_7 = QtWidgets.QVBoxLayout()
                self.verticalLayout_7.setObjectName("verticalLayout_7")
                self.horizontalLayout = QtWidgets.QHBoxLayout()
                self.horizontalLayout.setObjectName("horizontalLayout")
                self.circuitFailureLabel = QtWidgets.QLabel(parent=self.murphyControls)
                self.circuitFailureLabel.setObjectName("circuitFailureLabel")
                self.horizontalLayout.addWidget(self.circuitFailureLabel)
                self.murphyBlockNumber1 = QtWidgets.QSpinBox(parent=self.murphyControls)
                self.murphyBlockNumber1.setObjectName("murphyBlockNumber1")
                self.horizontalLayout.addWidget(self.murphyBlockNumber1)
                self.breakStatus1 = QtWidgets.QCheckBox(parent=self.murphyControls)
                self.breakStatus1.setObjectName("breakStatus1")
                self.horizontalLayout.addWidget(self.breakStatus1)
                self.verticalLayout_7.addLayout(self.horizontalLayout)
                self.gridLayout_3.addLayout(self.verticalLayout_7, 0, 0, 1, 1)
                self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_3.setObjectName("horizontalLayout_3")
                self.poewrFailureLabel = QtWidgets.QLabel(parent=self.murphyControls)
                self.poewrFailureLabel.setObjectName("poewrFailureLabel")
                self.horizontalLayout_3.addWidget(self.poewrFailureLabel)
                self.murphyBlockNumber2 = QtWidgets.QSpinBox(parent=self.murphyControls)
                self.murphyBlockNumber2.setObjectName("murphyBlockNumber2")
                self.horizontalLayout_3.addWidget(self.murphyBlockNumber2)
                self.breakStatus2 = QtWidgets.QCheckBox(parent=self.murphyControls)
                self.breakStatus2.setObjectName("breakStatus2")
                self.horizontalLayout_3.addWidget(self.breakStatus2)
                self.gridLayout_3.addLayout(self.horizontalLayout_3, 1, 0, 1, 1)
                self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_2.setObjectName("horizontalLayout_2")
                self.railFailureLabel_2 = QtWidgets.QLabel(parent=self.murphyControls)
                self.railFailureLabel_2.setObjectName("railFailureLabel_2")
                self.horizontalLayout_2.addWidget(self.railFailureLabel_2)
                self.murphyBlockNumber3 = QtWidgets.QSpinBox(parent=self.murphyControls)
                self.murphyBlockNumber3.setObjectName("murphyBlockNumber3")
                self.horizontalLayout_2.addWidget(self.murphyBlockNumber3)
                self.breakStatus3 = QtWidgets.QCheckBox(parent=self.murphyControls)
                self.breakStatus3.setObjectName("breakStatus3")
                self.horizontalLayout_2.addWidget(self.breakStatus3)
                self.murphyBlockNumber1.setMinimum(1)
                self.murphyBlockNumber1.setMaximum(150)
                self.murphyBlockNumber2.setMinimum(1) 
                self.murphyBlockNumber2.setMaximum(150)
                self.murphyBlockNumber3.setMinimum(1)
                self.murphyBlockNumber3.setMaximum(150)
                self.gridLayout_3.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
                self.verticalLayout_3.addWidget(self.murphyControls)
                self.verticalLayout_5 = QtWidgets.QVBoxLayout()
                self.verticalLayout_5.setObjectName("verticalLayout_5")
                self.verticalLayout_6 = QtWidgets.QVBoxLayout()
                self.verticalLayout_6.setObjectName("verticalLayout_6")
                self.gridLayout_16 = QtWidgets.QGridLayout()
                self.gridLayout_16.setObjectName("gridLayout_16")
                self.tempStepper = QtWidgets.QSpinBox(parent=self.trackLayout_header)
                self.tempStepper.setStyleSheet("font: 20pt \"Times New Roman\";")
                self.tempStepper.setWrapping(False)
                self.tempStepper.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tempStepper.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.UpDownArrows)
                self.tempStepper.setAccelerated(False)
                self.tempStepper.setMinimum(-50)
                self.tempStepper.setMaximum(150)
                self.tempStepper.setProperty("value", 40)
                self.tempStepper.setObjectName("tempStepper")
                self.gridLayout_16.addWidget(self.tempStepper, 3, 1, 1, 1)
                self.heaterStatus = QtWidgets.QLabel(parent=self.trackLayout_header)
                self.heaterStatus.setStyleSheet("font: 10pt \"Times New Roman\";\n"
                "background-color: rgb(68, 68, 68);\n"
                "color: rgb(0, 0, 0);")
                self.heaterStatus.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.heaterStatus.setObjectName("heaterStatus")
                self.gridLayout_16.addWidget(self.heaterStatus, 3, 0, 1, 1)
                self.tempLabel = QtWidgets.QLabel(parent=self.trackLayout_header)
                self.tempLabel.setStyleSheet("font: 30pt \"Times New Roman\";")
                self.tempLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tempLabel.setObjectName("tempLabel")
                self.gridLayout_16.addWidget(self.tempLabel, 2, 0, 1, 2)
                self.verticalLayout_6.addLayout(self.gridLayout_16)
                self.uploadButton = QtWidgets.QPushButton(parent=self.trackLayout_header)
                self.uploadButton.setStyleSheet("font: 30pt \"Times New Roman\";")
                self.uploadButton.setAutoDefault(False)
                self.uploadButton.setDefault(False)
                self.uploadButton.setFlat(False)
                self.uploadButton.setObjectName("uploadButton")
                self.verticalLayout_6.addWidget(self.uploadButton)
                self.verticalLayout_5.addLayout(self.verticalLayout_6)
                self.verticalLayout_3.addLayout(self.verticalLayout_5)
                self.gridLayout_14.addWidget(self.trackLayout_header, 3, 3, 1, 1)
                self.tab1Label = QtWidgets.QLabel(parent=self.tab)
                self.tab1Label.setStyleSheet("font: 40pt \"Times New Roman\";\n"
                "background-color: rgb(0, 85, 255);\n"
                "color: rgb(255, 255, 255);")
                self.tab1Label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.tab1Label.setObjectName("tab1Label")
                self.gridLayout_14.addWidget(self.tab1Label, 0, 0, 2, 4)
                self.blockTable = QtWidgets.QTableWidget(parent=self.tab)
                self.blockTable.setObjectName("blockTable")
                self.gridLayout_14.addWidget(self.blockTable, 3, 0, 2, 1)
                self.tabs.addTab(self.tab, "")
                self.tab_2 = QtWidgets.QWidget()
                self.tab_2.setObjectName("tab_2")
                self.gridLayout_19 = QtWidgets.QGridLayout(self.tab_2)
                self.gridLayout_19.setObjectName("gridLayout_19")
                self.verticalLayout_9 = QtWidgets.QVBoxLayout()
                self.verticalLayout_9.setObjectName("verticalLayout_9")
                self.passInfoTable = QtWidgets.QTableWidget(parent=self.tab_2)
                self.blockTable.setRowCount(0)
                self.passInfoTable.setStyleSheet("font: 14pt \"Times New Roman\";\n"
                "color: rgb(0, 0, 0);")
                self.passInfoTable.setObjectName("passInfoTable")
                self.passInfoTable.setColumnCount(3)
                self.passInfoTable.setRowCount(15)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(2, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(3, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(4, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(5, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(6, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(7, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(8, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(9, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(10, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(11, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(12, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(13, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setVerticalHeaderItem(14, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setHorizontalHeaderItem(0, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setHorizontalHeaderItem(1, item)
                item = QtWidgets.QTableWidgetItem()
                self.passInfoTable.setHorizontalHeaderItem(2, item)
                self.passInfoTable.horizontalHeader().setDefaultSectionSize(123)
                self.verticalLayout_9.addWidget(self.passInfoTable)
                self.gridLayout_19.addLayout(self.verticalLayout_9, 7, 0, 1, 1)
                self.applyChangesButton = QtWidgets.QPushButton(parent=self.tab_2)
                self.applyChangesButton.setStyleSheet("font: 14pt \"Times New Roman\";\n"
                "color: rgb(0, 0, 0);")
                self.applyChangesButton.setObjectName("applyChangesButton")
                self.gridLayout_19.addWidget(self.applyChangesButton, 8, 0, 1, 2)
                self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_5.setObjectName("horizontalLayout_5")
                self.gridLayout_19.addLayout(self.horizontalLayout_5, 5, 0, 1, 1)
                self.textEdit = QtWidgets.QTextEdit(parent=self.tab_2)
                self.textEdit.setObjectName("textEdit")
                self.gridLayout_19.addWidget(self.textEdit, 3, 1, 5, 1)
                self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
                self.horizontalLayout_4.setObjectName("horizontalLayout_4")
                self.gridLayout_19.addLayout(self.horizontalLayout_4, 3, 0, 1, 1)
                self.beaconLabel = QtWidgets.QLabel(parent=self.tab_2)
                self.beaconLabel.setStyleSheet("font: 14pt \"Times New Roman\";\n"
                "color: rgb(0, 0, 0);")
                self.beaconLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.beaconLabel.setObjectName("beaconLabel")
                self.gridLayout_19.addWidget(self.beaconLabel, 0, 1, 1, 1)
                self.verticalLayout_2 = QtWidgets.QVBoxLayout()
                self.verticalLayout_2.setObjectName("verticalLayout_2")
                self.label_3 = QtWidgets.QLabel(parent=self.tab_2)
                self.label_3.setStyleSheet("font: 20pt \"Times New Roman\";\n"
                "color: rgb(0, 0, 0);")
                self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.label_3.setObjectName("label_3")
                self.verticalLayout_2.addWidget(self.label_3)
                self.positionValue = QtWidgets.QDoubleSpinBox(parent=self.tab_2)
                self.positionValue.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                self.positionValue.setObjectName("positionValue")
                self.verticalLayout_2.addWidget(self.positionValue)
                self.gridLayout_19.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
                self.switchCommands = QtWidgets.QGroupBox(parent=self.tab_2)
                self.switchCommands.setObjectName("switchCommands")
                self.gridLayout_2 = QtWidgets.QGridLayout(self.switchCommands)
                self.gridLayout_2.setObjectName("gridLayout_2")
                self.switches = QtWidgets.QComboBox(parent=self.switchCommands)
                self.switches.setStyleSheet("font: 16pt \"Times New Roman\";\n"
                "color: rgb(0, 0, 0);")
                self.switches.setObjectName("switches")
                self.gridLayout_2.addWidget(self.switches, 3, 0, 1, 1)
                self.switchToggle = QtWidgets.QCheckBox(parent=self.switchCommands)
                self.switchToggle.setObjectName("switchToggle")
                self.gridLayout_2.addWidget(self.switchToggle, 3, 1, 1, 1)
                self.gridLayout_19.addWidget(self.switchCommands, 4, 0, 1, 1)
                self.stationPicker = QtWidgets.QComboBox(parent=self.tab_2)
                self.stationPicker.setStyleSheet("font: 14pt \"Times New Roman\";\n"
                "color: rgb(0, 0, 0);")
                self.stationPicker.setObjectName("stationPicker")
                self.stationPicker.addItem("")
                self.stationPicker.addItem("")
                self.stationPicker.addItem("")
                self.gridLayout_19.addWidget(self.stationPicker, 1, 1, 1, 1)
                self.groupBox = QtWidgets.QGroupBox(parent=self.tab_2)
                self.groupBox.setObjectName("groupBox")
                self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox)
                self.gridLayout_4.setObjectName("gridLayout_4")
                self.crossings = QtWidgets.QComboBox(parent=self.groupBox)
                self.crossings.setObjectName("crossings")
                self.gridLayout_4.addWidget(self.crossings, 0, 0, 1, 1)
                self.crossingStatus = QtWidgets.QCheckBox(parent=self.groupBox)
                self.crossingStatus.setObjectName("crossingStatus")
                self.gridLayout_4.addWidget(self.crossingStatus, 0, 1, 1, 1)
                self.lightStatus = QtWidgets.QLabel(parent=self.groupBox)
                self.lightStatus.setStyleSheet("color: rgb(0, 0, 0);\n"
                "font: 16pt \"Times New Roman\";")
                self.lightStatus.setText("")
                self.lightStatus.setObjectName("lightStatus")
                self.gridLayout_4.addWidget(self.lightStatus, 0, 2, 1, 1)
                self.gridLayout_19.addWidget(self.groupBox, 6, 0, 1, 1)
                self.tabs.addTab(self.tab_2, "")
                self.verticalLayout.addWidget(self.tabs)
                self.gridLayout.addLayout(self.verticalLayout, 1, 1, 1, 1)
                TrackModel.setCentralWidget(self.centralwidget)
                self.statusbar = QtWidgets.QStatusBar(parent=TrackModel)
                self.statusbar.setObjectName("statusbar")
                TrackModel.setStatusBar(self.statusbar)

                self.retranslateUi(TrackModel)
                self.tabs.setCurrentIndex(0)
                QtCore.QMetaObject.connectSlotsByName(TrackModel)

                # self.blockTable.setRowCount(151)

                # # glorious king zach changing the headers of the rows
                # labels = []
                # for i in range(len(151)):
                #         if i == 0:
                #                 labels.append("Yard")

                #         else:
                #                 labels.append(f"{i}")

                # self.blockTable.setVerticalHeaderLabels(labels)

                # headers = ["Functional", "Occupied", "Switch State", "Crossing State", "Light State", "People at Station"]
                # self.blockTable.setColumnCount(len(headers))
                # self.blockTable.setHorizontalHeaderLabels(headers)

        def retranslateUi(self, TrackModel):
                _translate = QtCore.QCoreApplication.translate
                TrackModel.setWindowTitle(_translate("TrackModel", "Track Model"))
                self.murphyControls.setTitle(_translate("TrackModel", "Murphy\'s Controls"))
                self.circuitFailureLabel.setText(_translate("TrackModel", "Circuit Failure: Block"))
                self.breakStatus1.setText(_translate("TrackModel", "BREAK"))
                self.poewrFailureLabel.setText(_translate("TrackModel", "Power Failure: Block"))
                self.breakStatus2.setText(_translate("TrackModel", "BREAK"))
                self.railFailureLabel_2.setText(_translate("TrackModel", "Rail Failure: Block"))
                self.breakStatus3.setText(_translate("TrackModel", "BREAK"))
                self.tempStepper.setSuffix(_translate("TrackModel", " F"))
                self.heaterStatus.setText(_translate("TrackModel", "Heater"))
                self.tempLabel.setText(_translate("TrackModel", "Rail Temperature"))
                self.uploadButton.setText(_translate("TrackModel", "Upload New Layout"))
                self.tab1Label.setText(_translate("TrackModel", "Track Layout"))
                # item = self.blockTable.horizontalHeaderItem(0)
                # item.setText(_translate("TrackModel", "0"))
                # item = self.blockTable.horizontalHeaderItem(1)
                # item.setText(_translate("TrackModel", "1"))
                # item = self.blockTable.horizontalHeaderItem(2)
                # item.setText(_translate("TrackModel", "2"))
                # item = self.blockTable.horizontalHeaderItem(3)
                # item.setText(_translate("TrackModel", "3"))
                # item = self.blockTable.horizontalHeaderItem(4)
                # item.setText(_translate("TrackModel", "4"))
                # item = self.blockTable.horizontalHeaderItem(5)
                # item.setText(_translate("TrackModel", "5"))
                # item = self.blockTable.horizontalHeaderItem(6)
                # item.setText(_translate("TrackModel", "6"))
                # item = self.blockTable.horizontalHeaderItem(7)
                # item.setText(_translate("TrackModel", "7"))
                # item = self.blockTable.horizontalHeaderItem(8)
                # item.setText(_translate("TrackModel", "8"))
                # item = self.blockTable.horizontalHeaderItem(9)
                # item.setText(_translate("TrackModel", "9"))
                self.tabs.setTabText(self.tabs.indexOf(self.tab), _translate("TrackModel", "Track Layout"))
                item = self.passInfoTable.verticalHeaderItem(0)
                item.setText(_translate("TrackModel", "Block 1"))
                item = self.passInfoTable.verticalHeaderItem(1)
                item.setText(_translate("TrackModel", "Block 2"))
                item = self.passInfoTable.verticalHeaderItem(2)
                item.setText(_translate("TrackModel", "Block 3"))
                item = self.passInfoTable.verticalHeaderItem(3)
                item.setText(_translate("TrackModel", "Block 4"))
                item = self.passInfoTable.verticalHeaderItem(4)
                item.setText(_translate("TrackModel", "Block 5"))
                item = self.passInfoTable.verticalHeaderItem(5)
                item.setText(_translate("TrackModel", "Block 6"))
                item = self.passInfoTable.verticalHeaderItem(6)
                item.setText(_translate("TrackModel", "Block 7"))
                item = self.passInfoTable.verticalHeaderItem(7)
                item.setText(_translate("TrackModel", "Block 8"))
                item = self.passInfoTable.verticalHeaderItem(8)
                item.setText(_translate("TrackModel", "Block 9"))
                item = self.passInfoTable.verticalHeaderItem(9)
                item.setText(_translate("TrackModel", "Block 10"))
                item = self.passInfoTable.verticalHeaderItem(10)
                item.setText(_translate("TrackModel", "Block 11"))
                item = self.passInfoTable.verticalHeaderItem(11)
                item.setText(_translate("TrackModel", "Block 12"))
                item = self.passInfoTable.verticalHeaderItem(12)
                item.setText(_translate("TrackModel", "Block 13"))
                item = self.passInfoTable.verticalHeaderItem(13)
                item.setText(_translate("TrackModel", "Block 14"))
                item = self.passInfoTable.verticalHeaderItem(14)
                item.setText(_translate("TrackModel", "Block 15"))
                item = self.passInfoTable.horizontalHeaderItem(0)
                item.setText(_translate("TrackModel", "Commanded Speed"))
                item = self.passInfoTable.horizontalHeaderItem(1)
                item.setText(_translate("TrackModel", "Authority"))
                item = self.passInfoTable.horizontalHeaderItem(2)
                item.setText(_translate("TrackModel", "Vacancy"))
                self.applyChangesButton.setText(_translate("TrackModel", "Apply Changes"))
                self.beaconLabel.setText(_translate("TrackModel", "Beacon Information"))
                self.label_3.setText(_translate("TrackModel", "Position"))
                self.positionValue.setSuffix(_translate("TrackModel", " m"))
                self.switchCommands.setTitle(_translate("TrackModel", "Switch Commands"))
                self.switchToggle.setText(_translate("TrackModel", "Toggle"))
                self.stationPicker.setItemText(0, _translate("TrackModel", "Station A"))
                self.stationPicker.setItemText(1, _translate("TrackModel", "Station B"))
                self.stationPicker.setItemText(2, _translate("TrackModel", "Station C"))
                self.groupBox.setTitle(_translate("TrackModel", "Crossing Commands"))
                self.crossingStatus.setText(_translate("TrackModel", "Toggle"))
                self.tabs.setTabText(self.tabs.indexOf(self.tab_2), _translate("TrackModel", "Testbench"))

        def initializa_block_info_table(self):
                self.blockInfo.setRowCount(10)
                self.blockInfo.setColumnCount(1)
                self.blockInfo.setVerticalHeaderLabels([
                "Line", "Section", "Number", "Length", "Grade", "Speed Limit", 
                "Infrastructure", "Elevation", "Cumulative Elevation", "Side"
                ])
                self.blockInfo.setItem(0, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(1, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(2, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(3, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(4, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(5, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(6, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(7, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(8, 0, QtWidgets.QTableWidgetItem(""))
                self.blockInfo.setItem(9, 0, QtWidgets.QTableWidgetItem(""))