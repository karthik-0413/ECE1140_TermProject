# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module:           Wayside Controller (Software)
# PLC Program:      Green Line PLC 2
#
# Created:          10/19/2024
# Last Update:      11/11/2024
# Last Updated by:  Zachary McPherson
# Python Version:   3.12.6
# PyQt Version:     6.7.1
#
# Notes: This is the PLC Program for the second wayside controller on the Green Line.
#        This program oversees sections H, I, J, K, L, T, U, V, W, X, and Y of the Green Line.
#        This program views the occupancies of sections M and Z.
#        This program controls 2 switches and 1 crossing


####################################################################################################
#
#                                               Libraries
#
####################################################################################################

# import green_line_plc_2_shell_communicate

####################################################################################################
#
#                                               Classes
#
####################################################################################################

# Wayside Class
class green_line_plc_2_class:
    
    # Constructor
    def __init__(self):

        # print("Green Line PLC 2 Initialized")
        # self.sec_array = sections
        self.yard_occupancy = 0
        self.yard_stop_go = 1

        # Sections
        H = Section(3)
        I = Section(22)
        J = Section(5)
        K = Section(6)
        L = Section(5)
        M = Section(3)
        T = Section(5)
        U = Section(7)
        V = Section(5)
        W = Section(22)
        X = Section(3)
        Y = Section(3)
        Z = Section(1)
        #                 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
        self.sec_array = [H, I, J, K, L, M, T, U, V, W,  X,  Y,  Z]

    def green_plc_2_is_created(self):
        return True
    
    # Update block occupancies
    def update_block_occupancies(self):

        # OR Track Model occupancies with CTC maintenance blocks
        self.read_block_occupancies_array = [a or b for a, b in zip(self.read_block_occupancies_array, self.read_maintenance_block_array)]

        # Update Yard Occupancy
        self.yard_occupancy = self.read_block_occupancies_array[0]

        # Index to traverse input block occupancy array
        BlockArrayIndex = 1

        # Traverse through each section
        for i in range(len(self.sec_array)):
            
            # Traverse through each block in each section
            for j in range(len(self.sec_array[i].block_occupancy)):
                    
                # Update block occupancy
                self.sec_array[i].block_occupancy[j] = self.read_block_occupancies_array[BlockArrayIndex]

                # Increment index
                BlockArrayIndex += 1

    # Update stop/go command for each block
    def update_block_stop_go(self):

        # Reset each block to go
        self.yard_stop_go = 1

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude sections M and Z
            if i != 5 and i != 12:

                # Traverse through each block in each section
                for j in range(len(self.sec_array[i].block_stop_go)):
                    self.sec_array[i].block_stop_go[j] = 1

        # Check for block occupancies

        # Traverse each section for occupancies
        for i in range(len(self.sec_array)):
            
            # Traverse each block in each section
            for j in range(len(self.sec_array[i].block_occupancy)):

                # Check if block is occupied
                if self.sec_array[i].block_occupancy[j] == 1:

                    # Check which section the block is in
                    # Section H
                    if i == 0:

                        # Check each block
                        if j == 1: # Block 34
                            self.sec_array[0].block_stop_go[0] = 0 # Block 33

                        elif j == 2: # Block 35
                            self.sec_array[0].block_stop_go[1] = 0 # Block 34
                            self.sec_array[0].block_stop_go[0] = 0 # Block 33

                    # Section I
                    elif i == 1:
                        
                        # Check edge blocks
                        if j == 0: # Block 36
                            self.sec_array[0].block_stop_go[2] = 0 # Block 35
                            self.sec_array[0].block_stop_go[1] = 0 # Block 34

                        elif j == 1: # Block 37
                            self.sec_array[0].block_stop_go[2] = 0 # Block 35
                            self.sec_array[1].block_stop_go[0] = 0 # Block 36

                        # Not edge blocks
                        elif j > 1: # Blocks 38 --> 57
                            self.sec_array[1].block_stop_go[j - 2] = 0
                            self.sec_array[1].block_stop_go[j - 1] = 0

                    # Section J
                    elif i == 2:

                        # Check edge blocks
                        if j == 0: # Block 58

                            # Check switch 1 position
                            if self.write_switch_cmd_array[0]:
                                self.sec_array[1].block_stop_go[21] = 0 # Block 57
                                self.sec_array[1].block_stop_go[20] = 0 # Block 56

                        elif j == 1: # Block 59

                            # Check switch 1 position
                            if self.write_switch_cmd_array[0]:
                                self.sec_array[1].block_stop_go[21] = 0 # Block 57

                            self.sec_array[2].block_stop_go[0] = 0 # Block 58

                        # Not edge blocks
                        elif j > 1: # Blocks 60 --> 62
                            self.sec_array[2].block_stop_go[j - 2] = 0
                            self.sec_array[2].block_stop_go[j - 1] = 0

                    # Section K
                    elif i == 3:

                        # Check edge blocks
                        if j == 0: # Block 63

                            # Check switch 2 position
                            if self.write_switch_cmd_array[1]:
                                self.yard_stop_go = 0 # Yard block
                            else:
                                self.sec_array[2].block_stop_go[4] = 0 # Block 62
                                self.sec_array[2].block_stop_go[3] = 0 # Block 61

                        elif j == 1: # Block 64

                            # Check switch 2 position
                            if not self.write_switch_cmd_array[1]:
                                self.sec_array[2].block_stop_go[4] = 0 # Block 62
                            else:
                                self.yard_stop_go = 0

                            self.sec_array[3].block_stop_go[0] = 0 # Block 63

                        # Not edge blocks
                        elif j > 1: # Blocks 65 --> 68
                            self.sec_array[3].block_stop_go[j - 2] = 0
                            self.sec_array[3].block_stop_go[j - 1] = 0

                    # Section L
                    elif i == 4:

                        # Check edge blocks
                        if j == 0: # Block 69
                            self.sec_array[3].block_stop_go[5] = 0 # Block 68
                            self.sec_array[3].block_stop_go[4] = 0 # Block 67

                        elif j == 1: # Block 70
                            self.sec_array[3].block_stop_go[5] = 0 # Block 68
                            self.sec_array[4].block_stop_go[0] = 0 # Block 69

                        # Not edge blocks
                        elif j > 1: # Blocks 71 --> 73
                            self.sec_array[4].block_stop_go[j - 2] = 0
                            self.sec_array[4].block_stop_go[j - 1] = 0

                    # Section M
                    elif i == 5:

                        # Check edge blocks
                        if j == 0: # Block 74
                            self.sec_array[4].block_stop_go[4] = 0 # Block 73
                            self.sec_array[4].block_stop_go[3] = 0 # Block 72

                        elif j == 1: # Block 75
                            self.sec_array[4].block_stop_go[4] = 0 # Block 73

                    # Section T
                    elif i == 6:

                        # Check edge blocks
                        if j == 1: # Block 106
                            self.sec_array[6].block_stop_go[0] = 0 # Block 105

                        # Not edge blocks
                        elif j > 1: # Blocks 107 --> 109
                            self.sec_array[6].block_stop_go[j - 1] = 0
                            self.sec_array[6].block_stop_go[j - 2] = 0

                    # Section U
                    elif i == 7:

                        # Check edge blocks
                        if j == 0: # Block 110
                            self.sec_array[6].block_stop_go[4] = 0 # Block 109
                            self.sec_array[6].block_stop_go[3] = 0 # Block 108

                        elif j == 1: # Block 111
                            self.sec_array[6].block_stop_go[4] = 0 # Block 109
                            self.sec_array[7].block_stop_go[0] = 0 # Block 110

                        # Not edge blocks
                        elif j > 1: # Blocks 112 --> 116
                            self.sec_array[7].block_stop_go[j - 2] = 0
                            self.sec_array[7].block_stop_go[j - 1] = 0

                    # Section V
                    elif i == 8:

                        # Check edge blocks
                        if j == 0: # Block 117
                            self.sec_array[7].block_stop_go[6] = 0 # Block 116
                            self.sec_array[7].block_stop_go[5] = 0 # Block 115

                        elif j == 1: # Block 118
                            self.sec_array[7].block_stop_go[6] = 0 # Block 116
                            self.sec_array[8].block_stop_go[0] = 0 # Block 117

                        # Not edge blocks
                        elif j > 1: # Blocks 119 --> 121
                            self.sec_array[8].block_stop_go[j - 2] = 0
                            self.sec_array[8].block_stop_go[j - 1] = 0

                    # Section W
                    elif i == 9:

                        # Check edge blocks
                        if j == 0: # Block 122
                            self.sec_array[8].block_stop_go[4] = 0 # Block 121
                            self.sec_array[8].block_stop_go[3] = 0 # Block 120

                        elif j == 1: # Block 123
                            self.sec_array[8].block_stop_go[4] = 0 # Block 121
                            self.sec_array[9].block_stop_go[0] = 0 # Block 122

                        # Not edge blocks
                        elif j > 1: # Blocks 124 --> 143
                            self.sec_array[9].block_stop_go[j - 2] = 0
                            self.sec_array[9].block_stop_go[j - 1] = 0

                    # Section X
                    elif i == 10:

                        # Check each block
                        if j == 0: # Block 144
                            self.sec_array[9].block_stop_go[21] = 0 # Block 143
                            self.sec_array[9].block_stop_go[20] = 0 # Block 142

                        elif j == 1: # Block 145
                            self.sec_array[9].block_stop_go[21] = 0 # Block 143
                            self.sec_array[10].block_stop_go[0] = 0 # Block 144

                        elif j == 2: # Block 146
                            self.sec_array[10].block_stop_go[0] = 0 # Block 144
                            self.sec_array[10].block_stop_go[1] = 0 # Block 145

                    # Section Y
                    elif i == 11:

                        # Check each block
                        if j == 0: # Block 147
                            self.sec_array[10].block_stop_go[2] = 0 # Block 146
                            self.sec_array[10].block_stop_go[1] = 0 # Block 145

                        elif j == 1: # Block 148
                            self.sec_array[10].block_stop_go[2] = 0 # Block 146
                            self.sec_array[11].block_stop_go[0] = 0 # Block 147

                        elif j == 2: # Block 149
                            self.sec_array[11].block_stop_go[0] = 0 # Block 147
                            self.sec_array[11].block_stop_go[1] = 0 # Block 148

                    # Section Z
                    elif i == 12:

                        # Only one block, Block 150
                        self.sec_array[11].block_stop_go[2] = 0 # Block 149
                        self.sec_array[11].block_stop_go[1] = 0 # Block 148

        # Check switch positions
        if self.write_switch_cmd_array[1]: # Yard -> K
            self.sec_array[2].block_stop_go[4] = 0
            self.sec_array[2].block_stop_go[3] = 0
        else:                         # J -> K
            self.yard_stop_go = 0

    # Update command speed of each block
    def update_cmd_speed(self):
        
        # Index to traverse output suggested speed array
        BlockArrayIndex = 1
        
        # Check stop_go commands for each block
        if self.yard_stop_go == 0:
            self.write_cmd_speed_array[0] = 0
        else:
            self.write_cmd_speed_array[0] = self.read_sugg_speed_array[0]

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude section M and Z
            if i != 5 and i != 12:

                # Traverse each block in each section
                for j in range(len(self.sec_array[i].block_stop_go)):

                    # Block is commanding stop
                    if self.sec_array[i].block_stop_go[j] == 0:
                        self.write_cmd_speed_array[BlockArrayIndex] = 0

                    # Block is commanding go
                    else:
                        self.write_cmd_speed_array[BlockArrayIndex] = self.read_sugg_speed_array[BlockArrayIndex]
                    
                    # Increment index
                    BlockArrayIndex += 1

    # Update command authority of each block
    def update_cmd_authority(self):
        
        # Index to traverse output suggested authority array
        BlockArrayIndex = 1

        # Pass yard suggested authority
        self.write_cmd_authority_array[0] = self.read_sugg_authority_array[0]

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude section M and Z
            if i != 5 and i != 12:

                # Traverse each block in each section
                for j in range(len(self.sec_array[i].block_stop_go)):

                    # Pass suggested authority
                    self.write_cmd_authority_array[BlockArrayIndex] = self.read_sugg_authority_array[BlockArrayIndex]

                    # Increment index
                    BlockArrayIndex += 1

    # Update switch commands
    def update_switch_cmd(self):

        # Switch I
        self.write_switch_cmd_array[0] = 0 # I -> Yard

        # Switch K
        self.write_switch_cmd_array[1] = 1 # Yard -> K

        # Switch I maintenance
        if self.read_block_occupancies_array[0] and self.read_block_occupancies_array[25] and self.read_block_occupancies_array[26]:
            self.write_switch_cmd_array[0] = self.read_maintenance_switch_array[0]

        # Switch K maintenance
        if self.read_block_occupancies_array[0] and self.read_block_occupancies_array[30] and self.read_block_occupancies_array[31]:
            self.write_switch_cmd_array[1] = self.read_maintenance_switch_array[1]

    # Update signal commands
    def update_signal_cmd(self):
        
        # Check switch 1 position
        if self.write_switch_cmd_array[0]: # Switch I -> J
            self.write_signal_cmd_array[0] = 1 # Yard
            self.write_signal_cmd_array[1] = 0 # Section J
        else:                         # Switch I -> Yard
            self.write_signal_cmd_array[0] = 0 # Yard
            self.write_signal_cmd_array[1] = 1 # Section J

        # Signal for Section K
        self.write_signal_cmd_array[2] = 1 # Default signal

    # Update crossing command
    def update_crossing_cmd(self):

        # Check section T overall occupancy
        if self.sec_array[6].update_section_occupancy():
            self.write_crossing_cmd_array[0] = 1
        else:
            self.write_crossing_cmd_array[0] = 0


    ####################################################################################################
    #
    #                                              Read & Write
    #
    ####################################################################################################

    ################################
    #       CTC Office Inputs
    ################################

    # Variables
    read_maintenance_block_array = [0] * 91
    read_maintenance_switch_array = [None] * 2
    read_sugg_speed_array = [None] * 87
    read_sugg_authority_array = [None] * 87
    maintenance_block_check = 0
    maintenance_switch_check = 0
    sugg_speed_check = 0
    sugg_authority_check = 0

    # Functions
    def read_maintenance_block_handler(self, maintenance_block_array: list):
        self.read_maintenance_block_array = maintenance_block_array.copy()
        self.maintenance_block_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_switch_check and self.maintenance_block_check:

            # Update block occupancies
            self.update_block_occupancies()

            # Perform computations based on block occupancies
            self.update_switch_cmd()
            self.update_signal_cmd()
            self.update_crossing_cmd()
            self.update_block_stop_go()
            self.update_cmd_speed()
            self.update_cmd_authority()

            # Reset checks
            self.maintenance_block_check = 0
            self.maintenance_switch_check = 0
            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0

    def read_maintenance_switches_handler(self, maintenance_switch_array: list):
        self.read_maintenance_switch_array = maintenance_switch_array.copy()
        self.read_maintenance_switch_array[1] = not self.read_maintenance_switch_array[1]
        self.maintenance_switch_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_switch_check and self.maintenance_block_check:

            # Update block occupancies
            self.update_block_occupancies()

            # Perform computations based on block occupancies
            self.update_switch_cmd()
            self.update_signal_cmd()
            self.update_crossing_cmd()
            self.update_block_stop_go()
            self.update_cmd_speed()
            self.update_cmd_authority()

            # Reset checks
            self.maintenance_block_check = 0
            self.maintenance_switch_check = 0
            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0

    def read_sugg_speed_handler(self, sugg_speed_array: list):
        self.read_sugg_speed_array = sugg_speed_array.copy()
        self.sugg_speed_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_switch_check and self.maintenance_block_check:

            # Update block occupancies
            self.update_block_occupancies()

            # Perform computations based on block occupancies
            self.update_switch_cmd()
            self.update_signal_cmd()
            self.update_crossing_cmd()
            self.update_block_stop_go()
            self.update_cmd_speed()
            self.update_cmd_authority()

            # Reset checks
            self.maintenance_block_check = 0
            self.maintenance_switch_check = 0
            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0

    def read_sugg_authority_handler(self, sugg_authority_array: list):
        self.read_sugg_authority_array = sugg_authority_array.copy()
        self.sugg_authority_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_switch_check and self.maintenance_block_check:

            # Update block occupancies
            self.update_block_occupancies()

            # Perform computations based on block occupancies
            self.update_switch_cmd()
            self.update_signal_cmd()
            self.update_crossing_cmd()
            self.update_block_stop_go()
            self.update_cmd_speed()
            self.update_cmd_authority()

            # Reset checks
            self.maintenance_block_check = 0
            self.maintenance_switch_check = 0
            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0


    ################################
    #       TRK Model Inputs
    ################################

    # Variables
    read_block_occupancies_array = [0] * 91
    block_occupancy_check = 0

    # Functions
    def read_block_occupancy_handler(self, block_occupancy_array: list):
        self.read_block_occupancies_array = block_occupancy_array.copy()
        self.block_occupancy_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_switch_check and self.maintenance_block_check:

            # Update block occupancies
            self.update_block_occupancies()

            # Perform computations based on block occupancies
            self.update_switch_cmd()
            self.update_signal_cmd()
            self.update_crossing_cmd()
            self.update_block_stop_go()
            self.update_cmd_speed()
            self.update_cmd_authority()

            # Reset checks
            self.maintenance_block_check = 0
            self.maintenance_switch_check = 0
            self.sugg_speed_check = 0
            self.sugg_authority_check = 0
            self.block_occupancy_check = 0


    ################################
    #       CTC Office Outputs
    ################################

    # Block Occupancies are passed from Wayside shell file

    ################################
    #       TRK Model Outputs
    ################################

    # Variables
    write_cmd_speed_array = [None] * 87
    write_cmd_authority_array = [None] * 87
    write_switch_cmd_array = [0, 1]
    write_signal_cmd_array = [0, 1, 0]
    write_crossing_cmd_array = [0]

# Section Class
class Section:
    
    ##################################
    #           Constructor
    ##################################

    # Default Constructor
    def __init__(self, num_blocks):

        # default values
        self.block_occupancy = []
        self.block_stop_go = []
        
        # Fill empty arrays
        for i in range(num_blocks):
            self.block_occupancy.append(0)
            self.block_stop_go.append(1)

    ##################################
    #           Methods
    ##################################

    # Updates ovall occupancy of section
    def update_section_occupancy(self):
        
        # Check if any blocks are occupied
        for i in range(len(self.block_occupancy)):
            if self.block_occupancy[i]:
                return True
            
        return False




