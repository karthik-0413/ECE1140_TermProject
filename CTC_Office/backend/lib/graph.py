from node import Node, NodeType
from priority_queue import CustomQueue

class Graph:
    def __init__(self):
        self.nodes = list()

    def addNode(self, index, node_type:NodeType):
        node = Node(index, node_type)
        self.nodes.append(node)

    def addDirectionalEdge(self, node1, node2, weight):
        self.nodes[self.nodes.index(node1)].addEdge(node2, weight)
        #print("Edge added from " + f"{node1.index.block_number}" + " to " + f"{node2.index.block_number}" + " with weight " + str(weight))
        #print(len(node1.edge_list))

    def addTwoWayEdge(self, node1, node2, weight):
        self.addDirectionalEdge(node1, node2, weight)
        self.addDirectionalEdge(node2, node1, weight)

    def removeDirectionalEdge(self, node1, node2):
        self.nodes[self.nodes.index(node1)].removeEdge(node2)

    def removeTwoWayEdge(self, node1, node2):
        self.removeDirectionalEdge(node1, node2)
        self.removeDirectionalEdge(node2, node1)

    def removeNode(self, node):
        self.nodes.remove(node)

    def DijPathfind(self, start):
        for item in self.nodes:
            if item.index == start:
                beginning = item

        Q = CustomQueue()
        Q.push(beginning)

        distances = {node: float('inf') for node in self.nodes}
        distances[beginning] = 0

        predecessors = {node: None for node in self.nodes}

        while not Q.isEmpty():

            current = Q.pop()
            for edge in current.edge_list:
                neighbor = edge[0]
                weight = edge[1]
                new_dist = distances[current] + edge[1]

                if new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    predecessors[neighbor] = current.index
                    Q.push(neighbor)

        return distances, predecessors
    
    def distanceBetweenNodes(self, start, end):
        distances, predecessors = self.DijPathfind(start)
        return distances[end], predecessors[end]
    