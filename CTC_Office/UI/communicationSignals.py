from PyQt6.QtCore import pyqtSignal, QObject
import os
import sys

cur_dir = os.path.dirname(__file__)
lib_dir = os.path.join(cur_dir, '../backend/')
sys.path.append(lib_dir)

from block import Block, Signal

class Communicate(QObject):

    time = pyqtSignal(str)
    time_speedup = pyqtSignal(int)

    # pass ctc.layout[block_info_request]
    block_info_request = pyqtSignal(int)
    cur_block_info = pyqtSignal(Block)

    # pass ctc.trains[train_info_reqeust]
    train_info_request = pyqtSignal(int)
    cur_train_info = pyqtSignal(Block)


    signalColor = pyqtSignal(Signal)
    switchDirection = pyqtSignal(int)
    crossingState = pyqtSignal(bool)
    blockOccupied = pyqtSignal(bool)


