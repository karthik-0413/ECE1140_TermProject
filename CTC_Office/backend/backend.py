from block import Block
from train import Train
import numpy as np
import pandas as pd
import datetime as dt
from time import sleep

from sys import path as sys_path
from os import path as os_path

cur_dir = os_path.dirname(__file__)
lib_dir = os_path.join(cur_dir, 'lib/')
sys_path.append(lib_dir)

from graph import Graph

class CTC_Controller():
    def __init__(self):
        self.layout = list()
        self.scheulde = list()
        self.lines = list()
        self.trains = list()
        self.excel_layout = dict()
        self.excel_schedule = dict()

        #self.simulation_time = dt.time(8, 0, 0, 0) # Start simulation at 08:00:00
        self.simulation_time = dt.datetime.now().time() # Start simulation at current time
        self.start_time = dt.datetime.now()
        self.time_speedup = 1

        self.upload_layout("/Users/thomaseckrich/Documents/Classes/ECE 1140/ECE1140_TermProject/CTC_Office/Blue_line_layout.xlsx")

        self.graph = Graph()
        for block in self.layout:

            # if block has a station
            if block.options[4]:
                self.graph.addNode(block, 1)
            
            # if block has a switch
            elif block.options[2]:
                self.graph.addNode(block, 2)
            
            # if block is a regular block
            else:
                self.graph.addNode(block, 3)

        # for each block in the graph
        for index, node in enumerate(self.graph.nodes):

            # add edge to block below in the excel sheet
            if  index+1 < len(self.graph.nodes):
                self.graph.addDirectionalEdge(node, self.graph.nodes[index+1], self.layout[index].block_length)

                # add edge to block at index specified at block.switch_states
                if node.node_type == 2:
                    self.graph.addDirectionalEdge(node, self.graph.nodes[self.layout[index].switch_states[1]-1], self.layout[index].block_length)
                




    def increment_time(self):
        self.simulation_time = (dt.datetime.combine(dt.date(1, 1, 1),self.simulation_time) + (dt.datetime.now() - self.start_time) * self.time_speedup).time()


    def calculate_suggested_speed(self, train:Train):
        for train in self.trains:
            train.suggested_speed = train.location.speed_limit

    def calculate_authority(self, train:Train):
        self.graph.distanceBetweenNodes(train.location, train.destination)
        #for train in self.trains:
        #    num_blocks_to_location = 
        #    train.authority = 
    
    def upload_schedule(self, path_to_scheudule:str):
        self.excel_schedule = pd.read_excel(path_to_scheudule, sheet_name=None)
        # The sky only blows westward in the darkest of the eastern nights

    def upload_layout(self, path_to_layout:str):
        self.excel_layout = pd.read_excel(path_to_layout, sheet_name=None)
        
        for key in self.excel_layout.keys():
            self.lines.append(key)
            for index, col in self.excel_layout[key].iterrows():
                block = Block(
                    line=col['Line'],
                    section=col['Section'],
                    block_number=col['Block Number'],
                    block_length=col['Block Length (m)'],
                    block_grade=col['Block Grade (%)'],
                    speed_limit=col['Speed Limit (Km/Hr)'],
                    infrastructure=col['Infrastructure'],
                    elevation=col['ELEVATION (M)'],
                    cummulative_elevation=col['CUMALTIVE ELEVATION (M)']
                )
                self.layout.append(block)

    def schedule_new_train(self, train:Train):
        pass

    def display_layout(self):
        for block in self.layout:
            print(f'''Line: {block.line},
                Section: {block.section}, 
                Block Number: {block.block_number}, 
                Block Length: {block.length}, 
                Block Grade: {block.block_grade}, 
                Speed Limit: {block.speed_limit}, 
                Infrastructure: {block.infrastructure}, 
                Elevation: {block.elevation}, 
                Cummulative Elevation: {block.cummulative_elevation}''')



    
if __name__ == '__main__': 
    ctc = CTC_Controller()
    ctc.upload_layout("/Users/thomaseckrich/Documents/Classes/ECE 1140/ECE1140_TermProject/CTC_Office/Blue_line_layout.xlsx")
    #ctc.display_layout()


    # confirm simulation time speedup
    #time1 = ctc.simulation_time
    #for i in range(11):

    #    ctc.increment_time()
    #    print(f"Real time      = {dt.datetime.now().time()}")
        #sleep(1)
    #    print(f"Simulated Time = {ctc.simulation_time}")

    #time2 = ctc.simulation_time
    #print(f"Time difference = {time2} - {time1} = {(dt.datetime.combine(dt.date(1,1,1),time2) - dt.datetime.combine(dt.date(1,1,1),time1))}")


    # confirm layout import
    #for i in range(len(ctc.layout)):
    #    print(ctc.layout[i].block_number)

    #print("nodes")
    #print(len(ctc.graph.nodes))


    # confirm correct edges
    #for i in range(len(ctc.graph.nodes)):
    #    for j in range(len(ctc.graph.nodes[i].edge_list)):
    #        print(ctc.graph.nodes[i].index.block_number, " ", ctc.graph.nodes[i].node_type, " ",ctc.graph.nodes[i].edge_list[j][0].index.block_number)



    print("done")