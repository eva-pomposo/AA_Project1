import itertools
import json
import math
import numpy as np

def read_graph(num_vertices, percentage):
    adjacency_matrix = np.loadtxt("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", dtype=int)
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", "r")
    vertices = file.readline()[1:-1].replace("'", "\"").replace("(", "[").replace(")", "]")
    edges = file.readline()[1:-1].replace("'", "\"")
    file.close()
    vertices = {int(key):(value[0], value[1]) for key,value in json.loads(vertices).items()}
    edges = {int(key):value for key,value in json.loads(edges).items()}
    return vertices, edges, adjacency_matrix

def min_edge_dominating_set(vertices, edges, adjacency_matrix):
    sorted_edges = dict(sorted(edges.items(), key = lambda entry: len(entry[1]), reverse=True))
    sorted_edges = { key:sorted(value, key = lambda vertice: list(sorted_edges.keys()).index(vertice)) for key,value in sorted_edges.items() }
    result = set()

    while sorted_edges:
        vertice1_max_adjacency = list(sorted_edges.keys())[0]
        vertice1_adjacency_list = sorted_edges[vertice1_max_adjacency]
        vertice2_max_adjacency = vertice1_adjacency_list[0]
        
        result.add((vertice1_max_adjacency, vertice2_max_adjacency))
        del sorted_edges[vertice1_max_adjacency]

        for vertice in vertice1_adjacency_list:
            if vertice in sorted_edges.keys():
                if vertice == vertice2_max_adjacency:
                    vertice2_adjacency_list = sorted_edges[vertice]
                del sorted_edges[vertice]

        for vertice in vertice2_adjacency_list:
            if vertice in sorted_edges.keys():
                del sorted_edges[vertice]
                
    return result

def main():
    for vertices_num in range(2, 11):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges, adjacency_matrix = read_graph(vertices_num, percentage)
            print("Vertices num: ", str(vertices_num), " percentage: " + str(percentage) )
            print(min_edge_dominating_set(vertices, edges, adjacency_matrix))

if __name__ == "__main__":
    main()