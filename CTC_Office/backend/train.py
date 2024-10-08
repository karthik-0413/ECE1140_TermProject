from block import Block

class Train(): 
    def __init__(self, index, location):
        self.index = index
        self.suggested_speed = 0
        self.authority = 0
        self.destination = ""
        self.departure_time = int()
        self.location = location
