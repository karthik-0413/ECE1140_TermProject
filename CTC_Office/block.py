from enum import Enum
import re
import math

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
                next_block_string:str,
                station_time:str
                ):

        self.section = str(section)
        self.block_length = int(block_length)
        self.block_number = int(block_number)
        self.speed_limit = int(speed_limit)
        self.infrastructure = str(infrastructure)
        self.next_block_string = str(next_block_string)

        self.min_time_to_station = None

        if not math.isnan(float(station_time)):
            self.min_time_to_station = int(station_time)


        self.station_name = None
        self.occupied = False
        self.failure = False
        self.maintenance = False

        self.next_block_list = []

        self.switch_positions = None
        self.curr_switch_position = None

        # Choose which optional block characteristics to include

        self.set_infrastructure()
        # print("Block number: ", self.block_number, "\nStation : ", self.station_name)
        self.add_next_blocks()

    def set_infrastructure(self):
        # Check the infrastructure column to see if block has a station
        if re.search("STATION", self.infrastructure):
            pattern = r"STATION;\s(.*?);"
            match = re.search(pattern, self.infrastructure, re.IGNORECASE)

            if match:
                # print("Station found: ", match.group(1))
                self.station_name = match.group(1)

        switch_pattern = r"\d+-(\d+)"
        match_switch = re.findall(switch_pattern, self.infrastructure, re.IGNORECASE)
            
        temp = [int(sw_match) for sw_match in match_switch]
        if temp:
            self.switch_positions = temp
            self.curr_switch_position = False
            #print("Switch positions: ", self.switch_positions)
                
    def add_next_blocks(self):
        blocks = self.next_block_string.split(',')
        self.next_block_list = [int(block.strip()) for block in blocks]

    def update_occupancy(self, occupancy:bool):
        self.occupied = occupancy

    def update_failure(self, failure:bool):
        self.failure = failure

    def toggle_maintenance(self):
        self.maintenance = not self.maintenance

    def toggle_switch(self):
        if self.curr_switch_position != None:
            self.curr_switch_position = not self.curr_switch_position

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

        

    
    