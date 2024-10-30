from block import Block
import datetime as dt


class Train(): 
    def __init__(self, train_id, destination, destination_station):
        self.train_id = train_id
        self.suggested_speed = 0
        self.authority = 0
        self.location = 0
        self.prev_location = -1

        self.destinations = []
        self.destination_strings = []

        self.schedule_times = []

        self.to_yard = False
        

    def dispatch_train(self):
        """Send message to Train Model to create a new train"""
        pass

    def change_destination(self, old_destination, new_destination, station_name):
        """Change the destination of the train"""
        index = self.destinations.index(old_destination)
        self.destinations[index] = new_destination
        self.destination_strings[index] = station_name

    def add_destination(self, destination, station_name):
        """Add a destination to the train"""
        self.destinations.append(destination)
        self.destination_strings.append(station_name)

    def remove_destination(self, destination):
        """Remove a destination from the train"""
        index = self.destinations.index(destination)
        self.destinations.pop(index)
        self.destination_strings.pop(index)
        if len(self.destinations) == 0:
            self.to_yard = True