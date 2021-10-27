
def lowestLengthPath(ddg, s, t):
    """
    Finds the lowest length path between two given vertices of a directed graph
    :param ddg: A directed graph
    :param s: The source vertex
    :param t: The destination vertex
    :return:  A list containing all the vertices that form the minimum length path, in order
    """
    # There is no need to continue with the algorithm if the vertices provided are not valid
    if ddg.isVertex(s) is False or ddg.isVertex(t) is False:
        return []

    # Likewise, there is no need to continue if the target and the destination are the same
    if s == t:
        return [s]

    # A list will be used to mimic the behaviour of the queue used in the BFS algorithm
    Queue = []

    # Prev will contain pairs, each of which correspond to a child(key)-parent(value) relationship between two vertices
    prev = {}

    # Dist maps vertices that are accessible from the starting vertex
    # to their minimum distance (number of edges) from the starting vertex
    dist = {}

    # Visited is a set containing all the vertices that were already verified in our search
    visited = set()

    # Enqueue the starting vertex
    Queue.append(s)
    # Mark it as visited
    visited.add(s)
    # Set distance to 0
    dist[s] = 0

    # Set a flag so we know when to stop
    found = False

    while len(Queue) != 0 and not found:
        # Dequeue vertex
        x = Queue.pop()
        # Parse the outbound neighbours (children) of the current vertex
        for y in ddg.parseDout(x):
            if y not in visited:
                # Enqueue the child
                Queue.insert(0, y)
                # Mark it as visited
                visited.add(y)
                # Compute the distance up to child vertex
                dist[y] = dist[x] + 1
                # Record the parent vertex
                prev[y] = x
                if y == t:
                    found = True
                    break

    # Reconstruct the path to the target vertex using the prev dictionary
    path = []
    target = t

    # Check if the target vertex was actually found
    if target in prev.keys():
        path.insert(0, target)
        while target in prev.keys():
            path.insert(0, prev[target])
            target = prev[target]

    return path













