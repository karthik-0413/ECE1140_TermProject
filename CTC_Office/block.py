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
                block_length:str,
                speed_limit:str,
                infrastructure:str,
                next_block_string:str
                ):

        self.section = str(section)
        self.block_length = int(block_length)
        self.block_number = int(block_number)
        self.speed_limit = int(speed_limit)
        self.infrastructure = str(infrastructure)
        self.next_block_string = str(next_block_string)

        self.ideal_traverse_time = int((self.block_length / (self.speed_limit * 1000)) * 3600)

        self.station_name = None

        self.occupied = False
        self.failure = False
        self.maintenance = False

        self.next_block_list = []

        # Choose which optional block characteristics to include

        self.set_infrastructure()
        # print("Block number: ", self.block_number, "\nStation : ", self.station_name)
        self.add_next_blocks()


    def set_infrastructure(self):
        # Check the infrastructure column to see if block has a station
        if re.search("STATION", self.infrastructure):
            pattern = r"STATION;\s([A-Z]+)"
            match = re.search(pattern, self.infrastructure, re.IGNORECASE)
            if match:
                # print("Station found: ", match.group(1))
                self.station_name = match.group(1)
            else:
                pass
                # print("Station not found")

    def add_next_blocks(self):
        blocks = self.next_block_string.split(',')
        self.next_block_list = [int(block.strip()) for block in blocks]


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

        

    
    