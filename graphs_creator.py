import os
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import getopt, sys

def store_graph(vertices, edges, num_vertices, percentage, graph):
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", 'w')
    file.write(str({str(key): value for key, value in vertices.items()}) + "\n" + str({str(key): value for key, value in edges.items()}))
    file.close()
    
    nx.draw(graph, pos=vertices, with_labels = True, node_color='lightblue')
    plt.savefig("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
    plt.clf()

def calculate_max_num_edges(num_vertices):
    return num_vertices * (num_vertices - 1) / 2

def create_edges_and_graph(percentage_max_num_edges, vertices, num_vertices):
    G, edges = nx.Graph(), {}
    num_edges = math.ceil(percentage_max_num_edges * calculate_max_num_edges(num_vertices))
    isolated_vertices = list(vertices.keys())

    for edge in range(num_edges):
        if len(isolated_vertices) != 0:
            vertice1 = random.choice(isolated_vertices)
            isolated_vertices.remove(vertice1) 
            if len(isolated_vertices) != 0:
                vertice2 = random.choice(isolated_vertices)
                isolated_vertices.remove(vertice2)
                edges[vertice1] = [vertice2] 
                edges[vertice2] = [vertice1] 
                G.add_node(vertice1)
                G.add_node(vertice2)
            else:
                vertice2 = random.choice( [vertice for vertice in list(vertices.keys()) if vertice != vertice1] )
                edges[vertice1] = [vertice2] 
                edges[vertice2] = edges[vertice2] + [vertice1] 
                G.add_node(vertice1)
        else:
            vertice1 = random.choice([vertice for vertice in list(vertices.keys()) if len(edges[vertice]) < num_vertices - 1])
            vertice2 = random.choice( [vertice for vertice in list(vertices.keys()) if ( (vertice != vertice1) and (vertice not in edges[vertice1]) ) ] )
            edges[vertice1] = edges[vertice1] + [vertice2] 
            edges[vertice2] = edges[vertice2] + [vertice1] 
        G.add_edge(vertice1, vertice2)

    return edges, G

def create_vertices(vertices_num, max_value_coordinate):
    vertices = {}

    for vertice_name in range(1, vertices_num + 1):

        while True:
            x = random.randint(1, max_value_coordinate)
            y = random.randint(1, max_value_coordinate)
            if (x,y) not in vertices.values() and all(math.dist(coord, (x,y)) > 1 for coord in vertices.values()):
                vertices[vertice_name] = x,y
                break

    return vertices

def create_graphs(vertices_num_last_graph, max_value_coordinate):
    for vertices_num in range(2, vertices_num_last_graph + 1):
        vertices = create_vertices(vertices_num, max_value_coordinate)
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            edges, graph = create_edges_and_graph(percentage, vertices, vertices_num)
            store_graph(vertices, edges, vertices_num, percentage, graph)

def read_arguments():
    # Remove 1st argument from the list of command line arguments
    argumentList = sys.argv[1:]
    
    # Options
    options = "v:m:"
    long_options = ["Vertices_Num_Last_Graph", "Max_Value_Coordinate"]
    
    vertices_num_last_graph, max_value_coordinate = 10,20
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # Checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-v", "--Vertices_Num_Last_Graph"):
                vertices_num_last_graph = int(currentValue)
            elif currentArgument in ("-m", "--Max_Value_Coordinate"):
                max_value_coordinate = int(currentValue)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
    return vertices_num_last_graph, max_value_coordinate

def main():
    # Create the results folders if they don't exist already
    if not os.path.isdir("graphs"): 
        os.mkdir("graphs")
        
    random.seed(98513)

    print("Create graphs...")
    create_graphs(*read_arguments())

if __name__ == "__main__":
    main()