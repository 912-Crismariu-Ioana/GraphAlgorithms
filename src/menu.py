from graph import DirectedGraph, readingFunc1,readingFunc2, generate, writeToFile, UndirectedGraph
from BFS import lowestLengthPath
from FloydWarshall import lowestCostWalk


class UI:
    def __init__(self):
        self._command_dict = {"1" :self.read_graph_ui, "2": self.print_vertices_ui, "3": self.print_edges_ui,
                              "4":self.vertex_count_ui, "5": self.edge_count_ui,"6": self.add_vertex_ui,
                              "7": self.add_edge_ui, "8":self.remove_vertex_ui, "9":self.remove_edge_ui,
                              "10": self.inbound_neighbours_ui, "11": self.outbound_neighbours_ui,
                              "12": self.indegree_ui, "13": self.outdegree_ui, "14":self.is_edge_ui,
                              "15": self.print_cost_edge_ui, "16": self.modify_cost_edge_ui,
                              "17":self.inbound_edges_ui, "18":self.outbound_edges_ui, "19": self.random_graph_ui,
                              "20": self.write_to_file_ui, "22":self.isolated_vertices_UI, "23":self.min_lenght_path, "24":self.min_cost_path}
        self._ddg = DirectedGraph()

    @staticmethod
    def menu():
        print("\n")
        print("Choose one of the following functionalities:")
        print("1.Read a graph from a file")
        print("2.Display vertices")
        print("3.Display edges")
        print("4.Display vertex count")
        print("5.Display edge count")
        print("6.Add a vertex")
        print("7.Add an edge")
        print("8.Remove a vertex")
        print("9.Remove an edge")
        print("10.Display inbound neighbours of a specified vertex")
        print("11.Display outbound neighbours of a specified vertex")
        print("12.Display the indegree of a specified vertex")
        print("13.Display the outdegree of a specified vertex")
        print("14.Check the existence of an edge")
        print("15.Display the cost of an edge")
        print("16.Modify the cost of an edge")
        print("17.Display the inbound edges for a specified vertex")
        print("18.Display the outbound edges for a specified vertex")
        print("19.Generate a random graph")
        print("20.Write the current graph to a file")
        print("21.Exit")
        print("22.Isolated vertices")
        print("23.Minimum length path")
        print("23.Minimum cost path")
        print("\n")

    def console(self):
        done = False
        while not done:
            try:
                self.menu()
                inp = input("Enter a number:").strip().lower()
                if inp in self._command_dict.keys():
                    self._command_dict[inp]()
                elif inp == '21':
                    print("Exiting...")
                    done = True
                else:
                    print("Bad command!")
            except ValueError as ve:
                print(str(ve))

    def read_graph_ui(self):
        file_name = input("Enter the name of the file:").strip().lower()
        print("Choose a file format")
        print("1.File explicitly specifying the vertex and edge count")
        print("2.File specifying only the edges")
        inp = input("Enter the number:").strip().lower()
        graph = DirectedGraph()
        if inp == '1':
            readingFunc1(file_name, graph)
        elif inp == '2':
            readingFunc2(file_name, graph)
        else:
            print("Wrong input")
        self._ddg = graph

    def print_vertices_ui(self):
        vertices = self._ddg.parseX()
        for vertex in vertices:
            print(vertex)

    def print_edges_ui(self):
        edges = self._ddg.parseXY()
        for edge in edges:
            print(edge)

    def vertex_count_ui(self):
        print(self._ddg.vertexCount)

    def edge_count_ui(self):
        print(self._ddg.edgeCount)

    def add_vertex_ui(self):
        vertex = input("Enter an integer to assign to the vertex:").strip().lower()
        self._ddg.addVertex(int(vertex))

    def add_edge_ui(self):
        origin = input("Enter the origin vertex:").strip().lower()
        destination = input("Enter the destination vertex:").strip().lower()
        cost = input("Assign a cost:").strip().lower()
        self._ddg.addEdge(int(origin), int(destination), int(cost))

    def remove_vertex_ui(self):
        vertex = input("Enter the vertex you want to remove:").strip().lower()
        self._ddg.removeVertex(int(vertex))

    def remove_edge_ui(self):
        origin = input("Enter the origin vertex:").strip().lower()
        destination = input("Enter the destination vertex:").strip().lower()
        self._ddg.removeEdge(int(origin), int(destination))

    def inbound_neighbours_ui(self):
        vertex = input("Enter the vertex:").strip().lower()
        inbound_neighbours = self._ddg.parseDin(int(vertex))
        for neighbour in inbound_neighbours:
            print(neighbour)

    def outbound_neighbours_ui(self):
        vertex = input("Enter the vertex:").strip().lower()
        outbound_neighbours = self._ddg.parseDout(int(vertex))
        for neighbour in outbound_neighbours:
            print(neighbour)

    def indegree_ui(self):
        vertex = input("Enter the vertex:").strip().lower()
        print(self._ddg.getIndegree(int(vertex)))

    def outdegree_ui(self):
        vertex = input("Enter the vertex:").strip().lower()
        print(self._ddg.getOutdegree(int(vertex)))

    def is_edge_ui(self):
        origin = input("Enter the origin vertex:").strip().lower()
        destination = input("Enter the destination vertex:").strip().lower()
        print(self._ddg.isEdge(int(origin), int(destination)))

    def print_cost_edge_ui(self):
        origin = input("Enter the origin vertex:").strip().lower()
        destination = input("Enter the destination vertex:").strip().lower()
        print(self._ddg.costEdge(int(origin), int(destination)))

    def modify_cost_edge_ui(self):
        origin = input("Enter the origin vertex:").strip().lower()
        destination = input("Enter the destination vertex:").strip().lower()
        cost = input("Assign a new cost:").strip().lower()
        self._ddg.setCostEdge(int(origin), int(destination), int(cost))

    def inbound_edges_ui(self):
        vertex = input("Enter the vertex:").strip().lower()
        inbound_edges = self._ddg.inboundEdges(int(vertex))
        for edge in inbound_edges:
            print(edge)

    def outbound_edges_ui(self):
        vertex = input("Enter the vertex:").strip().lower()
        outbound_edges = self._ddg.outboundEdges(int(vertex))
        for edge in outbound_edges:
            print(edge)

    def random_graph_ui(self):
        ddg = DirectedGraph()
        vertices = input("Enter the vertex count:")
        edges = input("Enter the edge count")
        generate(ddg,int(vertices), int(edges))
        self._ddg = ddg

    def write_to_file_ui(self):
        file_name = input("Enter the name of the file:")
        writeToFile(self._ddg, file_name)

    def isolated_vertices_UI(self):
        for isolated in self._ddg.isolated_vertices():
            print(isolated)

    def min_lenght_path(self):
        source = input("Enter a source vertex:")
        dest = input("Enter a destination vertex")
        if self._ddg.isVertex(int(source)) is False or self._ddg.isVertex(int(dest)) is False:
            print("The provided vertices are not in the graph")
            return
        path = lowestLengthPath(self._ddg, int(source), int(dest))
        length = len(path)-1
        if length == -1:
            print ("There is no minimum length path from " + source + " to " + dest)
        else:
            result = "Minimum length path from vertex " + source + " to vertex " + dest + ": " + str(path) + ", Length: " + str(length)
            print(result)

    def min_cost_path(self):
        source = input("Enter a source vertex:")
        dest = input("Enter a destination vertex")
        if self._ddg.isVertex(int(source)) is False or self._ddg.isVertex(int(dest)) is False:
            print("The provided vertices are not in the graph")
            return
        lowestCostWalk(self._ddg, int(source), int(dest))

if __name__ == "__main__":
    c = UI()
    c.console()