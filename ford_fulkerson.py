from collections import defaultdict
import SAP

class FordFulkerson:
    def __init__(self):
        pass

    def ford_fulkerson(self, source, sink, edges, dijkstra_variation):
        # Create a residual graph with capacities initialized to the original capacities
        residual_graph = self.initialize_residual_graph(edges)
        # print(edges)
        # Initialize metrics
        paths = 0
        total_length = 0
        max_length = 0
        iteration = 0
        no_of_edges = len(edges)

        while True:
            dijkstra = SAP.SAPDijkstra()
            if dijkstra_variation == 1:
                # Find a shortest augmenting path using SAP-Dijkstra
                augmenting_paths = dijkstra.sap_dijkstra(source, sink, edges, list(residual_graph.keys()))
            elif dijkstra_variation == 2:
                # Find the augmenting path using DFS-like Dijkstra
                augmenting_paths = dijkstra.dfs_like_dijkstra(source, sink, edges, list(residual_graph.keys()))
            
            elif dijkstra_variation == 3:
                # Find the augmenting path using DFS-like Dijkstra
                augmenting_paths = dijkstra.random_dijkstra(source, sink, edges, list(residual_graph.keys()))
                
            if len(augmenting_paths[0]) < 2:
                break  # No more augmenting paths, terminate the loop
            
            # Find the bottleneck capacity along the augmenting path
            bottleneck_capacity = float('inf')
            for i in range(len(augmenting_paths[0]) - 1):
                u, v = augmenting_paths[0][i], augmenting_paths[0][i+1]
                bottleneck_capacity = min(bottleneck_capacity, self.get_capacity(residual_graph, u, v))

            # Update residual capacities along the augmenting path
            for i in range(len(augmenting_paths[0]) - 1):
                u, v = augmenting_paths[0][i], augmenting_paths[0][i+1]
                self.update_capacity(residual_graph, edges, u, v, bottleneck_capacity)
            
            
            # Update metrics
            paths += 1
            total_length += len(augmenting_paths[0]) - 1
            max_length = max(max_length, len(augmenting_paths[0]) - 1)

            
            # print(edges)
            iteration = iteration + 1
            #print(f"Iteration: {iteration}")
            #print(f"Paths: {paths}")
            continue
            
        return residual_graph, paths, total_length, max_length, no_of_edges



    def initialize_residual_graph(self, edges):
        # Create a defaultdict to represent the residual graph
        residual_graph = defaultdict(list)

        for u, v, capacity in edges:
            residual_graph[u].append((v, capacity))
            residual_graph[v].append((u, 0))  # Initialize reverse edge with residual capacity

        return residual_graph
    
    def get_capacity(self, graph, u, v):
        # Helper function to get the capacity of the edge (u, v) in the graph
        for neighbor, capacity in graph[u]:
            if neighbor == v:
                return capacity
        return 0
    
    def update_capacity(self, graph, edges, u, v, flow):
        # Helper function to update the capacity of the edge (u, v) in the graph
        for i, (neighbor, capacity) in enumerate(graph[u]):
            if neighbor == v:
                graph[u][i] = (neighbor, capacity - flow)
                edges.remove((u, v, capacity))
                edges.append((u, v, capacity - flow))
                break
        
        # Update the reverse edge (v, u) with the residual capacity
        for i, (neighbor, capacity) in enumerate(graph[v]):
            if neighbor == u:
                graph[v][i] = (neighbor, capacity + flow)
                break