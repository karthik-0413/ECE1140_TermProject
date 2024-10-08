import sys
import os

cur_dir = os.path.dirname(__file__)
lib_dir = os.path.join(cur_dir, '../lib/')
sys.path.append(lib_dir)

from node import Node
from priority_queue import CustomQueue

node1 = Node("A", "Station")
node2 = Node("B", "Station")
node1.addEdge(node2, 200)
print(node1.get_string())
