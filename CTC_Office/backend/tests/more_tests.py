from Node import Node

node1 = Node("A", 10)
node2 = Node("B", 20)
node1.addEdge(node2, 200)
print(node1.get_string())

node3 = Node(None, None)
print(node3.get_string())