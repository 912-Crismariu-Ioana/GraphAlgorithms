from vertex import Vertex
from edge import Edge
import copy
import random

class DirectedGraph:
    def __init__(self):
        self._dictOut = {}
        self._dictIn = {}
        self._dictCost = {}

    @property
    def vertexCount(self):
        # Returns the number of vertices of the graph
        return len(self._dictOut.keys())

    @property
    def edgeCount(self):
        # Returns the number of edges of the graph
        return len(self._dictCost.keys())

    def addVertex(self, x):
        # Adds a new vertex with a given label (both in Din and Dout)
        # Precondition: The vertex does not exist (the label is unique)
        if self.isVertex(x):
            raise ValueError("Vertex already in the graph!")
        new_vertex = Vertex(x)
        self._dictIn[new_vertex] = []
        self._dictOut[new_vertex] = []

    def parseX(self):
        # Returns an iterator for parsing all the vertices
        for x in self._dictOut.keys():
            yield x.label

    def parseXY(self):
        #Returns an iterator for parsing all the vertices
        for edge in self._dictCost.keys():
            cost = self._dictCost[edge]
            yield Edge(edge.origin, edge.destination, cost)

    def parseDout(self,x):
        # Returns an iterator for parsing the outbound neighbours of x
        # Precondition: the given vertex exists
        if not self.isVertex(x):
            raise ValueError("The vertex specified is not valid")
        for neighbour in self._dictOut[Vertex(x)]:
            yield neighbour.label

    def parseDin(self,x):
        # Returns an iterator for parsing the inbound neighbours of x
        # Precondition: the given vertex exists
        if not self.isVertex(x):
            raise ValueError("The vertex specified is not valid")
        for neighbour in self._dictIn[Vertex(x)]:
            yield neighbour.label

    def isEdge(self,x,y):
        # Returns True if there is an edge from x to y, False otherwise
        # Precondition: Both of the given endpoints are vertices of the graph
        if not self.isVertex(x):
            return False
        if not self.isVertex(y):
            return False
        return Vertex(y) in self._dictOut[Vertex(x)]

    def addEdge(self,x,y,c):
        # Adds an edge from x to y
        # Precondition: there is no edge from x to y
        if self.isEdge(x,y):
            raise ValueError("Edge already exists!")
        # Add y as an outbound neighbour of x
        self._dictOut[Vertex(x)].append(Vertex(y))
        # Add x as an inbound neighbour of y
        self._dictIn[Vertex(y)].append(Vertex(x))
        # Create an Edge object (generate a new key - value pair for the Dcost)
        new_edge = Edge(x, y, c)
        self._dictCost[new_edge] = new_edge.weight

    def isVertex(self, x):
        # Checks for the existence of a vertex with a given label
        if Vertex(x) in self._dictOut.keys():
            return True
        return False

    def getIndegree(self,x):
        # Calculates the indegree for a given vertex
        # (number of edges having the given vertex as their target)
        # Precondition: The given vertex exists
        if not self.isVertex(x):
            raise ValueError("The vertex specified is not valid")
        return len(self._dictIn[Vertex(x)])

    def getOutdegree(self,x):
        # Calculates the outdegree for a given vertex
        # (number of edges having the given vertex as their origin)
        # Precondition: The given vertex exists
        if not self.isVertex(x):
            raise ValueError("The vertex specified is not valid")
        return len(self._dictOut[Vertex(x)])

    def removeEdge(self, x, y):
        # Removes an edge given a souce and a destination vertex
        # Precondition: The edge exists
        rem_edge = Edge(x,y)
        if rem_edge not in self._dictCost.keys():
            raise ValueError("Edge does not exist!")

        # Delete x as a predecessor of y
        self._dictIn[Vertex(y)].remove(Vertex(x))

        # Delete y as a successor of x
        self._dictOut[Vertex(x)].remove(Vertex(y))

        # Delete the key from Dcost
        self._dictCost.pop(rem_edge)

    def removeVertex(self, x):
        # Removes a vertex having a given label
        # Precondition: the vertex exists
        if Vertex(x) not in self._dictOut.keys():
            raise ValueError("Vertex does not exist!")

        # Traverse the list of inbound neighbours
        predecessors = self._dictIn[Vertex(x)]
        for i in range(len(predecessors)):
            # Delete the key-value pair from dictCost
            edge_in = Edge(predecessors[i].label,x)
            self._dictCost.pop(edge_in)
            # Delete x as a successor of the current inbound neighbour
            self._dictOut[predecessors[i]].remove(Vertex(x))

        # Traverse the list of outbound neighbours
        successors = self._dictOut[Vertex(x)]
        for j in range(len(successors)):
            # Delete the key-value pair from dictCost
            edge_out = Edge(x,successors[j].label)
            self._dictCost.pop(edge_out)
            # Delete x as a predecessor of the current outbound neighbour
            self._dictIn[successors[j]].remove(Vertex(x))

        # Delete the key vertex from Din and Dout
        self._dictIn.pop(Vertex(x))
        self._dictOut.pop(Vertex(x))

    def costEdge(self, x, y):
        # Returns the cost of an edge specified by the two endpoints
        # Precondition: The edge exists
        if self.isEdge(x,y):
            found = Edge(x,y)
            return self._dictCost[found]
        else:
            raise ValueError("The edge does not exist!")

    def setCostEdge(self, x, y, c):
        # Modifies the cost of an edge
        # Precondition : The edge exists
        if self.isEdge(x,y):
            found = Edge(x,y)
            self._dictCost[found] = c
        else:
            raise ValueError("The edge does not exist!")

    def inboundEdges(self, x):
        # Returns an iterator for parsing all the inbound edges for a specified vertex
        # Precondition: The vertex exists
        if not self.isVertex(x):
            raise ValueError("The vertex specified is not valid")
        for inbound in self._dictIn[Vertex(x)]:
            inbound_edge = Edge(inbound.label,x)
            cost = self._dictCost[inbound_edge]
            yield Edge(inbound.label, x, cost)

    def outboundEdges(self,x):
        # Returns an iterator for parsing all the outbound edges for a specified vertex
        # Precondition: The vertex exists
        if not self.isVertex(x):
            raise ValueError("The vertex specified is not valid")
        for outbound in self._dictOut[Vertex(x)]:
            outbound_edge = Edge(x,outbound.label)
            cost = self._dictCost[outbound_edge]
            yield Edge(x, outbound.label, cost)

    def deepcopy(self):
        # Generates a deep copy of a Double Directed Graph instance and returns it
        copy_ddg = DirectedGraph()
        copy_ddg._dictOut = copy.deepcopy(self._dictOut)
        copy_ddg._dictIn = copy.deepcopy(self._dictIn)
        copy_ddg._dictCost = copy.deepcopy(self._dictCost)
        return copy_ddg

    def clear(self):
        self._dictOut.clear()
        self._dictIn.clear()
        self._dictCost.clear()

    def isolated_vertices(self):
        for vertex in self._dictOut.keys():
            if self.getIndegree(vertex.label) == 0 and self.getOutdegree(vertex.label) == 0:
                yield vertex.label


class UndirectedGraph:
    def __init__(self):
        self._vertices = {}
        self._edges = {}

    @property
    def vertexCount(self):
        # Returns the number of vertices of the graph
        # Complexity: Theta(1)
        return len(self._vertices.keys())

    @property
    def edgeCount(self):
        # Returns the number of edges of the graph
        # Complexity: Theta(1)
        return len(self._edges.keys())

    def degree(self, x):
        # Returns the number of vertices adjacent to X
        if Vertex(x) not in self._vertices.keys():
            raise ValueError("Vertex does not exist!")
        return len(self._vertices[Vertex(x)])


    def isVertex(self, x):
        # Checks for the existence of a vertex with a given label
        # Complexity: O(n)
        if Vertex(x) in self._vertices.keys():
            return True
        return False

    def isEdge(self, x, y):
        # Returns True if there is an edge from x to y, False otherwise
        # Precondition: Both of the given endpoints are vertices of the graph
        # Complexity: O(n + m)
        if not self.isVertex(x):
            return False
        if not self.isVertex(y):
            return False
        return Vertex(y) in self._vertices[Vertex(x)]

    def parseX(self):
        # Returns an iterator for parsing all the vertices
        for x in self._vertices.keys():
            yield x.label

    def parseXY(self):
        # Returns an iterator for parsing all the vertices
        for edge in self._edges:
            cost = self._edges[edge]
            yield Edge(edge.origin, edge.destination, cost)

    def parseAdjacent(self, x):
        # Returns an iterator for parsing all vertices adjacent to X
        if Vertex(x) not in self._vertices.keys():
            raise ValueError("Vertex does not exist!")
        for adj in self._vertices[Vertex(x)]:
            yield adj.label


    def addVertex(self, x):
        # Adds a new vertex with a given label
        # Precondition: The vertex does not exist (the label is unique)
        # Complexity: O(n)
        if self.isVertex(x):
            raise ValueError("Vertex already in the graph!")
        new_vertex = Vertex(x)
        self._vertices[new_vertex] = []

    def addEdge(self,x,y,c):
        # Adds an edge from x to y
        # Precondition: there is no edge from x to y
        # Complexity: O(n+m)

        if self.isEdge(x,y):
            raise ValueError("Edge already exists!")
        self._vertices[Vertex(x)].append(Vertex(y))
        self._vertices[Vertex(y)].append(Vertex(x))
        new_edge = Edge(x, y, c)
        self._edges[new_edge] = c

    def removeEdge(self, x, y):
        # Removes an edge given two endpoints
        # Precondition: The edge exists
        # Complexity: O(n+m)
        if not self.isEdge(x,y):
            raise ValueError("Edge does not exist!")
        self._vertices[Vertex(x)].remove(Vertex(y))
        self._vertices[Vertex(y)].remove(Vertex(x))
        rem_edge = Edge(x, y, 0)
        if rem_edge not in self._edges.keys():
            rem_edge = Edge(y, x, 0)
        self._edges.pop(rem_edge)

    def removeVertex(self, x):
        # Removes a vertex having a given label
        # Precondition: the vertex exists
        # Complexity O(n+m)
        if Vertex(x) not in self._vertices.keys():
            raise ValueError("Vertex does not exist!")
        adjacent = self._vertices[Vertex(x)]
        for vertex in adjacent:
            self._vertices[vertex].remove(Vertex(x))
            rem_edge = Edge(x, vertex.label, 0)
            if rem_edge not in self._edges.keys():
                rem_edge = Edge(vertex.label, x, 0)
            self._edges.pop(rem_edge)
        self._vertices.pop(Vertex(x))

    def costEdge(self, x, y):
        # Returns the cost of an edge specified by the two endpoints
        # Precondition: The edge exists
        if self.isEdge(x,y):
            found = Edge(x,y)
        #     return self._edges[found]
        # elif self.isEdge(y, x):
        #     found = Edge(y, x)
        #     return self._edges[found]
            if found not in self._edges.keys():
                return self._edges[Edge(y,x)]
            return self._edges[found]
        else:
            raise ValueError("The edge does not exist!")

    def setCostEdge(self, x, y, c):
        # Modifies the cost of an edge
        # Precondition : The edge exists
        if self.isEdge(x,y):
            found = Edge(x,y)
            self._edges[found] = c
        elif self.isEdge(y, x):
            found = Edge(y, x)
            self._edges[found] = c
        else:
            raise ValueError("The edge does not exist!")

    def deepcopy(self):
        # Generates a deep copy of a Double Directed Graph instance and returns it
        copy_udg = UndirectedGraph()
        copy_udg._edges = copy.deepcopy(self._edges)
        copy_udg._vertices = copy.deepcopy(self._vertices)
        return copy_udg

    def clear(self):
        self._edges.clear()
        self._vertices.clear()

    def isolated_vertices(self):
        for vertex in self._vertices.keys():
            if len(self._vertices[vertex]) == 0:
                yield vertex.label


def readingFunc1(file_name, ddg):
    """
    Reading function for the file format that explicitly specifies
    the number of vertices and and edges
    :param file_name: The name of the file
    :return:
    """
    ddg.clear()
    f = open(file_name, 'rt')
    line = f.readlines()
    f.close()
    # Split the number indicating the vertices and the edges
    v_e = line[0].strip().split(' ')
    vertices = int(v_e[0])
    edges = int(v_e[1])
    for i in range(vertices):
        ddg.addVertex(i)
    # Iterate through the lines specifying the edges and shape the graph
    for j in range(1,edges+1):
        edge = line[j].strip().split(' ',3)
        ddg.addEdge(int(edge[0]),int(edge[1]),int(edge[2]))


def readingFunc2(file_name,ddg):
    """
    Reading function for the file format that only specifies the edges
    and isolated vertices
    :param file_name: The name of the file
    :return:
    """
    ddg.clear()
    f = open(file_name, 'rt')
    lines = f.readlines()
    f.close()
    # Iterate through the lines that specify the edges and shape the graph
    for j in range(len(lines)):
        # Split the parameters: starting vertex, destination vertex, weight
        edge = lines[j].strip().split(' ', 3)
        if len(edge) >= 1:
            if not ddg.isVertex(int(edge[0])):
                ddg.addVertex(int(edge[0]))
            if len(edge) >= 2:
                if not ddg.isVertex(int(edge[1])):
                    ddg.addVertex(int(edge[1]))
                if not ddg.isEdge(int(edge[0]), int(edge[1])):
                    ddg.addEdge(int(edge[0]), int(edge[1]), int(edge[2]))


def generate(ddg, x, y):
    """
    Generates a graph with a given number of vertices and edges, the latter of which are randomly assigned
    :param ddg: A directed graph instance
    :param x: The number of vertices
    :param y: The number of edges
    :return:
    """
    ddg.clear()
    # Add the vertices
    for i in range(x):
        ddg.addVertex(i)
    # Add the edges
    # The maximum number of edges for a double directed graph is x(x-1)
    # In case a larger number is provided for the edge count, generate only the maximum number possible
    if y > x*(x-1):
        y = x*(x-1)
    while ddg.edgeCount < y:
        randomOrigin = random.randint(0,x-1)
        randomDestination = random.randint(0,x-1)
        randomCost = random.randint(0,1000)
        if (randomOrigin != randomDestination) and not ddg.isEdge(randomOrigin, randomDestination):
            ddg.addEdge(randomOrigin, randomDestination, randomCost)

def writeToFile(ddg, file_name):
    """
    Writes the data associated to a directed graph to a file
    :param ddg: A given instance of graph
    :param file_name: The path to the file
    :return:
    """
    f = open(file_name, 'wt')

    # Add the edges
    for edge in ddg.parseXY():
        line = str(edge.origin) + ' ' + str(edge.destination) + ' ' + str(edge.weight)
        f.write(line)
        f.write('\n')

    # Add the isolated vertices
    for vertex in ddg.parseX():
        if ddg.getIndegree(vertex) == 0 and ddg.getOutdegree(vertex) == 0:
            line = str(vertex)
            f.write(line)
            f.write('\n')




