import unittest
from time import sleep
import datetime as dt
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CTC_Office.CTC_frontend import CTC_frontend
from CTC_Office.CTC_logic import CTC_logic
from Resources.CTCWaysideComm import CTCWaysideControllerComm
from Resources.CTCTrain import CTCTrain
from CTC_Office.block import Block

def add_time_to_curr(seconds):
    return (dt.datetime.now() + dt.timedelta(seconds=seconds)).time()

class TestUploadLayoutValid(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')
        
    def test_blocks_uploaded(self):
        self.assertEqual(len(self.ctc.line.layout), 152)
    
    def test_next_blocks(self):
        # Confirm two example blocks
        self.assertEqual(self.ctc.line.layout[100].next_block(99), 85)
        self.assertEqual(self.ctc.line.layout[150].next_block(149), 28)

    def test_station_names(self):
        # Confirm two example station names
        self.assertEqual(self.ctc.line.layout[9].station_name, "EDGEBROOK")
        self.assertEqual(self.ctc.line.layout[48].station_name, "INGLEWOOD")


class TestUploadLayoutInvalid(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)

    def test_invalid_layout_file(self):
        self.assertRaises(ValueError, self.ctc.upload_layout_to_line, 'CTC_Office/train.py')


class TestUploadScheduleValid(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')
        #self.ctc.upload_schedule_to_line('CTC_Office/Green_Line_Schedule.xlsx')

    def test_train_schedule_uploaded(self):
        ## Confirm that station list has been uploaded to trains
        pass

class TestUploadScheduleInvalid(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')

    def test_invalid_schedule_file(self):
        #self.assertRaises(ValueError, self.ctc.upload_schedule_to_line, 'CTC_Office/train.py')
        pass


class TestManuallyScheduleTrain(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')

    def test_1_destination_manual(self):
        arrival_time = dt.datetime.now().time()
        self.ctc.add_new_train_to_line(73, arrival_time, "DORMONT")
        self.assertEqual(self.ctc.line.train_list[0].destinations[0], 73)
        self.assertEqual(self.ctc.line.train_list[0].destination_strings[0], "DORMONT")
        self.assertEqual(self.ctc.line.train_list[0].arrival_times[0], arrival_time)

    def test_2_destinations_manual(self):
        arrival_time_1 = dt.datetime.now().time()
        self.ctc.add_new_train_to_line(114, arrival_time_1, "GLENBURY")
        sleep(1)
        arrival_time_2 = dt.datetime.now().time()
        self.ctc.add_train_destination_on_line(1, 57, arrival_time_2, "OVERBROOK")
        self.assertEqual(self.ctc.line.train_list[0].destinations[0], 114)
        self.assertEqual(self.ctc.line.train_list[0].destinations[1], 57)
        self.assertEqual(self.ctc.line.train_list[0].destination_strings[0], "GLENBURY")
        self.assertEqual(self.ctc.line.train_list[0].destination_strings[1], "OVERBROOK")
        self.assertEqual(self.ctc.line.train_list[0].arrival_times[0], arrival_time_1)
        self.assertEqual(self.ctc.line.train_list[0].arrival_times[1], arrival_time_2)

    def test_2_trains_manual(self):
        arrival_time_1 = dt.datetime.now().time()
        self.ctc.add_new_train_to_line(2, arrival_time_1, "PIONEER")
        sleep(1)
        arrival_time_2 = dt.datetime.now().time()
        self.ctc.add_new_train_to_line(9, arrival_time_2, "EDGEBROOK")
        self.assertEqual(self.ctc.line.train_list[0].destinations[0], 2)
        self.assertEqual(self.ctc.line.train_list[1].destinations[0], 9)


class TestRemoveTrainDestination(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')
        self.ctc.add_new_train_to_line(73, dt.datetime.now().time(), "DORMONT")
        self.ctc.add_train_destination_on_line(1, 57, dt.datetime.now().time(), "OVERBROOK")

    def test_remove_destination(self):
        self.ctc.remove_train_destination_on_line(1, 57)
        self.assertEqual(len(self.ctc.line.train_list[0].destinations), 1)
        self.assertEqual(self.ctc.line.train_list[0].destinations[0], 73)
        self.assertEqual(self.ctc.line.train_list[0].destination_strings[0], "DORMONT")


class TestCalculateAuthority(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')
        self.ctc.add_new_train_to_line(73, dt.datetime.now().time(), "DORMONT")

    def test_calculate_authority(self):
        self.ctc.update_authority_list()
        self.assertEqual(self.ctc.line.train_list[0].authority, 11)
        self.ctc.line.train_list[0].location = 63
        self.ctc.update_authority_list()
        self.assertEqual(self.ctc.line.train_list[0].authority, 10)
        self.ctc.line.train_list[0].location = 64
        self.ctc.update_authority_list()
        self.assertEqual(self.ctc.line.train_list[0].authority, 9)
        self.ctc.line.train_list[0].location = 72
        self.ctc.update_authority_list()
        self.assertEqual(self.ctc.line.train_list[0].authority, 1)
        self.ctc.line.train_list[0].location = 73
        self.ctc.update_authority_list()
        self.assertEqual(self.ctc.line.train_list[0].authority, 0)
        self.ctc.update_authority_list()
        self.assertEqual(self.ctc.line.train_list[0].authority, 151)


class TestCalculateSpeed(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')
        self.ctc.add_new_train_to_line(73, dt.datetime.now().time(), "DORMONT")

    def test_calculate_speed(self):
        self.ctc.update_suggested_speed_list()
        self.assertEqual(self.ctc.line.train_list[0].suggested_speed, 5)
        self.ctc.line.train_list[0].location = 63
        self.ctc.update_suggested_speed_list()
        self.assertEqual(self.ctc.line.train_list[0].suggested_speed, 70)
        self.ctc.line.train_list[0].location = 64
        self.ctc.update_suggested_speed_list()
        self.assertEqual(self.ctc.line.train_list[0].suggested_speed, 70)
        self.ctc.line.train_list[0].location = 67
        self.ctc.update_suggested_speed_list()
        self.assertEqual(self.ctc.line.train_list[0].suggested_speed, 40)
        self.ctc.line.train_list[0].location = 119
        self.ctc.update_suggested_speed_list()
        self.assertEqual(self.ctc.line.train_list[0].suggested_speed, 15)


class UpdateBlockMaintenanceStatus(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')

    def test_toggle_maintenance(self):
        self.ctc.select_line_for_maintenance("Green", 63)
        self.assertTrue(self.ctc.line.layout[63].maintenance)
        self.ctc.select_line_for_maintenance("Green", 63)
        self.assertFalse(self.ctc.line.layout[63].maintenance)

    def test_toggle_switch_positions_valid(self):
        self.ctc.select_line_for_maintenance("Green", 1)
        self.ctc.select_line_for_maintenance("Green", 12)
        self.ctc.select_line_for_maintenance("Green", 13)
        #self.ctc.toggle_switch_position(13, 0)
        #self.assertFalse(self.ctc.line.layout[13].switch_position)
        #self.ctc.toggle_switch_position(13, 1)
        #self.assertTrue(self.ctc.line.layout[13].switch_position)

    def test_toggle_switch_positions_invalid(self):
        #self.ctc.toggle_switch_position(28, 0)
        #self.assertFalse(self.ctc.line.layout[28].switch_position)
        #self.ctc.toggle_switch_position(28, 1)
        #self.assertFalse(self.ctc.line.layout[28].switch_position)
        pass


class TestSelectMode(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')

    def test_select_mode(self):
        self.assertFalse(self.ctc.automatic)
        self.ctc.toggle_maintenance_mode()
        self.assertTrue(self.ctc.maintenance_mode)
        self.ctc.toggle_maintenance_mode()
        self.ctc.toggle_automatic_manual()
        self.assertTrue(self.ctc.automatic)


class TestUpdateTrackStatusInformation(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')

    def test_update_block_occupancies(self):
        self.ctc.update_blocks_on_line([True for _ in range(152)])
        for block in self.ctc.line.layout:
            self.assertTrue(block.occupied)
        self.ctc.update_blocks_on_line([False for _ in range(152)])
        for block in self.ctc.line.layout:
            self.assertFalse(block.occupied)
        
    def test_update_switch_positions(self):
        #self.ctc.update_switch_positions([0 for _ in range(152)])
        #for block in self.ctc.line.layout:
        #    self.assertFalse(block.switch_position)
        #self.ctc.update_switch_positions([1 for _ in range(152)])
        #for block in self.ctc.line.layout:
        #    self.assertTrue(block.switch_position)
        pass


if __name__ == '__main__':
    unittest.main()