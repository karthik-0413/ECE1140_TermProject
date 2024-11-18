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
# Notes: This is the PLC Program for the third wayside controller on the Green Line.
#        This program oversees sections M, N1, N2, O, P, Q, R, and S of the Green Line.
#        This program views the occupanices of section T
#        This program controls 2 switches and 0 crossings


####################################################################################################
#
#                                               Libraries
#
####################################################################################################

#import green_line_plc_3_shell_communicate

####################################################################################################
#
#                                               Classes
#
####################################################################################################

# Wayside Class
class green_line_plc_3_class:
    
    ##################################
    #           Constructor
    ##################################

    # Default Constructor
    def __init__(self):
        
        print("Green Line PLC 3 Initialized")

        self.N_direction = 0
        self.N_direction_update = 1
        self.N_occupancy = 0

        # Sections
        M = Section(3)
        N1 = Section(5) # Direction Matters
        N2 = Section(4) # Direction Matters
        O = Section(3)
        P = Section(9)
        Q = Section(3)
        R = Section(1)
        S = Section(3)
        T = Section(5)

        self.sec_array = [M, N1, N2, O, P, Q, R, S, T]

    ##################################
    #           Methods
    ##################################
    
    def is_created(self):
        return True

    # Update block occupancies
    def update_block_occupancies(self):

        # Index to traverse input block occupancy array
        BlockArrayIndex = 0

        # Traverse through each section
        for i in range(len(self.sec_array)):
            
            # Traverse through each block in each section
            for j in range(len(self.sec_array[i].block_occupancy)):
                    
                # Update block occupancy
                self.sec_array[i].block_occupancy[j] = self.read_block_occupancies_array[BlockArrayIndex]

                # Increment index
                BlockArrayIndex += 1
        
            # Update overall occupancy of section
            self.sec_array[i].update_section_occupancy()

        # Update overall occupancy of N sections
        if self.sec_array[1].overall_occupancy or self.sec_array[2].overall_occupancy:
            self.N_occupancy = 1
        else:
            self.N_occupancy = 0

    # Update stop/go command for each block
    def update_block_stop_go(self):

        # Reset each block to go

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude section H
            if i != 8:

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
                    # Section M
                    if i == 0:

                        # Check each block
                        if j == 1: # Block 75
                            self.sec_array[0].block_stop_go[0] = 0 # Block 74
                        
                        elif j == 2: # Block 76
                            self.sec_array[0].block_stop_go[1] = 0
                            self.sec_array[0].block_stop_go[0] = 0

                    # Section N1
                    if i == 1:

                        # Check each block
                        if j == 0: # Block 77
                            
                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[0].block_stop_go[2] = 0 # Block 76
                                self.sec_array[0].block_stop_go[1] = 0 # Block 75
                            else:                # Moving right, away from loop
                                self.sec_array[1].block_stop_go[1] = 0 # Block 78
                                self.sec_array[1].block_stop_go[2] = 0 # Block 79

                        elif j == 1: # Block 78

                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[1].block_stop_go[0] = 0 # Block 77
                                self.sec_array[0].block_stop_go[2] = 0 # Block 76
                            else:                # Moving right, away from loop
                                self.sec_array[1].block_stop_go[0] = 0 # Block 79
                                self.sec_array[0].block_stop_go[2] = 0 # Block 80

                        elif j == 2: # Block 79

                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[1].block_stop_go[0] = 0 # Block 77
                                self.sec_array[1].block_stop_go[1] = 0 # Block 78
                            else:                # Moving right, away from loop
                                self.sec_array[1].block_stop_go[3] = 0 # Block 80
                                self.sec_array[1].block_stop_go[4] = 0 # Block 81

                        elif j == 3: # Block 80

                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[1].block_stop_go[2] = 0 # Block 79
                                self.sec_array[1].block_stop_go[1] = 0 # Block 78
                            else:                # Moving right, away from loop
                                self.sec_array[1].block_stop_go[4] = 0 # Block 81
                                self.sec_array[2].block_stop_go[0] = 0 # Block 82

                        elif j == 4: # Block 81

                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[1].block_stop_go[3] = 0 # Block 80
                                self.sec_array[1].block_stop_go[2] = 0 # Block 79
                            else:                # Moving right, away from loop
                                self.sec_array[2].block_stop_go[0] = 0 # Block 82
                                self.sec_array[2].block_stop_go[1] = 0 # Block 83
                    
                    # Section N2
                    elif i == 2:

                        # Check each block
                        if j == 0: # Block 82
                            
                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[1].block_stop_go[4] = 0 # Block 81
                                self.sec_array[1].block_stop_go[3] = 0 # Block 80
                            else:                # Moving right, away from loop
                                self.sec_array[2].block_stop_go[1] = 0 # Block 83
                                self.sec_array[2].block_stop_go[2] = 0 # Block 84

                        elif j == 1: # Block 83

                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[1].block_stop_go[4] = 0 # Block 81
                                self.sec_array[2].block_stop_go[0] = 0 # Block 82
                            else:                # Moving right, away from loop
                                self.sec_array[2].block_stop_go[2] = 0 # Block 84
                                self.sec_array[2].block_stop_go[3] = 0 # Block 85

                        elif j == 2: # Block 84

                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[2].block_stop_go[0] = 0 # Block 82
                                self.sec_array[2].block_stop_go[1] = 0 # Block 83
                            else:                # Moving right, away from loop
                                self.sec_array[2].block_stop_go[3] = 0 # Block 85
                                self.sec_array[5].block_stop_go[2] = 0 # Block 100

                        elif j == 3: # Block 85

                            # Check direction of N sections
                            if self.N_direction: # Moving left, towards loop
                                self.sec_array[2].block_stop_go[1] = 0 # Block 83
                                self.sec_array[2].block_stop_go[2] = 0 # Block 84
                            else:                # Moving right, away from loop
                                self.sec_array[5].block_stop_go[2] = 0 # Block 100
                                self.sec_array[5].block_stop_go[1] = 0 # Block 99

                    # Section O
                    elif i == 3:

                        # Check each block
                        if j == 0: # Block 86

                            # Check if any trains are heading towards loop based on switch position
                            if not self.write_switch_cmd_array[1]:
                                self.sec_array[2].block_stop_go[3] = 0 # Block 85
                                self.sec_array[2].block_stop_go[2] = 0 # Block 84

                        elif j == 1: # block 87

                            # Check if any trains are heading towards loop based on switch position
                            if not self.write_switch_cmd_array[1]:
                                self.sec_array[2].block_stop_go[3] = 0 # Block 85

                            self.sec_array[3].block_stop_go[0] = 0 # Block 86

                        elif j == 2: # Block 88
                            self.sec_array[3].block_stop_go[0] = 0 # Block 86
                            self.sec_array[3].block_stop_go[1] = 0 # Block 87

                    # Section P
                    elif i == 4:

                        # Check edge blocks
                        if j == 0: # Block 89
                            self.sec_array[3].block_stop_go[1] = 0 # Block 87
                            self.sec_array[3].block_stop_go[2] = 0 # Block 88

                        elif j == 1: # Block 90
                            self.sec_array[3].block_stop_go[2] = 0 # Block 88
                            self.sec_array[4].block_stop_go[0] = 0 # Block 89

                        # Not edge block
                        elif j > 1: # Blocks 91 --> 97
                            self.sec_array[4].block_stop_go[j - 1] = 0
                            self.sec_array[4].block_stop_go[j - 2] = 0
                    
                    # Section Q
                    elif i == 5:

                        # Check edge blocks
                        if j == 0: # Block 98
                            self.sec_array[4].block_stop_go[8] = 0 # Block 97
                            self.sec_array[4].block_stop_go[7] = 0 # Block 96

                        elif j == 1: # Block 99
                            self.sec_array[5].block_stop_go[0] = 0 # Block 98
                            self.sec_array[4].block_stop_go[8] = 0 # Block 97

                        # Not edge block
                        elif j == 2: # Block 100
                            self.sec_array[5].block_stop_go[1] = 0 # Block 99
                            self.sec_array[5].block_stop_go[0] = 0 # Block 98

                    # Section R
                    elif i == 6:

                        # Only one block, 101

                        # Check switch 1 position
                        if not self.write_switch_cmd_array[0]:
                            self.sec_array[1].block_stop_go[0] = 0 # Block 77
                            self.sec_array[1].block_stop_go[1] = 0 # Block 78
                        
                    # Section S
                    elif i == 7:

                        # Check each block
                        if j == 0: # Block 102

                            # Check if any trains are heading away from loop based on occupancy
                            if not self.write_switch_cmd_array[0]:
                                self.sec_array[1].block_stop_go[0] = 0 # Block 77

                            self.sec_array[6].block_stop_go[0] = 0 # Block 101

                        elif j == 1: # block 103
                            self.sec_array[6].block_stop_go[0] = 0 # Block 101
                            self.sec_array[7].block_stop_go[0] = 0 # Block 102

                        elif j == 2: # Block 104
                            self.sec_array[7].block_stop_go[1] = 0 # Block 103
                            self.sec_array[7].block_stop_go[0] = 0 # Block 102

                    # Section T
                    elif i == 8:

                        # Check first two blocks
                        if j == 0: # Block 105
                            self.sec_array[7].block_stop_go[2] = 0 # Block 104
                            self.sec_array[7].block_stop_go[1] = 0 # Block 103

                        elif j == 1: # Block 106
                            self.sec_array[7].block_stop_go[2] = 0 # Block 104

        # Check switch positions
        # Switch 1
        if not self.write_switch_cmd_array[0]: # N1 -> R
            self.sec_array[0].block_stop_go[1] = 0 # Block 75
            self.sec_array[0].block_stop_go[2] = 0 # Block 76

        # Switch 2
        if not self.write_switch_cmd_array[1]: # O <- N2
            self.sec_array[5].block_stop_go[2] = 0 # Block 100
            self.sec_array[5].block_stop_go[1] = 0 # Block 99              
                                
    # Update overall direction of sections N1, N2                            
    def update_N_direction(self):
        
        # Check if any blocks in DEF are occupied
        if self.N_occupancy:
            
            # Find new direction
            # Away from loop
            if self.sec_array[2].block_occupancy[3]:
                
                # Check if direction is already set
                if self.N_direction_update:
                    self.N_direction = 0
                    self.N_direction_update = 0
            
            # Towards loop
            elif self.sec_array[1].block_occupancy[7]:

                # Check if direction is already set
                if self.N_direction_update:
                    self.N_direction = 1
                    self.N_direction_update = 0

        # Direction is ready to be updated
        else:
            self.N_direction_update = 1

    # Update commanded speed of each block
    def update_cmd_speed(self):

        # Index to traverse output suggested speed array
        BlockArrayIndex = 0
        
        # Check stop_go commands for each block

        # Traverse each section
        for i in range(len(self.sec_array) - 1): # Exclude section T

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

    # Update commanded authority of each block
    def update_cmd_authority(self):
        
        # Index to traverse output suggested authority array
        BlockArrayIndex = 0

        # Traverse each section
        for i in range(len(self.sec_array) - 1): # Exclude section T

            # Traverse each block in each section
            for j in range(len(self.sec_array[i].block_stop_go)):

                # Pass suggested authority
                self.write_cmd_authority_array[BlockArrayIndex] = self.read_sugg_authority_array[BlockArrayIndex]

                # Increment index
                BlockArrayIndex += 1

    # Update switch commands
    def update_switch_cmd(self):
        
        # Check if DEF needs new direction status
        if self.N_direction_update:

            # Check occupancy of sections Q and M

            # Train heading towards loop
            if self.sec_array[5].overall_occupancy:
                self.write_switch_cmd_array[0] = 0 # N1 -> R
                self.write_switch_cmd_array[1] = 1 # Q -> N2 

            # Train heading towards yard
            elif self.sec_array[0].overall_occupancy:
                self.write_switch_cmd_array[1] = 1 # N1 <- M
                self.write_switch_cmd_array[0] = 0 # O <- N2

            # Default positions
            else:
                self.write_switch_cmd_array[1] = 0 # N1 <- M
                self.write_switch_cmd_array[0] = 1 # O <- N2

        # DEF direction is set
        else:

            # Check direction of DEF Sections

            # Train heading towards loop
            if self.N_direction:
                self.write_switch_cmd_array[0] = 0 # D -> C
                self.write_switch_cmd_array[1] = 1 # F <- Z
            
            # Train heading towards yard
            else:
                self.write_switch_cmd_array[0] = 1 # D <- A
                self.write_switch_cmd_array[1] = 0 # F -> G

    # Update signal commands
    def update_signal_cmd(self):
        
        # Check status of switch 1
        if self.write_switch_cmd_array[0]: # N1 <- M
            self.write_signal_cmd_array[0] = 0 # Section N1
            self.write_signal_cmd_array[1] = 1 # Section R
        else:                         # N2 -> R
            self.write_signal_cmd_array[0] = 1 # Section N1
            self.write_signal_cmd_array[1] = 0 # Section R

        # Check status of switch 2
        if self.write_switch_cmd_array[1]: # Q -> N2
            self.write_signal_cmd_array[2] = 0 # Section N2
            self.write_signal_cmd_array[3] = 1 # Section O
        else:                         # O <- N2
            self.write_signal_cmd_array[2] = 1 # Section N2
            self.write_signal_cmd_array[3] = 0 # Section O



####################################################################################################
#
#                               Initial Sections with Default Path
#
####################################################################################################



# Wayside
# wayside = Wayside([M, N1, N2, O, P, Q, R, S, T])

    ####################################################################################################
    #
    #                                              Read & Write
    #
    ####################################################################################################

    ################################
    #       CTC Office Inputs
    ################################

    # Variables
    read_maintenance_switch_array = [None] * 2
    read_sugg_speed_array = [None] * 31
    read_sugg_authority_array = [None] * 31
    #maintenance_switch_check =0
    sugg_speed_check = 0
    sugg_authority_check = 0

    # Functions
    # def read_maintenance_switches_handler(self, maintenance_switch_array):
    #     self.read_maintenance_switch_array = maintenance_switch_array
    #     self.maintenance_switch_check = 1

    def read_sugg_speed_handler(self, sugg_speed_array):
        self.read_sugg_speed_array = sugg_speed_array
        self.sugg_speed_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check:

         # Update block occupancies
         self.update_block_occupancies()

         # Perform computations based on block occupancies
         self.update_switch_cmd()
         self.update_signal_cmd()
         self.update_block_stop_go()
         self.update_cmd_speed()
         self.update_cmd_authority()

         # Reset checks
         #self.maintenance_switch_check = 0
         self.sugg_speed_check = 0
         self.sugg_authority_check = 0
         self.block_occupancy_check = 0

    def read_sugg_authority_handler(self, sugg_authority_array):
        self.read_sugg_authority_array = sugg_authority_array
        self.sugg_authority_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check:

         # Update block occupancies
         self.update_block_occupancies()

         # Perform computations based on block occupancies
         self.update_switch_cmd()
         self.update_signal_cmd()
         self.update_block_stop_go()
         self.update_cmd_speed()
         self.update_cmd_authority()

         # Reset checks
         #self.maintenance_switch_check = 0
         self.sugg_speed_check = 0
         self.sugg_authority_check = 0
         self.block_occupancy_check = 0


    ################################
    #       TRK Model Inputs
    ################################

    # Variables
    read_block_occupancies_array = [0] * 36
    block_occupancy_check = 0

    # Functions
    def read_block_occupancy_handler(self, block_occupancy_array):
        self.read_block_occupancies_array = block_occupancy_array
        self.block_occupancy_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check:

         # Update block occupancies
         self.update_block_occupancies()

         # Perform computations based on block occupancies
         self.update_switch_cmd()
         self.update_signal_cmd()
         self.update_block_stop_go()
         self.update_cmd_speed()
         self.update_cmd_authority()

         # Reset checks
         #self.maintenance_switch_check = 0
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
    write_cmd_speed_array = [None] * 31
    write_cmd_authority_array = [None] * 31
    write_switch_cmd_array = [1, 0]
    write_signal_cmd_array = [0, 1, 1, 0]

# # Write to Wayside Shell
# def write_to_wayside_shell():
#     green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_cmd_speed.emit(write_cmd_speed_array)
#     green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_cmd_authority.emit(write_cmd_authority_array)
#     green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_switch_cmd.emit(write_switch_cmd_array)
#     green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_signal_cmd.emit(write_signal_cmd_array)

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
        self.overall_occupancy = 0
        
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
                self.overall_occupancy = 1
                break

####################################################################################################
#
#                                         Main Execution
#
####################################################################################################

# # Establish connection to Wayside shell
# green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_maintenance_switch_cmd.connect(read_maintenance_switches_handler)
# green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_sugg_speed.connect(read_sugg_speed_handler)
# green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_sugg_authority.connect(read_sugg_authority_handler)
# green_line_plc_3_shell_communicate.green_plc_3.green_line_plc_3_block_occupancy.connect(read_block_occupancy_handler)

# while True:

#     if maintenance_switch_check and sugg_speed_check and sugg_authority_check and block_occupancy_check:

#         # Update block occupancies
#         wayside.update_block_occupancies()

#         # Perform computations based on block occupancies
#         wayside.update_switch_cmd()
#         wayside.update_signal_cmd()
#         wayside.update_block_stop_go()
#         wayside.update_cmd_speed()
#         wayside.update_cmd_authority()
        
#         # Write commands to Wayside shell
#         write_to_wayside_shell()

#         # Reset checks
#         maintenance_switch_check = 0
#         sugg_speed_check = 0
#         sugg_authority_check = 0
#         block_occupancy_check = 0


