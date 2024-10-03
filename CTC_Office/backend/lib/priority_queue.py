from node import Node
import queue

class CustomQueue:
    def __init__(self):
        self.queue = queue.PriorityQueue[Node]

    def push(self, item):
        pass
        

    def pop(self):
        if len(self.queue) == 0:
            raise ValueError("Queue is empty.")
        min = 1000000000000
        min_node = None
        for node in self.queue:
            for edge in node:
                if node.edge_list[edge] < min:
                    min = edge
                    min_node = node

        self.queue.edge_list.remove(edge)
        return min
