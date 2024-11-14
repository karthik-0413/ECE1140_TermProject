import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from CTC_Office.line import Line

from TrainModel.CTC_communicate import CTC_Train_Model_Communicate
from Resources.CTCWaysideComm import CTCWaysideControllerComm
from Resources.CTCTrain import CTCTrain

class CTC_logic():
    def __init__(self, train_model_communicate: CTCTrain, wayside_communicate: CTCWaysideControllerComm):
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

        # New stuff - zach




    def write_to_communicate_objects(self):
        print("Writing to communicate objects")
        #print("self.line.send_new_values = ", self.line.send_new_values)

        # Write all buffered information to the communicate objects
        # self.train_model_communicate.dispatch_train_signal.emit(self.num_trains)
        if self.line.send_new_values and len(self.line.train_list):
            #print("speed: ", self.suggested_speed_list[0])
            #print("auth: ", self.suggested_authority_list[0])
            self.wayside_communicate.suggested_speed_signal.emit(self.suggested_speed_list)
            self.wayside_communicate.suggested_authority_signal.emit(self.suggested_authority_list)
            self.line.send_new_values = False
            
        if len(self.line.train_list):
            if self.line.train_list[0].to_yard and self.line.just_reached_station:
                self.wayside_communicate.suggested_speed_signal.emit(self.suggested_speed_list)
                self.wayside_communicate.suggested_authority_signal.emit(self.suggested_authority_list)
                self.line.just_reached_station = False
        

    def upload_layout_to_line(self, path_to_layout:str):
        self.line.read_excel_layout(path_to_layout)

        # Set the lists to the correct size
        self.suggested_authority_list = [None for _ in self.line.layout]
        self.suggested_speed_list = [None for _ in self.line.layout]
    
    def upload_schedule_to_line():
        pass

    def add_new_train_to_line(self, line_name:str, destination:int, destination_station:str, departure_time):
        
        # Add destinations to the train object 
        self.line.create_train(destination, destination_station, departure_time)
        print("Adding train")
        self.num_trains = len(self.line.train_list)
        print("Num trains = ", self.num_trains)
        
        self.update_authority_list()
        self.update_suggested_speed_list()

        #self.train_model_communicate.current_train_count_signal.emit(self.num_trains)

    def add_train_destination_on_line(self, line_name:str, train_id:int, destination:int, station_name:str):
        self.line.add_train_destination(train_id, destination, station_name)

    def update_authority_list(self):

        self.suggested_authority_list = [None for _ in self.suggested_authority_list]

        for train in self.line.train_list:
            self.line.calc_auth(train.train_id)
            self.suggested_authority_list[train.location] = train.authority

    def update_suggested_speed_list(self):
        #print("Updating suggested speed list")
        self.suggested_speed_list = [None for _ in self.suggested_speed_list]

        for train in self.line.train_list:
            self.line.calc_speed(train.train_id)
            self.suggested_speed_list[train.location] = train.suggested_speed

    def update_train_locations_list(self):
        self.line.update_train_locations()
            
    def confirm_train_paths():
        pass

    def select_line_for_maintenance(self, line_name:str, block_number:int):
        self.line.layout[block_number].toggle_maintenance()

    def update_blocks_on_line(self, block_occupancies: list):
        # Update block occupancies based on the wayside controller
        for block in self.line.layout:
            block.update_occupancy(block_occupancies[block.block_number])

        self.update_train_locations_list()
        self.update_authority_list()
        self.update_suggested_speed_list()
        self.calculate_total_throughput()
        #self.send_new_values = self.line.not_at_destination()

    def calculate_total_throughput(self):
        pass
        # total_throughput = 0
        # for line in self.lines:
        #     line.calculate_line_throughput()
        #     total_throughput += line.throughput

    def toggle_automatic_manual(self):
        self.automatic = not self.automatic
        print("Toggled")

    def get_stations(self):
        return self.line.get_stations()
    
    def find_destination(self, station_name:str):
        return self.line.find_destination(station_name)