from node_old import Node
import node_old
import pytest
import numpy as np

def test_creation():
    node1 = Node("A", 49)
    assert node1.data == 49
    node2 = Node("B", "HI")
    assert node2.data == "HI"
    node3 = Node("C", list())
    assert node3.data == list()
    node4 = Node("D", -238)
    assert node4.data == -238

def test_edgeAdd():
    node1 = Node("A", 10)
    node2 = Node("B", 15)
    node1.addEdge(node2, 200)
    assert node1.get_string() == "Data = 10\nConnections to nodes: ['B']\nWeights are: [200]"

def test_emptyNode():
    node1 = Node("A", 10)
    assert node1.get_string() == "Data = 10\nConnections to nodes: []\nWeights are: []"
    
def test_nullNode():
    with pytest.raises(ValueError):
        node1 = Node(None, None)

def test_edgeRemove():
    node1 = Node("A", 10)
    node2 = Node("B", 15)
    node1.addEdge(node2, 200)
    node1.removeEdge(node2)
    assert node1.get_string() == "Data = 10\nConnections to nodes: []\nWeights are: []"

def test_removeFromEmpty():
    node1 = Node("A", 10)
    with pytest.raises(ValueError):
        node1.removeEdge(0)

def test_removeBadIndex():
    node1 = Node("A", 10)
    node2 = Node("B", 15)
    node1.addEdge(node2, 200)
    with pytest.raises(ValueError):
        node1.removeEdge(node1)

def test_createDirectionalEdge():
    node_list = list[Node]
    node_list.append(Node("A", 10))
    node_list.append(Node("B", 15))
    adj_list = np.zeros((len(node_list), len(node_list)))
    node_old.newDirectionalEdge(node_list, adj_list, "A", "B", 100)
    
