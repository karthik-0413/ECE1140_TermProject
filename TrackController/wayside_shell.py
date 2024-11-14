# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module:           Wayside Controller (Software)
# PLC Program:      Wayside Shell
#
# Created:          11/05/2024
# Created by:       Zachary McPherson
#
# Last Update:      11/13/2024
# Last Updated by:  Zachary McPherson
#
# Python Version:   3.12.6
# PyQt Version:     6.7.1
#
# Notes: This is the Wayside Shell Program for the Train Control System.
#        This program holds the UI interface for the Wayside Controller
#        This program executes PLC programs uploaded through the UI
#        This program communicates with the CTC Office and Track Model Modules


####################################################################################################
#
#                                               Imports
#
####################################################################################################

# System library
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# PyQt6 libraries
from PyQt6.QtWidgets import QApplication

# Wayside UI Interface
from TrackController import wayside_ui

# CTC Office Communication Files
from Resources import CTCWaysideComm

# Track Model Communication Files
from Resources import WaysideTrackComm

# PLC Communication Files
from TrackController import green_line_plc_1_shell_communicate
from TrackController import green_line_plc_2_shell_communicate
from TrackController import green_line_plc_3_shell_communicate


####################################################################################################
#
#                                               Main Class
#
####################################################################################################

class wayside_shell_class:
      
    ####################################################################################################
    #
    #                                               Variables
    #
    ####################################################################################################

    # Input from CTC Office
    read_sugg_speed = [2] * 152

    read_sugg_authority = [2] * 152

#    read_maintenance_blocks = [0] * 151
#    read_maintenance_switch_cmd = [None] * 6

    # Input from Track Model
    read_block_occupancy = [0] * 152

    # Output to CTC Office
    write_block_occupancy = [0] * 152

    # Output to Track Model
    write_cmd_speed = [1] * 152
    write_cmd_authority = [1] * 152

    #                    D   F   I   K  N1  N2   
    #write_switch_cmd = [ 1,  1,  0,  0,  0,  0]

    #                    C   D   F   G   J   K  N1  N2   O   R  Yard 
    #write_signal_cmd = [ 0,  1,  0,  1,  1,  0,  0,  1,  0,  1,  0 ]

    #                     E  T
    #write_crossing_cmd = [0, 0]

    # Test Values
    read_sugg_speed = [1] * 152

    write_switch_cmd = [ 1,  1,  0,  0,  0,  0]

    #                    C   D   F   G   J   K  N1  N2   O   R  Yard 
    write_signal_cmd = [ 0,  1,  0,  1,  1,  0,  0,  1,  0,  1,  0 ]

    #                     E  T
    write_crossing_cmd = [0, 0]

    ####################################################################################################
    #
    #                                         Module Handler Functions
    #
    ####################################################################################################

    # Inputs from CTC Office
    def read_sugg_speed_handler(self, sugg_speed_array):
        print('read_sugg_speed_handler')

        self.read_sugg_speed = sugg_speed_array

        # Update Wayside user interface table
        self.ui.past_sugg_speed = self.ui.green_line_sugg_speed
        self.ui.green_line_sugg_speed = sugg_speed_array
        self.sugg_speed_check = 1

        if self.sugg_speed_check == 1 and self.sugg_authority_check == 1 and self.block_occupancy_check == 1:

            self.ui.update_table()

            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0

        # Call PLC Program handler functions
        self.green_line_plc_1_sugg_speed_handler()
        self.green_line_plc_2_sugg_speed_handler()
        self.green_line_plc_3_sugg_speed_handler()

    def read_sugg_authority_handler(self, sugg_authority_array):
        print('read_sugg_authority_handler')

        self.read_sugg_authority = sugg_authority_array

        # Update Wayside user interface table
        self.ui.past_sugg_authority = self.ui.green_line_sugg_auth
        self.ui.green_line_sugg_auth = sugg_authority_array
        self.sugg_authority_check = 1
        
        if self.sugg_speed_check == 1 and self.sugg_authority_check == 1 and self.block_occupancy_check == 1:

            self.ui.update_table()

            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0

        # Call PLC Program handler functions
        self.green_line_plc_1_sugg_authority_handler()
        self.green_line_plc_2_sugg_authority_handler()
        self.green_line_plc_3_sugg_authority_handler()

        # Update Wayside user interface table
        self.ui.update_table()

#    def read_maintenance_blocks_handler(self, maintenance_blocks_array):
#        self.read_maintenance_blocks = maintenance_blocks_array

#    def read_maintenance_switch_cmd_handler(self, maintenance_switch_cmd_array):
#        self.read_maintenance_switch_cmd = maintenance_switch_cmd_array

    # Inputs from Track Model
    def read_block_occupancy_handler(self, block_occupancy_array):
        self.read_block_occupancy = block_occupancy_array

        # Update Wayside user interface table
        self.ui.green_line_block_occupancy = block_occupancy_array
        self.block_occupancy_check = 1
        
        if self.sugg_speed_check == 1 and self.sugg_authority_check == 1 and self.block_occupancy_check == 1:

            self.ui.update_table()

            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0

        # Call PLC Program handler functions
        self.green_line_plc_1_block_occupancy_handler()
        self.green_line_plc_2_block_occupancy_handler()
        self.green_line_plc_3_block_occupancy_handler()

    ####################################################################################################
    #
    #                                         PLC Handler Functions
    #
    ####################################################################################################

    ####################################
    #     Green Line PLC Program 1
    ####################################

    # Inputs from CTC Office
    def green_line_plc_1_sugg_speed_handler(self):
        plc_1_sugg_speed = []

        for i in range(1, 33):
            plc_1_sugg_speed.append(self.read_sugg_speed[i])
        plc_1_sugg_speed.append(self.read_sugg_speed[150])
        plc_1_sugg_speed.append(self.read_sugg_speed[151])


        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_sugg_speed.emit(plc_1_sugg_speed)

    def green_line_plc_1_sugg_authority_handler(self):
        plc_1_sugg_authority = []

        for i in range(1, 33):
            plc_1_sugg_authority.append(self.read_sugg_speed[i])
        plc_1_sugg_authority.append(self.read_sugg_speed[150])
        plc_1_sugg_authority.append(self.read_sugg_speed[151])

        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_sugg_authority.emit(plc_1_sugg_authority)

    # Inputs from Track Model
    def green_line_plc_1_block_occupancy_handler(self):
        plc_1_block_occupancy = []

        for i in range(1, 36):
            plc_1_block_occupancy.append(self.read_block_occupancy[i])
        plc_1_block_occupancy.append(self.read_block_occupancy[150])
        plc_1_block_occupancy.append(self.read_block_occupancy[151])

        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_block_occupancy.emit(plc_1_block_occupancy)

    # Outputs to Track Model
    def green_line_plc_1_cmd_speed_handler(self, cmd_speed_array):
        for i in range(1, 33):
            self.write_cmd_speed[i] = cmd_speed_array[i-1]
        self.write_cmd_speed[150] = cmd_speed_array[32]
        self.write_cmd_speed[151] = cmd_speed_array[33]

    def green_line_plc_1_cmd_authority_handler(self, cmd_authority_array):
        for i in range(1, 33):
            self.write_cmd_authority[i] = cmd_authority_array[i-1]
        self.write_cmd_authority[150] = cmd_authority_array[32]
        self.write_cmd_authority[151] = cmd_authority_array[33]

    def green_line_plc_1_switch_cmd_handler(self, switch_cmd_array):
        self.write_switch_cmd[0] = not switch_cmd_array[0] # D
        self.write_switch_cmd[1] = switch_cmd_array[1] # F

    def green_line_plc_1_signal_cmd_handler(self, signal_cmd_array):
        signal_cmd_array[0] = signal_cmd_array[0]
        signal_cmd_array[1] = signal_cmd_array[1]
        signal_cmd_array[2] = signal_cmd_array[2]
        signal_cmd_array[3] = signal_cmd_array[3]

    def green_line_plc_1_crossing_cmd_handler(self, crossing_cmd_bool):
        self.write_crossing_cmd[0] = crossing_cmd_bool

    # Connect to PLC 1 communication signals
    def connect_green_line_plc_1_signals(self):
        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_cmd_speed.connect(self.green_line_plc_1_cmd_speed_handler)
        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_cmd_authority.connect(self.green_line_plc_1_cmd_authority_handler)
        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_switch_cmd.connect(self.green_line_plc_1_switch_cmd_handler)
        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_signal_cmd.connect(self.green_line_plc_1_signal_cmd_handler)
        green_line_plc_1_shell_communicate.green_plc_1.green_line_plc_1_crossing_cmd.connect(self.green_line_plc_1_crossing_cmd_handler)

    ####################################
    #     Green Line PLC Program 2
    ####################################

    # Inputs from Track Model
    def green_line_plc_2_sugg_speed_handler(self):
        plc_2_sugg_apeed = []

        plc_2_sugg_apeed.append(self.read_sugg_speed[0])

        for i in range(33, 74):
            plc_2_sugg_apeed.append(self.read_sugg_speed[i])

        for i in range(105, 150):
            plc_2_sugg_apeed.append(self.read_sugg_speed[i])

        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_sugg_speed.emit(plc_2_sugg_apeed)

    def green_line_plc_2_sugg_authority_handler(self):
        plc_2_sugg_authority = []

        plc_2_sugg_authority.append(self.read_sugg_authority[0])

        for i in range(33, 74):
            plc_2_sugg_authority.append(self.read_sugg_authority[i])

        for i in range(105, 150):
            plc_2_sugg_authority.append(self.read_sugg_authority[i])

        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_sugg_authority.emit(plc_2_sugg_authority)

    # Inputs from Track Model
    def green_line_plc_2_block_occupancy_handler(self):
        plc_2_block_occupancy = []

        plc_2_block_occupancy.append(self.read_block_occupancy[0])

        for i in range(33, 77):
            plc_2_block_occupancy.append(self.read_block_occupancy[i])

        for i in range(105, 151):
            plc_2_block_occupancy.append(self.read_block_occupancy[i])

        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_block_occupancy.emit(plc_2_block_occupancy)

    # Outputs to Track Model
    def green_line_plc_2_cmd_speed_handler(self, cmd_speed_array):
        self.write_cmd_speed[0] = cmd_speed_array[0]

        for i in range(33, 74):
            self.write_cmd_speed[i] = cmd_speed_array[i-32]
        
        for i in range(105, 150):
            self.write_cmd_speed[i] = cmd_speed_array[i-60]

    def green_line_plc_2_cmd_authority_handler(self, cmd_authority_array):
        self.write_cmd_authority[0] = cmd_authority_array[0]

        for i in range(33, 74):
            self.write_cmd_authority[i] = cmd_authority_array[i-32]
        
        for i in range(105, 150):
            self.write_cmd_authority[i] = cmd_authority_array[i-60]

    def green_line_plc_2_switch_cmd_handler(self, switch_cmd_array):
        self.write_switch_cmd[2] = switch_cmd_array[0] # I
        self.write_switch_cmd[3] = not switch_cmd_array[1] # K

    def green_line_plc_2_signal_cmd_handler(self, signal_cmd_array):
        signal_cmd_array[10] = signal_cmd_array[0] # Yard
        signal_cmd_array[4] = signal_cmd_array[1]  # J
        signal_cmd_array[5] = signal_cmd_array[2]  # K

    def green_line_plc_2_crossing_cmd_handler(self, crossing_cmd_bool):
        self.write_crossing_cmd[0] = crossing_cmd_bool

    # Connect to PLC 2 communication signals
    def connect_green_line_plc_2_signals(self):
        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_cmd_speed.connect(self.green_line_plc_2_cmd_speed_handler)
        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_cmd_authority.connect(self.green_line_plc_2_cmd_authority_handler)
        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_switch_cmd.connect(self.green_line_plc_2_switch_cmd_handler)
        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_signal_cmd.connect(self.green_line_plc_2_signal_cmd_handler)
        green_line_plc_2_shell_communicate.green_plc_2.green_line_plc_2_crossing_cmd.connect(self.green_line_plc_2_crossing_cmd_handler)

    ####################################
    #     Green Line PLC Program 3
    ####################################

    # Inputs from Track Model
    def green_line_plc_3_sugg_speed_handler(self):
        plc_3_sugg_speed = []

        for i in range(74, 105):
            plc_3_sugg_speed.append(self.read_sugg_speed[i])

        green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_sugg_speed.emit(plc_3_sugg_speed)
    
    def green_line_plc_3_sugg_authority_handler(self):
        plc_3_sugg_authority = []

        for i in range(74, 105):
            plc_3_sugg_authority.append(self.read_block_occupancy[i])

        green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_sugg_authority.emit(plc_3_sugg_authority)

    # Inputs from Track Model
    def green_line_plc_3_block_occupancy_handler(self):
        plc_3_block_occupancy = []

        for i in range(74, 110):
            plc_3_block_occupancy.append(self.read_block_occupancy[i])

        green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_block_occupancy.emit(plc_3_block_occupancy)

    # Outputs to Track Model
    def green_line_plc_3_cmd_speed_handler(self, cmd_speed_array):
        for i in range(74, 105):
            self.write_cmd_speed[i] = cmd_speed_array[i-74]

    def green_line_plc_3_cmd_authority_handler(self, cmd_authority_array):
        for i in range(74, 105):
            self.write_cmd_authority[i] = cmd_authority_array[i-74]

    def green_line_plc_3_switch_cmd_handler(self, switch_cmd_array):
        self.write_switch_cmd[4] = not switch_cmd_array[0] # N1
        self.write_switch_cmd[5] = switch_cmd_array[1] # N2

    def green_line_plc_3_signal_cmd_handler(self, signal_cmd_array):
        signal_cmd_array[6] = signal_cmd_array[0] # N1
        signal_cmd_array[9] = signal_cmd_array[1] # R
        signal_cmd_array[7] = signal_cmd_array[2] # N2
        signal_cmd_array[8] = signal_cmd_array[3] # O

    # No crossing commands for PLC Program 3

    # Connect to PLC 3 communication signals
    def connect_green_line_plc_3_signals(self):
        green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_cmd_speed.connect(self.green_line_plc_3_cmd_speed_handler)
        green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_cmd_authority.connect(self.green_line_plc_3_cmd_authority_handler)
        green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_switch_cmd.connect(self.green_line_plc_3_switch_cmd_handler)
        green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_signal_cmd.connect(self.green_line_plc_3_signal_cmd_handler)

    ####################################################################################################
    #
    #                                             Read Function
    #
    ####################################################################################################

    def connect_ctc_signals(self):
        self.ctc_wayside_comm_object.suggested_speed_signal.connect(self.read_sugg_speed_handler)
        self.ctc_wayside_comm_object.suggested_authority_signal.connect(self.read_sugg_authority_handler)

    def connect_track_model_signals(self):
        self.wayside_track_comm_object.block_occupancy_signal.connect(self.read_block_occupancy_handler)

    ####################################################################################################
    #
    #                                             Write Function
    #
    ####################################################################################################

    def write(self):

        ####################################
        #     Green Line Emit Signals
        ####################################

        # CTC Office
        self.ctc_wayside_comm_object.block_occupancy_signal.emit(self.write_block_occupancy)

        # Track Model
        self.wayside_track_comm_object.commanded_speed_signal.emit(self.write_cmd_speed)
        self.wayside_track_comm_object.commanded_authority_signal.emit(self.write_cmd_authority)
        self.wayside_track_comm_object.switch_cmd_signal.emit(self.write_switch_cmd)
        self.wayside_track_comm_object.signal_cmd_signal.emit(self.write_signal_cmd)
        self.wayside_track_comm_object.crossing_cmd_signal.emit(self.write_crossing_cmd)

        ####################################
        #    Green Line Update UI
        ####################################

        # Commanded Speed
        self.ui.green_line_cmd_speed = self.write_cmd_speed

        # Commanded Authority
        self.ui.green_line_cmd_auth = self.write_cmd_authority

        # Switch Command
        self.ui.past_sw_cmd = self.ui.green_line_sw_cmd
        self.ui.green_line_sw_cmd = self.write_switch_cmd

        # Signal Command
        self.ui.past_sig_cmd = self.ui.green_line_sig_cmd
        self.ui.green_line_sig_cmd = self.write_signal_cmd

        # Crossing Command
        self.ui.green_line_cross_cmd = self.write_crossing_cmd

        # Update Wayside user interface data table
        self.ui.update_table()

        # Update Wayside user interface update log
        self.ui.update_log()

    ####################################################################################################
    #
    #                                               UI Interface
    #
    ####################################################################################################

    # Initialize the Wayside UI Interface
    def __init__(self, ctc_wayside, wayside_track):

        # Initialize update UI checks
        self.block_occupancy_check = 0
        self.sugg_speed_check = 0
        self.sugg_authority_check = 0

        # Initialize CTC Office and Wayside communication object
        self.ctc_wayside_comm_object = ctc_wayside
        
        # Initialize Wayside and Track Model communication object
        self.wayside_track_comm_object = wayside_track

        # Connect to CTC Office signals
        self.connect_ctc_signals()

        # Connect to PLC program signals
        self.connect_green_line_plc_1_signals()
        self.connect_green_line_plc_2_signals()
        self.connect_green_line_plc_3_signals()

        # Initialize and show the Wayside user interface
        self.ui = wayside_shell_ui()
        self.ui.show()

class wayside_shell_ui(wayside_ui.QtWidgets.QMainWindow, wayside_ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

    # Close the window and terminate all running processes
    def closeEvent(self, event):

            # Terminate all running processes
            for process in self.processes:
                    
                    process.terminate()

                    print('Terminated process')

            # Close the window
            event.accept()

####################################################################################################
#
#                                               Main Execution
#
####################################################################################################