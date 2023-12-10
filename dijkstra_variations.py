from collections import deque
import heapq
import random


class Dijkstra:
    def __init__(self):
        pass

    def sap_dijkstra(self, source, sink, residual_graph, vertices):
        distances = {vertex: float('inf') for vertex in vertices}
        predecessors = {vertex: None for vertex in vertices}
        distances[source] = 0

        # Initialize the priority queue (Q) with starting vertices and distances
        Q = deque([(vertex, distances[vertex]) for vertex in vertices])

        while Q:
            current_vertex, current_distance = Q.popleft()
            neighbors = [v for v, capacity in residual_graph[current_vertex] if capacity > 0]
            for neighbor in neighbors:
                if distances[neighbor] > current_distance + 1:  # Taking edge lengths as 1
                    distances[neighbor] = current_distance + 1
                    predecessors[neighbor] = current_vertex
                    Q.append((neighbor, distances[neighbor]))

        augmenting_paths = self.reconstruct_path(predecessors, sink)

        for i in augmenting_paths:
            print i
        return augmenting_paths

    def dfs_like_dijkstra(self, source, sink, residual_graph, vertices):
        distances = {vertex: float('inf') for vertex in vertices}
        predecessors = {vertex: None for vertex in vertices}
        counter = 1e9  # Start with a large counter value

        distances[source] = 0

        # Initialize the queue with starting vertex and distance
        Q = [(0, source)]
        heapq.heapify(Q)

        while Q:
            current_distance, current_vertex = heapq.heappop(Q)

            neighbors = [v for v, capacity in residual_graph[current_vertex] if capacity > 0]
            for neighbor in neighbors:
                if distances[neighbor] == float('inf'):
                    counter -= 1  # Decrease the key value for v from a large value to a decreasing counter value
                    distances[neighbor] = counter
                    predecessors[neighbor] = current_vertex
                    # print(f"Predecessor of {neighbor} is {current_vertex}")
                    heapq.heappush(Q, (distances[neighbor], neighbor))

        augmenting_paths = self.reconstruct_path(predecessors, sink)

        # print(f"Augmenting Path: {augmenting_paths}")
        # print(f"Visited: {visited}")
        return augmenting_paths

    def maxcap_dijkstra(self, source, sink, residual_graph, vertices):
        distances = {vertex: float('-inf') for vertex in vertices}
        predecessors = {vertex: None for vertex in vertices}
        distances[source] = float('inf')

        # Initialize the priority queue (Q) with starting vertices and distances
        Q = deque([(vertex, distances[vertex]) for vertex in vertices])

        while Q:
            current_vertex, current_distance = Q.popleft()

            neighbors = [(v, capacity) for v, capacity in residual_graph[current_vertex] if capacity > 0]
            for neighbor, capacity in neighbors:
                if min(distances[current_vertex], capacity) > distances[neighbor]:
                    distances[neighbor] = min(distances[current_vertex], capacity)
                    predecessors[neighbor] = current_vertex
                    Q.append((neighbor, distances[neighbor]))

        augmenting_paths = self.reconstruct_path(predecessors, sink)
        max_capacity = distances[sink]

        # print(f"Augmenting Path: {augmenting_paths}")
        # print(f"Max Cap: {max_capacity}")
        return augmenting_paths

    def random_dijkstra(self, source, sink, residual_graph, vertices):
        distances = {vertex: float('inf') for vertex in vertices}
        predecessors = {vertex: None for vertex in vertices}

        distances[source] = 0

        # Initialize the queue with starting vertex and distance
        Q = [(0, source)]
        heapq.heapify(Q)

        while Q:
            current_distance, current_vertex = heapq.heappop(Q)

            neighbors = [v for v, capacity in residual_graph[current_vertex] if capacity > 0]
            for neighbor in neighbors:
                if distances[neighbor] == float('inf'):
                    distances[neighbor] = random.randint(1, 1000000)
                    predecessors[neighbor] = current_vertex
                    # print(f"Predecessor of {neighbor} is {current_vertex}")
                    heapq.heappush(Q, (distances[neighbor], neighbor))

        augmenting_paths = self.reconstruct_path(predecessors, sink)

        # print(f"Augmenting Path: {augmenting_paths}")
        # print(f"Visited: {visited}")
        return augmenting_paths

    def reconstruct_path(self, predecessors, sink):
        path = []
        current = sink
        # print("Started reconstruction")
        while current is not None:
            # print(f"current: {current}")
            path.insert(0, current)  # Tracing from sink to back, adding new element on left of list
            current = predecessors[current]
            # print(f"Predecessor: {current}")
        return [path]
