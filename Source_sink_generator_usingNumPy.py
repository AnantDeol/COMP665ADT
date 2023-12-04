import numpy as np
import csv
from collections import deque
import os


class GraphGenerator:
    def __init__(self):
        pass

    def generate_sink_source_graph(self, n, r, upper_cap):
        
        # Define a set of vertices V such that |V| = n
        vertices = np.arange(n)

        # Assign random Cartesian coordinates to each node
        coordinates = {u: np.random.rand(2) for u in vertices}

        # Generate edges based on Euclidean distances and assign capacities
        edges = set()
        for u in vertices:
            for v in vertices:
                if u != v and np.sum((coordinates[u] - coordinates[v]) ** 2) <= r ** 2:
                    rand = np.random.rand()
                    if rand < 0.5:
                        if (u, v) not in edges and (v, u) not in edges:
                            edges.add((u, v))
                    else:
                        if (u, v) not in edges and (v, u) not in edges:
                            edges.add((v, u))
        
        # Add capacity to each edge
        edges = [(u, v, np.random.randint(1, upper_cap)) for (u, v) in edges]

        # Randomly select a source node and apply BFS to find the longest acyclic path
        source_node_candidates = [edge[0] for edge in edges]
        source = np.random.choice(source_node_candidates)
        longest_path = self.bfs_longest_path(source, edges)

        # Define the sink node as the last element of the longest path
        sink = longest_path[-1]

        # Write the graph and capacities to a CSV file
        with open("source_sink_graph.csv", "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Source", "Sink", "Capacity"])
            for edge in edges:
                writer.writerow([edge[0], edge[1], edge[2]])
        
        return source, sink, edges, vertices

    """generate_sink_source_graph(10,2,25)"""

    def bfs_longest_path(self, source, edges):
        visited = set()
        queue = deque([(source, [])])  # Each element in the queue is a tuple (node, path)
        max_path = []

        while queue:
            node, path = queue.popleft()

            if node not in visited:
                visited.add(node)
                path = path + [node]

                neighbors = [n[1] for n in edges if n[0] == node]
                for neighbor in neighbors:
                    if neighbor not in path:
                        queue.append((neighbor, path))

                if len(path) > len(max_path):
                    max_path = path

        return max_path
