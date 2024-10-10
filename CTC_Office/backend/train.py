from block import Block
import datetime as dt


class Train(): 
    def __init__(self, index, location:int):
        self.index = index
        self.suggested_speed = 0
        self.authority = 0
        self.destination = ""
        self.departure_time = dt.datetime.now().time()
        self.departure_time_str = self.departure_time.strftime("%H:%M:%S")
        self.arrival_time = dt.time()
        self.location = location
        self.task = False

    def arrival_time_str(self):
        return self.arrival_time.strftime("%H:%M:%S")