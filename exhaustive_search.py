import getopt
import itertools
import json
import os
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
    plt.savefig("results/exhaustive_search/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
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
    max_num_edges, edges_set, basic_operations_num, configurations_tested = [], set(), 2, 0
    for vertice1 in edges:
        max_num_edges.append(len(edges[vertice1]))
        basic_operations_num += 3
        for vertice2 in edges[vertice1]:
            basic_operations_num += 1
            if (vertice2, vertice1) not in edges_set:
                edges_set.add((vertice1, vertice2))
                basic_operations_num += 1

    max_num_edges = int(sum(max_num_edges) / 2)
    basic_operations_num += 1

    for num_edges in range(1,max_num_edges):
        subsets = list(itertools.combinations(edges_set, num_edges))

        for subset in subsets:
            configurations_tested += 1
            subset, is_solution = set(subset), True
            edges_not_in_subset = edges_set - subset
            basic_operations_num += 4
            for edge in edges_not_in_subset:
                basic_operations_num += (2 * num_edges) + 1
                if all(edge[0] not in i and edge[1] not in i for i in subset):
                    is_solution = False
                    basic_operations_num += 1
                    break
            basic_operations_num += 1
            if is_solution:
                return subset, basic_operations_num, configurations_tested
    return edges_set, basic_operations_num, configurations_tested

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
    # Create the results folders if they don't exist already
    if not os.path.isdir("results"): 
        os.mkdir("results")
        os.mkdir("results/exhaustive_search")
    elif not os.path.isdir("results/exhaustive_search"):
        os.mkdir("results/exhaustive_search")
        
    file = open("results/analyze_exhaustive_search.txt", 'w')
    file.write("vertices_num percentage_max_num_edges basic_operations_num configurations_tested execution_time\n")
    solutions = []

    for vertices_num in range(2, read_arguments() + 1):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges = read_graph(vertices_num, percentage)

            execution_time = time.time()
            solution_edges, basic_operations_num, configurations_tested = min_edge_dominating_set(vertices, edges)
            execution_time = time.time() - execution_time

            file.write("%s %f %s %s %f\n" % (vertices_num, percentage, basic_operations_num, configurations_tested, execution_time))
            solutions.append((vertices, solution_edges, vertices_num, percentage))
    
    file.close()
    
    print("Create and save image of solution graphs...")
    for solution in solutions:
        create_graphic_image(*solution)
        
if __name__ == "__main__":
    main()