import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

import pandas as pd
import datetime as dt

from CTC_Office.block import Block
from CTC_Office.train import Train

class Line():
    def __init__(self, line_name:str):
        self.layout = []
        self.train_list = []
        self.throughput = 0

        self.next_train_id = 1

        self.pending_trains = []

        self.excel_layout = {}
        self.excel_schedule = {}

    def read_excel_layout(self, path_to_layout:str):
        self.excel_layout = pd.read_excel(path_to_layout, sheet_name=None)

        for key in self.excel_layout.keys():
            for index, row in self.excel_layout[key].iterrows():
                block = Block(
                    section=row['Section'],
                    block_number=row['Block Number'],
                    block_length=row['Block Length (m)'],
                    speed_limit=row['Speed Limit (Km/Hr)'],
                    infrastructure=row['Infrastructure'],
                    next_block_string=row['Next Block']
                )
                self.layout.append(block)
                print(f"Block number: {block.block_number}  Block length: {block.block_length}  Section: {block.section}  Infrastructure: {block.infrastructure}")

    def read_excel_schedule():
        pass

    def calc_auth(self, train_id:int):

        if self.train_list:

            train_index = [train.train_id for train in self.train_list].index(train_id)
            
            if self.train_list[train_index].destinations or self.train_list[train_index].to_yard:
                authority = 0
                start = 0
                end = 0

                # start is the current location of the train
                # end is the destination of the train
                # curr is the current block of the calculation
                # prev is the previous block of the calculation
                if self.train_list[train_index].to_yard:
                    start, end = self.train_list[train_index].location, 0
                else:
                    start, end = self.train_list[train_index].location, self.train_list[train_index].destinations[0]

                curr = start
                prev = self.train_list[train_index].prev_location

                # while the current block of calculation is not the destination
                while True:

                    if curr == end:
                        break

                    # calculate the next block to travel to
                    temp = curr
                    curr = self.layout[curr].next_block(prev)
                    prev = temp

                    self.train_list[train_index].path.append(curr)
                    authority = authority + 1
                    
                self.train_list[train_index].authority = authority

                if authority == 0:

                    if not self.train_list[train_index].to_yard:
                        self.remove_train_destination(train_id, end)
                        if not self.train_list[train_index].destinations:
                            self.train_list[train_index].to_yard = True
                            self.self.calc_path(self.train_list[train_index].location, 0)

            else:
                self.train_list[train_index].authority = 0

    def calc_speed(self, train_id:int):
            
        for train in self.train_list:
            if train.train_id == train_id:
                index = self.train_list.index(train)
                self.train_list[index].suggested_speed = self.layout[self.train_list[index].location].speed_limit

    def calc_path(self, start, end):
        path = []
        curr = start
        prev = -1

        while True:
            if curr == end:
                break

            temp = curr
            curr = self.layout[curr].next_block(prev)
            prev = temp

            path.append(curr)

        return path

    #def calc_arrival_times(self):
        for train in self.train_list:

            if not train.arrivals_calculated:
                train.arrivals_calculated = True
                train.path = []
                total_traverse_time = 0
                traverse_time = 0

                # calculate first traverse time since it goes from curr location to first destination
                path = self.calc_path(train.location, train.destinations[0])
                for block_num in train.path[0]:
                    traverse_time = traverse_time + self.layout[block_num].ideal_traverse_time

                total_traverse_time = total_traverse_time + traverse_time
                date = dt.datetime.now().date()
                datetime_last = dt.datetime.combine(date, train.departure_times[0])
                datetime = datetime_last + dt.timedelta(seconds=traverse_time)
                train.arrival_times.append(datetime.time())

                # arrival times for stations
                for prev_dest_index, dest in enumerate(train.destinations[1:]):
                    
                    path = self.calc_path(train.destinations[prev_dest_index], train.destinations[prev_dest_index + 1])
                    # Add 60 seconds for dwell time at station
                    traverse_time = 60
                    for block_num in path:
                        traverse_time = traverse_time + self.layout[block_num].ideal_traverse_time

                    total_traverse_time = total_traverse_time + traverse_time
                    date = dt.datetime.now().date()
                    datetime_last = dt.datetime.combine(date, train.arrival_times[-1])
                    datetime = datetime_last + dt.timedelta(seconds=traverse_time)
                    train.arrival_times.append(datetime.time())

                # final calculation for path to yard
                traverse_time = 60
                path = self.calc_path(train.destinations[-1], 0)
                for block_num in path:
                    traverse_time = traverse_time + self.layout[block_num].ideal_traverse_time
                
                total_traverse_time = total_traverse_time + traverse_time
                date = dt.datetime.now().date()
                datetime_last = dt.datetime.combine(date, train.arrival_times[-1])
                datetime = datetime_last + dt.timedelta(seconds=traverse_time)
                train.arrival_times.append(datetime.time())

    def create_train(self, destination, arrival_time, destination_station=None):
        """ Directly add a train to the line """
        self.train_list.append(Train(self.next_train_id, destination, arrival_time, destination_station, departure_time=dt.datetime.now().time()))
        self.next_train_id += 1
        self.train_list[-1].path.append(self.calc_path(0, destination))
        self.calc_auth(self.train_list[-1].train_id)

    def add_pending_train(self, destination, arrival_time, destination_station=None, depart_time:str=None):
        """ Add a train to be dispatched later"""
        self.pending_trains.append(Train(self.next_train_id, destination, arrival_time, destination_station, depart_time))
        self.pending_trains[-1].path.append(self.calc_path(0, destination))
        self.next_train_id += 1

    def dispatch_pending_train(self, train_id):
        """ Dispatch a train that was pending departure """
        train_index = [train.train_id for train in self.pending_trains].index(train_id)
        self.train_list.append(self.pending_trains.pop(train_index))
        self.calc_auth(train_id)

    def remove_train(self, train_id):
        self.train_list.pop(train_id)

    def add_train_destination(self, train_id, destination, arrival_time, station_name=None):
        train_index = [train.train_id for train in self.train_list].index(train_id)

        # Confirm that the train is not going to yard
        if (not self.train_list[train_index].destinations) and self.train_list[train_index].path:
            self.train_list[train_index].to_yard = False
            self.train_list[train_index].path = []

        # add the destination and find the index it was placed at
        self.train_list[train_index].add_destination(destination, arrival_time, station_name)
        index = self.train_list[train_index].destinations.index(destination)

        # if there is a destination before the new one, path goes from the previous destination to the new one
        if index > 0:
            self.train_list[train_index].path.insert(index, self.calc_path(self.train_list[train_index].destinations[index - 1], destination))
        # if there are no destinations before it, path goes from the current location to the new destination
        else:
            self.train_list[train_index].path.insert(index, self.calc_path(self.train_list[train_index].location, destination))

        # if new destination is the not the last one, adjust the path after the new destination
        if destination != self.train_list[train_index].destinations[-1]:
            self.train_list[train_index].path.append(self.calc_path(destination, self.train_list[train_index].destinations[index + 1]))
        
    def remove_train_destination(self, train_id, destination):
        train_index = [train.train_id for train in self.train_list].index(train_id)
        self.train_list[train_index].remove_destination(destination)

        # recalculate path to next destination if it exists
        if train_index in [train.destinations for train in self.train_list]:

            # Remove path to destination.  Then remove the next destination and path to destination, then readd with the recalculated path
            self.train_list[train_index].path.pop(train_index)
            self.train_list[train_index].path.pop(train_index)
            dest = self.train_list[train_index].destinations[train_index]
            dest_string = self.train_list[train_index].destination_strings[train_index]
            arrival_time = self.train_list[train_index].arrival_times[train_index]
            self.train_list[train_index].remove_destination(self.train_list[train_index].destinations[train_index])
            self.add_train_destination(train_id, dest, arrival_time, dest_string)

        # send train 
        for train in self.train_list:
            if not train.destinations:
                self.train_list[train].to_yard = True

    def toggle_block_maintenance(self, block_number):
        self.layout[block_number].toggle_maintenance()

    def calculate_line_throughput(self):
        for train in self.train_list:
            stops = len(train.destinations)

    def update_train_locations(self):
        # Update the locations stored by the Trains
        print("Updating train locations")

        for train in self.train_list:
            next = self.layout[train.location].next_block(train.prev_location)
            print("Current location: ", train.location)
            print("Next location: ", next)
            print("Next Occupied: ", self.layout[next].occupied)

            if self.layout[next].occupied:
                print("Train location updated")
                train.prev_location = train.location
                train.location = next

    def get_stations(self):
        stations = []
        for block in self.layout:
            if block.station_name != None:
                stations.append(block.station_name)
        return stations
            
    def find_destination(self, station_name:str):
        for block in self.layout:
            if block.station_name == station_name:
                return block.block_number
        return -1