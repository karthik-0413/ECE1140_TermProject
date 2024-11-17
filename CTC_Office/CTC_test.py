import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CTC_Office.CTC_frontend import CTC_frontend
from CTC_Office.CTC_logic import CTC_logic
from Resources.CTCWaysideComm import CTCWaysideControllerComm
from Resources.CTCTrain import CTCTrain
from CTC_Office.block import Block

class TestUploadSchedule(unittest.TestCase):
    def setUp(self):
        self.train_comm = CTCTrain
        self.wayside_comm = CTCWaysideControllerComm
        self.ctc = CTC_logic(self.train_comm, self.wayside_comm)
        self.ctc.upload_layout_to_line('CTC_Office/Green_Line_Layout.xlsx')
        print("next block", self.ctc.line.layout[100].next_block)
        
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


if __name__ == '__main__':
    unittest.main()