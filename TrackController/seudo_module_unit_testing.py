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

# Sugg Speed
def seudo_ctc_sugg_speed_plc_1(indexies: list, sugg_speeds: list, speed_test_array: list):

    # Reset test array
    for i in range(len(speed_test_array)):
        speed_test_array[i] = None

    # Insert sugg speeds into test array
    for i in range(len(indexies)):
        speed_test_array[indexies[i]-1] = sugg_speeds[i]

# Sugg authority
def seudo_ctc_sugg_authority_plc_1(indexies: list, sugg_authoritys: list, authority_test_array: list):

    # Reset test array
    for i in range(len(authority_test_array)):
        authority_test_array[i] = None

    # Insert sugg speeds into test array
    for i in range(len(indexies)):
        authority_test_array[indexies[i]-1] = sugg_authoritys[i]

################################
#        Track Model
################################

# Block occupancy
def seudo_track_model_occupancy_plc_1(indexies: list, occupancy_test_array: list):

    # Reset test array
    for i in range(len(occupancy_test_array)):
        occupancy_test_array[i] = False

    # Insert sugg speeds into test array
    for i in range(len(indexies)):
        occupancy_test_array[indexies[i]-1] = True
