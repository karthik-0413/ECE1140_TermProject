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
# Last Update:      11/11/2024
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
#                                               Imports
#
####################################################################################################

# Communicate file
import green_line_plc_1_shell_communicate

####################################################################################################
#
#                                               Classes
#
####################################################################################################

# Wayside Class
class Wayside:
    
    ##################################
    #           Constructor
    ##################################

    # Default Constructor
    def __init__(self, sections):
        self.sec_array = sections
        self.DEF_direction = 0
        self.DEF_direction_update = 1
        self.DEF_occupancy = 0

    ##################################
    #           Methods
    ##################################

    # Update block occupancies
    def update_block_occupancies(self):

        # Define global variable
        global read_block_occupancies_array

        # Index to traverse input block occupancy array
        BlockArrayIndex = 0

        # Traverse through each section
        for i in range(len(self.sec_array)):
            
            # Traverse through each block in each section
            for j in range(len(self.sec_array[i].block_occupancy)):
                    
                # Update block occupancy
                self.sec_array[i].block_occupancy[j] = read_block_occupancies_array[BlockArrayIndex]

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

        # Define global variable
        global write_switch_cmd_array

        # Reset each block to go

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude section H
            if i != 7:

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
                        if j == 5: # Block 12

                            # Check if any trains are heading towards loop based on switch position
                            if write_switch_cmd_array[0] == 0:
                                self.sec_array[3].block_stop_go[0] = 0 # Block 13
                                self.sec_array[3].block_stop_go[1] = 0 # Block 14

                        elif j == 4: # block 11

                            # Check if any trains are heading towards loop based on switch position
                            if write_switch_cmd_array[0] == 0:
                                self.sec_array[3].block_stop_go[0] = 0 # Block 13

                            self.sec_array[2].block_stop_go[5] = 0 # Block 12

                        # Not edge block
                        elif j < 4: # Blocks 7 --> 10
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
                                self.sec_array[2].block_stop_go[1] = 0 # Block 14
                    
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
                            if self.sec_array[5].switch_cmd == 0:
                                self.sec_array[5].block_stop_go[7] = 0 # Block 28
                                self.sec_array[5].block_stop_go[6] = 0 # Block 27

                        elif j == 2: # block 30

                            # Check if any trains are heading towards loop based on occupancy
                            if self.sec_array[5].switch_cmd == 0: 
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
        if not write_switch_cmd_array[0]: # D -> C
            self.sec_array[0].block_stop_go[0] = 0 # Block 1
            self.sec_array[0].block_stop_go[1] = 0 # Block 2

        # Switch 2
        if not write_switch_cmd_array[1]: # F -> G
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

        # Define global variables
        global write_cmd_speed_array
        global read_sugg_speed_array

        # Index to traverse output suggested speed array
        BlockArrayIndex = 0
        
        # Check stop_go commands for each block

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude section H
            if i != 7:

                # Traverse each block in each section
                for j in range(len(self.sec_array[i].block_stop_go)):

                    # Block is commanding stop
                    if self.sec_array[i].block_stop_go[j] == 0:
                        write_cmd_speed_array[BlockArrayIndex] = 0

                    # Block is commanding go
                    else:
                        write_cmd_speed_array[BlockArrayIndex] = read_sugg_speed_array[BlockArrayIndex]
                    
                    # Increment index
                    BlockArrayIndex += 1

    # Update commanded authority of each block
    def update_cmd_authority(self):

        # Define global variable
        global write_cmd_authority_array
        global read_sugg_authority_array
        
        # Index to traverse output suggested authority array
        BlockArrayIndex = 0

        # Traverse each section
        for i in range(len(self.sec_array)):

            # Exclude section H
            if i != 7:

                # Traverse each block in each section
                for j in range(len(self.sec_array[i].block_stop_go)):

                    # Pass suggested authority
                    write_cmd_authority_array[BlockArrayIndex] = read_sugg_authority_array[BlockArrayIndex]

                    # Increment index
                    BlockArrayIndex += 1

    # Update switch commands
    def update_switch_cmd(self):

        # Define global variable
        global write_switch_cmd_array
        
        # Check if DEF needs new direction status
        if self.DEF_direction_update:

            # Check occupancy of sections A and Z

            # Train heading towards loop
            if self.sec_array[8].overall_occupancy:
                write_switch_cmd_array[0] = 0 # D -> C
                write_switch_cmd_array[1] = 1 # F <- Z

            # Train heading towards yard
            elif self.sec_array[0].overall_occupancy:
                write_switch_cmd_array[0] = 1 # D <- A
                write_switch_cmd_array[1] = 0 # F -> G

            # Default positions
            else:
                write_switch_cmd_array[0] = 0 # D -> C
                write_switch_cmd_array[1] = 1 # F <- Z

        # DEF direction is set
        else:

            # Check direction of DEF Sections

            # Train heading towards loop
            if self.DEF_direction:
                write_switch_cmd_array[0] = 0 # D -> C
                write_switch_cmd_array[1] = 1 # F <- Z
            
            # Train heading towards yard
            else:
                write_switch_cmd_array[0] = 1 # D <- A
                write_switch_cmd_array[1] = 0 # F -> G

    # Update signal commands
    def update_signal_cmd(self):

        # Define global variables
        global write_signal_cmd_array
        global write_switch_cmd_array
        
        # Check status of switch 1
        if write_switch_cmd_array[0]: # D <- A
            write_signal_cmd_array[0] = 1 # Section C
            write_signal_cmd_array[1] = 0 # Section D
        else:                         # D -> C 
            write_signal_cmd_array[0] = 0 # Section C
            write_signal_cmd_array[1] = 1 # Section D

        # Check status of switch 2
        if write_switch_cmd_array[1]: # F <- Z
            write_signal_cmd_array[2] = 0 # Section F
            write_signal_cmd_array[3] = 1 # Section G
        else:                         # F -> G
            write_signal_cmd_array[2] = 1 # Section F
            write_signal_cmd_array[3] = 0 # Section G

    # Update crossing command
    def update_crossing_cmd(self):
        
        # Define global variable
        global write_cross_cmd_array
        
        # Check section E occupancy
        if self.sec_array[4].overall_occupancy:
            write_cross_cmd_array[0] = 1
        else:
            write_cross_cmd_array[0] = 0

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
#                               Initial Sections with Default Path
#
####################################################################################################

# Sections
A = Section(3)
B = Section(3)
C = Section(6)
D = Section(4) # Direction matters
E = Section(4) # Direction matters
F = Section(8) # Direction matters
G = Section(4)
H = Section(3)
Z = Section(1)

# Wayside
wayside = Wayside([A, B, C, D, E, F, G, H, Z])

####################################################################################################
#
#                                          Read & Write Handler Functions
#
####################################################################################################

################################
#       CTC Office Inputs
################################

# Variables
read_maintenance_switch_array = [None] * 2
read_sugg_speed_array = [None] * 33
read_sugg_authority_array = [None] * 33
maintenance_switch_check = 0
sugg_speed_check = 0
sugg_authority_check = 0

# Functions
def read_maintenance_switches_handler(maintenance_switch_array):
    global read_maintenance_switch_array
    global maintenance_switch_check
    read_maintenance_switch_array = maintenance_switch_array
    maintenance_switch_check = 1

    

def read_sugg_speed_handler(sugg_speed_array):
    global read_sugg_speed_array
    global sugg_speed_check
    read_sugg_speed_array = sugg_speed_array
    sugg_speed_check = 1
    

def read_sugg_authority_handler(sugg_authority_array):
    global read_sugg_authority_array
    global sugg_authority_check
    read_sugg_authority_array = sugg_authority_array
    sugg_authority_check = 1


################################
#       TRK Model Inputs
################################

# Variables
read_block_occupancies_array = [0] * 36
block_occupancy_check = 0

# Functions
def read_block_occupancy_handler(block_occupancy_array):
    global read_block_occupancies_array
    global block_occupancy_check
    read_block_occupancies_array = block_occupancy_array
    block_occupancy_check = 1


################################
#       CTC Office Outputs
################################

# Block Occupancies are passed from Wayside shell file

################################
#       TRK Model Outputs
################################

# Variables
write_cmd_speed_array = [None] * 32
write_cmd_authority_array = [None] * 32
write_switch_cmd_array = [0, 1]
write_signal_cmd_array = [0, 1, 0, 1]
write_cross_cmd_array = [0]

####################################################################################################
#
#                                         Write Function
#
####################################################################################################

# Write to Wayside Shell
def write_to_wayside_shell():
    green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_cmd_speed.emit(write_cmd_speed_array)
    green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_cmd_authority.emit(write_cmd_authority_array)
    green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_switch_cmd.emit(write_switch_cmd_array)
    green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_signal_cmd.emit(write_signal_cmd_array)
    green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_crossing_cmd.emit(write_cross_cmd_array[0])

####################################################################################################
#
#                                         Main Execution
#
####################################################################################################

# Establish connection to Wayside shell
green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_maintenance_switch_cmd.connect(read_maintenance_switches_handler)
green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_sugg_speed.connect(read_sugg_speed_handler)
green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_sugg_authority.connect(read_sugg_authority_handler)
green_line_plc_1_shell_communicate.green_line_plc_1.green_line_plc_1_block_occupancy.connect(read_block_occupancy_handler)

while True:

    if maintenance_switch_check and sugg_speed_check and sugg_authority_check and block_occupancy_check:

        # Update block occupancies
        wayside.update_block_occupancies()

        # Perform computations based on block occupancies
        wayside.update_DEF_direction()
        wayside.update_switch_cmd()
        wayside.update_signal_cmd()
        wayside.update_crossing_cmd()
        wayside.update_block_stop_go()
        wayside.update_cmd_speed()
        wayside.update_cmd_authority()
        
        # Write commands to Wayside shell
        write_to_wayside_shell()

        # Reset checks
        maintenance_switch_check = 0
        sugg_speed_check = 0
        sugg_authority_check = 0
        block_occupancy_check = 0