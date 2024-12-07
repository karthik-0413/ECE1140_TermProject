import unittest
import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow
from track_model import track_model
from TrackTrainCommunicate import TrackTrainComms as TrainComms
from WaysideTrackCommunicate import WaysideTrackComms as WaysideComms

# Add the parent directory to sys.path to allow absolute imports
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)


class TrackModelTesting(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Initialize QApplication
        cls.app = QApplication(sys.argv)

    def setUp(self):
        # Initialize the required communicators
        self.train_comms = TrainComms()
        self.wayside_comms = WaysideComms()

        # Create an instance of track_model
        self.track_model_instance = track_model(self.train_comms, self.wayside_comms)

    def test_initialization(self):
        # Test if the track_model is initialized properly
        self.assertIsNotNone(self.track_model_instance)
        self.assertIsInstance(self.track_model_instance, track_model)


if __name__ == '__main__':
    unittest.main()


    #########################################################
    # def test_update_polarity_values(self):
    #     # Test the update_polarity_values method
    #     # Before updating
    #     initial_polarity_values = self.track_model_instance.polarity_values.copy()

    #     # Call the method
    #     self.track_model_instance.update_polarity_values()

    #     # After updating
    #     updated_polarity_values = self.track_model_instance.polarity_values
    #     self.assertNotEqual(initial_polarity_values, updated_polarity_values)

    # def test_update_grade_values(self):
    #     # Test the update_grade_values method
    #     # Before updating
    #     initial_grade_values = self.track_model_instance.grade_values.copy()

    #     # Call the method
    #     self.track_model_instance.update_grade_values()

    #     # After updating
    #     updated_grade_values = self.track_model_instance.grade_values
    #     self.assertNotEqual(initial_grade_values, updated_grade_values)

    # def test_update_elevation_values(self):
    #     # Test the update_elevation_values method
    #     # Before updating
    #     initial_elevation_values = self.track_model_instance.elevation_values.copy()

    #     # Call the method
    #     self.track_model_instance.update_elevation_values()

    #     # After updating
    #     updated_elevation_values = self.track_model_instance.elevation_values
    #     self.assertNotEqual(initial_elevation_values, updated_elevation_values)

    # def test_get_num_passengers_leaving(self):
    #     # Test the get_num_passengers_leaving method
    #     num_passengers_leaving = self.track_model_instance.get_num_passengers_leaving()

    #     # Check that the returned value is an integer and non-negative
    #     self.assertIsInstance(num_passengers_leaving, int)
    #     self.assertGreaterEqual(num_passengers_leaving, 0)

    # def test_handle_num_passenger_leaving_signal(self):
    #     # Test the handle_num_passenger_leaving_signal method
    #     test_num_people = [5, 10, 15]

    #     # Before handling the signal
    #     initial_num_passengers_at_station = self.track_model_instance.num_passengers_at_station.copy()

    #     # Call the method
    #     self.track_model_instance.handle_num_passenger_leaving_signal(test_num_people)

    #     # After handling the signal
    #     updated_num_passengers_at_station = self.track_model_instance.num_passengers_at_station
    #     self.assertNotEqual(initial_num_passengers_at_station, updated_num_passengers_at_station)
    #     self.assertEqual(updated_num_passengers_at_station, test_num_people)

    # def test_get_num_passengers_boarding(self):
    #     # Test the get_num_passengers_boarding method
    #     num_passengers_boarding = self.track_model_instance.get_num_passengers_boarding()

    #     # Check that the returned value is an integer and non-negative
    #     self.assertIsInstance(num_passengers_boarding, int)
    #     self.assertGreaterEqual(num_passengers_boarding, 0)

    # def test_handle_seat_vacancy_signal(self):
    #     # Test the handle_seat_vacancy_signal method
    #     test_train_vacancy = [50, 60, 70]

    #     # Before handling the signal
    #     initial_open_train_seats = self.track_model_instance.open_train_seats.copy()

    #     # Call the method
    #     self.track_model_instance.handle_seat_vacancy_signal(test_train_vacancy)

    #     # After handling the signal
    #     updated_open_train_seats = self.track_model_instance.open_train_seats
    #     self.assertNotEqual(initial_open_train_seats, updated_open_train_seats)
    #     self.assertEqual(updated_open_train_seats, test_train_vacancy)

    # def test_get_seat_vacancy(self):
    #     # Test the get_seat_vacancy method
    #     seat_vacancy = self.track_model_instance.get_seat_vacancy()

    #     # Check that the returned value is an integer and non-negative
    #     self.assertIsInstance(seat_vacancy, int)
    #     self.assertGreaterEqual(seat_vacancy, 0)

    # def test_handle_position_signal(self):
    #     # Test the handle_position_signal method
    #     test_positions = [1, 2, 3]

    #     # Before handling the signal
    #     initial_positions = self.track_model_instance.position_list.copy()

    #     # Call the method
    #     self.track_model_instance.handle_position_signal(test_positions)

    #     # After handling the signal
    #     updated_positions = self.track_model_instance.position_list
    #     self.assertNotEqual(initial_positions, updated_positions)
    #     self.assertEqual(updated_positions, test_positions)

    # def test_update_block_values(self):
    #     # Test the update_block_values method
    #     # Before updating
    #     initial_all_blocks = self.track_model_instance.all_blocks.copy()

    #     # Call the method
    #     self.track_model_instance.update_block_values()

    #     # After updating
    #     updated_all_blocks = self.track_model_instance.all_blocks
    #     self.assertNotEqual(initial_all_blocks, updated_all_blocks)

    # def test_switch_commands(self):
    #     # Test handling of switch commands
    #     initial_switch_cmds = self.track_model_instance.switch_cmds.copy()
    #     self.track_model_instance.switch_cmds = [0, 1, 0]

    #     # Verify that switch commands are updated
    #     self.assertNotEqual(initial_switch_cmds, self.track_model_instance.switch_cmds)
    #     self.assertEqual(self.track_model_instance.switch_cmds, [0, 1, 0])

    # def test_light_commands(self):
    #     # Test handling of light commands
    #     initial_light_cmds = self.track_model_instance.light_cmds.copy()
    #     self.track_model_instance.light_cmds = [1, 0, 1]

    #     # Verify that light commands are updated
    #     self.assertNotEqual(initial_light_cmds, self.track_model_instance.light_cmds)
    #     self.assertEqual(self.track_model_instance.light_cmds, [1, 0, 1])

    # def test_crossing_commands(self):
    #     # Test handling of crossing commands
    #     initial_crossing_cmds = self.track_model_instance.crossing_cmds.copy()
    #     self.track_model_instance.crossing_cmds = [1, 1, 0]

    #     # Verify that crossing commands are updated
    #     self.assertNotEqual(initial_crossing_cmds, self.track_model_instance.crossing_cmds)
    #     self.assertEqual(self.track_model_instance.crossing_cmds, [1, 1, 0])

    # def test_cmd_speeds_wayside(self):
    #     # Test command speeds from wayside
    #     initial_cmd_speeds = self.track_model_instance.cmd_speeds_wayside.copy()
    #     self.track_model_instance.cmd_speeds_wayside = [30.0, 45.0, 50.0]

    #     # Verify that speeds are updated
    #     self.assertNotEqual(initial_cmd_speeds, self.track_model_instance.cmd_speeds_wayside)
    #     self.assertEqual(self.track_model_instance.cmd_speeds_wayside, [30.0, 45.0, 50.0])

    # def test_cmd_authorities_wayside(self):
    #     # Test command authorities from wayside
    #     initial_cmd_authorities = self.track_model_instance.cmd_authorities_wayside.copy()
    #     self.track_model_instance.cmd_authorities_wayside = [5, 10, 15]

    #     # Verify that authorities are updated
    #     self.assertNotEqual(initial_cmd_authorities, self.track_model_instance.cmd_authorities_wayside)
    #     self.assertEqual(self.track_model_instance.cmd_authorities_wayside, [5, 10, 15])

    # def test_upload_file(self):
    #     # Create a test file
    #     test_file = 'test_upload.txt'
    #     with open(test_file, 'w') as f:
    #         f.write('Test content')

    #     # Call the upload_file function
    #     result = track_model.upload_file(test_file)

    #     # Check if the upload was successful
    #     self.assertTrue(result)

    #     # Clean up the test file
    #     os.remove(test_file)