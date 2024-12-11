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
# Last Update:      12/07/2024
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
import importlib.util

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# PyQt6 libraries
from PyQt6.QtWidgets import QApplication, QFileDialog, QMainWindow

# Wayside UI Interface
from TrackController import wayside_ui_it_4_green_line
from TrackController import wayside_ui_it_4_red_line

# CTC Office Communication Files
from Resources import CTCWaysideComm

# Track Model Communication Files
from Resources import WaysideTrackComm

# PLC Communication Files
# from TrackController import green_line_plc_1_shell_communicate
# from TrackController import green_line_plc_2_shell_communicate
# from TrackController import green_line_plc_3_shell_communicate


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
    read_sugg_speed = [None] * 152

    read_sugg_authority = [None] * 152

    read_maintenance_blocks = [0] * 152
    read_maintenance_switch_cmd = [0] * 6

    # Input from Track Model
    read_block_occupancy = [0] * 152

    # Output to CTC Office
    write_block_occupancy = [0] * 152

    # Output to Track Model
    write_cmd_speed = [None] * 152
    write_cmd_authority = [None] * 152

    #                    D  F   I   K  N1  N2   
    write_switch_cmd = [ 1, 1,  0,  0,  0,  0]

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
    def read_sugg_speed_handler(self, sugg_speed_array: list):
        
        self.read_sugg_speed = sugg_speed_array.copy()

        # Update Wayside user interface table
        if self.read_sugg_speed:
            
            self.sugg_speed_check = 1

            if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check: #and self.maintenance_block_check and self.maintenance_switch_check:

                # Update UI suggested speed and authority table
                self.ui.shell_sugg_speed_auth_handler(self.read_sugg_speed, self.read_sugg_authority)
                self.ui.shell_occupancy_handler(self.read_block_occupancy, self.read_maintenance_blocks)

                self.maintenance_block_check = 0
                self.maintenance_switch_check = 0
                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    # Process incoming data
                    self.call_green_line_plc_1_operation_handlers()
                    self.call_green_line_plc_2_operation_handlers()
                    self.call_green_line_plc_3_operation_handlers()

    def read_sugg_authority_handler(self, sugg_authority_array: list):

        self.read_sugg_authority = sugg_authority_array.copy()

        # Update Wayside user interface table
        if self.read_sugg_authority:
            
            self.sugg_authority_check = 1
            
            if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check: #and self.maintenance_block_check and self.maintenance_switch_check:

                # Update UI suggested speed and authority table
                self.ui.shell_sugg_speed_auth_handler(self.read_sugg_speed, self.read_sugg_authority)
                self.ui.shell_occupancy_handler(self.read_block_occupancy, self.read_maintenance_blocks)

                self.maintenance_block_check = 0
                self.maintenance_switch_check = 0
                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    # Process incoming data
                    self.call_green_line_plc_1_operation_handlers()
                    self.call_green_line_plc_2_operation_handlers()
                    self.call_green_line_plc_3_operation_handlers()

    def read_maintenance_blocks_handler(self, maintenance_blocks_array: list):

        self.read_maintenance_blocks = maintenance_blocks_array.copy()

        # Update Wayside user interface table
        if self.read_maintenance_blocks:
            
            self.maintenance_block_check = 1
            
            if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_block_check and self.maintenance_switch_check:

                # Update UI suggested speed and authority table
                self.ui.shell_sugg_speed_auth_handler(self.read_sugg_speed, self.read_sugg_authority)
                self.ui.shell_occupancy_handler(self.read_block_occupancy, self.read_maintenance_blocks)

                self.maintenance_block_check = 0
                self.maintenance_switch_check = 0
                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    # Process incoming data
                    self.call_green_line_plc_1_operation_handlers()
                    self.call_green_line_plc_2_operation_handlers()
                    self.call_green_line_plc_3_operation_handlers()

    def read_maintenance_switch_cmd_handler(self, maintenance_switch_cmd_array: list):

        self.read_maintenance_switch_cmd = maintenance_switch_cmd_array.copy()

        # Update Wayside user interface table
        if self.read_maintenance_switch_cmd:
            
            self.maintenance_block_check = 1
            
            if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_block_check and self.maintenance_switch_check:

                # Update UI suggested speed and authority table
                self.ui.shell_sugg_speed_auth_handler(self.read_sugg_speed, self.read_sugg_authority)
                self.ui.shell_occupancy_handler(self.read_block_occupancy, self.read_maintenance_blocks)

                self.maintenance_block_check = 0
                self.maintenance_switch_check = 0
                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    # Process incoming data
                    self.call_green_line_plc_1_operation_handlers()
                    self.call_green_line_plc_2_operation_handlers()
                    self.call_green_line_plc_3_operation_handlers()

    # Inputs from Track Model
    def read_block_occupancy_handler(self, block_occupancy_array: list):

        self.read_block_occupancy = block_occupancy_array.copy()
        self.write_block_occupancy = block_occupancy_array.copy()

        # Update Wayside user interface table
        if self.read_block_occupancy:
            
            self.block_occupancy_check = 1
            
            if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check: #and self.maintenance_block_check and self.maintenance_switch_check:

                # Update UI suggested speed and authority table
                self.ui.shell_sugg_speed_auth_handler(self.read_sugg_speed, self.read_sugg_authority)
                self.ui.shell_occupancy_handler(self.read_block_occupancy, self.read_maintenance_blocks)

                self.maintenance_block_check = 0
                self.maintenance_switch_check = 0
                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    # print('Calling PLC Program read functions')
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    # print("Calling PLC Program operation functions")
                    # Process incoming data
                    self.call_green_line_plc_1_operation_handlers()
                    self.call_green_line_plc_2_operation_handlers()
                    self.call_green_line_plc_3_operation_handlers()

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

        # Check if the sugg_speed_array is empty
        if len(self.read_sugg_speed):

            for i in range(1, 33):
                plc_1_sugg_speed.append(self.read_sugg_speed[i])
            plc_1_sugg_speed.append(self.read_sugg_speed[150])
            plc_1_sugg_speed.append(self.read_sugg_speed[151])

            # Pass suggested speeds to PLC Program 1
            if self.plc_program_1 != None:
                self.plc_program_1.read_sugg_speed_handler(plc_1_sugg_speed)

    def green_line_plc_1_sugg_authority_handler(self):
        plc_1_sugg_authority = []

        # Check if the sugg_authority_array is empty
        if len(self.read_sugg_authority):
            for i in range(1, 33):
                plc_1_sugg_authority.append(self.read_sugg_speed[i])
            plc_1_sugg_authority.append(self.read_sugg_speed[150])
            plc_1_sugg_authority.append(self.read_sugg_speed[151])

            # Pass suggested authorities to PLC Program 1
            if self.plc_program_1 != None:
                self.plc_program_1.read_sugg_authority_handler(plc_1_sugg_authority)

    def green_line_plc_1_maintenance_block_handler(self):
        plc_1_maintenance_blocks = []

        # Check if the maintenance_block array is empty
        if self.read_maintenance_blocks:
            for i in range(1, 36):
                plc_1_maintenance_blocks.append(self.read_maintenance_blocks[i])
            plc_1_maintenance_blocks.append(self.read_maintenance_blocks[150])
            plc_1_maintenance_blocks.append(self.read_maintenance_blocks[151])

            # Pass maintenance blocks to PLC Program 1
            if self.plc_program_1 != None:
                self.plc_program_1.read_maintenance_block_handler(plc_1_maintenance_blocks)

    def green_line_plc_1_maintenance_switch_handler(self):
        plc_1_maintenance_switch_cmd = []

        # Check if the maintenance_switch array is empty
        if self.read_maintenance_switch_cmd:
            plc_1_maintenance_switch_cmd.append(self.read_maintenance_switch_cmd[0])
            plc_1_maintenance_switch_cmd.append(self.read_maintenance_switch_cmd[1])

            # Pass maintenance switch commands to PLC Program 1
            if self.plc_program_1 != None:
                self.plc_program_1.read_maintenance_switches_handler(plc_1_maintenance_switch_cmd)

    # Inputs from Track Model
    def green_line_plc_1_block_occupancy_handler(self):
        plc_1_block_occupancy = []

        # Check if the sugg_speed_array is empty
        if self.read_block_occupancy and self.read_maintenance_blocks:
            for i in range(1, 36):
                plc_1_block_occupancy.append(self.read_block_occupancy[i])
            plc_1_block_occupancy.append(self.read_block_occupancy[150])
            plc_1_block_occupancy.append(self.read_block_occupancy[151])

            # Pass block occupancies to PLC Program 1
            if self.plc_program_1 != None:
                self.plc_program_1.read_block_occupancy_handler(plc_1_block_occupancy)

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
        self.write_signal_cmd[0] = signal_cmd_array[0]
        self.write_signal_cmd[1] = signal_cmd_array[1]
        self.write_signal_cmd[2] = signal_cmd_array[2]
        self.write_signal_cmd[3] = signal_cmd_array[3]

    def green_line_plc_1_crossing_cmd_handler(self, crossing_cmd_bool):
        self.write_crossing_cmd[0] = crossing_cmd_bool

    def call_green_line_plc_1_read_handlers(self):
        self.green_line_plc_1_maintenance_block_handler()
        self.green_line_plc_1_maintenance_switch_handler()
        self.green_line_plc_1_sugg_speed_handler()
        self.green_line_plc_1_sugg_authority_handler()
        self.green_line_plc_1_block_occupancy_handler()

    def call_green_line_plc_1_operation_handlers(self):
        self.green_line_plc_1_cmd_speed_handler(self.plc_program_1.write_cmd_speed_array)
        self.green_line_plc_1_cmd_authority_handler(self.plc_program_1.write_cmd_authority_array)
        self.green_line_plc_1_switch_cmd_handler(self.plc_program_1.write_switch_cmd_array)
        self.green_line_plc_1_signal_cmd_handler(self.plc_program_1.write_signal_cmd_array)
        self.green_line_plc_1_crossing_cmd_handler(self.plc_program_1.write_cross_cmd_array[0])

    ####################################
    #     Green Line PLC Program 2
    ####################################

    # Inputs from CTC Office
    def green_line_plc_2_sugg_speed_handler(self):
        plc_2_sugg_speed = []

        # Check if the sugg_speed_array is empty
        if self.read_sugg_speed:
            plc_2_sugg_speed.append(self.read_sugg_speed[0])

            for i in range(33, 74):
                plc_2_sugg_speed.append(self.read_sugg_speed[i])

            for i in range(105, 150):
                plc_2_sugg_speed.append(self.read_sugg_speed[i])

            # Pass suggested speeds to PLC Program 2
            if self.plc_program_2 != None:
                self.plc_program_2.read_sugg_speed_handler(plc_2_sugg_speed)

    def green_line_plc_2_sugg_authority_handler(self):
        plc_2_sugg_authority = []

        # Check if the sugg_authority_array is empty
        if self.read_sugg_authority:

            plc_2_sugg_authority.append(self.read_sugg_authority[0])

            for i in range(33, 74):
                plc_2_sugg_authority.append(self.read_sugg_authority[i])

            for i in range(105, 150):
                plc_2_sugg_authority.append(self.read_sugg_authority[i])

            # Pass suggested authorities to PLC Program 2
            if self.plc_program_2 != None:
                self.plc_program_2.read_sugg_authority_handler(plc_2_sugg_authority)

    def green_line_plc_2_maintenance_block_handler(self):
        plc_2_maintenance_blocks = []

        # Check if the maintenance_block array is empty
        if len(self.read_block_occupancy):

            plc_2_maintenance_blocks.append(self.read_maintenance_blocks[0])

            for i in range(33, 77):
                plc_2_maintenance_blocks.append(self.read_maintenance_blocks[i])

            for i in range(105, 151):
                plc_2_maintenance_blocks.append(self.read_maintenance_blocks[i])

            # Pass maintenance blocks to PLC Program 2
            if self.plc_program_2 != None:
                self.plc_program_2.read_maintenance_block_handler(plc_2_maintenance_blocks)

    def green_line_plc_2_maintenance_switch_handler(self):
        plc_2_maintenance_switch_cmd = []

        # Check if the maintenance_switch array is empty
        if self.read_maintenance_switch_cmd:
            plc_2_maintenance_switch_cmd.append(self.read_maintenance_switch_cmd[2])
            plc_2_maintenance_switch_cmd.append(self.read_maintenance_switch_cmd[3])

            # Pass maintenance switch commands to PLC Program 2
            if self.plc_program_2 != None:
                self.plc_program_2.read_maintenance_switches_handler(plc_2_maintenance_switch_cmd)

    # Inputs from Track Model
    def green_line_plc_2_block_occupancy_handler(self):
        plc_2_block_occupancy = []

        # Check if the block_occupancy_array is empty
        if len(self.read_block_occupancy):

            plc_2_block_occupancy.append(self.read_block_occupancy[0])

            for i in range(33, 77):
                plc_2_block_occupancy.append(self.read_block_occupancy[i])

            for i in range(105, 151):
                plc_2_block_occupancy.append(self.read_block_occupancy[i])

            # Pass block occupancies to PLC Program 2
            if self.plc_program_2 != None:
                self.plc_program_2.read_block_occupancy_handler(plc_2_block_occupancy)

    # Outputs to Track Model
    def green_line_plc_2_cmd_speed_handler(self, cmd_speed_array):

        self.write_cmd_speed[0] = cmd_speed_array[0]

        for i in range(33, 74):
            self.write_cmd_speed[i] = cmd_speed_array[i-32]
        
        for i in range(105, 150):
            self.write_cmd_speed[i] = cmd_speed_array[i-63]

    def green_line_plc_2_cmd_authority_handler(self, cmd_authority_array):
        self.write_cmd_authority[0] = cmd_authority_array[0]

        for i in range(33, 74):
            self.write_cmd_authority[i] = cmd_authority_array[i-32]
        
        for i in range(105, 150):
            self.write_cmd_authority[i] = cmd_authority_array[i-63]

    def green_line_plc_2_switch_cmd_handler(self, switch_cmd_array):
        self.write_switch_cmd[2] = switch_cmd_array[0] # I
        self.write_switch_cmd[3] = not switch_cmd_array[1] # K

    def green_line_plc_2_signal_cmd_handler(self, signal_cmd_array):
        self.write_signal_cmd[10] = signal_cmd_array[0] # Yard
        self.write_signal_cmd[4] = signal_cmd_array[1]  # J
        self.write_signal_cmd[5] = signal_cmd_array[2]  # K

    def green_line_plc_2_crossing_cmd_handler(self, crossing_cmd_bool):
        self.write_crossing_cmd[0] = crossing_cmd_bool

    def call_green_line_plc_2_read_handlers(self):
        self.green_line_plc_2_maintenance_block_handler()
        self.green_line_plc_2_maintenance_switch_handler()
        self.green_line_plc_2_sugg_speed_handler()
        self.green_line_plc_2_sugg_authority_handler()
        self.green_line_plc_2_block_occupancy_handler()

    def call_green_line_plc_2_operation_handlers(self):
        self.green_line_plc_2_cmd_speed_handler(self.plc_program_2.write_cmd_speed_array)
        self.green_line_plc_2_cmd_authority_handler(self.plc_program_2.write_cmd_authority_array)
        self.green_line_plc_2_switch_cmd_handler(self.plc_program_2.write_switch_cmd_array)
        self.green_line_plc_2_signal_cmd_handler(self.plc_program_2.write_signal_cmd_array)
        self.green_line_plc_2_crossing_cmd_handler(self.plc_program_2.write_crossing_cmd_array[0])

    ####################################
    #     Green Line PLC Program 3
    ####################################

    # Inputs from Track Model
    def green_line_plc_3_sugg_speed_handler(self):
        plc_3_sugg_speed = []

        # Check if the sugg_speed_array is empty
        if len(self.read_sugg_speed):
            for i in range(74, 105):
                plc_3_sugg_speed.append(self.read_sugg_speed[i])

            # Pass suggested speeds to PLC Program 3
            if self.plc_program_3 != None:
                self.plc_program_3.read_sugg_speed_handler(plc_3_sugg_speed)

    def green_line_plc_3_sugg_authority_handler(self):
        plc_3_sugg_authority = []

        # Check if the sugg_authority_array is empty
        if len(self.read_sugg_authority):
            for i in range(74, 105):
                plc_3_sugg_authority.append(self.read_sugg_authority[i])

            # Pass suggested speeds to PLC Program 3
            if self.plc_program_3 != None:
                self.plc_program_3.read_sugg_authority_handler(plc_3_sugg_authority)

    def green_line_plc_3_maintenance_block_handler(self):
        plc_3_maintenance_blocks = []

        # Check if the maintenance_block array is empty
        if self.read_maintenance_blocks:
            for i in range(74, 110):
                plc_3_maintenance_blocks.append(self.read_maintenance_blocks[i])

            # Pass maintenance blocks to PLC Program 3
            if self.plc_program_3 != None:
                self.plc_program_3.read_maintenance_block_handler(plc_3_maintenance_blocks)

    def green_line_plc_3_maintenance_switch_handler(self):
        plc_3_maintenance_switch_cmd = []

        # Check if the maintenance_switch array is empty
        if self.read_maintenance_switch_cmd:
            plc_3_maintenance_switch_cmd.append(self.read_maintenance_switch_cmd[4])
            plc_3_maintenance_switch_cmd.append(self.read_maintenance_switch_cmd[5])

            # Pass maintenance switch commands to PLC Program 3
            if self.plc_program_3 != None:
                self.plc_program_3.read_maintenance_switches_handler(plc_3_maintenance_switch_cmd)


    # Inputs from Track Model
    def green_line_plc_3_block_occupancy_handler(self):
        plc_3_block_occupancy = []

        # Check if the block_occupancy_array is empty
        if len(self.read_block_occupancy):
            for i in range(74, 110):
                plc_3_block_occupancy.append(self.read_block_occupancy[i])

            # Pass suggested speeds to PLC Program 3
            if self.plc_program_3 != None:
                self.plc_program_3.read_block_occupancy_handler(plc_3_block_occupancy)

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
        self.write_signal_cmd[6] = signal_cmd_array[0] # N1
        self.write_signal_cmd[9] = signal_cmd_array[1] # R
        self.write_signal_cmd[7] = signal_cmd_array[2] # N2
        self.write_signal_cmd[8] = signal_cmd_array[3] # O

    # No crossing commands for PLC Program 3

    def call_green_line_plc_3_read_handlers(self):
        self.green_line_plc_3_maintenance_block_handler()
        self.green_line_plc_3_maintenance_switch_handler()
        self.green_line_plc_3_sugg_speed_handler()
        self.green_line_plc_3_sugg_authority_handler()
        self.green_line_plc_3_block_occupancy_handler()

    def call_green_line_plc_3_operation_handlers(self):
        self.green_line_plc_3_cmd_speed_handler(self.plc_program_3.write_cmd_speed_array)
        self.green_line_plc_3_cmd_authority_handler(self.plc_program_3.write_cmd_authority_array)
        self.green_line_plc_3_switch_cmd_handler(self.plc_program_3.write_switch_cmd_array)
        self.green_line_plc_3_signal_cmd_handler(self.plc_program_3.write_signal_cmd_array)

    ####################################################################################################
    #
    #                                             Read Function
    #
    ####################################################################################################

    def connect_ctc_signals(self):
        self.ctc_wayside_comm_object.suggested_speed_signal.connect(self.read_sugg_speed_handler)
        self.ctc_wayside_comm_object.suggested_authority_signal.connect(self.read_sugg_authority_handler)

    def connect_track_model_signals(self):
        self.wayside_track_comm_object.block_occupancies_signal.connect(self.read_block_occupancy_handler)

    ####################################################################################################
    #
    #                                             Write Function
    #
    ####################################################################################################

    def write(self):

        # Wayside 1 manual mode
        if self.ui.wayside_1_operational_mode == 1:
            self.write_switch_cmd[0] = self.ui.ui_switches[0]
            self.write_switch_cmd[1] = self.ui.ui_switches[1]
        
        # Wayside 2 manual mode
        if self.ui.wayside_2_operational_mode == 1:
            self.write_switch_cmd[2] = self.ui.ui_switches[2]
            self.write_switch_cmd[3] = self.ui.ui_switches[3]

        # Wayside 3 manual mode
        if self.ui.wayside_3_operational_mode == 1:
            self.write_switch_cmd[4] = self.ui.ui_switches[4]
            self.write_switch_cmd[5] = self.ui.ui_switches[5]

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
        #           Update UI
        ####################################

        # Commanded speed and authority
        self.ui.shell_cmd_speed_auth_handler(self.write_cmd_speed, self.write_cmd_authority)

        # Switch, Signal, and Crossing Commands
        self.ui.shell_switch_signal_crossing_handler(self.write_switch_cmd, self.write_signal_cmd, self.write_crossing_cmd)
        
        # Update UI data table
        self.ui.update_data_table()

        # Update UI log table
        self.ui.update_log_table()

    ####################################################################################################
    #
    #                                               UI Interface
    #
    ####################################################################################################

    ###################################
    #       Upload PLC Program
    ###################################

    # Open file manager to select PLC programs
    def open_file_dialog(self):

            # Open a file dialog to select Python files
            file_paths, _ = QFileDialog.getOpenFileNames(self.ui, 'Open Python files', '', 'Python Files (*.py)')

            # Check if any files were selected
            if file_paths:

                # Run PLC programs in separate processes
                self.execute_files(file_paths)

    # Execute the selected Python files
    def execute_files(self, file_paths):

            # Start each file in a separate process
                    
            # Import filepath

            # PLC Program 1
            module_name = 'gp1'
            gp1_spec = importlib.util.spec_from_file_location(module_name, file_paths[0])
            self.plc_1 = importlib.util.module_from_spec(gp1_spec)
            gp1_spec.loader.exec_module(self.plc_1)

            # PLC Program 2
            module_name = 'gp2'
            gp2_spec = importlib.util.spec_from_file_location(module_name, file_paths[1])
            self.plc_2 = importlib.util.module_from_spec(gp2_spec)
            gp2_spec.loader.exec_module(self.plc_2)

            # PLC Program 3
            module_name = 'gp3'
            gp3_spec = importlib.util.spec_from_file_location(module_name, file_paths[2])
            self.plc_3 = importlib.util.module_from_spec(gp3_spec)
            gp3_spec.loader.exec_module(self.plc_3)

            # PLC Program 1
            self.plc_program_1 = self.plc_1.green_line_plc_1_class()

            # PLC Program 2
            self.plc_program_2 = self.plc_2.green_line_plc_2_class()

            # PLC Program 3
            self.plc_program_3 = self.plc_3.green_line_plc_3_class()

            # Green Line
            if self.line_color == 'Green':

                # PLC 1
                try:
                    green_1 = self.plc_program_1.green_plc_1_is_created()
                except:
                    green_1 = False

                # PLC 2
                try:
                    green_2 = self.plc_program_2.green_plc_2_is_created()
                except:
                    green_2 = False

                # PLC 3
                try:
                    green_3 = self.plc_program_3.green_plc_3_is_created()
                except:
                    green_3 = False

                # PLC programs are correctly initialized
                if green_1 and green_2 and green_3:

                    # Change Upload PLC button text
                    self.ui.UploadPLCButton.setText('PLCs\nUploaded')

                    # Change Upload PLC button color
                    self.ui.UploadPLCButton.setStyleSheet("border: 2px solid black; border-radius: 5px; background-color: lime;")

                    # Disable Upload PLC button
                    self.ui.UploadPLCButton.setEnabled(False)

            # Red Line
            if self.line_color == 'Red':

                # PLC 1
                try:
                    red_1 = self.plc_program_1.red_plc_1_is_created()
                except:
                    red_1 = False
                
                # PLC 2
                try:
                    red_2 = self.plc_program_2.red_plc_2_is_created()
                except:
                    red_2 = False

                # PLC 3
                try:
                    red_3 = self.plc_program_3.red_plc_3_is_created()
                except:
                    red_3 = False

                # PLC programs are correctly initialized
                if red_1 and red_2 and red_3:

                    # Change Upload PLC button text
                    self.ui.UploadPLCButton.setText('PLCs\nUploaded')

                    # Change Upload PLC button color
                    self.ui.UploadPLCButton.setStyleSheet("border: 2px solid black; border-radius: 5px; background-color: lime;")

                    # Disable Upload PLC button
                    self.ui.UploadPLCButton.setEnabled(False)

    # Initialize the Wayside UI Interface
    def __init__(self, ctc_wayside, wayside_track, line_color='Green'):

        # Initialize line color
        self.line_color = line_color

        # Initialize run PLC checks
        self.maintenance_block_check = 0
        self.maintenance_switch_check = 0
        self.block_occupancy_check = 0
        self.sugg_speed_check = 0
        self.sugg_authority_check = 0

        # Initialize PLC Program Imports
        self.plc_1 = None
        self.plc_2 = None
        self.plc_3 = None

        # Initizalize PLC Program objects
        self.plc_program_1 = None
        self.plc_program_2 = None
        self.plc_program_3 = None

        # Initialize CTC Office and Wayside communication object
        self.ctc_wayside_comm_object = ctc_wayside
        
        # Initialize Wayside and Track Model communication object
        self.wayside_track_comm_object = wayside_track

        # Connect to CTC Office signals
        self.connect_ctc_signals()

        # Connect to Track Model signals
        self.connect_track_model_signals()

        # Initialize and show the Wayside user interface
        if line_color == 'Green':
            self.ui = wayside_shell_ui_green_line()
        elif line_color == 'Red':
            self.ui = wayside_shell_ui_red_line()

        # Connect to upload button
        self.ui.UploadPLCButton.clicked.connect(self.open_file_dialog)

        
# Green Line Wayside UI
class wayside_shell_ui_green_line(QMainWindow, wayside_ui_it_4_green_line.wayside_ui_green_line):
    def __init__(self):

        # Initialize the parent classes
        super().__init__()

        # QT Designer
        self.setupUi(self)

        # Show the Wayside UI
        self.show()

        # Connect signals
        self.connect_filter_buttons_signals()
        self.connect_operational_mode_signals()
        self.connect_wayside_select_signals()
        self.connect_toggle_switch_signals()

        # Initial past data
        self.ui_past_sugg_speed = self.ui_sugg_speed.copy()
        self.ui_past_cmd_authority = self.ui_cmd_authority.copy()
        self.ui_past_switches = self.ui_switches.copy()
        self.ui_past_crossings = self.ui_crossings.copy()

# Red Line Wayside UI
class wayside_shell_ui_red_line(QMainWindow, wayside_ui_it_4_red_line.wayside_ui_red_line):
    def __init__(self):

        # Initialize the parent classes
        super().__init__()
        
        # QT Designer
        self.setupUi(self)

        # Show the Wayside UI
        self.show()

        # Connect signals
        self.connect_filter_buttons_signals()
        self.connect_operational_mode_signals()
        self.connect_wayside_select_signals()
        self.connect_toggle_switch_signals()

        # Initial past data
        self.ui_past_sugg_speed = self.ui_sugg_speed.copy()
        self.ui_past_cmd_authority = self.ui_cmd_authority.copy()
        self.ui_past_switches = self.ui_switches.copy()
        self.ui_past_crossings = self.ui_crossings.copy()

####################################################################################################
#
#                                               Main Execution
#
####################################################################################################

if __name__ == '__main__':

    ctc_wayside = CTCWaysideComm.CTCWaysideControllerComm()
    wayside_track = WaysideTrackComm.WaysideControllerTrackComm()

    app = QApplication(sys.argv)

    # Initialize the Wayside Shell
    wayside_shell = wayside_shell_class(ctc_wayside, wayside_track, 'Green')

    sys.exit(app.exec())