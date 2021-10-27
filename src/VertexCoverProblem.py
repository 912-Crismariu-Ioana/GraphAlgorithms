from graph import UndirectedGraph, readingFunc1, readingFunc2
import copy


# A vertex cover of a graph G is a set of vertices which cover all the edges of the graph
# The vertex cover problem: What is the minimum size vertex cover in G?

# Algorithm 1: Approximation Algorithm for Vertex Cover

def vertex_cover_approx(ud):
    '''
    Finds a minimum subset S of the set of all vertices such that
    every edge of the graph is incident to at least one vertex in S
    :param ud: An undirected graph
    :return: The subset S that covers all the edges -> The vertex cover returned
    is actually twice the optimal cover
    '''

    # This is the set where we will add vertices that are part of the solution
    cover = set()

    # The visited dictionary maps every vertex of the graph to a boolean value
    # Instead of 'removing' edges, we will mark one of or both vertices that are endpoints of a deleted edge as visited
    visited = {}
    for vertex in ud.parseX():
        visited[vertex] = False

    # Consider every edge one by one
    for u in ud.parseX():
        # If the vertex is not the endpoint of a deleted edge
        if visited[u] is False:
            # We parse the adjacent vertices
            for v in ud.parseAdjacent(u):
                if visited[v] is False:
                    # We stop once we find the first edge that was not yet deleted
                    # By marking both endpoints as visited, we can be sure
                    # That edges which are incident to either of them
                    # will no longer be taken into consideration
                    # i.e. the other endpoints will not be part of the solution
                    visited[u] = True
                    visited[v] = True
                    break

    # Add visited vertices that were randomly selected earlier to the solution subset
    for vertex in visited.keys():
        if visited[vertex] is True:
            cover.add(vertex)

    return cover


# Algorithm 2: Clever Greedy Approach

def vertex_cover_greedy(ud):
    '''
    Finds a minimum subset S of the set of all vertices such that
    every edge of the given graph is incident to at least
    one vertex in S. What differentiates the greedy approach
     from the earlier approximation algorithm is favouring vertices
    of highest degree instead of picking random endpoints
    of the edges of the graph
    :param ud: An undirected graph
    :return: The subset S that covers all the edges -> The solution is not always optimal
    but it is an acceptable approximation
    '''
    # This is the set where we will add vertices that are part of the solution
    cover = set()
    # The candidates dictionary maps every vertex of the graph to its degree in order to simplify the selection process
    # We ignore isolated vertices as they will not be included in the solution
    candidates = {}
    for vertex in ud.parseX():
        if ud.degree(vertex) > 0:
            candidates[vertex] = ud.degree(vertex)
    # We make a copy of the candidate dictionary so we can modify it in order to signal that an edge was deleted
    remaining_edges = copy.deepcopy(candidates)
    # We keep a count of how many edges are left abd we initialize it with the total number of edges
    remaining_edge_count = ud.edgeCount

    while remaining_edge_count > 0:
        # While we still have uncovered egdes
        # Pick the vertex of highest degree
        candidate = max(candidates, key=lambda vrtx: candidates[vrtx])
        # Remove it from the candidate dictionary
        candidates.pop(candidate)
        # Add it to the solution
        cover.add(candidate)
        for adj in ud.parseAdjacent(candidate):
            # We 'delete' edges that are incident to our candidate
            # By decrementing the degree of the other endpoint
            # To keep an accurate number of remaining edges for each vertex
            if remaining_edges[adj] > 0:
                remaining_edges[adj] -= 1
        # We subtract the number of edges incident to our candidate from the total number of edges
        remaining_edge_count -= remaining_edges[candidate]
        # Set the number of incident edges of the candidate to 0
        remaining_edges[candidate] = 0
    return cover




