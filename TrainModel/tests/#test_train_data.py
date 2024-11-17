# TrainModel/tests/test_train_data.py

import unittest
from unittest.mock import MagicMock, patch
from PyQt6.QtCore import QCoreApplication
import sys
import os

# Adjust sys.path to include the project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Now import the necessary classes
from TrainModel.train_data import TrainData
from Resources.TrainTrainControllerComm import TrainTrainController
from TrackModel.TrackTrainCommunicate import TrackTrainComms
from Resources.CTCTrain import CTCTrain

class TestTrainData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the QCoreApplication once for all tests."""
        cls.app = QCoreApplication.instance()
        if cls.app is None:
            cls.app = QCoreApplication(sys.argv)

    def setUp(self):
        """Set up the TrainData instance with mocked communication classes and initialize one train."""
        # Create mocked instances of communication classes
        self.tc = MagicMock(spec=TrainTrainController)
        self.tm = MagicMock(spec=TrackTrainComms)
        self.ctc = MagicMock(spec=CTCTrain)

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

    def test_initialization(self):
        """Test that TrainData initializes correctly with one train."""
        self.assertEqual(self.train_data.train_count, 1, "Train count should be initialized to 1.")
        self.assertEqual(len(self.train_data.passenger_count), 1, "Passenger count list should have 1 entry.")
        self.assertEqual(len(self.train_data.commanded_power), 1, "Commanded power list should have 1 entry.")
        # Add more assertions for other initial states as needed
        self.assertEqual(self.train_data.interior_light, [False], "Interior lights should be off initially.")
        self.assertEqual(self.train_data.exterior_light, [False], "Exterior lights should be off initially.")


        
    def test_toggle_exterior_light_on(self):
        """Test turning the exterior light on."""
        # Emit exterior_light_signal to turn on the exterior light
        self.tc.exterior_lights_signal.emit([True])

        # Verify that exterior_light is updated
        self.assertEqual(self.train_data.exterior_light, [True], "Exterior light should be turned on.")

        # Verify that data_changed signal was emitted
        self.assertTrue(self.data_changed_mock.called, "data_changed signal should be emitted when exterior light is toggled on.")

    def test_toggle_exterior_light_off(self):
        """Test turning the exterior light off."""
        # First, turn the exterior light on
        self.tc.exterior_lights_signal.emit([True])
        self.data_changed_mock.reset_mock()

        # Now, turn the exterior light off
        self.tc.exterior_lights_signal.emit([False])

        # Verify that exterior_light is updated
        self.assertEqual(self.train_data.exterior_light, [False], "Exterior light should be turned off.")

        # Verify that data_changed signal was emitted
        self.assertTrue(self.data_changed_mock.called, "data_changed signal should be emitted when exterior light is toggled off.")

    def tearDown(self):
        """Clean up after each test if necessary."""
        pass

if __name__ == '__main__':
    unittest.main()
