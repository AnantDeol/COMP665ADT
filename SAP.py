from collections import deque
import heapq
import numpy as np

class SAPDijkstra:
    def __init__(self):
        pass

    def sap_dijkstra(self, source, sink, edges, vertices):
        distances = dict((vertex, float('inf')) for vertex in vertices)
        predecessors = dict((vertex, None) for vertex in vertices)
        distances[source] = 0

        # Initialize the priority queue (Q) with starting vertices and distances
        Q = deque([(vertex, distances[vertex]) for vertex in vertices])

        while Q:
            current_vertex, current_distance = Q.popleft()
            neighbors = [n[1] for n in edges if n[0] == current_vertex and n[2] > 0]
            for neighbor in neighbors:
                if distances[neighbor] > current_distance + 1: # Taking edge lengths as 1
                    distances[neighbor] = current_distance + 1
                    predecessors[neighbor] = current_vertex
                    Q.append((neighbor, distances[neighbor]))
        
        augmenting_paths = self.reconstruct_path(predecessors, sink)  
    
        print("Augmenting Path: {}".format(augmenting_paths))
        return augmenting_paths
    
    def dfs_like_dijkstra(self, source, sink, edges, vertices):
        distances = dict((vertex, float('inf')) for vertex in vertices)
        predecessors = dict((vertex, None) for vertex in vertices)
        counter = 1e9  # Start with a large counter value

        distances[source] = 0

        # Initialize the queue with starting vertex and distance
        Q = [(0, source)]
        heapq.heapify(Q)

        while Q:
            current_distance, current_vertex = heapq.heappop(Q)
            neighbors = [n[1] for n in edges if n[0] == current_vertex and n[2] > 0]
            for neighbor in neighbors:
                if distances[neighbor] == float('inf'):
                    counter -= 1  # Decrease the key value for v from a large value to a decreasing counter value
                    distances[neighbor] = counter             
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(Q, (distances[neighbor], neighbor))     

        augmenting_paths = self.reconstruct_path(predecessors, sink)

        print("Augmenting Path: {}".format(augmenting_paths))
        return augmenting_paths
    
    def random_dijkstra(self, source, sink, edges, vertices):
        distances = dict((vertex, float('inf')) for vertex in vertices)
        predecessors = dict((vertex, None) for vertex in vertices)

        distances[source] = 0

        # Initialize the queue with starting vertex and distance
        Q = [(0, source)]
        heapq.heapify(Q)

        while Q:
            current_distance, current_vertex = heapq.heappop(Q)
            neighbors = [n[1] for n in edges if n[0] == current_vertex and n[2] > 0]
            for neighbor in neighbors:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = np.random.randint(1, 1000000)            
                    predecessors[neighbor] = current_vertex
                    heapq.heappush(Q, (distances[neighbor], neighbor))     

        augmenting_paths = self.reconstruct_path(predecessors, sink)

        print("Augmenting Path: {}".format(augmenting_paths))
        return augmenting_paths


    def reconstruct_path(self, predecessors, sink):
        path = []
        current = sink
        while current is not None:
            path.insert(0, current)  # Tracing from sink to back, adding a new element on the left of the list
            current = predecessors[current]
        return [path]
