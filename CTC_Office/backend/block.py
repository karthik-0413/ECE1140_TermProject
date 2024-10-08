from enum import Enum

class Signal(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

class Block():
    def __init__(self, block_id, length:int, speed_limit:int, has_crossing:bool):
        self.block_id = 0
        self.occupied = False
        self.has_crossing = False # True if block has it's crossing down
        self.signal = Signal.GREEN
        self.length = length
        self.speed_limit = speed_limit
        self.crossing = False

    
    