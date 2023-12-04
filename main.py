import SAP
import Source_sink_generator_usingNumPy
import ford_fulkerson
import os
os.chdir(r"C:\Users\anant\OneDrive\Documents\MEngg\COMP 6651 Algo\Project")


def main(n, r, upper_cap):
    graph_generator = Source_sink_generator_usingNumPy.GraphGenerator()
    source, sink, edges, vertices = graph_generator.generate_sink_source_graph(n, r, upper_cap)
    
    print(f"Source: {source}, Sink: {sink}")

    FF = ford_fulkerson.FordFulkerson()

    residual_graph, paths, total_length, max_length, no_of_edges = FF.ford_fulkerson(source, sink, edges, 3)

    mean_length = total_length/paths if paths > 0 else 0

    print(f"Paths: {paths}")
    print(f"Mean Length: {mean_length}")
    print(f"Mean Proportional Length: {mean_length/max_length if max_length > 0 else 0}")
    print(f"Total Edges: {no_of_edges}")


    """aug_path = sap_dijkstra.sap_dijkstra(source, sink, edges, vertices)"""

    """for edge in edges:
        print(edge)
    print(f"Augmenting Path: {aug_path}")"""



if __name__ == "__main__":
    n = 200
    r = 0.2
    upper_cap = 50
    main(n, r, upper_cap)