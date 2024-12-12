# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module:           Wayside Controller (Software)
# PLC Program:      Green Line PLC 1
#
# Created:          12/08/2024
# Created by:       Zachary McPherson
#
# Last Update:      12/08/2024
# Last Updated by:  Zachary McPherson
#
# Python Version:   3.12.6
#
# Notes: This is file is used to set test values for the testing of the Wayside Controller
#        These functions will be used in the plc_unit_testing.py file


####################################################################################################
#
#                                    CTC Office and Track Model Outputs
#
####################################################################################################

################################
#          CTC Office
################################


################################
#        Track Model
################################

# Block occupancy
def seudo_track_model_occupancy_plc_1(indexies: list, occupancy_test_array: list):

    # Reset test array
    for i in range(len(occupancy_test_array)):
        occupancy_test_array[i] = False

    # Insert occupancies into test array
    for i in range(len(indexies)):
        occupancy_test_array[indexies[i]-1] = True

def seudo_track_model_occupancy_plc_2(indexies: list, occupancy_test_array: list):

    # Reset test array
    for i in range(len(occupancy_test_array)):
        occupancy_test_array[i] = False

    # Insert occupancies into test array
    for i in range(len(indexies)):
        if indexies[i] == 0:
            occupancy_test_array[indexies[i]] = True
        if 33 <= indexies[i] <= 76:
            occupancy_test_array[indexies[i]-32] = True
        if 105 <= indexies[i] <= 150:
            occupancy_test_array[indexies[i]-60] = True

def seudo_track_model_occupancy_plc_3(indexies: list, occupancy_test_array: list):

    # Reset test array
    for i in range(len(occupancy_test_array)):
        occupancy_test_array[i] = False

    # Insert occupancies into test array
    for i in range(len(indexies)):
        occupancy_test_array[indexies[i]-74] = True


    
    