# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module:           Wayside Controller (Software)
# PLC Program:      Green Line PLC 1
#
# Created:          10/19/2024
# Created by:       Zachary McPherson
#
# Last Update:      12/10/2024
# Last Updated by:  Zachary McPherson
#
# Python Version:   3.12.6
# PyQt Version:     6.7.1
#
# Notes: This is the PLC Program for the first wayside controller on the Green Line.
#        This program oversees sections A, B, C, D, E, F, G, and Z of the Green Line.
#        This program views the occupancies of section H
#        This program controls 2 switches and 1 crossing

####################################################################################################
#
#                                               Classes
#
####################################################################################################

# Wayside Class
class green_line_plc_1_class:
    
    ##################################
    #           Constructor
    ##################################

    # Default Constructor
    def __init__(self):

        # print("Green Line PLC 1 Initialized")

        self.DEF_direction = 0
        self.DEF_direction_update = 1
        self.DEF_occupancy = 0

        # Sections
        A = Section(3)
        B = Section(3)
        C = Section(7)
        D = Section(4) # Direction matters
        E = Section(4) # Direction matters
        F = Section(8) # Direction matters
        G = Section(4)
        H = Section(3)
        Z = Section(1)

        self.sec_array = [A, B, C, D, E, F, G, H, Z]

    ##################################
    #           Methods
    ##################################
    
    def green_plc_1_is_created(self):
        return True

    # Update block occupancies
    def update_block_occupancies(self):

        # OR Track Model occupancies with CTC maintence blocks
        self.read_block_occupancies_array = [a or b for a, b in zip(self.read_block_occupancies_array, self.read_maintenance_block_array)]

        # Index to traverse input block occupancy array
        BlockArrayIndex = 0

        # Traverse through each section
        for i in range(len(self.sec_array)):
            
            # Traverse through each block in each section
            for j in range(len(self.sec_array[i].block_occupancy)):
                
                # Check if section C, block 151
                if i == 2 and j == 0:
                    self.sec_array[2].block_occupancy[0] = self.read_block_occupancies_array[36]
                
                # Check every other block
                else:
                    
                    # Update block occupancy
                    self.sec_array[i].block_occupancy[j] = self.read_block_occupancies_array[BlockArrayIndex]

                    # Increment index
                    BlockArrayIndex += 1
        
            # Update overall occupancy of section
            self.sec_array[i].update_section_occupancy()

        # Update overall occupancy of DEF sections
        if self.sec_array[3].overall_occupancy or self.sec_array[4].overall_occupancy or self.sec_array[5].overall_occupancy:
            self.DEF_occupancy = 1
        else:
            self.DEF_occupancy = 0

    # Update stop/go command for each block
    def update_block_stop_go(self):

        # Reset each block to go

        # Traverse each section
        for i in range(len(self.sec_array)):
                
            # Traverse through each block in each section
            for j in range(len(self.sec_array[i].block_stop_go)):
                self.sec_array[i].block_stop_go[j] = 1

        # Check for block occupancies

        # Traverse each section for occupancies
        for i in range(len(self.sec_array) - 1):
            
            # Traverse each block in each section
            for j in range(len(self.sec_array[i].block_occupancy)):

                # Check if block is occupied
                if self.sec_array[i].block_occupancy[j] == 1:

                    # Check which section the block is in
                    # Section A
                    if i == 0:

                        # Check if block is edge block
                        if j == 2: # Block 3
                            self.sec_array[1].block_stop_go[0] = 0 # Block 4
                            self.sec_array[1].block_stop_go[1] = 0 # Block 5

                        # Not edge block
                        elif j == 0: # Block 1
                            self.sec_array[0].block_stop_go[1] = 0 # Block 2
                            self.sec_array[0].block_stop_go[2] = 0 # Block 3

                        elif j == 1: # Block 2
                            self.sec_array[0].block_stop_go[2] = 0 # Block 3
                            self.sec_array[1].block_stop_go[0] = 0 # Block 4
                    
                    # Section B
                    elif i == 1:

                        # Check if block is edge block
                        if j == 2: # Block 6
                            self.sec_array[2].block_stop_go[0] = 0 # Block 7
                            self.sec_array[2].block_stop_go[1] = 0 # Block 8

                        # Not edge block
                        elif j == 0: # Block 4
                            self.sec_array[1].block_stop_go[1] = 0 # Block 5
                            self.sec_array[1].block_stop_go[2] = 0 # Block 6
                        
                        elif j == 1: # Block 5
                            self.sec_array[1].block_stop_go[2] = 0 # Block 6
                            self.sec_array[2].block_stop_go[0] = 0 # Block 7

                    # Section C
                    elif i == 2:

                        # Check if block is edge block
                        if j == 6: # Block 12

                            # Check if any trains are heading towards loop based on switch position
                            if self.write_switch_cmd_array[0] == 0:
                                self.sec_array[3].block_stop_go[0] = 0 # Block 13
                                self.sec_array[3].block_stop_go[1] = 0 # Block 14

                        elif j == 5: # block 11

                            # Check if any trains are heading towards loop based on switch position
                            if self.write_switch_cmd_array[0] == 0:
                                self.sec_array[3].block_stop_go[0] = 0 # Block 13

                            self.sec_array[2].block_stop_go[6] = 0 # Block 12

                        # Not edge block
                        elif j < 5: # Blocks 151 --> 10
                            self.sec_array[2].block_stop_go[j + 1] = 0
                            self.sec_array[2].block_stop_go[j + 2] = 0

                    # Section D
                    elif i == 3:

                        # Check each block
                        if j == 0: # Block 13

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[3].block_stop_go[1] = 0 # Block 14
                                self.sec_array[3].block_stop_go[2] = 0 # Block 15
                            else:                  # Moving left, away from loop
                                self.sec_array[0].block_stop_go[0] = 0 # Block 1
                                self.sec_array[0].block_stop_go[1] = 0 # Block 2

                        elif j == 1: # Block 14

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[3].block_stop_go[2] = 0 # Block 15
                                self.sec_array[3].block_stop_go[3] = 0 # Block 16
                            else:                  # Moving left, away from loop
                                self.sec_array[3].block_stop_go[0] = 0 # Block 13
                                self.sec_array[0].block_stop_go[0] = 0 # Block 1

                        elif j == 2: # Block 15

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[3].block_stop_go[3] = 0 # Block 16
                                self.sec_array[4].block_stop_go[0] = 0 # Block 17
                            else:                  # Moving left, away from loop
                                self.sec_array[3].block_stop_go[0] = 0 # Block 13
                                self.sec_array[3].block_stop_go[1] = 0 # Block 14
                        
                        elif j == 3: # Block 16

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[4].block_stop_go[0] = 0 # Block 17
                                self.sec_array[4].block_stop_go[1] = 0 # Block 18
                            else:                 # Moving left, away from loop
                                self.sec_array[3].block_stop_go[2] = 0 # Block 15
                                self.sec_array[3].block_stop_go[1] = 0 # Block 14
                    
                    # Section E
                    elif i == 4:

                        # Check each block
                        if j == 0: # Block 17

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[4].block_stop_go[1] = 0 # Block 18
                                self.sec_array[4].block_stop_go[2] = 0 # Block 19
                            else:                  # Moving left, away from loop
                                self.sec_array[3].block_stop_go[3] = 0 # Block 16
                                self.sec_array[3].block_stop_go[2] = 0 # Block 15

                        elif j == 1: # Block 18

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[4].block_stop_go[2] = 0 # Block 19
                                self.sec_array[4].block_stop_go[3] = 0 # Block 20
                            else:                  # Moving left, away from loop
                                self.sec_array[4].block_stop_go[0] = 0 # Block 17
                                self.sec_array[3].block_stop_go[3] = 0 # Block 16

                        elif j == 2: # Block 19

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[4].block_stop_go[3] = 0 # Block 20
                                self.sec_array[5].block_stop_go[0] = 0 # Block 21
                            else:                  # Moving left, away from loop
                                self.sec_array[4].block_stop_go[1] = 0 # Block 18
                                self.sec_array[4].block_stop_go[0] = 0 # Block 17
                        
                        elif j == 3: # Block 20

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[5].block_stop_go[0] = 0 # Block 21
                                self.sec_array[5].block_stop_go[1] = 0 # Block 22
                            else:                  # Moving left, away from loop
                                self.sec_array[4].block_stop_go[2] = 0 # Block 19
                                self.sec_array[4].block_stop_go[1] = 0 # Block 18

                    # Section F
                    elif i ==5:

                        # Check if block is edge block
                        if j == 0: # Block 21
                            
                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[5].block_stop_go[1] = 0 # Block 22
                                self.sec_array[5].block_stop_go[2] = 0 # Block 23
                            else:                  # Moving left, away from loop
                                self.sec_array[4].block_stop_go[3] = 0 # Block 20
                                self.sec_array[4].block_stop_go[2] = 0 # Block 19

                        elif j == 1: # Block 22

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[5].block_stop_go[2] = 0 # Block 23
                                self.sec_array[5].block_stop_go[3] = 0 # Block 24
                            else:                  # Moving left, away from loop
                                self.sec_array[5].block_stop_go[0] = 0 # Block 21
                                self.sec_array[4].block_stop_go[3] = 0 # Block 20

                        elif j == 7: # Block 28

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[8].block_stop_go[0] = 0 # Block 150
                            else:                  # Moving left, away from loop
                                self.sec_array[5].block_stop_go[6] = 0 # Block 27
                                self.sec_array[5].block_stop_go[5] = 0 # Block 26

                        elif j == 6: # Block 27

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[5].block_stop_go[7] = 0 # Block 28
                                self.sec_array[8].block_stop_go[0] = 0 # Block 150
                            else:                  # Moving left, away from loop
                                self.sec_array[5].block_stop_go[5] = 0 # Block 26
                                self.sec_array[5].block_stop_go[4] = 0 # Block 15

                        # Not edge block
                        elif 1 < j < 6: # Blocks 23 --> 26

                            # Check direction of DEF Sections
                            if self.DEF_direction: # Moving right, towards loop
                                self.sec_array[5].block_stop_go[j + 1] = 0
                                self.sec_array[5].block_stop_go[j + 2] = 0
                            else:                  # Moving left, away from loop
                                self.sec_array[5].block_stop_go[j - 1] = 0
                                self.sec_array[5].block_stop_go[j - 2] = 0

                    # Section G
                    elif i == 6:

                        # Check if block is edge block
                        if j == 0: # Block 29

                            # Check if any trains are heading away from loop based on occupancy
                            if self.write_switch_cmd_array[1] == 0:
                                self.sec_array[5].block_stop_go[7] = 0 # Block 28
                                self.sec_array[5].block_stop_go[6] = 0 # Block 27

                        elif j == 1: # block 30

                            # Check if any trains are heading towards loop based on occupancy
                            if self.write_signal_cmd_array[0] == 1: 
                                self.sec_array[5].block_stop_go[7] = 0 # Block 28

                            self.sec_array[6].block_stop_go[0] = 0 # Block 29

                        # Not edge block
                        elif j > 1: # Blocks 31 --> 32
                            self.sec_array[6].block_stop_go[j - 1] = 0
                            self.sec_array[6].block_stop_go[j - 2] = 0

                    # Section H
                    elif i == 7:

                        # Check first two blocks
                        if j == 0: # Block 33
                            self.sec_array[6].block_stop_go[3] = 0 # Block 32
                            self.sec_array[6].block_stop_go[2] = 0 # Block 21

                        elif j == 1: # Block 34
                            self.sec_array[6].block_stop_go[3] = 0 # Block 32

        # Check switch positions
        # Switch 1
        if not self.write_switch_cmd_array[0]: # D -> C
            self.sec_array[0].block_stop_go[0] = 0 # Block 1
            self.sec_array[0].block_stop_go[1] = 0 # Block 2

        # Switch 2
        if not self.write_switch_cmd_array[1]: # F -> G
            self.sec_array[8].block_stop_go[0] = 0 # Block 150              
                                
    # Update overall direction of sections D, E, F                            
    def update_DEF_direction(self):
        
        # Check if any blocks in DEF are occupied
        if self.DEF_occupancy:
            
            # Find new direction
            # Away from loop
            if self.sec_array[3].block_occupancy[0]:
                
                # Check if direction is already set
                if self.DEF_direction_update:
                    self.DEF_direction = 0
                    self.DEF_direction_update = 0
            
            # Towards loop
            elif self.sec_array[5].block_occupancy[7]:

                # Check if direction is already set
                if self.DEF_direction_update:
                    self.DEF_direction = 1
                    self.DEF_direction_update = 0

        # Direction is ready to be updated
        else:
            self.DEF_direction_update = 1

    # Update commanded speed of each block
    def update_cmd_speed(self):

        # Index to traverse output suggested speed array
        BlockArrayIndex = 0
        
        # Check stop_go commands for each block

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude section H
            if i != 7:

                # Traverse each block in each section
                for j in range(len(self.sec_array[i].block_stop_go)):

                    # Check for section C, block 151
                    if i == 2 and j == 0:
                        if self.sec_array[2].block_stop_go[0] == 0:
                            self.write_cmd_speed_array[33] = 0
                        else:
                            self.write_cmd_speed_array[33] = self.read_sugg_speed_array[33]
                    else:

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
        for i in range(len(self.sec_array)):

            # Exclude section H
            if i != 7:

                # Traverse each block in each section
                for j in range(len(self.sec_array[i].block_stop_go)):

                    # Check for section C, block 151
                    if i == 2 and j == 0:
                        self.write_cmd_authority_array[33] = self.read_sugg_authority_array[33]
                    else:

                        # Pass suggested authority
                        self.write_cmd_authority_array[BlockArrayIndex] = self.read_sugg_authority_array[BlockArrayIndex]

                        # Increment index
                        BlockArrayIndex += 1

    # Update switch commands
    def update_switch_cmd(self):
        
        # Check if DEF needs new direction status
        if self.DEF_direction_update:

            # Check occupancy of sections A and Z

            # Train heading towards loop
            if self.sec_array[8].overall_occupancy:
                self.write_switch_cmd_array[0] = 0 # D -> C
                self.write_switch_cmd_array[1] = 1 # F <- Z

            # Train heading towards yard
            elif self.sec_array[0].overall_occupancy:
                self.write_switch_cmd_array[0] = 1 # D <- A
                self.write_switch_cmd_array[1] = 0 # F -> G

            # Default positions
            else:
                self.write_switch_cmd_array[0] = 0 # D -> C
                self.write_switch_cmd_array[1] = 1 # F <- Z

        # DEF direction is set
        else:

            # Check direction of DEF Sections

            # Train heading towards loop
            if self.DEF_direction:
                self.write_switch_cmd_array[0] = 0 # D -> C
                self.write_switch_cmd_array[1] = 1 # F <- Z
            
            # Train heading towards yard
            else:
                self.write_switch_cmd_array[0] = 1 # D <- A
                self.write_switch_cmd_array[1] = 0 # F -> G

        # Switch D maintenance
        if self.read_block_occupancies_array[12] and self.read_block_occupancies_array[11] and self.read_block_occupancies_array[0]:
            self.write_switch_cmd_array[0] = self.read_maintenance_switch_array[0]
        
        # Switch F maintenance
        if self.read_block_occupancies_array[35] and self.read_block_occupancies_array[27] and self.read_block_occupancies_array[28]:
            self.write_switch_cmd_array[1] = self.read_maintenance_switch_array[1]

    # Update signal commands
    def update_signal_cmd(self):
        
        # Check status of switch 1
        if self.write_switch_cmd_array[0]: # D <- A
            self.write_signal_cmd_array[0] = 1 # Section C
            self.write_signal_cmd_array[1] = 0 # Section D
        else:                         # D -> C 
            self.write_signal_cmd_array[0] = 0 # Section C
            self.write_signal_cmd_array[1] = 1 # Section D

        # Check status of switch 2
        if self.write_switch_cmd_array[1]: # F <- Z
            self.write_signal_cmd_array[2] = 0 # Section F
            self.write_signal_cmd_array[3] = 1 # Section G
        else:                         # F -> G
            self.write_signal_cmd_array[2] = 1 # Section F
            self.write_signal_cmd_array[3] = 0 # Section G

    # Update crossing command
    def update_crossing_cmd(self):
        print('Section E Overall Occ:', self.sec_array[4].overall_occupancy)
        # Check section E occupancy
        if self.sec_array[4].overall_occupancy:
            print('in crossing if statement')
            self.write_cross_cmd_array[0] = 1
        else:
            self.write_cross_cmd_array[0] = 0


    ####################################################################################################
    #
    #                                          Read & Write Handler Functions
    #
    ####################################################################################################

    ################################
    #       CTC Office Inputs
    ################################

    # Variables
    read_maintenance_block_array = [0] * 37
    read_maintenance_switch_array = [None] * 2
    read_sugg_speed_array = [None] * 34
    read_sugg_authority_array = [None] * 34
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
            self.update_DEF_direction()
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
        self.read_maintenance_switch_array[0] = not self.read_maintenance_switch_array[0]
        self.maintenance_switch_check = 1

        # Check if all handlers have been called
        if self.sugg_speed_check and self.sugg_authority_check and self.block_occupancy_check and self.maintenance_switch_check and self.maintenance_block_check:

            # Update block occupancies
            self.update_block_occupancies()

            # Perform computations based on block occupancies
            self.update_DEF_direction()
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
            self.update_DEF_direction()
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
            self.update_DEF_direction()
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
    read_block_occupancies_array = [0] * 37
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
            self.update_DEF_direction()
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
    write_cmd_speed_array = [None] * 34
    write_cmd_authority_array = [None] * 34
    write_switch_cmd_array = [0, 1]
    write_signal_cmd_array = [0, 1, 0, 1]
    write_cross_cmd_array = [0]

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

        # Reset overall occupancy
        self.overall_occupancy = 0
        
        # Check if any blocks are occupied
        for i in range(len(self.block_occupancy)):
            if self.block_occupancy[i]:
                self.overall_occupancy = 1
                break





