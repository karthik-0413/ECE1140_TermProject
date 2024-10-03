class Node:
    def __init__(self, index, status):
        self.index = index
        self.status = status
        self.edge_list = list()

    def addEdge(self, connectedNode, weight): 
        self.edge_list.append((self.index, connectedNode, weight))

    def removeEdge(self, connectedNode):
        self.edge_list = [edge for edge in self.edge_list if self.edge_list[1] != connectedNode]

    def get_string(self) -> str:
        return str(self.edge_list)
    