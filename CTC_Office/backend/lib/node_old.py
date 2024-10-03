
class Node:
    def __init__(self, identifier, data):
        if identifier == None:
            raise ValueError("Identifier cannot be None.")
        self.identifier = identifier
        self.data = data
        #self.connections = list()
        #self.weights = list()

    #def addEdge(self, new_connection, weight: int):
    #   """Add a directional edge from this node to the node 'new_connection' with specified 'weight'."""
    #    self.connections.append(new_connection)
    #    self.weights.append(weight)

    #def removeEdge(self, node_to_remove):
    #    """Remove edge from Node"""
    #    if len(self.connections) <= 0:
    #       raise 

    #    index = self.connections.index(node_to_remove)
    #    self.connections.pop(index)
    #    self.weights.pop(index)

    # Graph functions
    def get_string(self):
        """Format values of Node into a string"""
        string = "Data = " + str(self.data) + "\nConnections to nodes: " + str([node.identifier for node in self.connections]) + "\nWeights are: " + str(self.weights)
        return string
        

def newDirectionalEdge(node_list: list[Node], adj_list: list, i, j, weight):
    """Creates a new directional edge and adds it to the adjacency list."""
    #node_list[i].addEdge(j, weight)
    adj_list[i][j] = weight

def newEdge(node_list: list[Node], adj_list: list, n1, n2, weight):
    """Creates a new edge that goes both ways, and adds to the adjacency list."""
    i = node_list.index(n1)
    j = node_list.index(n2)
    #node_list[i].addEdge(n2, weight)
    adj_list[i][j] = weight
    #node_list[j].addEdge(n1, weight)
    adj_list[j][i] = weight

def removeDirectionalEdge(node_list: list[Node], adj_list: list, i, j):
    """Remove specific edge ( i => j )"""
    #node_list[i].removeEdge(j)
    adj_list[i][j] = 0

def removeEdge(node_list: list[Node], adj_list: list, i, j):
    """Remove edges both ways between i and j."""
    #node_list[i].removeEdge(j)
    adj_list[i][j] = 0
    #node_list[j].removeEdge(i)
    adj_list[j][i] = 0

