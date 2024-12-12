import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CTC_Office.block import Block
import datetime as dt


class Train(): 
    def __init__(self, train_id, destination, arrival_time, destination_station=None, departure_time=None):
        """Initialize a train object
        destination is the block number
        destination_station is the station name
        """
        self.train_id = train_id
        self.suggested_speed = 0
        self.authority = 0
        self.location = 0
        self.prev_location = -1

        self.departure_time = departure_time
        self.departed = False

        self.destinations = []
        self.destination_strings = []

        self.arrivals_calculated = False
        self.arrival_times = []

        self.path = []

        self.destinations.append(destination)
        self.arrival_times.append(arrival_time)

        if destination_station != None:
            self.destination_strings.append(destination_station)

        self.to_yard = False
        
        

    def dispatch_train(self):
        """Send message to Train Model to create a new train"""
        if self.departure_time == None:
            self.departure_time = dt.datetime.now().time()
        

    def add_destination(self, destination, arrival_time, station_name=None):
        """Add a destination to the train"""
        self.destinations.append(destination)
        self.destination_strings.append(station_name)
        self.arrival_times.append(arrival_time)

    def remove_destination(self, destination):
        """Remove a destination from the train"""
        if self.to_yard == False:
            index = self.destinations.index(destination)
            self.destinations.pop(index)
            self.destination_strings.pop(index)
            self.path.pop(index)
            self.arrival_times.pop(index)
            if len(self.destinations) == 0:
                self.to_yard = True
                self.destinations.append(0)
                self.destination_strings.append("Yard")
