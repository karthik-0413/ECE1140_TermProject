import sys, os, csv, re, random
from typing import List, Dict
from PyQt6 import QtWidgets, QtCore, QtGui
from PyQt6.QtCore import (QObject, pyqtSignal)


# from TrackModel.track_model_ui import Ui_TrackModel
# from TrackModel.TrackTrainCommunicate import TrackTrainComms as TrainComms
# from TrackModel.WaysideTrackCommunicate import WaysideTrackComms as WaysideComms

from TrackModel.track_model_ui import Ui_TrackModel
from TrackTrainCommunicate import TrackTrainComms as TrainComms
from WaysideTrackCommunicate import WaysideTrackComms as WaysideComms

class Block():
    def __init__(self, line, section, number: int, length: float, grade: float, speedLimit: float, infrastructure: str, side, elevation: float, cumulativeElevation: float, polarity: bool):
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
        self.functional = True
        self.occupied = False

    # def checkFailure(ui) -> bool:
    #     return any(toggle.isChecked() for toggle in [ui.breakStatus1, ui.breakStatus2, ui.breakStatus3])

class track_model:
    # defaultRedPath = [
    #     0, 9, 8, 7, 6, 5, 4, 3, 2, 1, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 76, 75,
    #     74, 73, 72, 33, 34, 35, 36, 37, 38, 71, 70, 69, 68, 67, 44, 45, 46, 47, 48, 49, 50, 51,
    #     52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 52, 51, 50, 49, 48, 47, 46,
    #     45, 44, 43, 42, 41, 40, 39, 38, 37, 36, 35, 34, 33, 32, 31, 30, 29, 28, 27, 26, 25, 24,
    #     23, 22, 21, 20, 19, 18, 17, 16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0
    # ]
    defaultGreenPath = [
        0, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100,
        85, 84, 83, 82, 81, 80, 79, 78, 77, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124,
        125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 28, 27, 26, 25, 24, 23,
        22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 151, 6, 5, 4, 3, 2, 1, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
        32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 0
    ]
    
    ############################################################################################################
    #
    #                                           Constructor Function   
    #
    ############################################################################################################
    def __init__(self, train_communicator: TrainComms, wayside_communicator: WaysideComms):
        # communicate object for both wayside and train model
        self.train_communicator = train_communicator
        self.wayside_communicator = wayside_communicator

        # ui object
        self.ui = track_ui()
        self.ui.show()

        self.ui.uploadButton.clicked.connect(self.upload_file)
        self.ui.murphyBlockNumber1.valueChanged.connect(self.handle_circuit_failure_num_step)
        self.ui.murphyBlockNumber2.valueChanged.connect(self.handle_power_failure_num_step)
        self.ui.murphyBlockNumber3.valueChanged.connect(self.handle_rail_failure_num_step)
        self.ui.breakStatus1.toggled.connect(self.handle_circuit_failure_checkbox)
        self.ui.breakStatus2.toggled.connect(self.handle_power_failure_checkbox)
        self.ui.breakStatus3.toggled.connect(self.handle_rail_failure_checkbox)

        # remove comments for testing
        # self.read_train()
        # self.read_wayside()
        self.update_block_values()

    # important arrays
    all_blocks = []
    layout_data = []
    ui_switch_array = []
    ui_light_array = []
    ui_crossing_array = []
    ui_people_at_station = []
    position_list = []
    occupancies = []
    default_length_array = []
    station_list = []

    current_block = []

        # self.timer = QtCore.QTimer(self)
        # self.timer.timeout.connect(self.recurring)
        # self.timer.start(1000)
        # self.tempIncreaseTimer = QtCore.QTimer(self)
        # self.tempIncreaseTimer.timeout.connect(self.increaseTemp)

    
    ############################################################################################################
    #
    #                                           Train Model Integration   
    #
    ############################################################################################################
    # variables
    num_passengers_at_station = []
    num_passengers_embarking = []
    grade_values = []
    elevation_values = []
    polarity_values = []

    # Speed and Authority to be sent to Train Model
    cmd_speeds_train = []
    cmd_authorities_train = []

    # Passengers
    open_train_seats = []

    # get the number of passengers leaving the train from the train model
    def get_num_passengers_leaving(self):
        self.train_communicator.number_passenger_leaving_signal.connect(self.handle_num_passenger_leaving_signal)

    # store the number of passengers leaving the train
    def handle_num_passenger_leaving_signal(self, num_people: list):
        self.num_passengers_disembarking = num_people

    # generate a random number between 0 and the number of people at station, send this value to the train model
    def get_num_passengers_boarding(self):
        self.num_passengers_embarking = random.randint(0, min(self.num_passengers_at_station, self.open_train_seats))

    # store the number of passengers leaving the train
    def handle_seat_vacancy_signal(self, train_vacancy: list): 
        self.open_train_seats = train_vacancy

    # get the number of open seats on the train from the train model
    def get_seat_vacancy(self):
        self.train_communicator.seat_vacancy_signal.connect(self.handle_seat_vacancy_signal)

    def handle_position_signal(self, positions: list):
        self.position_list = positions
        print(f"received position: {self.position_list}")
        self.set_train_occupancies()
        self.update_polarity_values()

    # def get_positions(self):
    #     self.train_communicator.position_signal.connect(self.handle_position_signal)

   
    def update_polarity_values(self):
        self.polarity_values.clear()
        for i in range(len(self.current_block)):
            if self.all_blocks[self.current_block[i]].polarity == 0:
                self.polarity_values.append(False)
            else:
                self.polarity_values.append(True)
        # print(f"track: {self.polarity_values}")

    def update_grade_values(self):
        self.all_blocks.clear()
        for block in self.all_blocks:
            if block.occupied == True and block.functional == True:
                self.grade_values.append(block.grade)

    def update_elevation_values(self):
        self.elevation_values.clear()
        for block in self.all_blocks:
            if block.occupied == True and block.functional == True:
                self.elevation_values.append(block.elevation)

    def update_block_values(self):
        self.update_grade_values()
        self.update_elevation_values()

############################################################################################################
#
#                                           Wayside Integration   
#
############################################################################################################
    # variables
    switch_cmds = []
    light_cmds = []
    crossing_cmds = []
    cmd_speeds_wayside = []
    cmd_authorities_wayside = []
    past_cmd_speeds_wayside = []
    past_cmd_authorities_wayside = []

    # Lights
        # holds the values of all the lights on the track.
        # 0: green
        # 1: red
            # section C, block 12
            # section D, block 13
            # section F, block 28
            # section G, block 29
            # section J, block 58
            # section K, block 63
            # section N, block 77
            # section N, block 85
            # section O, block 86
            # section R, block 101
            # yard
    
    # Switches
        # holds the values of all the switches on the track.
        # 0: goes to the smaller block number that does not repeat twice in the infrastructure string
        # 1: goes to the larger block number that does not repeat twice in the infrastructure string
            # section D, block 13: 1, 12
            # section F, block 28: 29, 150
            # section I, block 57: 0, 58
            # section K, block 63: 0, 62
            # section N, block 77: 76, 101
            # section N, block 85: 86, 100
    

    # Crossings
        # holds the values of all the crossings on the track.
        # 0: open
        # 1: closed

    def handle_switch_cmd_signal(self, switch_cmds: list):
        self.switch_cmds = switch_cmds
        self.update_switch_status()

    def handle_signal_cmd_signal(self, light_cmds: list):
        self.light_cmds = light_cmds
        self.update_light_status()

    def handle_crossing_cmd_signal(self, crossing_cmds: list):
        self.crossing_cmds = crossing_cmds
        self.update_crossing_status()

    def handle_commanded_speed_signal(self, cmd_speeds: list):
        self.past_cmd_speeds_wayside = self.cmd_speeds_wayside
        self.cmd_speeds_wayside = cmd_speeds

        # if len(self.cmd_speeds_wayside):
        #      # print(f"Received Cmd Speed: {self.cmd_speeds_wayside[0]}")

        # Update the train commanded speeds
        self.update_train_cmd_speeds()

    def handle_commanded_authority_signal(self, cmd_authorities: list):
        self.cmd_authorities = cmd_authorities
        self.past_cmd_authorities_wayside = self.cmd_authorities_wayside
        self.cmd_authorities_wayside = cmd_authorities

        # if len(self.cmd_authorities_wayside):
        #     # print(f"Received Cmd Authority: {self.cmd_authorities_wayside[0]}")

        # Update the train commanded authorities
        self.update_train_cmd_authorities()

    ############################################################################################################
    #
    #                                           Read and Writes
    #
    ############################################################################################################

    # uncomment for testing
    # def read_train(self):
    #     self.train_communicator.number_passenger_leaving_signal.connect(self.handle_num_passenger_leaving_signal)
    #     self.train_communicator.seat_vacancy_signal.connect(self.handle_seat_vacancy_signal)
    #     self.train_communicator.position_signal.connect(self.handle_position_signal)

    # def read_wayside(self):
    #     self.wayside_communicator.switch_cmd_signal.connect(self.handle_switch_cmd_signal)
    #     self.wayside_communicator.signal_cmd_signal.connect(self.handle_signal_cmd_signal)
    #     self.wayside_communicator.crossing_cmd_signal.connect(self.handle_crossing_cmd_signal)
    #     self.wayside_communicator.commanded_speed_signal.connect(self.handle_commanded_speed_signal)
    #     self.wayside_communicator.commanded_authority_signal.connect(self.handle_commanded_authority_signal)

    def write(self):
        # print('Occupancies:', self.occupancies)


        # Update UI
        self.update_ui_list()
        
    def upload_file(self) -> None:
        self.ui_switch_array.clear()
        self.ui_light_array.clear()
        fileDialog = QtWidgets.QFileDialog()
        filePath, _ = fileDialog.getOpenFileName(self.ui, "Open CSV File", "", "CSV Files (*.csv)")
        if filePath:
            try:
                self.read_layout_file(filePath)
            except Exception as e:
                pass
                # print(f"Error reading file: {e}")

    def read_layout_file(self, filePath: str) -> None:
        with open(filePath, newline='') as layoutFile:
            reader = csv.reader(layoutFile, delimiter=',', quotechar='|')
            next(reader)
            self.layout_data = []
            for row in reader:
                self.layout_data.append(row)
                for row in self.layout_data:
                    line, section, number, length, grade, speedLimit, infrastructure, side, elevation, cumulativeElevation, polarity = row[:11]
                    temp_block = Block(line,section,int(number),float(length),float(grade),float(speedLimit),infrastructure,side,float(elevation),float(cumulativeElevation),int(polarity)
                )
                self.all_blocks.append(temp_block)
        self.initialize_arrays()
        self.update_ui_list()
        # for block in self.all_blocks:
        #     # print(f"{block.number}, {block.polarity}")

    def create_length_array(self):
        self.default_length_array.clear()
        # iterate through all the numbers in the default green path
        for block_number in self.defaultGreenPath:
            # append the length of the block to the default length array
            # # print(block_number)
            self.default_length_array.append(self.all_blocks[block_number].length)
            
    def set_train_occupancies(self):
        # resets all occupancies from the previous train ~ glorious king zach
        self.occupancies.clear()
        self.current_block.clear()
        for block in self.all_blocks:
            block.occupied = False

        #print(f"Position List: {self.position_list}")
        for position_value in self.position_list:
            #print(f"Position Value: {position_value}")
            # Position value confirmed
            block_start = 0
            for i in range(len(self.default_length_array)):
                block_end = block_start + self.default_length_array[i]
                if (block_start <= position_value < block_end):
                    self.all_blocks[self.defaultGreenPath[i]].occupied = True
                    self.current_block.append(self.all_blocks[self.defaultGreenPath[i]].number)
                #else:
                    #self.all_blocks[self.defaultGreenPath[i]].occupied = False
                block_start = block_end

        for block in self.all_blocks:
            self.occupancies.append(block.occupied)

        print(f"Occupancy locations: {[block.number for block in self.all_blocks if block.occupied == True]}")

        

    def set_failure_occupancies(self):
        for i in range(len(self.all_blocks)):
            if self.ui.functional_list[i] != 1:
                self.occupancies[i] = True

############################################################################################################
#
#                                           Testbench Functions  
#
############################################################################################################
    # def checkTemp(self):
    #     temp = self.ui.tempStepper.value()
    #     if temp <= 32:
    #         self.ui.heaterStatus.setStyleSheet("font: 10pt \"Times New Roman\";\nbackground-color: yellow;\ncolor: rgb(0, 0, 0);")
    #         QtCore.QTimer.singleShot(2000, self.initiateTempIncrease)
    #     else:
    #         self.ui.heaterStatus.setStyleSheet("font: 10pt \"Times New Roman\";\nbackground-color: rgb(68, 68, 68);\ncolor: rgb(0, 0, 0);")
    #         self.tempIncreaseTimer.stop()

    # def initiateTempIncrease(self) -> None:
    #     self.tempIncreaseTimer.start(500)

    # def increaseTemp(self) -> None:
    #     temp = self.ui.tempStepper.value()
    #     if temp <= 32:
    #         self.ui.tempStepper.setValue(temp + 1)
    #     else:
    #         self.tempIncreaseTimer.stop()

    # def applyChanges(self) -> None:
    #     self.# printPassInfo()

    # def checkSwitch(self) -> str:
    #     switchText = self.ui.switches.currentText()
    #     if switchText:
    #         joint = int(re.search(r'\d+', switchText).group())
    #         switch = next((b for blocks in self.blocks.values() for b in blocks if b.number == joint), None)
    #         if switch is None:
    #             return "Switch not found"
    #         switch_numbers = [num for num in self.getSwitchNums(switch.infrastructure) if num != joint]
    #         if switch_numbers:
    #             leg1 = min(switch_numbers)
    #             leg2 = max(switch_numbers)
    #         else:
    #             leg1 = leg2 = None
    #         if self.ui.switchToggle.isChecked():
    #             self.setLightColor(leg2, 'green')
    #             self.setLightColor(leg1, 'red')
    #             return f"{joint} to {leg2}"
    #         else:
    #             self.setLightColor(leg2, 'red')
    #             self.setLightColor(leg1, 'green')
    #             return f"{joint} to {leg1}"
    #     return "No switch selected"

    # def setLightColor(self, blockNum: int, color: str) -> None:
    #     for light in self.ui_light_array:
    #         if light['leg1'] == blockNum or light['leg2'] == blockNum:
    #             if color == 'green':
    #                 self.ui.blockTable.item(blockNum , 2).setBackground(QtGui.QColor('green'))
    #             elif color == 'red':
    #                 self.ui.blockTable.item(blockNum , 2).setBackground(QtGui.QColor('red'))

    # def createCrossings(self) -> None:
    #     self.crossingArray = []
    #     for blocks in self.blocks.values():
    #         for block in blocks:
    #             if "RAILWAY CROSSING" in block.infrastructure:
    #                 self.crossingArray.append(block.number)
    #                 self.setCrossingLights(block.number, 'green')
    #     self.ui.crossings.clear()
    #     for crossing in self.crossingArray:
    #         self.ui.crossings.addItem(f"Crossing at Block {crossing}")

    # def checkCrossing(self) -> None:
    #     crossingText = self.ui.crossings.currentText()
    #     if crossingText:
    #         crossing = int(re.search(r'\d+', crossingText).group())
    #         if self.ui.crossingStatus.isChecked():
    #             self.setCrossingLights(crossing, 'red')
    #             return (f"Crossing at Block {crossing} is active.") 
    #         else:
    #             self.setCrossingLights(crossing, 'green')
    #             return (f"Crossing at Block {crossing} is clear.") 
            
    # def setCrossingLights(self, blockNum: int, color: str) -> None:
    #     crossingText = self.ui.crossings.currentText()
    #     if crossingText:
    #         crossing = int(re.search(r'\d+', crossingText).group())
    #         if color == 'red':
    #             self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('red'))
    #         else:
    #             self.ui.blockTable.item(blockNum - 1, 2).setBackground(QtGui.QColor('green'))

    # def # printPassInfo(self) -> None:
    #     rowCount = self.ui.passInfoTable.rowCount()
    #     colCount = self.ui.passInfoTable.columnCount()
    #     for row in range(rowCount):
    #         data = [self.ui.passInfoTable.item(row, column).text() if self.ui.passInfoTable.item(row, column) else "" for column in range(colCount)]
    #         # print(data)

############################################################################################################
#
#                                           Station Functions
#
############################################################################################################
    def update_station_list(self):
        for block in self.all_blocks:
            if "STATION" in block.infrastructure:
                self.station_list.append(block.number)

    # generate a random number of passengers at the station between 1 and 222
    def gen_num_passengers_at_station(self):
        for i in range(len(self.station_list)):
            self.num_passengers_at_station.append(random.randint(1, 222)) 

    # update the number of passengers at the station according to people boarding and leaving the train
    def update_num_passengers_at_station(self, passengers_disembarking, seats_available):
        for i in range(len(self.station_list)):
            temp_num = random.randint(0, min(self.num_passengers_at_station[i], seats_available))
            self.num_passengers_at_station[i] -= temp_num
            self.num_passengers_at_station[i] += passengers_disembarking


############################################################################################################
#
#                                           Internal Functions: Switches
#
############################################################################################################
    # variables
    switch_state_array = []
    switch_block_array = []
    @staticmethod
    def getSwitchNums(infrastructure: str) -> List[int]:
        return list(map(int, re.findall(r'\d+', infrastructure)))
    
    # this function updates the two key values that we want to use in updating our block table
    def update_switch_states(self):
        for block in self.all_blocks:
            if "SWITCH" in block.infrastructure:
                switch_numbers = self.getSwitchNums(block.infrastructure)
                joint = next(num for num in switch_numbers if switch_numbers.count(num) == 2)
                leg1 = min(num for num in switch_numbers if num != joint)
                leg2 = max(num for num in switch_numbers if num != joint)
                self.switch_state_array.append([f"{joint} to {leg1}", f"{joint} to {leg2}"])
                self.switch_block_array.append(joint)
        
    # this function will get the switch state to update the block table
    def update_switch_status(self):
            if len(self.switch_state_array) > 0:
                self.ui_switch_array.clear()
                for i in range(len(self.switch_cmds)):
                    if self.switch_cmds[i]:
                        self.ui_switch_array.append([self.switch_state_array[i][1], self.switch_block_array[i]]) 
                    else:
                        self.ui_switch_array.append([self.switch_state_array[i][0], self.switch_block_array[i]])


############################################################################################################
#
#                                           Internal Functions: Crossings
#
############################################################################################################
    # variables
    crossing_block_array = []

    def update_crossing_states(self):
        for block in self.all_blocks:
            if "RAILWAY CROSSING" in block.infrastructure:
                self.crossing_block_array.append(block.number)

    def update_crossing_status(self):
        if len(self.crossing_block_array) > 0:
            self.ui_crossing_array.clear()
            for i in range(len(self.crossing_cmds)):
                if self.crossing_cmds[i]:
                    self.ui_crossing_array.append(["Closed", self.crossing_block_array[i]])
                else:
                    self.ui_crossing_array.append(["Open", self.crossing_block_array[i]])


############################################################################################################
#
#                                           Internal Functions: Lights
#
############################################################################################################
    # variables
    light_block_array = []

    def update_light_states(self):
        for block in self.all_blocks:
            if "LIGHT" in block.infrastructure:
                self.light_block_array.append(block.number)

    def update_light_status(self):
        if len(self.light_block_array) > 0:
            self.ui_light_array.clear()
            for i in range(len(self.light_cmds)):
                if self.light_cmds[i]:
                    self.ui_light_array.append(['red', self.light_block_array[i]]) # 0 is red, 1 is green
                else:
                    self.ui_light_array.append(['green', self.light_block_array[i]])


############################################################################################################
#
#                                           Internal Functions: People
#
############################################################################################################
    
    def update_people_at_station(self):
        self.ui_people_at_station.clear()
        for i in range(len(self.station_list)):
            self.ui_people_at_station.append([self.num_passengers_at_station[i], self.station_list[i]])


############################################################################################################
#
#                                           Internal Functions: Update Cmd Speeds
#
############################################################################################################

    def update_train_cmd_speeds(self):
        
        # Check if current block array is empty
        if len(self.current_block):
            
            # Iterate through all the current block array
            for i in range(len(self.current_block)):

                # Check if current cmd speed is NONE
                if self.cmd_speeds_wayside[self.current_block[i]] != None:
                    # print(f"index i: {i}")
                    # print(f"Current Block: {self.current_block[i]}")
                    
                    # Set train commanded speeds to the wayside commanded speeds
                    self.cmd_speeds_train.append(self.cmd_speeds_wayside[self.current_block[i]])

                    # print(f"Train Cmd Speed: {self.cmd_speeds_train[i]}")

############################################################################################################
#
#                                           Internal Functions: Update Cmd Authorites
#
############################################################################################################

    def update_train_cmd_authorities(self):
        
        # Check if current block array is empty
        if len(self.current_block):

            # Iterate through current_block array
            for i in range(len(self.current_block)):

                # print(f"index i: {i}")
                # print(f"Current Block: {self.current_block[i]}")

                if len(self.cmd_authorities_train) != len(self.current_block):

                    # print(f"len cmd_auth_train: {len(self.cmd_authorities_train)}")
                    # print(f"len current_block: {len(self.current_block)}")
                    # print(f"len cmd_auth_wayside: {len(self.cmd_authorities_wayside)}")
                    # print(f"cmd_auth_wayside: {self.cmd_authorities_wayside[self.current_block[len(self.cmd_authorities_train)]]}")
                    

                    self.cmd_authorities_train.append(self.cmd_authorities_wayside[self.current_block[len(self.cmd_authorities_train)]])
                    self.past_cmd_authorities_wayside.append(self.cmd_authorities_wayside[self.current_block[len(self.cmd_authorities_train)-1]])
                
                    # print(f"Train Cmd Authority: {self.cmd_authorities_train[-1]}")

                else:
                    # Check if current cmd authority is not equal to the past cmd authority
                    #if self.cmd_authorities_train[i] != self.past_cmd_authorities_wayside[self.current_block[i]]:

                    # Check if cmd authority is NONE
                    if self.cmd_authorities_wayside[self.current_block[i]] != None:

                        # Set train commanded authority to new wayside commanded authority
                        self.cmd_authorities_train[i] = self.cmd_authorities_wayside[self.current_block[i]]
                        # print(f"Train Cmd Authority: {self.cmd_authorities_train[i]}")
                            
            #self.train_communicator.commanded_authority_signal.emit(self.cmd_authorities_train)

############################################################################################################
#
#                                           Murphy Functions
#
############################################################################################################
    functional_blocks = []

    def initialize_functional(self):
        self.functional_blocks.clear()
        for block in self.all_blocks:
            self.functional_blocks.append(1)
    
    def handle_circuit_failure_num_step(self, block_num: int):
        if self.ui.toggle_circuit_failure[block_num]:
            self.ui.breakStatus1.toggled.disconnect(self.handle_circuit_failure_checkbox)
            self.ui.breakStatus1.setChecked(True)
            self.ui.breakStatus1.toggled.connect(self.handle_circuit_failure_checkbox)
        else:
            self.ui.breakStatus1.toggled.disconnect(self.handle_circuit_failure_checkbox)
            self.ui.breakStatus1.setChecked(False)
            self.ui.breakStatus1.toggled.connect(self.handle_circuit_failure_checkbox)

    def handle_power_failure_num_step(self, block_num: int):
        if self.ui.toggle_power_failure[block_num]:
            self.ui.breakStatus2.toggled.disconnect(self.handle_power_failure_checkbox)
            self.ui.breakStatus2.setChecked(True)
            self.ui.breakStatus2.toggled.connect(self.handle_power_failure_checkbox)
        else:
            self.ui.breakStatus2.toggled.disconnect(self.handle_power_failure_checkbox)
            self.ui.breakStatus2.setChecked(False)
            self.ui.breakStatus2.toggled.connect(self.handle_power_failure_checkbox)

    def handle_rail_failure_num_step(self, block_num: int):
        if self.ui.toggle_rail_failure[block_num]:
            self.ui.breakStatus3.toggled.disconnect(self.handle_rail_failure_checkbox)
            self.ui.breakStatus3.setChecked(True)
            self.ui.breakStatus3.toggled.connect(self.handle_rail_failure_checkbox)
        else:
            self.ui.breakStatus3.toggled.disconnect(self.handle_rail_failure_checkbox)
            self.ui.breakStatus3.setChecked(False)
            self.ui.breakStatus3.toggled.connect(self.handle_rail_failure_checkbox)

    def handle_circuit_failure_checkbox(self, block_num: int):
        if self.ui.toggle_circuit_failure[block_num]:
            self.ui.toggle_circuit_failure[block_num] = False
        else:
            self.ui.toggle_circuit_failure[block_num] = True

    def handle_power_failure_checkbox(self, block_num: int):
        if self.ui.toggle_power_failure[block_num]:
            self.ui.toggle_power_failure[block_num] = False
        else:
            self.ui.toggle_power_failure[block_num] = True

    def handle_rail_failure_checkbox(self, block_num: int):
        if self.ui.toggle_rail_failure[block_num]:
            self.ui.toggle_rail_failure[block_num] = False
        else:
            self.ui.toggle_rail_failure[block_num] = True

############################################################################################################
#
#                                           UI Signals
#
############################################################################################################
    def update_ui_list(self):
        self.ui.functional_list = self.functional_blocks
        self.ui.occupancy_list = self.occupancies
        self.ui.switch_list = self.ui_switch_array
        self.ui.lights_list = self.ui_light_array
        self.ui.crossing_list = self.ui_crossing_array
        self.ui.num_people_at_station_list = self.ui_people_at_station
        self.ui.update_block_table()

    def update_functional(self):
        for i in range(len(self.all_blocks)):
            if self.ui.toggle_circuit_failure[i]:
                self.functional_blocks[i] = 2
            elif self.ui.toggle_power_failure[i]:
                self.functional_blocks[i] = 3
            elif self.ui.toggle_rail_failure[i]:
                self.functional_blocks[i] = 4
            else:
                self.functional_blocks[i] = 1

    def update_occupancies(self):
        self.set_train_occupancies()
        self.set_failure_occupancies()

    def update_switches(self):
        self.update_switch_states()
        self.update_switch_status()
            
    def update_lights(self):
        self.update_light_states()
        self.update_light_status()

    def update_crossings(self):
        self.update_crossing_states()
        self.update_crossing_status()

    def update_people(self):
        self.update_people_at_station()

    def initialize_occupancy(self):
        for block in self.all_blocks:
            self.occupancies.append(False)

    def initialize_switches(self):
        self.switch_cmds = [1, 1, 0, 0, 0, 0]
        self.update_switch_states()
        self.update_switch_status()

    def initialize_lights(self):
        self.light_cmds = [0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0]
        self.update_light_states()
        self.update_light_status()

    def initialize_crossings(self):
        self.crossing_cmds = [0, 0]
        self.update_crossing_states()
        self.update_crossing_status()

    def initialize_people(self):
        self.update_station_list()
        self.gen_num_passengers_at_station()
        self.update_people_at_station()

    def initialize_failures(self):
        temp_failures = []
        for block in self.all_blocks:
            temp_failures.append(False)
        self.ui.toggle_circuit_failure = temp_failures
        self.ui.toggle_power_failure = temp_failures
        self.ui.toggle_rail_failure = temp_failures
        
    def initialize_arrays(self):
        self.initialize_functional()
        self.initialize_occupancy()
        self.initialize_switches()
        self.initialize_lights()
        self.initialize_crossings()
        self.initialize_people()
        self.initialize_failures()
        self.create_length_array()
        self.ui.initialize_block_table(len(self.all_blocks))
        
    # def updateBlockTable(self) -> None:
    #     blocks = self.all_blocks
    #     self.ui.blockTable.setRowCount(len(blocks))

    #     # glorious king zach changing the headers of the rows
    #     labels = []
    #     for i in range(len(blocks)):
    #         if i == 0:
    #             labels.append("Yard")

    #         else:
    #             labels.append(f"{i}")

    #     self.ui.blockTable.setVerticalHeaderLabels(labels)
    #     #

    #     headers = ["Functional", "Occupied", "Switch State"]
    #     self.ui.blockTable.setColumnCount(len(headers))
    #     self.ui.blockTable.setHorizontalHeaderLabels(headers)

    #     for row, block in enumerate(blocks):
    #         functional_item = QtWidgets.QTableWidgetItem(str(block.functional))
    #         occupancy_item = QtWidgets.QTableWidgetItem(str(block.occupied))
    #         switch_item = QtWidgets.QTableWidgetItem("")
    #         passeneger_item = QtWidgets.QTableWidgetItem("")

    #         for switch in self.ui_switch_array:
    #             if block.number == switch['joint']:
    #                 switch_item.setText(self.checkSwitch())


    #         self.ui.blockTable.setItem(row, 0, functional_item)
    #         self.ui.blockTable.setItem(row, 1, occupancy_item)
    #         self.ui.blockTable.setItem(row, 2, switch_item)

    #         if block.occupied:
    #             for col in range(len(headers)-1):
    #                 self.ui.blockTable.item(row, col).setBackground(QtGui.QColor('lightblue'))
    #         if not block.functional:
    #             for col in range(len(headers)-1):
    #                 self.ui.blockTable.item(row, col).setBackground(QtGui.QColor('lightcoral'))

    #     self.ui.blockTable.cellClicked.connect(self.handleCellClick)

    # def handleCellClick(self, row: int, column: int) -> None:
    #     if column == 2: 
    #         selectedBlock = self.all_blocks[row]
    #         for switch in self.ui_switch_array:
    #             if selectedBlock.number == switch['joint']:
    #                 self.ui.switches.setCurrentText(f"Switch at Block {switch['joint']}")
    #                 self.ui.switchToggle.setChecked(not self.ui.switchToggle.isChecked())
    #                 switch_state = self.checkSwitch()
    #                 self.ui.blockTable.item(row, column).setText(switch_state)
    #                 break

    # def # printBlockInfo(self) -> None:
    #     selectedItems = self.ui.blockTable.selectedItems()
    #     if not selectedItems:
    #         return
    #     selectedRow = selectedItems[0].row()
    #     allBlocks = [block for blocks in self.blocks.values() for block in blocks]
    #     selectedBlock = allBlocks[selectedRow]

    #     self.ui.blockInfo.setRowCount(11)
    #     self.ui.blockInfo.setColumnCount(1)
    #     self.ui.blockInfo.setVerticalHeaderLabels([
    #         "Line", "Section", "Number", "Length", "Grade", "Speed Limit", 
    #         "Infrastructure", "Elevation", "Cumulative Elevation", "Side", "Polarity"
    #     ])
    #     self.ui.blockInfo.setItem(0, 0, QtWidgets.QTableWidgetItem(selectedBlock.line))
    #     self.ui.blockInfo.setItem(1, 0, QtWidgets.QTableWidgetItem(selectedBlock.section))
    #     self.ui.blockInfo.setItem(2, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.number)))
    #     self.ui.blockInfo.setItem(3, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.length)))
    #     self.ui.blockInfo.setItem(4, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.grade)))
    #     self.ui.blockInfo.setItem(5, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.speedLimit)))
    #     self.ui.blockInfo.setItem(6, 0, QtWidgets.QTableWidgetItem(selectedBlock.infrastructure))
    #     self.ui.blockInfo.setItem(7, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.elevation)))
    #     self.ui.blockInfo.setItem(8, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.cumulativeElevation)))
    #     self.ui.blockInfo.setItem(9, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.side)))
    #     self.ui.blockInfo.setItem(10, 0, QtWidgets.QTableWidgetItem(str(selectedBlock.polarity)))

    # def updateOccupancy(self) -> None:
    #     position = self.ui.positionValue.value()
    #     self.occupancies = TrackModel.set_train_occupancies(self)
    #     self.updateBlockTable()

    # def recurring(self) -> None:
    #     self.updateOccupancy()
    #     self.checkSwitch()
    #     self.checkCrossing()
    #     self.checkTemp()        


class track_ui(QtWidgets.QMainWindow, Ui_TrackModel):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


#comment out for testing
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    object = track_model(TrainComms, WaysideComms)
    sys.exit(app.exec())