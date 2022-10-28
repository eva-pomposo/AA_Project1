import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math
from itertools import product

MIN_VALUE_COORDINATE = 1
MAX_VALUE_COORDINATE = 20
ALL_COORDINATE_POSSIBILITIES = list([coord for coord in product(range(MIN_VALUE_COORDINATE, MAX_VALUE_COORDINATE + 1), repeat = 2)])

def create_graphic_image(vertices, edges, adjacency_matrix, percentage_max_num_edges):
    G = nx.Graph() 
    G.add_nodes_from(list(vertices.keys()))
    G.add_edges_from([ (vertice1,vertice2) for vertice1 in edges for vertice2 in edges[vertice1]])
    nx.draw(G, pos=vertices, with_labels = True, node_color='lightblue')
    plt.savefig("graphs/graph_num_vertices_" + str(len(vertices)) + "_percentage_" + str(percentage_max_num_edges) + ".png")
    plt.clf()

def calculate_max_num_edges(num_vertices):
    return num_vertices * (num_vertices - 1) / 2

def create_edges(percentage_max_num_edges, vertices):
    edges = {}
    num_vertices = len(vertices)
    num_edges = math.ceil(percentage_max_num_edges * calculate_max_num_edges(num_vertices))
    #matriz de adjacencia, a primeira linha e a primeira coluna representam a primeira chave de vertices, e assim sucessivamente
    adjacency_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
    isolated_vertices_index_in_adjacency_matrix = list(range(num_vertices))
    for edge in range(num_edges):
        if len(isolated_vertices_index_in_adjacency_matrix) != 0:
            vertice1_index = random.choice(isolated_vertices_index_in_adjacency_matrix)
            isolated_vertices_index_in_adjacency_matrix.remove(vertice1_index)
            if len(isolated_vertices_index_in_adjacency_matrix) != 0:
                vertice2_index = random.choice(isolated_vertices_index_in_adjacency_matrix)
                isolated_vertices_index_in_adjacency_matrix.remove(vertice2_index)
                edges[vertice1_index + 1] = [vertice2_index + 1] 
                edges[vertice2_index + 1] = [vertice1_index + 1] 
            else:
                vertice2_index = random.choice( [index for index in range(num_vertices) if index != vertice1_index] )
                edges[vertice1_index + 1] = [vertice2_index + 1] 
                edges[vertice2_index + 1] = edges[vertice2_index + 1] + [vertice1_index + 1] 
                '''
                tmp = adjacency_matrix[vertice1_index]
                tmp = list(np.where(tmp == 0)[0])
                tmp.remove(vertice1_index)
                vertice2_index = random.choice(tmp)
                '''
                '''
                while True:
                    vertice2_index = random.randrange(0,num_vertices)
                    if adjacency_matrix[vertice2_index][vertice1_index] == 0:
                        break
                '''
        else:
            #print(adjacency_matrix)
            #print(np.sum(adjacency_matrix, axis=1))
            #print(np.where(np.sum(adjacency_matrix, axis=1) != 2)[0])
            vertice1_index = random.choice([index for index in range(num_vertices) if len(edges[(index + 1)]) < num_vertices - 1])
            #print("key ", vertice1_index + 1)
            #print(edges)
            #print(edges[(vertice1_index + 1)])
            vertice2_index = random.choice( [index for index in range(num_vertices) if ( (index != vertice1_index) and ((index + 1) not in edges[(vertice1_index + 1)]) ) ] )
            #print(vertice2_index)
            edges[vertice1_index + 1] = edges[vertice1_index + 1] + [vertice2_index + 1] 
            edges[vertice2_index + 1] = edges[vertice2_index + 1] + [vertice1_index + 1] 

            '''
            vertice1_index = random.choice(list(set(np.where(adjacency_matrix == 0)[0])))
            tmp = adjacency_matrix[vertice1_index]
            tmp = list(np.where(tmp == 0)[0])
            tmp.remove(vertice1_index)
            vertice2_index = random.choice(tmp)
            '''
            '''
            vertice1_index = random.randrange(0,num_vertices)
            while True:
                vertice1_index = random.randrange(0,num_vertices)
                print(adjacency_matrix[vertice1_index])
                print(adjacency_matrix[vertice1_index][0:vertice1_index:num_vertices-1])
                if not np.all(adjacency_matrix[vertice1_index][0:vertice1_index:num_vertices-1] == 1):
                    break
            while True:
                vertice2_index = random.randrange(0,num_vertices)
                if adjacency_matrix[vertice2_index][vertice1_index] == 0:
                    break    
            '''
        adjacency_matrix[vertice1_index][vertice2_index] = 1
        adjacency_matrix[vertice2_index][vertice1_index] = 1

        #print(vertice1_index)
        #print(vertice2_index)
        #print(G.nodes)
        #G.add_edge(vertice1_index, vertice2_index)
        #print(G.nodes)

    np.savetxt("graphs/graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage_max_num_edges) + ".txt",adjacency_matrix, fmt="%1u", header=str(vertices) + "\n" + str(edges))
    return edges, adjacency_matrix

def create_vertices(vertices_num):
    vertices = {}
    used_coordinates = set()

    for vertice_index in range(vertices_num):
        vertices[vertice_index + 1] = random.choice( list(set(ALL_COORDINATE_POSSIBILITIES) - used_coordinates) )
        used_coordinates.add(vertices[vertice_index + 1])
        
        '''
        while True:
            x = random.randint(MIN_VALUE_COORDINATE, MAX_VALUE_COORDINATE)
            y = random.randint(MIN_VALUE_COORDINATE, MAX_VALUE_COORDINATE)
            if (x,y) not in vertices.values():
                vertices[vertice_index + 1] = x,y
                break
        '''
    return vertices

def create_graphs(vertices_num_in_larger_graph):
    for vertices_num in range(2, vertices_num_in_larger_graph + 1):
        vertices = create_vertices(vertices_num)
        edges, adjacency_matrix = create_edges(0.125, vertices)
        create_graphic_image(vertices, edges, adjacency_matrix, 0.125)
        edges, adjacency_matrix = create_edges(0.25, vertices)
        create_graphic_image(vertices, edges, adjacency_matrix, 0.25)
        edges, adjacency_matrix = create_edges(0.50, vertices)
        create_graphic_image(vertices, edges, adjacency_matrix, 0.5)
        edges, adjacency_matrix = create_edges(0.75, vertices)
        create_graphic_image(vertices, edges, adjacency_matrix, 0.75)

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

    create_graphs(10)

if __name__ == "__main__":
    main()


# https://www.programiz.com/dsa/graph-adjacency-matrix