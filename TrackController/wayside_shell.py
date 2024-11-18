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
import importlib.util

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# PyQt6 libraries
from PyQt6.QtWidgets import QApplication, QFileDialog

# Wayside UI Interface
from TrackController import wayside_ui

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

#    read_maintenance_blocks = [0] * 151
#    read_maintenance_switch_cmd = [None] * 6

    # Input from Track Model
    read_block_occupancy = [0] * 152

    # Output to CTC Office
    write_block_occupancy = [0] * 152

    # Output to Track Model
    write_cmd_speed = [None] * 152
    write_cmd_authority = [None] * 152

    #                    D   F   I   K  N1  N2   
    #write_switch_cmd = [ 1,  1,  0,  0,  0,  0]

    #                    C   D   F   G   J   K  N1  N2   O   R  Yard 
    #write_signal_cmd = [ 0,  1,  0,  1,  1,  0,  0,  1,  0,  1,  0 ]

    #                     E  T
    #write_crossing_cmd = [0, 0]

    # Test Values

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
        print(f'read_sugg_speed_handler, {sugg_speed_array[0] if len(sugg_speed_array) else 'empty'}')

        self.read_sugg_speed = sugg_speed_array

        # Update Wayside user interface table
        if len(self.read_sugg_speed):
            self.ui.past_sugg_speed = self.ui.green_line_sugg_speed
            self.ui.green_line_sugg_speed = sugg_speed_array
            self.sugg_speed_check = 1

            if self.sugg_speed_check == 1 and self.sugg_authority_check == 1 and self.block_occupancy_check == 1:

                self.ui.update_table()

                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    print('Calling PLC Program read functions')
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    print("Calling PLC Program operation functions")
                    # Process incoming data
                    self.call_green_line_plc_1_operation_handlers()
                    self.call_green_line_plc_2_operation_handlers()
                    self.call_green_line_plc_3_operation_handlers()

    def read_sugg_authority_handler(self, sugg_authority_array):
        print(f'read_sugg_authority_handler, {sugg_authority_array[0] if len(sugg_authority_array) else 'empty'}')

        self.read_sugg_authority = sugg_authority_array

        # Update Wayside user interface table
        if len(self.read_sugg_authority):
            self.ui.past_sugg_authority = self.ui.green_line_sugg_auth
            self.ui.green_line_sugg_auth = sugg_authority_array
            self.sugg_authority_check = 1
            
            if self.sugg_speed_check == 1 and self.sugg_authority_check == 1 and self.block_occupancy_check == 1:

                self.ui.update_table()

                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    print('Calling PLC Program read functions')
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    print("Calling PLC Program operation functions")
                    # Process incoming data
                    self.call_green_line_plc_1_operation_handlers()
                    self.call_green_line_plc_2_operation_handlers()
                    self.call_green_line_plc_3_operation_handlers()

#    def read_maintenance_blocks_handler(self, maintenance_blocks_array):
#        self.read_maintenance_blocks = maintenance_blocks_array

#    def read_maintenance_switch_cmd_handler(self, maintenance_switch_cmd_array):
#        self.read_maintenance_switch_cmd = maintenance_switch_cmd_array

    # Inputs from Track Model
    def read_block_occupancy_handler(self, block_occupancy_array):
        self.read_block_occupancy = block_occupancy_array
        self.write_block_occupancy = block_occupancy_array

        # Update Wayside user interface table
        if len(self.read_block_occupancy):
            self.ui.green_line_block_occupancy = block_occupancy_array
            self.block_occupancy_check = 1
            
            if self.sugg_speed_check == 1 and self.sugg_authority_check == 1 and self.block_occupancy_check == 1:

                self.ui.update_table()

                self.sugg_speed_check = 0
                self.sugg_authority_check = 0
                self.block_occupancy_check = 0

                # Call PLC Program handler functions
                if self.plc_program_1 != None and self.plc_program_2 != None and self.plc_program_3 != None:
                    
                    print('Calling PLC Program read functions')
                    # Read incoming data
                    self.call_green_line_plc_1_read_handlers()
                    self.call_green_line_plc_2_read_handlers()
                    self.call_green_line_plc_3_read_handlers()

                    print("Calling PLC Program operation functions")
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

        # Check if the sugg_speed_array is empty
        if len(self.read_sugg_speed):
            for i in range(1, 33):
                plc_1_sugg_authority.append(self.read_sugg_speed[i])
            plc_1_sugg_authority.append(self.read_sugg_speed[150])
            plc_1_sugg_authority.append(self.read_sugg_speed[151])

            # Pass suggested authorities to PLC Program 1
            if self.plc_program_1 != None:
                self.plc_program_1.read_sugg_authority_handler(plc_1_sugg_authority)

    # Inputs from Track Model
    def green_line_plc_1_block_occupancy_handler(self):
        plc_1_block_occupancy = []

        # Check if the sugg_speed_array is empty
        if len(self.read_sugg_speed):
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

    # Inputs from Track Model
    def green_line_plc_2_sugg_speed_handler(self):
        plc_2_sugg_speed = []

        # Check if the sugg_speed_array is empty
        if len(self.read_sugg_speed):
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
        if len(self.read_sugg_authority):

            plc_2_sugg_authority.append(self.read_sugg_authority[0])

            for i in range(33, 74):
                plc_2_sugg_authority.append(self.read_sugg_authority[i])

            for i in range(105, 150):
                plc_2_sugg_authority.append(self.read_sugg_authority[i])

            # Pass suggested authorities to PLC Program 2
            if self.plc_program_2 != None:
                self.plc_program_2.read_sugg_authority_handler(plc_2_sugg_authority)

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
        print(f'\n{len(signal_cmd_array)},\t{signal_cmd_array}\n')

        self.write_signal_cmd[10] = signal_cmd_array[0] # Yard
        self.write_signal_cmd[4] = signal_cmd_array[1]  # J
        self.write_signal_cmd[5] = signal_cmd_array[2]  # K

    def green_line_plc_2_crossing_cmd_handler(self, crossing_cmd_bool):
        self.write_crossing_cmd[0] = crossing_cmd_bool

    def call_green_line_plc_2_read_handlers(self):
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

        ####################################
        #     Green Line Emit Signals
        ####################################
        print('Wayside occ', self.write_block_occupancy)

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
        if len(self.write_cmd_speed):
            self.ui.green_line_cmd_speed = self.write_cmd_speed

        # Commanded Authority
        if len(self.write_cmd_authority):
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

    ###################################
    #       Upload PLC Program
    ###################################

    # Open file manager to select PLC programs
    def open_file_dialog(self):

            # Open a file dialog to select Python files
            file_paths, _ = QFileDialog.getOpenFileNames(self.ui, 'Open Python files', '', 'Python Files (*.py)')

            # Run PLC programs in separate processes
            self.execute_files(file_paths)
            
    def upload_plc_program(self, file_paths):
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



    # Initialize the Wayside UI Interface
    def __init__(self, ctc_wayside, wayside_track):

        # Initialize update UI checks
        self.block_occupancy_check = 0
        self.sugg_speed_check = 0
        self.sugg_authority_check = 0

        # Define PLC Program Import Variables
        self.plc_1 = None
        self.plc_2 = None
        self.plc_3 = None

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
        self.ui = wayside_shell_ui()
        self.ui.show()

        # Connect to upload button
        self.ui.UploadPLCButton.clicked.connect(self.open_file_dialog)

        

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

if __name__ == '__main__':

    ctc_wayside = CTCWaysideComm.CTCWaysideControllerComm()
    wayside_track = WaysideTrackComm.WaysideControllerTrackComm()

    app = QApplication(sys.argv)

    # Initialize the Wayside Shell
    wayside_shell = wayside_shell_class(ctc_wayside, wayside_track)

    sys.exit(app.exec())