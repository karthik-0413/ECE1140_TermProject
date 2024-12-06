import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Resources.CTCWaysideComm import CTCWaysideControllerComm as Communicate1
from Resources.WaysideTrackComm import WaysideControllerTrackComm as Communicate2
from PyQt6.QtWidgets import QApplication, QWidget

app = QApplication(sys.argv)

from wayside_shell import wayside_shell_class

class TestTuning(unittest.TestCase):
    def setUp(self):
        self.comm1 = Communicate1()
        self.comm2 = Communicate2()
        self.wayside = wayside_shell_class(self.comm1, self.comm2)
        self.paths = [
            "TrackController/green_plc_1.py",
            "TrackController/green_plc_2.py",
            "TrackController/green_plc_3.py",
        ]
        
    def test_plc_upload(self):
        self.wayside.upload_plc_program(self.paths)
        self.assertTrue(self.wayside.plc_program_1.is_created())
        self.assertTrue(self.wayside.plc_program_2.is_created())
        self.assertTrue(self.wayside.plc_program_3.is_created())
    
if __name__ == '__main__':
    unittest.main()