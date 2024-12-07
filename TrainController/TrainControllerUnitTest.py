import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.TrainTrainControllerComm import TrainTrainController as Communicate

from TrainController import (
    Doors, Tuning, BrakeStatus, PowerCommand, SpeedControl, FailureModes, Lights, Position, Temperature
)

class TestTuning(unittest.TestCase):
    def setUp(self):
        self.tuning = Tuning()

    def test_set_kp(self):
        self.tuning.set_kp(1.5)
        self.assertEqual(self.tuning.get_kp(), 1.5)

    def test_set_ki(self):
        self.tuning.set_ki(0.5)
        self.assertEqual(self.tuning.get_ki(), 0.5)

class TestBrakeStatus(unittest.TestCase):
    def setUp(self):
        self.communicator = Communicate()
        self.brake_status = BrakeStatus(self.communicator)

    def test_apply_emergency_brake(self):
        self.brake_status.apply_emergency_brake()
        self.assertTrue(self.brake_status.get_emergency_brake_status())

    def test_no_apply_emergency_brake(self):
        self.brake_status.no_apply_emergency_brake()
        self.assertFalse(self.brake_status.get_emergency_brake_status())

class TestPowerCommand(unittest.TestCase):
    def setUp(self):
        self.brake_status = BrakeStatus(Communicate())
        self.tuning = Tuning()
        self.power_command = PowerCommand(self.brake_status, self.tuning)

    def test_update_kp(self):
        self.power_command.update_kp(2.0)
        self.assertEqual(self.tuning.get_kp(), 2.0)

    def test_update_ki(self):
        self.power_command.update_ki(1.0)
        self.assertEqual(self.tuning.get_ki(), 1.0)

class TestSpeedControl(unittest.TestCase):
    def setUp(self):
        self.brake_status = BrakeStatus(Communicate())
        self.power_command = PowerCommand(self.brake_status, Tuning())
        self.speed_control = SpeedControl(self.power_command, self.brake_status, Communicate())

    def test_set_manual_mode(self):
        self.speed_control.set_manual_mode()
        # Add assertions to verify manual mode is set

    def test_set_auto_mode(self):
        self.speed_control.set_auto_mode()
        # Add assertions to verify auto mode is set

if __name__ == '__main__':
    unittest.main()