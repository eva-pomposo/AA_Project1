import getopt
import json
import sys
import time
import networkx as nx
import matplotlib.pyplot as plt

def create_graphic_image(vertices, edges_set, num_vertices, percentage):
    G = nx.Graph() 
    for edge in edges_set:
        G.add_node(edge[0], pos=vertices[edge[0]])
        G.add_node(edge[1], pos=vertices[edge[1]])
        G.add_edge(*edge)
    nx.draw(G, pos=nx.get_node_attributes(G,'pos'), with_labels = True, node_color='lightblue')
    plt.savefig("results/greedy_heuristics/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
    plt.clf()

def read_graph(num_vertices, percentage):
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", "r")
    vertices = file.readline()[:-1].replace("'", "\"").replace("(", "[").replace(")", "]")
    edges = file.readline().replace("'", "\"")
    file.close()
    vertices = {int(key):(value[0], value[1]) for key,value in json.loads(vertices).items()}
    edges = {int(key):value for key,value in json.loads(edges).items()}
    return vertices, edges

def min_edge_dominating_set(vertices, edges):
    result, basic_operations_num = set(), 0
    sorted_edges = dict(sorted(edges.items(), key = lambda entry: len(entry[1]), reverse=True))
    sorted_edges = { key:sorted(value, key = lambda vertice: list(sorted_edges.keys()).index(vertice)) for key,value in sorted_edges.items() }

    while sorted_edges:
        vertice1_max_adjacency = list(sorted_edges.keys())[0]
        adjacent_vertices = sorted_edges[vertice1_max_adjacency]
        vertice2_max_adjacency = adjacent_vertices[0]
        
        result.add((vertice1_max_adjacency, vertice2_max_adjacency))
        del sorted_edges[vertice1_max_adjacency]
    
        if vertice2_max_adjacency in sorted_edges.keys():
            adjacent_vertices = adjacent_vertices + sorted_edges[vertice2_max_adjacency]
            del sorted_edges[vertice2_max_adjacency]

        for vertice in set(adjacent_vertices):
            if vertice in sorted_edges.keys():
                adjacency_list = sorted_edges[vertice] 
                if vertice1_max_adjacency in adjacency_list:
                    adjacency_list.remove(vertice1_max_adjacency)
                if vertice2_max_adjacency in adjacency_list:
                    adjacency_list.remove(vertice2_max_adjacency)
                if len(adjacency_list) != 0:
                    sorted_edges[vertice] = adjacency_list
                else:
                    del sorted_edges[vertice]
                
    return result, basic_operations_num
    
def read_arguments():
    # Remove 1st argument from the list of command line arguments
    argumentList = sys.argv[1:]
    
    # Options
    options = "v:"
    long_options = ["Vertices_Num_Last_Graph"]
    
    vertices_num_last_graph = 10
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        
        # Checking each argument
        for currentArgument, currentValue in arguments:
    
            if currentArgument in ("-v", "--Vertices_Num_Last_Graph"):
                vertices_num_last_graph = int(currentValue)
    except getopt.error as err:
        # Output error, and return with an error code
        print (str(err))
    return vertices_num_last_graph

def main():
    file = open("results/analyze_greedy.txt", 'w')
    file.write("vertices_num percentage_max_num_edges basic_operations_num execution_time\n")
    solutions = []
    
    for vertices_num in range(2, read_arguments() + 1):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges = read_graph(vertices_num, percentage)

            execution_time = time.time()
            solution_edges, basic_operations_num = min_edge_dominating_set(vertices, edges)
            execution_time = time.time() - execution_time

            file.write("%s %f %s %f\n" % (vertices_num, percentage, basic_operations_num, execution_time))
            solutions.append((vertices, solution_edges, vertices_num, percentage))
    
    file.close()
    
    print("Create and save image of solution graphs...")
    for solution in solutions:
        create_graphic_image(*solution)

if __name__ == "__main__":
    main()