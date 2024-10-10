from block import Block
import datetime as dt


class Train(): 
    def __init__(self, index, location:int):
        self.index = index
        self.suggested_speed = 0
        self.authority = 0
        self.destination = ""
        self.departure_time = dt.time()
        self.location = location
        self.task = False
