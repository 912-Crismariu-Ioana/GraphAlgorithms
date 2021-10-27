from graph import DirectedGraph
import networkx as nx
import matplotlib.pyplot as plt


def read_list_of_activities(ddg, duration, file_name):
    """
    Reads files containing activities in the format 'activity duration prerequisites'
    and populates a given graph structure accordingly
    :param ddg: A directed graph
    :param duration: A dictionary where each activity will be mapped to its corresponding
    duration in arbitrary time units
    :param file_name: The name of the file to be read
    :return:
    """
    ddg.clear()
    duration.clear()

    f = open(file_name, 'rt')
    lines = f.readlines()
    f.close()

    for j in range(len(lines)):
        edge = lines[j].strip().split(' ', 3)
        if len(edge) >= 2:
            vertex = edge[0].strip().lower()
            if not ddg.isVertex(vertex):
                ddg.addVertex(vertex)
                duration[vertex] = int(edge[1])

    for i in range(len(lines)):
        edge = lines[i].strip().split(' ', 3)
        if len(edge) >= 3:
            predecessors = edge[2].strip().split(',')
            for predecessor in predecessors:
                predecessor.strip().lower()
                if not ddg.isEdge(predecessor, edge[0]):
                    ddg.addEdge(predecessor, edge[0], 0)


def topo_sort_predecessors(ddg):
    """
    Performs a topological sorting of all the vertices of the graph
    using the predecessor counting algorithm
    if the given graph is a DAG, else detects circular dependencies
    :param ddg: A directed graph
    :return: A list of all the vertices sorted topologically,
    else an empty list if the graph is not a DAG
    """

    # The list to be filled with the vertices in topological order
    sorted = []
    # A queue that, at any point during the execution of the algorithm
    # will contain only vertices with no predecessors
    Queue = []
    # A dictionary that maps each vertex to the number of its predecessors
    count = {}
    for vertex in ddg.parseX():
        count[vertex] = ddg.getIndegree(vertex)
        # First enqueue only vertices with no predecessors in the given graph
        if count[vertex] == 0:
            Queue.insert(0,vertex)

    while len(Queue) > 0:
        # We take a vertex with no predecessors, add it to the sorted list
        # and 'eliminate' it from the graph by decrementing
        # the number of predecessors of its outbound neighbours
        # If the given graph is a DAG, naturally, every such outbound neighbour
        # will end up on the sorted list
        x = Queue.pop()
        sorted.append(x)
        for y in ddg.parseDout(x):
            count[y] = count[y] - 1
            if count[y] == 0:
                Queue.insert(0,y)

    # If the given graph is a DAG, we will run out of vertices with no predecessors quicker
    # and we will exit the loop before all vertices were processed and added to the sorted list
    if len(sorted) < ddg.vertexCount:
        sorted = []
    return sorted


def schedule_activities(duration, ddg):
    """
    Computes earliest and latest starting and finishing time
    for every activity represented by a vertex in a given graph
    :param duration: A dictionary that maps each activity (vertex of our given graph) to its duration
    in arbitrary time units
    :param ddg: A directed acyclic graph
    :return:
    """

    # Get the list of vertices sorted topologically
    sorted = topo_sort_predecessors(ddg)
    if len(sorted) == 0:
        print("The provided graph is not a directed acyclic graph, topological sorting cannot be performed")
        return

    # Copy the graph so that it may be altered for convenience
    result = ddg.deepcopy()

    # Initialize the two dictionaries that will map each activity to
    # its earliest time to start and finish respectively
    earliest_start_time = {}
    earliest_end_time = {}

    # We add two 'fictional' nodes that will mark the beginning and the end
    # of the project execution
    result.addVertex("start")
    result.addVertex("end")

    # The 'start' node will precede each real node with no predecessors
    # The 'end' node will succeed each real node with no successors
    for vertex in sorted:
        if result.getIndegree(vertex) == 0:
            result.addEdge("start", vertex, 0)
        if result.getOutdegree(vertex) == 0:
            result.addEdge(vertex, "end", 0)

    # Add the fictional nodes to the duration dictionary
    duration["start"] = 0
    duration["end"] = 0

    # Insert the fictional nodes in the sorted list at the first and last position respectively
    # so that the topological ordering is preserved
    sorted.insert(0,"start")
    sorted.append("end")

    earliest_start_time["start"] = 0
    earliest_end_time["start"] = 0

    # Each activity may start as soon as the latest of its prerequisites finish
    # Given that the activities are topologically sorted, we will always have the end time of each prerequisite
    # already computed and thus we may compare them
    for vertex in sorted[1:]:
        earliest_start_time[vertex] = max([earliest_end_time[predecessor] for predecessor in result.parseDin(vertex)])
        earliest_end_time[vertex] = earliest_start_time[vertex] + duration[vertex]

    # Initialize the two dictionaries that will map each activity to
    # its latest possible time to start and finish respectively
    latest_start_time = {}
    latest_end_time = {}

    # The total time needed to complete the project has to be the same, so we already know
    # the values for the last activity to be done (represented by the fictional 'end' vertex)
    end = earliest_end_time["end"]
    latest_end_time["end"] = end
    latest_start_time["end"] = latest_end_time["end"] - duration["end"]

    # Each activity may end as late as the earliest activity that depends on it starts
    # In order to obtain the latest start times of said dependant activities and compare them
    # we will reverse the list of the vertices sorted topologically
    for vertex in sorted[::-1][1:]:
        latest_end_time[vertex] = min([latest_start_time[successor] for successor in result.parseDout(vertex)])
        latest_start_time[vertex] = latest_end_time[vertex] - duration[vertex]

    printResult(earliest_start_time, latest_start_time, end)
    displayGraph(result)


def printResult(earliest_start_time, latest_start_time, total):
    for activity in earliest_start_time:
        print("Activity " + str(activity) + " may start as early as " + str(earliest_start_time[activity]) + " or as late as " + str(latest_start_time[activity]) + "\n")
    print("Critical activities: " + ','.join([x for x in earliest_start_time.keys() if earliest_start_time[x] == latest_start_time[x]]))
    print("Minimal time for execution is " + str(total))


def displayGraph(ddg):
    G = nx.DiGraph()
    for vertex in ddg.parseX():
        G.add_node(vertex)
    for edge in ddg.parseXY():
        G.add_edge(edge.origin, edge.destination)
    nx.draw(G, with_labels=True)
    plt.savefig('fig.png', bbox_inches='tight')
    # plt.show()













