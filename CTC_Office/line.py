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
        self.elapsed_time = 1

        self.excel_layout = {}
        self.excel_schedule = {}

        self.final_destination = 1

        self.send_new_values = True
        self.just_reached_station = True

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
        authority = 0
        traverse_time = 0

        # start is the current location of the train
        # end is the destination of the train
        # curr is the current block of the calculation
        # prev is the previous block of the calculation
        if not self.train_list[train_id].to_yard:
            start, end = self.train_list[train_id].location, self.train_list[train_id].destination
        else:
            start, end = self.train_list[train_id].location, 0


        curr = start
        prev = self.train_list[train_id].prev_location

        # while the current block of calculation is not the destination
        while True:
            authority = authority + 1
            #print("Current block: ", curr)
            traverse_time = traverse_time + self.layout[curr].ideal_traverse_time
            #print("Traversal time: ", traverse_time)

            # calculate the next block to travel to
            temp = curr
            curr = self.layout[curr].next_block(prev)
            prev = temp

            # Break out of loop
            if curr == end:
                authority = authority + 1
                traverse_time = traverse_time + self.layout[curr].ideal_traverse_time
                break
            



        # assign authority
        self.train_list[train_id].authority = authority

        date = dt.datetime.now().date()
        datetime = dt.datetime.combine(date, self.train_list[train_id].departure_time)
        datetime = datetime + dt.timedelta(seconds=traverse_time)
        self.train_list[train_id].arrival_time = datetime.time()


            

    def calc_speed(self, train_id:int):
            
            for train in self.train_list:
                if train.train_id == train_id:
                    index = self.train_list.index(train)

            self.train_list[index].suggested_speed = self.layout[self.train_list[index].location].speed_limit

    def create_train(self, destination, destination_station, departure_time):
        self.train_list.append(Train(len(self.train_list), destination, destination_station, departure_time))
        self.calc_auth(len(self.train_list) - 1)

    def add_train_destination(self, train_id, destination, station_name):
        #self.train_list[train_id].add_destination(destination, station_name)
        pass
        
    def remove_train_destination(self, train_id, destination):
        self.train_list[train_id].remove_destination(destination)

    # consider this
    def at_destination(self):
        if len(self.train_list):
            if self.train_list[0].location == self.train_list[0].destination:
                self.train_list[0].to_yard = True
                self.train_list[0].destination = 0

            


    def toggle_block_maintenance(self, block_number):
        self.layout[block_number].update_maintenance()

    def calculate_line_throughput(self):
        for train in self.train_list:
            stops = len(train.destinations)

    def update_train_locations(self):
        # Update the locations stored by the Trains

        for train in self.train_list:
            next = self.layout[train.location].next_block(train.prev_location)
            if self.layout[train.location].occupied:
                train.prev_location = train.location
                train.location = next.block_number

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