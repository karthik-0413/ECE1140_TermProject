import sys
import os

cur_dir = os.path.dirname(__file__)
lib_dir = os.path.join(cur_dir, '../lib/')
sys.path.append(lib_dir)

from node import Node
import pytest
import numpy as np

def test_creation():
    node1 = Node("A", "Station")
    assert node1.node_type == "Station"
    node2 = Node("B", "Switch")
    assert node2.node_type == "Switch"
    node3 = Node("C", None)
    assert node3.node_type == None
    node4 = Node("D", "Garbage")
    assert node4.node_type == "Garbage"

def test_str():
    node1 = Node("A", "Station")
    assert node1.get_string() == "***| Node Info |*** \n" + "Name: " + "A" + "\nType: " + "Station" + "\nStatus: " + "Clear"

def test_edgeAdd():
    node1 = Node("A", "Station")
    node2 = Node("B", "Switch")
    node1.addEdge(node2, 200)
    assert node1.numEdges() == 1

def test_edgeRemove():
    node1 = Node("A", "Station")
    node2 = Node("B", "Switch")
    node1.addEdge(node2, 200)
    node1.removeEdge(node2)
    assert node1.numEdges() == 0

def test_removeFromEmpty():
    node1 = Node("A", "Station")
    with pytest.raises(ValueError):
        node1.removeEdge(0)

def test_removeBadIndex():
    node1 = Node("A", "Station")
    node2 = Node("B", "Switch")
    node1.addEdge(node2, 200)
    with pytest.raises(ValueError):
        node1.removeEdge(node1)

    
