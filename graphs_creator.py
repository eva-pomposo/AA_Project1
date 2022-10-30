import random
import networkx as nx
import matplotlib.pyplot as plt
import math
from itertools import product

MIN_VALUE_COORDINATE = 1
MAX_VALUE_COORDINATE = 20
ALL_COORDINATE_POSSIBILITIES = list([coord for coord in product(range(MIN_VALUE_COORDINATE, MAX_VALUE_COORDINATE + 1), repeat = 2)])
VERTICES_NUM_LAST_GRAPH = 10

def store_graph(vertices, edges, num_vertices, percentage, graph):
    print(str({str(key): value for key, value in vertices.items()}) + "\n" + str({str(key): value for key, value in edges.items()}))
    
    file = open("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".txt", 'w')
    file.write(str({str(key): value for key, value in vertices.items()}) + "\n" + str({str(key): value for key, value in edges.items()}))
    file.close()
    
    nx.draw(graph, pos=vertices, with_labels = True, node_color='lightblue')
    plt.savefig("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage) + ".png")
    plt.clf()

def calculate_max_num_edges(num_vertices):
    return num_vertices * (num_vertices - 1) / 2

def create_edges_and_graph(percentage_max_num_edges, vertices, num_vertices):
    G = nx.Graph() 
    edges = {}
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

def create_vertices(vertices_num):
    vertices = {}

    for vertice_name in range(1, vertices_num + 1):
        vertices[vertice_name] = random.choice( ALL_COORDINATE_POSSIBILITIES )
        ALL_COORDINATE_POSSIBILITIES.remove(vertices[vertice_name])
        
    return vertices

def create_graphs(vertices_num_in_larger_graph):
    for vertices_num in range(2, vertices_num_in_larger_graph + 1):
        vertices = create_vertices(vertices_num)
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            edges, graph = create_edges_and_graph(percentage, vertices, vertices_num)
            store_graph(vertices, edges, vertices_num, percentage, graph)

def main():
    random.seed(98513)

    #  distância entre dois vértices tem de ser superior a 1
    coordinates_to_remove = []

    for coord_index in range(len(ALL_COORDINATE_POSSIBILITIES)):
        if ALL_COORDINATE_POSSIBILITIES[coord_index] not in coordinates_to_remove:
            for next_coord in ALL_COORDINATE_POSSIBILITIES[(coord_index + 1):]:
                if (next_coord not in coordinates_to_remove) and (math.dist(ALL_COORDINATE_POSSIBILITIES[coord_index], next_coord) <= 1):
                        coordinates_to_remove.append(next_coord)

    [ ALL_COORDINATE_POSSIBILITIES.remove(coord) for coord in coordinates_to_remove ]

    create_graphs(VERTICES_NUM_LAST_GRAPH)

if __name__ == "__main__":
    main()