import itertools
import json
import numpy as np

def read_graph(num_vertices, percentage):
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", "r")
    vertices = file.readline()[:-1].replace("'", "\"").replace("(", "[").replace(")", "]")
    edges = file.readline().replace("'", "\"")
    file.close()
    vertices = {int(key):(value[0], value[1]) for key,value in json.loads(vertices).items()}
    edges = {int(key):value for key,value in json.loads(edges).items()}
    return vertices, edges

def min_edge_dominating_set(vertices, edges):
    max_num_edges = int(sum([len(edges[vertice1]) for vertice1 in edges]) / 2)
    
    edges_set = set()
    for vertice1 in edges:
        for vertice2 in edges[vertice1]:
            if (vertice2, vertice1) not in edges_set:
                edges_set.add((vertice1, vertice2))

    for num_edges in range(1,max_num_edges + 1):
        subsets = list(itertools.combinations(edges_set, num_edges))

        for subset in subsets:
            flag_not_break = True
            edges_not_in_subset = edges_set - set(subset)
            for edge in edges_not_in_subset:
                if all(edge[0] not in i for i in subset) and all(edge[1] not in i for i in subset):
                    flag_not_break = False
                    break
            if flag_not_break:
                return set(subset)
    return set()

def main():
    for vertices_num in range(2, 11):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges = read_graph(vertices_num, percentage)
            print("Vertices num: ", str(vertices_num), " percentage: " + str(percentage) )
            print(min_edge_dominating_set(vertices, edges))

if __name__ == "__main__":
    main()