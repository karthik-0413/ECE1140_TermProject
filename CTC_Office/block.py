from enum import Enum
import re

class Signal(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

class Block():
    def __init__(self,
                section:str,
                block_number:str,
                speed_limit:str,
                infrastructure:str
                ):

        self.section = str(section)
        self.block_number = int(block_number)
        self.speed_limit = int(speed_limit)
        self.infrastructure = str(infrastructure)

        self.station_name = None

        self.occupied = False
        self.failure = False
        self.maintenance = False

        self.next_block_list = []

        # Choose which optional block characteristics to include

        self.set_infrastructure()


    def set_infrastructure(self):
        # Check the infrastructure column to see if block has a station
        if re.search("Station", self.infrastructure):
            pattern = r"Station\s+([A-Za-z0-9]+)"
            match = re.search(pattern, self.infrastructure, re.IGNORECASE)
            if match:
                self.station_name = match.group(1)

    def update_occupancy(self, occupancy:bool):
        self.occupied = occupancy

    def update_failure(self, failure:bool):
        self.failure = failure

    def toggle_maintenance(self):
        self.maintenance = not self.maintenance
        
    def next_block(self, prev_block):
        """Return the next block to be traversed given the last value traversed."""

        # if there is only one next block, then the train must go there.
        if len(self.next_block_list) == 1:
            return self.next_block_list[0]
        # if there is more than one next block, then the train will go from low to high
        elif prev_block < self.block_number:
            return self.next_block_list[1]
        # and from high to low
        elif prev_block > self.block_number:
            return self.next_block_list[0]
        # prev_block should never be equal to self.block_number
        

    
    