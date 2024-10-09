from enum import Enum
import re
from numpy import nan

class Signal(Enum):
    RED = 1
    YELLOW = 2
    GREEN = 3

class Block():
    def __init__(self,
                line:str,
                section:str,
                block_number:str,
                block_length:str,
                block_grade:str,
                speed_limit:str,
                infrastructure:str,
                elevation:str,
                cummulative_elevation:str
                ):
        
        
        self.line = str(line)
        self.section = str(section)
        self.block_number = int(block_number)
        self.block_length = int(block_length)
        self.block_grade = int(block_grade)
        self.speed_limit = int(speed_limit)
        self.infrastructure = str(infrastructure)
        self.elevation = int(elevation)
        self.cummulative_elevation = int(cummulative_elevation)

        self.occupied = False

        # Optional 
        self.signal = None
        self.crossing = None
        self.switch = None
        self.switch_states = list()
        self.transponder = None
        self.station = None
        self.station_name = None

        # Choose which optional block characteristics to include
        self.options = list()

        self.set_infrastructure()


    def set_infrastructure(self):
        
        # Check if block has a signal
        if re.search("Light", self.infrastructure):
            self.options.append(True)
        else:
            self.options.append(False)

        # Check if block has a crossing
        if re.search("RAILWAY CROSSING", self.infrastructure):
            self.options.append(True)
        else:
            self.options.append(False)

        # Check if block has a switch
        if re.search("Switch", self.infrastructure):
            # Find switch connections
            pattern = r"Switch\s*\(\s*\d+\s*to\s*(\d+)\s*\)(?:\s*or\s*\(\s*\d+\s*to\s*(\d+)\s*\))?(?:;\s*Light)?"
            match = re.search(pattern, self.infrastructure, re.IGNORECASE)
            if match:
                if match.group(2):
                    self.options.append(True)
                    self.switch_states.append(int(match.group(1))) 
                    self.switch_states.append(int(match.group(2)))
                else:
                    self.options.append(False)
                    self.switch_states.append(int(match.group(1)))
        else:
            self.options.append(False)

         # Check if block has a transponder
        if re.search("Transponder", self.infrastructure):
            self.options.append(True)
        else:
            self.options.append(False)

        # Check if block has a station
        if re.search("Station", self.infrastructure):
            self.options.append(True)
            pattern = r"Station\s+([A-Za-z0-9]+)"
            match = re.search(pattern, self.infrastructure, re.IGNORECASE)
            if match:
                self.station_name = match.group(1)


        else:
            self.options.append(False)

        

    def updateBlockInformation(self, signal, crossing, switch):
        if self.options[0]:
            self.signal = signal
        if self.options[1]:
            self.crossing = crossing
        if self.options[2]:
            self.switch = switch
        
        
    
    