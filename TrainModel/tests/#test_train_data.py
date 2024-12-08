# TrainModel/tests/test_train_data.py

import unittest
from PyQt6.QtCore import QObject, pyqtSignal, QCoreApplication
from unittest.mock import MagicMock
import sys
import os

# Adjust sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

#import classes
from TrainModel.train_data import TrainData

# Define mock communication classes with necessary signals
class MockTrainTrainController(QObject):
    interior_lights_signal = pyqtSignal(list)
    exterior_lights_signal = pyqtSignal(list)
    power_command_signal = pyqtSignal(list)
    service_brake_command_signal = pyqtSignal(list)
    emergency_brake_command_signal = pyqtSignal(list)
    desired_temperature_signal = pyqtSignal(list)
    left_door_signal = pyqtSignal(list)
    right_door_signal = pyqtSignal(list)
    announcement_signal = pyqtSignal(list)
    # Add other signals as needed

class MockTrackTrainCommunicate(QObject):
    # Define the signals used in TrainData
    commanded_speed_signal = pyqtSignal(list)
    commanded_authority_signal = pyqtSignal(list)
    block_grade_signal = pyqtSignal(list)
    block_elevation_signal = pyqtSignal(list)
    polarity_signal = pyqtSignal(list)
    number_passenger_boarding_signal = pyqtSignal(list)  # Added missing signal
    number_passenger_leaving_signal = pyqtSignal(list)
    seat_vacancy_signal = pyqtSignal(list)
    position_signal = pyqtSignal(list)

class MockCTCTrain(QObject):
    # Define the signals used in TrainData
    current_train_count_signal = pyqtSignal(int)
    dispatch_train_signal = pyqtSignal(list)  # Added missing signal

class TestInteriorLights(unittest.TestCase):
    def setUp(self):
        """Set up the TrainData instance with mocked communication classes and initialize one train."""
        # Create instances of the mock communication classes
        self.tc = MockTrainTrainController()
        self.tm = MockTrackTrainCommunicate()
        self.ctc = MockCTCTrain()

        # Initialize TrainData with the mocked communication instances
        self.train_data = TrainData(
            tc_communicate=self.tc,
            tm_communicate=self.tm,
            ctc_communicate=self.ctc
        )

        # Initialize with one train
        self.train_data.initialize_train()

        # Connect the data_changed signal to mock to verify its emission
        self.data_changed_mock = MagicMock()
        self.train_data.data_changed.connect(self.data_changed_mock)

    def test_turn_on_interior_light(self):
        """Test turning the interior light on."""
        # Emit interior_lights_signal
        self.tc.interior_lights_signal.emit([True])

        QCoreApplication.processEvents()

        # Verify that interior_light is updated
        self.assertEqual(self.train_data.interior_light, [True], "Interior light should be turned on.")

        # Verify data_changed signal
        self.assertTrue(self.data_changed_mock.called, "data_changed signal should be emitted when interior light is toggled on.")

    def test_turn_off_interior_light(self):
        """Test turning the interior light off."""
        # First, turn the interior light on
        self.tc.interior_lights_signal.emit([True])
        QCoreApplication.processEvents()

        self.data_changed_mock.reset_mock()

        # Now, turn the interior light off
        self.tc.interior_lights_signal.emit([False])
        QCoreApplication.processEvents()

        # Verify interior_light
        self.assertEqual(self.train_data.interior_light, [False], "Interior light should be turned off.")

        # Verify that data_changed signal
        self.assertTrue(self.data_changed_mock.called, "data_changed signal should be emitted when interior light is toggled off.")

class TestExteriorLights(unittest.TestCase):
    def setUp(self):
        """Set up the TrainData instance with mocked communication classes and initialize one train."""
        # Create instances of the mock communication classes
        self.tc = MockTrainTrainController()
        self.tm = MockTrackTrainCommunicate()
        self.ctc = MockCTCTrain()

        # Initialize TrainData with the mocked communication instances
        self.train_data = TrainData(
            tc_communicate=self.tc,
            tm_communicate=self.tm,
            ctc_communicate=self.ctc
        )

        # Initialize with one train
        self.train_data.initialize_train()

        # Connect the data_changed signal to a mock to verify its emission
        self.data_changed_mock = MagicMock()
        self.train_data.data_changed.connect(self.data_changed_mock)

    def test_turn_on_exterior_light(self):
        """Test turning the exterior light on."""
        self.tc.exterior_lights_signal.emit([True])

        QCoreApplication.processEvents()

        # Verify that exterior_light is updated
        self.assertEqual(self.train_data.exterior_light, [True], "Exterior light should be turned on.")

        self.assertTrue(self.data_changed_mock.called, "data_changed signal should be emitted when exterior light is toggled on.")

    def test_turn_off_exterior_light(self):
        """Test turning the exterior light off."""
        # First, turn the exterior light on
        self.tc.exterior_lights_signal.emit([True])
        QCoreApplication.processEvents()

        self.data_changed_mock.reset_mock()

        # Now, turn the exterior light off
        self.tc.exterior_lights_signal.emit([False])
        QCoreApplication.processEvents()

        self.assertEqual(self.train_data.exterior_light, [False], "Exterior light should be turned off.")

        self.assertTrue(self.data_changed_mock.called, "data_changed signal should be emitted when exterior light is toggled off.")

if __name__ == '__main__':
    unittest.main()
