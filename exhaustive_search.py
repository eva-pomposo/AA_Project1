import json
import numpy as np

MIN_VALUE_COORDINATE = 1
MAX_VALUE_COORDINATE = 20

def read_graph(num_vertices, percentage):
    adjacency_matrix = np.loadtxt("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", dtype=int)
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", "r")
    vertices = file.readline()[1:-1].replace("'", "\"").replace("(", "[").replace(")", "]")
    edges = file.readline()[1:-1].replace("'", "\"")
    vertices = {int(key):(value[0], value[1]) for key,value in json.loads(vertices).items()}
    edges = {int(key):value for key,value in json.loads(edges).items()}
    file.close()
    return vertices, edges, adjacency_matrix

def main():
    percentages = [0.125, 0.25, 0.50, 0.75]

    for vertices_num in range(2, 11):
        for percentage in percentages:
            vertices, edges, adjacency_matrix = read_graph(vertices_num, percentage)

if __name__ == "__main__":
    main()