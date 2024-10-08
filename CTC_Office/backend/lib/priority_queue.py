from node import Node
import heapq

class CustomQueue:
    def __init__(self):
        self.elements = []

    def isEmpty(self):
        return len(self.elements) == 0

    def push(self, item):
        heapq.heappush(self.elements, (item.minEdgeWeight(), item))

    def pop(self):
        node = heapq.heappop(self.elements)
        node.removeMinWeightEdge()
        if node.numEdges() != 0:
            self.push(node)


