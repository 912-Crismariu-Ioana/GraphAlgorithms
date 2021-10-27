import math
from tabulate import tabulate


def printResult(costMatrix, prevMatrix, source, destination):
    # If the cost from any vertex to itself becomes negative then for sure we have a negative cost cycle
    for i in range(len(costMatrix)):
        if costMatrix[i][i] < 0:
            print("The graph has negative cost cycles")
            return

    if costMatrix[source][destination] == math.inf:
        print("There is no minimum cost walk between " + str(source) + " and " + str(destination))
        return
    else:
        print("The minimum cost walk between " + str(source) + " and " + str(destination) + " has the cost " + str(
            costMatrix[source][destination]))

    path = []
    interm_vertex = destination
    path.insert(0,interm_vertex)
    while interm_vertex is not source:
        interm_vertex = prevMatrix[source][interm_vertex]
        path.insert(0,interm_vertex)

    print ("And it has the path " + str(path))


def printMatrix(matrix):
    print(tabulate(matrix, tablefmt="plain"))
    print('\n')


def lowestCostWalk(ddg, source, destination):
    """
    Determines the minimum cost walk from a source vertex to a target vertex
    :param ddg: A directed graph
    :param source: A given source vertex
    :param destination: A given destination vertex
    :return:
    """
    # Retrieve the number of vertices
    n = ddg.vertexCount
    # Initialize the cost and destination

    # The cost matrix is a matrix whose elements will represent, after the final step of the algorithm,
    # the minimum cost walk from the all vertices to all vertices of the graph
    # The line number represents the source vertex while the column number represents the target vertex
    costMatrix = [[math.inf for j in range(n)] for i in range(n)]
    # In the case of the cost matrix, an "infinity" element suggests that there is no walk
    # between the vertices represented by the line number and column number respectively

    # The prev matrix is a matrix that will help in reconstructing the path having the minimum cost
    # The line number represents the source vertex while the column number represents the target vertex
    # Its elements represent the predecessors of the aforementioned target vertices in the path
    prevMatrix = [[-1 for j in range(n)] for i in range(n)]
    # In the case of the prev matrix, an "-1" element suggests that there is no path
    # between the vertices represented by the line number and column number respectively
    # or that the target and destination vertices are equal, hence there is no "previous" vertex

    for i in range(n):
        for j in range(n):
            if i == j:
                # We will set the cost to 0 for trivial walks
                costMatrix[i][j] = 0
            elif ddg.isEdge(i, j):
                # Update the matrices if there is an edge between the vertices in the current iteration
                costMatrix[i][j] = ddg.costEdge(i, j)
                prevMatrix[i][j] = i

    print("Initial Cost Matrix\n")
    printMatrix(costMatrix)
    print("Initial Previous matrix\n")
    printMatrix(prevMatrix)

    # We will add all vertices one by one to the set of intermediate vertices
    # After each iteration, the vertex nr. k will be added
    # to the set of intermediate vertices and we will have computed
    # the lowest cost paths between all pairs of vertices such that
    # these lowest cost paths only take into consideration vertices from the set
    # {0, 1, ..., k}
    for k in range(n):
        print("Using vertex " + str(k) + " as an intermediate vertex\n")
        # Choose source vertex
        for i in range(n):
            # Pick destination vertex
            for j in range(n):
                if costMatrix[i][j] > costMatrix[i][k] + costMatrix[k][j]:
                    # If vertex k is contained in the shortest path from i to j
                    # Then update the cost matrix
                    costMatrix[i][j] = costMatrix[i][k] + costMatrix[k][j]
                    prevMatrix[i][j] = prevMatrix[k][j]

        print("Cost Matrix\n")
        printMatrix(costMatrix)
        print("Previous matrix\n")
        printMatrix(prevMatrix)


    printResult(costMatrix, prevMatrix, source, destination)


