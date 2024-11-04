import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))


from CTC_Office.block import Block
from CTC_Office.train import Train

class Line():
    def __init__(self, line_name:str):
        self.layout = [Block]
        self.train_list = [Train]
        self.throughput = 0
        self.elapsed_time = 1

    def read_excel_layout():
        pass

    def read_excel_schedule():
        pass

    def calc_auth(self, train_id:int):
        authority = 0

        # start is the current location of the train
        # end is the destination of the train
        # curr is the current block of the calculation
        # prev is the previous block of the calculation

        start, end = self.train_list[train_id].location, self.train_list[train_id].destinations[0]
        curr = start
        prev = self.train_list[train_id].prev_location

        # while the current block of calculation is not the destination
        while curr != end:
            authority = authority + 1

            # calculate the next block to travel to
            cur = self.layout[curr].next_block(prev)

        # assign authority
        self.train_list[train_id].authority = authority
            

    def calc_speed(self):
        for train in self.train_list:
            suggested_speed = self.layout[train.location].speed_limit

    def create_train(self, destination, destination_station):
        self.train_list.append(Train(len(self.train_list), destination, destination_station))

    def change_train_destination(self, train_id, old_destination, new_destination, station_name):
        self.train_list[train_id].change_destination(old_destination, new_destination, station_name)

    def add_train_destination(self, train_id, destination, station_name):
        self.train_list[train_id].add_destination(destination, station_name)
        
    def remove_train_destination(self, train_id, destination):
        self.train_list[train_id].remove_destination(destination)

    # consider this
    def on_correct_path():
        pass

    def toggle_block_maintenance(self, block_number):
        self.layout[block_number].update_maintenance()

    def calculate_line_throughput(self):
        for train in self.train_list:
            stops = len(train.destinations)
            
