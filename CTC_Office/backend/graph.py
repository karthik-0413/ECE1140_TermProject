from node import Node
import numpy as np
from collections import deque

class Graph:
    def __init__(self):
        self.node_list = list[Node]

    def addNode(self, index, status):
        for node in self.node_list:
            if node.index == index:
                raise ValueError("Node already exists")
            
        self.node_list.append(Node(index, status))

    def addDirectionalEdge(self, index1, index2, weight):
        self.node_list[index1].addEdge(index2, weight)

    def addTwoWayEdge(self, index1, index2, weight):
        self.node_list[index1].addEdge(index2,weight)

    def removeDirectionalEdge(self, index1, index2):
        self.node_list[index1].removeEdge(index2)

    def removeTwoWayEdge(self, index1, index2):
        self.node_list[index1].removeEdge(index2)
        self.node_list[index2].removeEdge(index1)

    def removeNode(self, index):
        pass 

    def DijPathfind(self, start, target):
        length = len(self.node_list)
        dist = np.array(length)
        prev = np.array(length)

        for node in range(length):
            dist =  1000000000
            prev = -1000000000

        dist[start] = 0
        prev[start] = -1000000000

        Q = deque()





    