import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CTC_Office.line import Line

from TrainModel.CTC_communicate import CTC_Train_Model_Communicate
from Resources.CTCWaysideComm import CTCWaysideControllerComm

class CTC_logic():
    def __init__(self, train_model_communicate: CTC_Train_Model_Communicate, wayside_communicate: CTCWaysideControllerComm):
        self.line = Line("Green")


        self.automatic = False
        self.num_trains = None

        # Destination list for the User to select from in the UI
        self.destination_list = []

        # Communication Buffers
        self.suggested_speed_list = []
        self.suggested_authority_list = []


        self.train_model_communicate = train_model_communicate
        self.wayside_communicate = wayside_communicate

        self.wayside_communicate.block_occupancy_signal.connect(self.update_blocks_on_line)

    def write_to_communicate_objects(self):

        # Write all buffered information to the communicate objects
        self.train_model_communicate.current_train_count_signal.emit(self.num_trains)
        self.wayside_communicate.suggested_speed_signal.emit(self.suggested_speed_list)
        self.wayside_communicate.suggested_authority_signal.emit(self.suggested_authority_list)

    def upload_layout_to_line(self, path_to_layout:str):
        self.line.read_excel_layout(path_to_layout)

        # Set the lists to the correct size
        self.suggested_authority_list = [None for _ in self.line.layout]
        self.suggested_speed_list = [None for _ in self.line.layout]
    
    def upload_schedule_to_line():
        pass

    def add_new_train_to_line(self, line_name:str, destination:int, destination_station:str):
        
        # Add destinations to the train object 
        self.lines[line_name].create_train(destination, destination_station)
        print("Adding train")
        self.num_trains = len(self.line.train_list)
        print("Num trains = ", self.num_trains)

        #self.train_model_communicate.current_train_count_signal.emit(self.num_trains)

    def add_train_destination_on_line(self, line_name:str, train_id:int, destination:int, station_name:str):
        self.lines[line_name].add_train_destination(train_id, destination, station_name)

    def update_authority_list(self):

        self.suggested_authority_list = [None for _ in self.suggested_authority_list]

        for train in self.line.train_list:
            self.line.calc_auth(train.train_id)
            self.suggested_authority_list[train.location] = train.authority

    def update_suggested_speed_list(self):

        self.suggested_speed_list = [None for _ in self.suggested_speed_list]

        for train in self.line.train_list:
            self.line.calc_speed(train.train_id)
            self.suggested_speed_list[train.location] = train.suggested_speed

    def update_train_locations_list(self):
        self.line.update_train_locations()
            
    def confirm_train_paths():
        pass

    def select_line_for_maintenance(self, line_name:str, block_number:int):
        self.lines[line_name].layout[block_number].toggle_maintenance()

    def update_blocks_on_line(self, block_occupancies: list):
        # Update block occupancies
        for block, in self.line.layout:
            block.update_occupancy(block_occupancies[block.block_number])

        self.update_train_locations_list()
        self.update_authority_list()
        self.update_suggested_speed_list()
        self.calculate_total_throughput()

    def calculate_total_throughput(self):

        total_throughput = 0
        for line in self.lines:
            line.calculate_line_throughput()
            total_throughput += line.throughput

    def toggle_automatic_manual(self):
        self.automatic = not self.automatic
        print("Toggled")

    def get_stations(self):
        return self.line.get_stations()
    
    def find_destination(self, station_name:str):
        return self.line.find_destination(station_name)