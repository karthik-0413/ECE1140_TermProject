# University of Pittsburgh
# Swanson School of Engineering
# ECE 1140: Systems and Project Engineering, Fall 2024
# Professor: Joseph A. Profeta III
# 
# Group 1
# Module:           Wayside Controller (Software)
# Program:          green_line_plc_2_shell_communicate
#
# Created:          11/10/2024
# Last Update:      11/11/2024
# Last Updated by:  Zachary McPherson
# Python Version:   3.12.6
# PyQt Version:     6.7.1
#
# Notes: This is the communicate file for the Wayside shell and plc program 2.
#        This program holds the pyqt signals used between the Wayside shell and green line plc program 2.

####################################################################################################
#
#                                               PLC Program 2
#
####################################################################################################

from PyQt6.QtCore import pyqtSignal, QObject

class green_line_plc_2(QObject):

    ###################################
    #     Inputs from CTC Office
    ###################################

    # Maintenance Switch Command
#    green_line_plc_2_maintenance_switch_cmd = pyqtSignal(list)

    # Suggested Speed
    green_line_plc_2_sugg_speed = pyqtSignal(list)

    # Suggested Authority
    green_line_plc_2_sugg_authority = pyqtSignal(list)

    ###################################
    #     Inputs from Track Model
    ###################################

    # Block occupancy
    green_line_plc_2_block_occupancy = pyqtSignal(list)

    ###################################
    #     Outputs to CTC Office
    ###################################

    # Block occupancies are passed from Wayside shell file

    ###################################
    #     Outputs to Track Model
    ###################################

    # Commanded Speed
    green_line_plc_2_cmd_speed = pyqtSignal(list)

    # Commanded Authority
    green_line_plc_2_cmd_authority = pyqtSignal(list)

    # Switch Command
    green_line_plc_2_switch_cmd = pyqtSignal(list)

    # Signal Command
    green_line_plc_2_signal_cmd = pyqtSignal(list)

    # Crossing Command
    green_line_plc_2_crossing_cmd = pyqtSignal(bool)

green_plc_2 = green_line_plc_2()