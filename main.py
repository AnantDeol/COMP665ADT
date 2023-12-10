from __future__ import division  # For enabling true division in Python 2
from __future__ import with_statement

import source_sink_generator
import ford_fulkerson
import os
import csv

#os.chdir(r"C:\Users\anant\OneDrive\Documents\MEngg\COMP 6651 Algo\Project")


def main(n, r, upper_cap, file_path):

    opt = "g"

    if opt == "r":
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            headers = next(reader)  # Read the headers

            start_index = headers.index("StartNode")
            end_index = headers.index("EndNode")
            capacity_index = headers.index("Capacity")

            edges = []
            for row in reader:
                start_node = int(row[start_index])
                end_node = int(row[end_index])
                capacity = int(row[capacity_index])

                edges.append((start_node, end_node, capacity))

        GG = source_sink_generator.GraphGenerator()
        source = 229
        longest_path = GG.bfs_longest_path(source, edges)

        # Define the sink node as the last element of the longest path
        sink = longest_path[-1]

    elif opt == "g":

        graph_generator = source_sink_generator.GraphGenerator()
        source, sink, edges, vertices = graph_generator.generate_sink_source_graph(n, r, upper_cap)

    print "Source: %s, Sink: %s" % (source, sink)

    # Run Ford Fulkerson on the graph
    FF = ford_fulkerson.FordFulkerson()

    residual_graph, paths, total_length, max_length, no_of_edges = FF.ford_fulkerson(source, sink, edges, 3)

    mean_length = total_length / paths if paths > 0 else 0

    print "Paths: %s" % paths
    print "Mean Length: %s" % mean_length
    print "Mean Proportional Length: %s" % (mean_length / max_length if max_length > 0 else 0)
    print "Total Edges: %s" % no_of_edges


if __name__ == "__main__":
    n = 200
    r = 0.2
    upper_cap = 50
    file_path = r"C:\Users\anant\OneDrive\Documents\MEngg\COMP 6651 Algo\Project\graph.csv"
    main(n, r, upper_cap, file_path)
