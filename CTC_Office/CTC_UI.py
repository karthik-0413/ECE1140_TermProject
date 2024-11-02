from backend.line import Line

class CTC_UI():
    def __init__(self):
        self.line = Line()
        self.automatic = False

    def upload_layout_to_line():
        pass
    
    def upload_schedule_to_line():
        pass

    def add_new_train_to_line(self, line_name:str, destination:int, destination_station:str):
        self.lines[line_name].create_train(destination, destination_station)

    def change_train_destination_on_line(self, line_name:str, train_id:int, old_destination:int, new_destination:int, station_name:str):
        self.lines[line_name].change_train_destination(train_id, old_destination, new_destination, station_name)

    def add_train_destination_on_line(self, line_name:str, train_id:int, destination:int, station_name:str):
        self.lines[line_name].add_train_destination(train_id, destination, station_name)

    #def remove_train_destination_on_line()
    #    pass

    def update_authority_list(self):
        updated_authorities = []
        for train in self.line.train_list:
            updated_authorities.append(train.authority)

        self.send_authority = updated_authorities

    def update_suggested_speed_list(self):
        updated_speeds = []
        for train in self.line.train_list:
            updated_speeds.append(train.suggested_speed)

        self.train_locations = updated_speeds

    def update_train_locations_list(self):
        updated_locations = []
        for train in self.line.train_list:
            updated_locations.append(train.location)

        self.train_locations = updated_locations
            

    def confirm_train_paths():
        pass

    def select_line_for_maintenance(self, line_name:str, block_number:int):
        self.lines[line_name].layout[block_number].toggle_maintenance()

    def update_blocks_on_line(self):
        
        for block, in self.line.layout:
            block.update_occupancy(self.block_occupancies[block.block_number])

    def calculate_total_throughput(self):

        total_throughput = 0
        for line in self.lines:
            line.calculate_line_throughput()
            total_throughput += line.throughput

    def toggle_automatic_manual(self):
        self.automatic = not self.automatic