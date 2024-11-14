import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CTC_Office.block import Block


class Train(): 
    def __init__(self, train_id, destination, destination_station, departure_time):
        """Initialize a train object
        destination is the block number
        destination_station is the station name
        """
        self.train_id = train_id
        self.suggested_speed = 0
        self.authority = 0
        self.location = 0
        self.prev_location = -1


        self.destination = destination
        self.destination_station = destination_station
        self.departure_time = departure_time
        self.arrival_time = -1

        # For implementing multiple destinations
        #self.destinations = []
        #self.destination_strings = []
        #self.schedule_times = []

        self.to_yard = False
        
        

    def dispatch_train(self):
        """Send message to Train Model to create a new train"""
        pass

    def add_destination(self, destination, station_name):
        """Add a destination to the train"""
        self.destinations.append(destination)
        self.destination_strings.append(station_name)

    def remove_destination(self, destination):
        """Remove a destination from the train"""
        if self.to_yard == False:
            index = self.destinations.index(destination)
            self.destinations.pop(index)
            self.destination_strings.pop(index)
            if len(self.destinations) == 0:
                self.to_yard = True
                self.destinations.append(0)
                self.destination_strings.append("Yard")
