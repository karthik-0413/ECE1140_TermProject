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
        self.arrival_times = []
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
                    next_block_string=row['Next Block'],
                    station_time=row['Min Time To Station']
                )
                self.layout.append(block)
                #print(f"Block number: {block.block_number}  Block length: {block.block_length}  Section: {block.section}  Infrastructure: {block.infrastructure}")
        
        self.calc_arrival_times()

    def read_excel_schedule():
        pass

    def calc_auth(self, train_id:int):

        if self.train_list:
            train_index = [train.train_id for train in self.train_list].index(train_id)
            
            if self.train_list[train_index].destinations or self.train_list[train_index].to_yard:
                authority = 0
                start = 0
                end = 0

                reached_first_time = False
                local_second_time = self.train_list[train_index].second_time[0]
                #print("Second Time", self.train_list[train_index].second_time[0])

                # start is the current location of the train
                # end is the destination of the train
                # curr is the current block of the calculation
                # prev is the previous block of the calculation
                if self.train_list[train_index].to_yard:
                    start, end = self.train_list[train_index].location, 0
                else:
                    start, end = self.train_list[train_index].location, abs(self.train_list[train_index].destinations[0])

                curr = start
                prev = self.train_list[train_index].prev_location

                count = 0

                # while the current block of calculation is not the destination
                while True:

                    if curr == end:
                        #print("second time: ", self.train_list[train_index].second_time[0])

                        # First time reaching the destination block
                        if not reached_first_time:
                            reached_first_time = True

                            # If you want to stop now
                            #print("Second_time", self.train_list[train_index].second_time[0])
                            if local_second_time == False:
                                break

                            # If you want to stop the second time
                            else:
                                temp = curr
                                curr = self.layout[curr].next_block(prev)
                                print("Curr: ", curr)
                                prev = temp
                                count = count + 1

                        # Second time reaching the destination block & want to stop the second time
                        else: #reached_first_time and self.train_list[train_index].second_time[0]:
                            if self.train_list[train_index].location == end:
                                self.train_list[train_index].second_time[0] = False
                                temp = curr 
                                curr = self.layout[curr].next_block(prev)
                                prev = temp
                                authority = authority + 1

                            break

                        # Second time reaching the destination block & want to continue
                        #else:
                            #self.train_list[train_index].second_time[0] = orig_second_time
                            #break

                    # calculate the next block to travel to
                    temp = curr
                    curr = self.layout[curr].next_block(prev)
                    prev = temp

                    #print("Current block: ", curr)

                    self.train_list[train_index].path.append(curr)
                    authority = authority + 1
                    
                self.train_list[train_index].authority = authority

                if authority == 0:

                    if self.train_list[train_index].to_yard:

                        self.remove_train_destination(train_id, end)
                        self.train_list[train_index].path.insert(0, (self.calc_path(self.train_list[train_index].location, abs(self.train_list[train_index].destinations[0]), self.train_list[train_index].second_time[0])))
                        traverse_time = 0
                        for block in [layout_block for layout_block in self.train_list[train_index].path[0] if self.layout[layout_block].min_time_to_station != None]:
                            traverse_time = traverse_time + self.layout[block].min_time_to_station

                        time = dt.datetime.combine(dt.datetime.today(), self.train_list[train_index].arrival_times[-1])   
                        time = time + dt.timedelta(seconds=traverse_time)
                        self.train_list[train_index].arrival_times.append(time.time())    

            else:
                self.train_list[train_index].authority = 0

    def calc_speed(self, train_id:int):
            
        for train in self.train_list:
            if train.train_id == train_id:
                index = self.train_list.index(train)
                self.train_list[index].suggested_speed = self.layout[self.train_list[index].location].speed_limit

    def calc_path(self, start, end, second_time):
        path = []
        curr = start
        prev = -1

        time_2 = second_time

        while True:
            if curr == end:
                if time_2:
                    time_2 = False
                else:
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

    #def calc_arrival_times(self):
        for train in self.train_list:
            train.arrival_times.clear()
            total_traverse_time = 0
            traverse_time = 0

            # first arrival
            for block_num in [block for block in train.path[0] if self.layout[block].min_time_to_station != None]:
                traverse_time = traverse_time + self.layout[block_num].min_time_to_station

            total_traverse_time = total_traverse_time + traverse_time
            train.arrival_times.append(total_traverse_time)

            for prev_dest_index, dest in enumerate(train.destinations[1:]):
                # Add 60 seconds for dwell time at station
                traverse_time = 60
                for block_num in [block for block in train.path[prev_dest_index + 1] if self.layout[block].min_time_to_station != None]:
                    traverse_time = traverse_time + self.layout[block_num].min_time_to_station

                total_traverse_time = total_traverse_time + traverse_time
                train.arrival_times.append(total_traverse_time)

            #traverse_time = 60
            #print("Path to yard: ", train.path[-1])
            #for block_num in [block for block in train.path[-1] if self.layout[block].min_time_to_station != None]:
            #    traverse_time = traverse_time + self.layout[block_num].min_time_to_station
            #    
            #total_traverse_time = total_traverse_time + traverse_time
            #train.arrival_times.append(total_traverse_time)

    def calc_arrival_times(self):
        for block in [layout_block for layout_block in self.layout if layout_block.min_time_to_station != None]:
            self.arrival_times.append((block.block_number, block.min_time_to_station))

    def arrival_time_between(self, start, end):
        if [0, 63, 64].count(start):
            start_index = 0
        else:
            start_index = [block[0] for block in self.arrival_times].index(start)
        end_index = [block[0] for block in self.arrival_times].index(abs(end))
        traverse_time = 0
        while start_index < end_index:
            traverse_time = traverse_time + self.arrival_times[start_index][1]
            start_index += 1

        return traverse_time

    def create_train(self, destination, arrival_time, destination_station=None):
        """ Directly add a train to the line """
        dest = abs(destination)
        self.train_list.append(Train(self.next_train_id, destination, arrival_time, destination_station))
        self.train_list[-1].second_time.append(destination < 0)
        self.next_train_id += 1
        self.train_list[-1].path.append(self.calc_path(0, dest, destination < 0))
        self.calc_auth(self.train_list[-1].train_id)

    def add_pending_train(self, destination, arrival_time, destination_station=None):
        """ Add a train to be dispatched later"""
        dest = abs(destination)
        self.pending_trains.append(Train(self.next_train_id, destination, arrival_time, destination_station))
        self.pending_trains[-1].second_time.append(destination < 0)
        self.pending_trains[-1].path.append(self.calc_path(0, dest, destination < 0))
        self.next_train_id += 1

    def dispatch_pending_train(self, train_id):
        """ Dispatch a train that was pending departure """
        train_index = [train.train_id for train in self.pending_trains].index(train_id)
        temp = self.pending_trains.pop(train_index)
        print("Train dispatched: ", temp.train_id)
        self.train_list.append(temp)
        print("Train list length: ", len(self.train_list))
        
        self.calc_auth(train_id)

    def remove_train(self, train_id):
        self.train_list.pop(train_id)

    def add_train_destination(self, train_id, destination, arrival_time, station_name=None):
        dest = abs(destination)
        train_index = [train.train_id for train in self.train_list].index(train_id)
        print("Train index: ", train_index, "Train id: ", train_id)

        # Confirm that the train is not going to yard
        if (not self.train_list[train_index].destinations) and self.train_list[train_index].path:
            self.train_list[train_index].to_yard = False
            self.train_list[train_index].path = []

        # add the destination and find the index it was placed at
        self.train_list[train_index].add_destination(destination, arrival_time, station_name)
        self.train_list[train_index].second_time.append(destination < 0)
        index = self.train_list[train_index].destinations.index(dest)

        # if there is a destination before the new one, path goes from the previous destination to the new one
        if index > 0:
            self.train_list[train_index].path.insert(index, self.calc_path(self.train_list[train_index].destinations[index - 1], dest, destination < 0))
        # if there are no destinations before it, path goes from the current location to the new destination
        else:
            self.train_list[train_index].path.insert(index, self.calc_path(self.train_list[train_index].location, dest, destination < 0))

        # if new destination is the not the last one, adjust the path after the new destination
        if dest != self.train_list[train_index].destinations[-1]:
            self.train_list[train_index].path.append(self.calc_path(dest, self.train_list[train_index].destinations[index + 1], destination < 0))
        
    def remove_train_destination(self, train_id, destination):
        train_index = [train.train_id for train in self.train_list].index(train_id)
        print("Train destination to be removed: ", destination)
        print("Train destinations: ", self.train_list[train_index].destinations)
        self.train_list[train_index].remove_destination(destination)

        # recalculate path to next destination if it exists
        if train_index in [train.destinations for train in self.train_list]:

            # Remove path to destination.  Then remove the next destination and path to destination, then read with the recalculated path
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

    def test_switch(self, block_number):
        self.layout[block_number].toggle_switch()

    def calculate_line_throughput(self):
        for train in self.train_list:
            stops = len(train.destinations)

    def update_train_locations(self):
        # Update the locations stored by the Trains
        # print("Updating train locations")

        for train in self.train_list:
            next = self.layout[train.location].next_block(train.prev_location)
            # print("Current location: ", train.location)
            # print("Next location: ", next)
            # print("Next Occupied: ", self.layout[next].occupied)

            if self.layout[next].occupied:
                # print("Train location updated")
                train.prev_location = train.location
                train.location = next

    def get_stations(self):
        stations = []
        path = self.calc_path(self.layout[0].next_block(-1), 0, False)
        for block_num in path:
            if self.layout[block_num].station_name != None:
                stations.append((self.layout[block_num].station_name, block_num))
        return stations
            
    def find_destination(self, station_name:str):
        for block in self.layout:
            if block.station_name == station_name:
                return block.block_number
        return -1