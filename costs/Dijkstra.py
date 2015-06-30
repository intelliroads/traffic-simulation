from Queue import Queue
def dijkstra(car):
    src = car.position
    dest = car.destination
    graph = car.graph
    """ calculates a shortest path tree routed in src
    """
    # a few sanity checks
    visited=[]
    distances={}
    predecessors={}
    if src not in graph.nodes:
        raise TypeError('the root of the shortest path tree cannot be found in the graph')
    if dest not in graph.nodes:
        raise TypeError('the target of the shortest path cannot be found in the graph')
    # ending condition
    queue = Queue()
    queue.put(src)
    while queue:
        src = queue.get()
        if src.nodeId == dest.nodeId:
            # We build the shortest path and display it
            path = []
            pred = dest
            while pred != None:
                path.insert(0,pred)
                pred = predecessors.get(pred.nodeId, None)
            print('shortest path: ' + str(path) + " cost=" + str(distances[dest.nodeId]))
            return path
        else:
            # if it is the initial  run, initializes the cost
            if not visited:
                distances[src.nodeId] = 0
            # visit the neighbors
            for arc in src.outArcs:
                neighbor = arc.nodeB
                if neighbor not in visited:
                    new_distance = car.calc_next_event_time(arc) + distances.get(src.nodeId, float('inf'))
                    if new_distance < distances.get(neighbor.nodeId, float('inf')):
                        distances[neighbor.nodeId] = new_distance
                        predecessors[neighbor.nodeId] = src
            # mark as visited
            visited.append(src)
            unvisited = {}
            for k in graph.nodes:
                if k not in visited:
                    unvisited[k] = distances.get(k.nodeId, float('inf'))
            queue.put(min(unvisited, key=unvisited.get))






