import source_sink_generator
import ford_fulkerson
import os
import csv
#os.chdir(r"C:\Users\anant\OneDrive\Documents\MEngg\COMP 6651 Algo\Project")


def main(n, r, upper_cap, file_path):

    # If user choses to generate new graph
    if action == 0:

        #Generate graph
        graph_generator = source_sink_generator.GraphGenerator()
        source, sink, edges, vertices = graph_generator.generate_sink_source_graph(n, r, upper_cap)
    
    #If user choses to read a file
    elif action == 1:
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)

            try:
                # Read first row to retrieve n, r, upperCap, source and sink values
                first_row = next(reader)
                n = int(first_row[0])
                r = float(first_row[1])
                upper_cap = int(first_row[2])
                source = int(first_row[3])
                sink = int(first_row[4])

            except(StopIteration, IndexError):
                print("Error. Make sure the CSV file has correct n, r, upperCap, SourceNode and SinkNode values in the first row")

            edges= []
            for row in reader:
                try:
                    start_node = int(row[0])
                    end_node = int(row[1])
                    capacity = int(row[2])

                    edges.append((start_node, end_node, capacity))
                except (IndexError, ValueError):
                    print("Error reading a row. Make sure each row has at least 3 columns with integer values.")
    
    print("Source: {0}, Sink: {1}".format(source, sink))
    
    #Run Ford Fulkerson on the graph
    FF = ford_fulkerson.FordFulkerson()

    for dijkstra_variation in range(1, 5):
 
        residual_graph, paths, total_length, max_length, no_of_edges, flow = FF.ford_fulkerson(source, sink, edges, dijkstra_variation)

        mean_length = total_length/paths if paths > 0 else 0

        variation_names = {
            1: "Shortest Augmenting Path (SAP)",
            2: "DFS-like",
            3: "Maximum Capacity (MaxCap)",
            4: "Random"
        }

        variation_name = variation_names.get(dijkstra_variation)

        print("Variation: {0}".format(variation_name))
        print("Paths: {0}".format(paths))
        print("Mean Length: {0}".format(mean_length))
        print("Mean Proportional Length: {0}".format(mean_length / max_length if max_length > 0 else 0))
        print("Total Edges: {0}".format(no_of_edges))
        #print("Total Flow: {0}".format(flow))
        print()

        dijkstra_variation += 1


if __name__ == "__main__":

    while True:
        
        try:
            action = int(input("Select your action:\n0. Generate new graph\n1. Select a graph\n"))
        except ValueError:
            print("\n Wrong input, please try again.\n")
            continue

        if action not in [0,1]:
            print("\n Wrong input, please try again.\n")
            continue
                
        #Generate new graph
        elif action == 0: 
            n = int(input("Enter number of nodes:\n"))
            if n > 0:
                pass
            else:
               print("\n Wrong input, please try a number greater than 0")

            
            while True:
                r = float(input("Enter r (Max distance between nodes sharing an edge):\n"))

                if r > 0:
                    break
                else:
                    print("\n Wrong input, please try a value greater than 0")
                    continue

            while True:
                upper_cap = int(input("Enter maximum capacity value\n"))

                if upper_cap > 0:
                    break
                else:
                    print("\n Wrong input, please try a number greater than 0")
                    continue
            
            main(n, r, upper_cap, None) # Call the main function

        elif action == 1:
            file_name = input("Enter the file name (name.csv): ")
            directory_path = os.path.abspath(os.path.dirname(__file__))
            file_path = os.path.join(directory_path, file_name)
            try:
                if os.path.exists(file_path):
                    pass
                else:
                    print(f"Error: File path '{file_path}' does not exist.")
                    continue
            
            except Exception as e:
                #Handle other exceptions if needed
                print(f"An error occurred: {e}")
        
            main(None, None, None, file_path) # Call the main function
            break
        break
                
    # file_path = r"C:\Users\anant\OneDrive\Documents\MEngg\COMP 6651 Algo\Project\graph.csv"
    
