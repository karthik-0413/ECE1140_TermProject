from enum import Enum

class NodeType(Enum):
    STATION = 1
    SWITCH = 2

class Node:
    def __init__(self, index, type:NodeType):
        self.index = index
        self.node_type = type
        self.status = "Clear"

        self.edge_list = list()
        """format = [(node, weight), (node, weight), ...]"""

    def numEdges(self):
        return len(self.edge_list)

    def addEdge(self, connectedNode, weight):
        if connectedNode not in self.edge_list:
            self.edge_list.append((connectedNode, weight))
        else:
            raise ValueError("Edge already exists")

    def removeEdge(self, connectedNode):
        self.edge_list = [edge for edge in self.edge_list if self.edge_list[1] != connectedNode]

    def get_string(self) -> str:
        return str("Node: \n" + "Name: " + self.index + "\nType: " + self.node_type + "\nStatus: " + self.status)
    
    def __getitem__(self, index):
        return self.edge_list[index][0], self.edge_list[index][1]
    
    def __setitem__(self, index, value: tuple[int, int, int]):
        if index < len(self.edge_list) & index >= 0:
            self.edge_list[index] = (value[0], value[1])
        else:
            raise IndexError("Index out of range")
    

if __name__ == '__main__': 
    # create new node called A that is a station
    node = Node("A", "Station")
    node2 = Node("B", "Station")

    # add an edge between node A and node B with a weight of 100
    node.addEdge(node2, 100)

    # Add an edge between node B and node A with a wieght of 120, by referencing B using A 
    node[0][0].addEdge(node, 100)

    print(node.get_string())