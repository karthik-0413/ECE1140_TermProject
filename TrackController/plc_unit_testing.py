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
# Notes: This is the main unit testing file for the PLC programs of the Wayside Controller
#        This file will test the PLC programs of the Green Line


####################################################################################################
#
#                              Import Unit Test Library and PLC Programs
#
####################################################################################################

# System Libraries
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Unit Test Library
import unittest

# Testing functions
from TrackController import seudo_module_unit_testing

# PLC Program 1
from TrackController.green_1_to_be_reviewed import green_line_plc_1_class

# PLC Program 2
from TrackController.green_2_to_be_reviewed import green_line_plc_2_class

# PLC Program 3
from TrackController.green_3_to_be_reviewed import green_line_plc_3_class

####################################################################################################
#
#                                      Extra Functions
#
####################################################################################################

def call_plc_1_handlers(plc_program_1: green_line_plc_1_class, sugg_speed_test_array: list, sugg_authority_test_array: list, occupancy_test_array: list):

    # Call plc handlers
    plc_program_1.read_sugg_speed_handler(sugg_speed_test_array)
    plc_program_1.read_sugg_authority_handler(sugg_authority_test_array)
    plc_program_1.read_block_occupancy_handler(occupancy_test_array)

def call_plc_2_handlers(plc_program_2: green_line_plc_2_class, sugg_speed_test_array: list, sugg_authority_test_array: list, occupancy_test_array: list):

    # Call plc handlers
    plc_program_2.read_sugg_speed_handler(sugg_speed_test_array)
    plc_program_2.read_sugg_authority_handler(sugg_authority_test_array)
    plc_program_2.read_block_occupancy_handler(occupancy_test_array)


####################################################################################################
#
#                                      PLC Program 1 Test Cases
#
####################################################################################################

# Receive occupancies test cases
class test_section_A_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([1, 2, 3], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section A occupancies
        self.assertTrue(self.plc_program_1.sec_array[0].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[0].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[0].block_occupancy[2])

class test_section_B_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([4, 5, 6], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section B occupancies
        self.assertTrue(self.plc_program_1.sec_array[1].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[1].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[1].block_occupancy[2])

class test_section_C_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([37, 7, 8, 9, 10, 11, 12], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section occupancies
        self.assertTrue(self.plc_program_1.sec_array[2].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[2].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[2].block_occupancy[2])
        self.assertTrue(self.plc_program_1.sec_array[2].block_occupancy[3])
        self.assertTrue(self.plc_program_1.sec_array[2].block_occupancy[4])
        self.assertTrue(self.plc_program_1.sec_array[2].block_occupancy[5])
        self.assertTrue(self.plc_program_1.sec_array[2].block_occupancy[6])
        
class test_section_D_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([13, 14, 15, 16], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section occupancies
        self.assertTrue(self.plc_program_1.sec_array[3].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[3].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[3].block_occupancy[2])
        self.assertTrue(self.plc_program_1.sec_array[3].block_occupancy[3])

class test_section_E_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([17, 18, 19, 20], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section occupancies
        self.assertTrue(self.plc_program_1.sec_array[4].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[4].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[4].block_occupancy[2])
        self.assertTrue(self.plc_program_1.sec_array[4].block_occupancy[3])

class test_section_F_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([21, 22, 23, 24, 25, 26, 27, 28], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section occupancies
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[2])
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[3])
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[4])
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[5])
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[6])
        self.assertTrue(self.plc_program_1.sec_array[5].block_occupancy[7])

class test_section_G_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([29, 30, 31, 32], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section occupancies
        self.assertTrue(self.plc_program_1.sec_array[6].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[6].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[6].block_occupancy[2])
        self.assertTrue(self.plc_program_1.sec_array[6].block_occupancy[3])
        
class test_section_H_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([33, 34, 35], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section occupancies
        self.assertTrue(self.plc_program_1.sec_array[7].block_occupancy[0])
        self.assertTrue(self.plc_program_1.sec_array[7].block_occupancy[1])
        self.assertTrue(self.plc_program_1.sec_array[7].block_occupancy[2])

class test_section_Z_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check section occupancies
        self.assertTrue(self.plc_program_1.sec_array[8].block_occupancy[0])

# Receive sugg speed and sugg authority test case
class test_receive_sugg_speed_and_authority(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass sugg speeds to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        self.plc_program_1.read_sugg_speed_handler(self.sugg_speed_test_array)
        self.plc_program_1.read_sugg_authority_handler(self.sugg_authority_test_array)
        self.plc_program_1.read_block_occupancy_handler(self.occupancy_test_array)

        # Check sugg speed and authority
        for i in range(len(self.sugg_speed_test_array)):
            self.assertEqual(self.plc_program_1.read_sugg_speed_array[i], 50)
            self.assertEqual(self.plc_program_1.read_sugg_authority_array[i], 100)

# Set DEF direction test cases
class test_set_def_direction_Z_to_C(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # No trains
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.DEF_occupancy)
        self.assertFalse(self.plc_program_1.DEF_direction)
        self.assertTrue(self.plc_program_1.DEF_direction_update)

        # Train enters wayside at section Z
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.DEF_occupancy)
        self.assertFalse(self.plc_program_1.DEF_direction)
        self.assertTrue(self.plc_program_1.DEF_direction_update)

        # Train travels from block 28 to 13
        for block in [28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertTrue(self.plc_program_1.DEF_occupancy)
            self.assertTrue(self.plc_program_1.DEF_direction)
            self.assertFalse(self.plc_program_1.DEF_direction_update)

        # Train enters block 12
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.DEF_occupancy)
        self.assertTrue(self.plc_program_1.DEF_direction)
        self.assertTrue(self.plc_program_1.DEF_direction_update)

class test_set_def_direction_A_to_G(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # No trains
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.DEF_occupancy)
        self.assertFalse(self.plc_program_1.DEF_direction)
        self.assertTrue(self.plc_program_1.DEF_direction_update)

        # Train enters wayside at section A
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.DEF_occupancy)
        self.assertFalse(self.plc_program_1.DEF_direction)
        self.assertTrue(self.plc_program_1.DEF_direction_update)

        # Train travels from block 13 to 28
        for block in [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertTrue(self.plc_program_1.DEF_occupancy)
            self.assertFalse(self.plc_program_1.DEF_direction)
            self.assertFalse(self.plc_program_1.DEF_direction_update)

        # Train enters block 29
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.DEF_occupancy)
        self.assertFalse(self.plc_program_1.DEF_direction)
        self.assertTrue(self.plc_program_1.DEF_direction_update)
        
# Set Switch and Signal Commands test cases
class test_default_switch_commands(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # No trains
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

class test_train_at_section_Z_switch_commands(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train enters wayside at section Z
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

class test_switch_commands_Z_to_C(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train enters wayside at section Z
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

        # Train travels from block 28 to 13
        for block in [28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

        # Train enters block 12
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

class test_train_at_section_A_switch_commands(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train enters wayside at section A
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [1, 0])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [1, 0, 1, 0])

class test_switch_commands_A_to_G(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train enters wayside at section Z
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [1, 0])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [1, 0, 1, 0])
        # Train travels from block 28 to 13
        for block in [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [1, 0])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [1, 0, 1, 0])

        # Train enters block 12
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

class test_switch_commands_Z_to_G(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train enters wayside at section Z
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

        # Train travels from block 28 to 13
        for block in [28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

        # Train travels from block 12 to 4
        for block in [12, 11, 10, 9, 8, 7, 37, 6, 5, 4]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])
        
        # Train travels from block 3 to 28
        for block in [3, 2, 1, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [1, 0])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [1, 0, 1, 0])

        # Train enters block 29
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([29], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

class test_switch_commands_train_waiting_at_Z(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train travels from block 3 to 20
        for block in [3, 2, 1, 13, 14, 15, 16, 17, 18, 19, 20]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [1, 0])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [1, 0, 1, 0])

        # Another train enters section Z
        for block in [21, 22, 23, 24, 25, 26, 27, 28]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block, 36], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [1, 0])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [1, 0, 1, 0])
        
        # first train enters section G
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([29, 36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

class test_switch_commands_train_waiting_at_A(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train travels from block 150 to 21
        for block in [36, 28, 27, 26, 25, 24, 23, 22, 21]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

        # Another train enters section A
        for block in [20, 19, 18, 17, 16, 15, 14, 13]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block, 1], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
            self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])
        
        # first train enters section C
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12, 1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [1, 0])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [1, 0, 1, 0])

class test_switch_commands_trains_waiting_at_Z_and_A(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Trains waiting at 150 and 1
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36, 1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_switch_cmd_array, [0, 1])
        self.assertEqual(self.plc_program_1.write_signal_cmd_array, [0, 1, 0, 1])

# Set crossing commands test cases
class test_crossing_commands_train_in_E(unittest.TestCase):
    
    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # No train
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.write_cross_cmd_array[0])

        # Train in section E
        for block in [17, 18, 19, 20]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertTrue(self.plc_program_1.write_cross_cmd_array[0])

class test_crossing_commands_train_everywhere_but_E(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [None] * 34
        self.sugg_authority_test_array = [None] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train everywhere but E
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([17, 18, 19, 20], self.occupancy_test_array)
        self.occupancy_test_array = [x ^ 1 for x in self.occupancy_test_array]
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.write_cross_cmd_array[0])

# Set block-stop-go commands, Commanded Speed, and Commanded Authority test cases
class test_block_stop_go_commands_train_Z_to_C(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # No trains
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters wayside at section Z
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 28
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([28], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 32:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 27
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([27], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 7:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 32 or i == 27:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 26
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([26], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 7:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 6:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 26 or i == 27:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 25
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([25], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 6:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 5:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 25 or i == 26:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 24
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([24], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 5:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 4:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 24 or i == 25:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 23
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([23], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 4:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 23 or i == 24:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 22
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([22], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 22 or i == 23:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 21
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([21], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 21 or i == 22:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 20
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([20], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 20 or i == 21:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 19
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([19], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 19 or i == 20:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 18
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([18], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 18 or i == 19:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 17
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([17], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 17 or i == 18:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 16
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([16], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 16 or i == 17:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 15
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([15], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 15 or i == 16:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 14
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([14], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 14 or i == 15:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 13
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([13], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 13 or i == 14:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 12
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 12 or i == 13:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 11
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([11], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 2 and block == 6:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 11 or i == 12:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)
        
class test_block_stop_go_commands_train_C_to_D(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train travels from block 12 to block 13
        for train_block in [12, 11, 10, 9, 8, 7, 37, 6, 5, 4, 3, 2, 1, 13]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([train_block], self.occupancy_test_array)
            call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            
            if train_block == 12:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[3].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[3].block_stop_go[1])
            elif train_block == 11:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[3].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[6])
            elif train_block == 10:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[6])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[5])
            elif train_block == 9:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[5])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[4])
            elif train_block == 8:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[4])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[3])
            elif train_block == 7:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[3])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[2])
            elif train_block == 37:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[2])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[1])
            elif train_block == 6:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[0])
            elif train_block == 5:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[2].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[1].block_stop_go[2])
            elif train_block == 4:
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[1].block_stop_go[2])
                self.assertFalse(self.plc_program_1.sec_array[1].block_stop_go[1])
            elif train_block == 3:
                self.assertFalse(self.plc_program_1.sec_array[8].block_stop_go[0])
                self.assertTrue(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertTrue(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[1].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[1].block_stop_go[0])
            elif train_block == 2:
                self.assertFalse(self.plc_program_1.sec_array[8].block_stop_go[0])
                self.assertTrue(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertTrue(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[1].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[2])
            elif train_block == 1:
                self.assertFalse(self.plc_program_1.sec_array[8].block_stop_go[0])
                self.assertTrue(self.plc_program_1.sec_array[0].block_stop_go[0])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[2])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
            elif train_block == 13:
                self.assertFalse(self.plc_program_1.sec_array[8].block_stop_go[0])
                self.assertTrue(self.plc_program_1.sec_array[0].block_stop_go[2])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[1])
                self.assertFalse(self.plc_program_1.sec_array[0].block_stop_go[0])

            if train_block == 12:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 11:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 10:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 9:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 8:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 7:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 37:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == 6 or i == 7:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 6:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == 33 or i == train_block:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 5:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == 33:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 4:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 3:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 32 or i == train_block or i == train_block+1:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 2:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 32 or i == 2 or i == 3:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 1:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 32 or i == 1 or i == 2:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            elif train_block == 13:
                for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
                    if i == 0 or i == 1 or i == 32:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
                    else:
                        self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
            
            for auth in self.plc_program_1.write_cmd_authority_array:
                self.assertEqual(auth, 100)

class test_block_stop_go_commands_train_A_to_H(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # No trains
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])

        # Train enters wayside at section A
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 0 and (block == 1 or block == 2):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 1 or i == 2:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 13
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([13], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 0 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 0 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 0 or i == 1:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 14
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([14], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 0 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 12 or i == 0:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 15
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([15], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 13 or i == 12:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 16
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([16], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 14 or i == 13:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 17
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([17], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 15 or i == 14:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 18
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([18], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 3 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 16 or i == 15:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 19
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([19], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 17 or i == 16:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 20
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([20], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 18 or i == 17:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 21
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([21], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 19 or i == 18:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 22
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([22], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 4 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 20 or i == 19:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 23
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([23], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 21 or i == 20:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 24
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([24], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 22 or i == 21:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 25
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([25], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 23 or i == 22:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 26
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([26], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 4:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 24 or i == 23:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 27
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([27], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 4:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 5:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 25 or i == 24:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 28
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([28], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 8 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 5:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 5 and block == 6:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 32 or i == 26 or i == 25:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 29
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([29], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 30
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([30], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 28:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 31
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([31], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 0:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 29 or i == 28:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 32
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([32], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 1:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 30 or i == 29:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 33
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([33], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 2:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 31 or i == 30:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # Train enters block 34
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([34], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        for sec in range(len(self.plc_program_1.sec_array)):
            for block in range(len(self.plc_program_1.sec_array[sec].block_stop_go)):
                if sec == 0 and (block == 0 or block == 1):
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                elif sec == 6 and block == 3:
                    self.assertFalse(self.plc_program_1.sec_array[sec].block_stop_go[block])
                else:
                    self.assertTrue(self.plc_program_1.sec_array[sec].block_stop_go[block])
        for i in range(self.plc_program_1.write_cmd_speed_array.__len__()):
            if i == 0 or i == 1 or i == 31:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 0)
            else:
                self.assertEqual(self.plc_program_1.write_cmd_speed_array[i], 50)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

class test_block_stop_go_commands_multiple_trains_Z_to_C(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass values to plc programs
    def test_passing_values_to_plc(self):

        # Train enters block 150
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Train enters block 28
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([28], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Train enters block 20 and another train enters block 150
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([20, 36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # First train enters block 12 and second train enters block 22
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12, 22], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.sec_array[3].block_stop_go[0])
        self.assertFalse(self.plc_program_1.sec_array[3].block_stop_go[1])
        self.assertFalse(self.plc_program_1.sec_array[5].block_stop_go[2])
        self.assertFalse(self.plc_program_1.sec_array[5].block_stop_go[3])
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[12], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[13], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[22], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[23], 0)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)
        
class test_block_stop_go_commands_multiple_trains_A_to_G(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass values to plc programs
    def test_passing_values_to_plc(self):

        # Train enters block 1
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Train enters block 13
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([13], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Train enters block 16 and another train enters block 1
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([16, 1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # First train enters block 29 and second train enters block 20
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([29, 20], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.sec_array[8].block_stop_go[0])
        self.assertFalse(self.plc_program_1.sec_array[5].block_stop_go[7])
        self.assertFalse(self.plc_program_1.sec_array[5].block_stop_go[6])
        self.assertFalse(self.plc_program_1.sec_array[4].block_stop_go[1])
        self.assertFalse(self.plc_program_1.sec_array[4].block_stop_go[2])
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[27], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[26], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[18], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[17], 0)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

        # First train enters block 30 and second train enters block 23
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([30, 23], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_1.sec_array[8].block_stop_go[0])
        self.assertFalse(self.plc_program_1.sec_array[6].block_stop_go[0])
        self.assertFalse(self.plc_program_1.sec_array[5].block_stop_go[7])
        self.assertFalse(self.plc_program_1.sec_array[5].block_stop_go[1])
        self.assertFalse(self.plc_program_1.sec_array[5].block_stop_go[0])
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[28], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[27], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[21], 0)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[20], 0)
        for auth in self.plc_program_1.write_cmd_authority_array:
            self.assertEqual(auth, 100)

class test_block_stop_go_commands_train_waiting_at_A(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass values to plc programs
    def test_passing_values_to_plc(self):

        # No trains
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Train enters block 150
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        

        # Train enters block 20 and another train enters block 1
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([20, 1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        
        # First train enters block 12
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([12, 1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[12], 50)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[13], 50)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[0], 50)

class test_block_stop_go_commands_train_waiting_at_Z(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 37
        self.sugg_speed_test_array = [50] * 34
        self.sugg_authority_test_array = [100] * 34

        # PLC Object
        self.plc_program_1 = green_line_plc_1_class()

    # Pass values to plc programs
    def test_passing_values_to_plc(self):

        # No trains
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Train enters block 1
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([1], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Train enters block 20 and another train enters block 150
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([20, 36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        
        # First train enters block 29
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_1([29, 36], self.occupancy_test_array)
        call_plc_1_handlers(self.plc_program_1, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[27], 50)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[26], 50)
        self.assertEqual(self.plc_program_1.write_cmd_speed_array[32], 50)


####################################################################################################
#
#                                      PLC Program 2 Test Cases
#
####################################################################################################

# Receive occupancies test cases
class test_section_H_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2([33, 34, 35], self.occupancy_test_array)

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section H occupancies
        self.assertTrue(self.plc_program_2.sec_array[0].block_occupancy[0])
        self.assertTrue(self.plc_program_2.sec_array[0].block_occupancy[1])
        self.assertTrue(self.plc_program_2.sec_array[0].block_occupancy[2])

class test_section_I_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(36, 58)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section I occupancies
        for block in self.plc_program_2.sec_array[1].block_occupancy:
            self.assertTrue(block)

class test_section_Yard_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2([0], self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section I occupancies
        self.assertTrue(self.plc_program_2.yard_occupancy)

class test_section_J_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(58, 63)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section J occupancies
        for block in self.plc_program_2.sec_array[2].block_occupancy:
            self.assertTrue(block)

class test_section_K_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(63, 69)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section K occupancies
        for block in self.plc_program_2.sec_array[3].block_occupancy:
            self.assertTrue(block)

class test_section_L_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(69, 74)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section L occupancies
        for block in self.plc_program_2.sec_array[4].block_occupancy:
            self.assertTrue(block)

class test_section_M_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(74, 77)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section M occupancies
        for block in self.plc_program_2.sec_array[5].block_occupancy:
            self.assertTrue(block)

class test_section_T_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(105, 110)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section T occupancies
        for block in self.plc_program_2.sec_array[6].block_occupancy:
            self.assertTrue(block)

class test_section_U_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(110, 117)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section U occupancies
        for block in self.plc_program_2.sec_array[7].block_occupancy:
            self.assertTrue(block)

class test_section_V_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(117, 122)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section V occupancies
        for block in self.plc_program_2.sec_array[8].block_occupancy:
            self.assertTrue(block)

class test_section_W_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(122, 144)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section W occupancies
        for block in self.plc_program_2.sec_array[9].block_occupancy:
            self.assertTrue(block)

class test_section_X_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(144, 147)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section X occupancies
        for block in self.plc_program_2.sec_array[10].block_occupancy:
            self.assertTrue(block)

class test_section_Y_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(147, 150)), self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section Y occupancies
        for block in self.plc_program_2.sec_array[11].block_occupancy:
            self.assertTrue(block)

class test_section_Z_occupancy(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Set occupancy
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2([150], self.occupancy_test_array)
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check section Z occupancies
        for block in self.plc_program_2.sec_array[12].block_occupancy:
            self.assertTrue(block)

# Receive sugg speed and sugg authority test case
class test_receive_sugg_speed_and_authority(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [50] * 87
        self.sugg_authority_test_array = [100] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass sugg speeds to PLC Program
    def test_passing_values_to_plc(self):

        # Call plc handlers
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)

        # Check sugg speed and authority
        for i in range(len(self.sugg_speed_test_array)):
            self.assertEqual(self.plc_program_2.read_sugg_speed_array[i], 50)
            self.assertEqual(self.plc_program_2.read_sugg_authority_array[i], 100)

# Set crossing commands test cases
class test_crossing_commands_train_in_T(unittest.TestCase):
    
    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # No train
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_2.write_crossing_cmd_array[0])

        # Train in section T
        for block in [105, 106, 107, 108, 109]:
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_2([block], self.occupancy_test_array)
            call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            self.assertTrue(self.plc_program_2.write_crossing_cmd_array[0])

class test_crossing_commands_train_everywhere_but_T(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [None] * 87
        self.sugg_authority_test_array = [None] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train everywhere but T
        seudo_module_unit_testing.seudo_track_model_occupancy_plc_2(list(range(105, 110)), self.occupancy_test_array)
        self.occupancy_test_array = [x ^ 1 for x in self.occupancy_test_array]
        call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
        self.assertFalse(self.plc_program_2.write_crossing_cmd_array[0])

# Set commanded speed and authority test cases
class test_commanded_speed_authority_H_to_Yard(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [50] * 87
        self.sugg_authority_test_array = [100] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train travels from H to Yard
        for block in list(range(33, 58)):
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_2([block], self.occupancy_test_array)
            call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            if block == 33:
                pass
            elif block == 34:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-33], 0)
            else:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-34], 0)
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-33], 0)
        for auth in self.plc_program_2.write_cmd_authority_array:
            self.assertEqual(auth, 100)

class test_commanded_speed_authority_Yard_to_M(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [50] * 87
        self.sugg_authority_test_array = [100] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train travels from Yard to M
        for block in list(range(63, 77)):
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_2([block], self.occupancy_test_array)
            call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            if block == 63:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-63], 0)
            elif block == 64:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-33], 0)
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-64], 0)
            elif block == 75:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-34], 0)
            elif block == 76:
                pass
            else:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-33], 0)
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-34], 0)
        for auth in self.plc_program_2.write_cmd_authority_array:
            self.assertEqual(auth, 100)

class test_commanded_speed_authority_T_to_Z(unittest.TestCase):

    # Set up test variables
    def setUp(self):
        
        # Test Arrays
        self.occupancy_test_array = [0] * 91
        self.sugg_speed_test_array = [50] * 87
        self.sugg_authority_test_array = [100] * 87

        # PLC Object
        self.plc_program_2 = green_line_plc_2_class()

    # Pass occupancies to PLC Program
    def test_passing_values_to_plc(self):

        # Train travels from Yard to M
        for block in list(range(105, 151)):
            seudo_module_unit_testing.seudo_track_model_occupancy_plc_2([block], self.occupancy_test_array)
            call_plc_2_handlers(self.plc_program_2, self.sugg_speed_test_array, self.sugg_authority_test_array, self.occupancy_test_array)
            if block == 105:
                pass
            elif block == 106:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-64], 0)
            else:
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-64], 0)
                self.assertEqual(self.plc_program_2.write_cmd_speed_array[block-65], 0)
        for auth in self.plc_program_2.write_cmd_authority_array:
            self.assertEqual(auth, 100)
            
####################################################################################################
#
#                                      PLC Program 3 Test Cases
#
####################################################################################################



####################################################################################################
#
#                                           Run Test Cases
#
####################################################################################################

if __name__ == '__main__':
    unittest.main()