import random
import csv
from collections import deque
from __future__ import with_statement, division


class GraphGenerator:
    def __init__(self):
        pass

    def generate_sink_source_graph(self, n, r, upper_cap):
        # Define a set of vertices V such that |V| = n
        vertices = range(n)

        # Assign random Cartesian coordinates to each node
        coordinates = {}
        for u in vertices:
            coordinates[u] = [random.random(), random.random()]

        # Generate edges based on Euclidean distances and assign capacities
        edges = set()
        for u in vertices:
            for v in vertices:
                if u != v and sum((coordinates[u][i] - coordinates[v][i]) ** 2 for i in range(2)) <= r ** 2:
                    rand = random.random()
                    if rand < 0.5:
                        if (u, v) not in edges and (v, u) not in edges:
                            edges.add((u, v))
                    else:
                        if (u, v) not in edges and (v, u) not in edges:
                            edges.add((v, u))

        # Add capacity to each edge
        edges = [(u, v, random.randint(1, upper_cap)) for (u, v) in edges]

        # Randomly select a source node and apply BFS to find the longest acyclic path
        source_node_candidates = [edge[0] for edge in edges]
        source = random.choice(source_node_candidates)
        longest_path = self.bfs_longest_path(source, edges)

        # Define the sink node as the last element of the longest path
        sink = longest_path[-1]

        # Write the graph and capacities to a CSV file
        with open("source_sink_graph.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["StartNode", "EndNode", "Capacity"])
            for edge in edges:
                writer.writerow([edge[0], edge[1], edge[2]])

        print 'Edges:', edges
        return source, sink, edges, vertices

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
