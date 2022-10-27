import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math

MIN_VALUE_COORDINATE = 1
MAX_VALUE_COORDINATE = 20

def calculate_max_num_edges(num_vertices):
    return num_vertices * (num_vertices - 1) / 2

def create_edges(percentage_max_num_edges, vertices):
    #G = nx.Graph()
    
    edges = {}
    num_vertices = len(vertices)
    num_edges = math.ceil(percentage_max_num_edges * calculate_max_num_edges(num_vertices))
    #matriz de adjacencia, a primeira linha e a primeira coluna representam a primeira chave de vertices, e assim sucessivamente
    adjacency_matrix = np.zeros((num_vertices, num_vertices), dtype=int)
    vertices_index_in_adjacency_matrix = list(range(num_vertices))
    print("FORRRRRRR")
    for edge in range(num_edges):
        if len(vertices_index_in_adjacency_matrix) != 0:
            vertice1 = random.choice(vertices_index_in_adjacency_matrix)
            vertices_index_in_adjacency_matrix.remove(vertice1)
            if len(vertices_index_in_adjacency_matrix) != 0:
                vertice2 = random.choice(vertices_index_in_adjacency_matrix)
                vertices_index_in_adjacency_matrix.remove(vertice2)
            else:
                vertice2 = random.choice( [number for number in range(num_vertices) if number != vertice1] )
                        
                '''
                tmp = adjacency_matrix[vertice1]
                tmp = list(np.where(tmp == 0)[0])
                tmp.remove(vertice1)
                vertice2 = random.choice(tmp)
                '''

                '''
                while True:
                    vertice2 = random.randrange(0,num_vertices)
                    if adjacency_matrix[vertice2][vertice1] == 0:
                        break
                '''
        else:
            return
            vertice1 = random.randrange(0,num_vertices)
            vertice2 = random.choice( [number for number in range(num_vertices) if number != vertice1] )
            '''
            vertice1 = random.choice(list(set(np.where(adjacency_matrix == 0)[0])))
            tmp = adjacency_matrix[vertice1]
            tmp = list(np.where(tmp == 0)[0])
            tmp.remove(vertice1)
            vertice2 = random.choice(tmp)
            '''
            
            '''
            vertice1 = random.randrange(0,num_vertices)
            while True:
                vertice1 = random.randrange(0,num_vertices)
                print(adjacency_matrix[vertice1])
                print(adjacency_matrix[vertice1][0:vertice1:num_vertices-1])
                if not np.all(adjacency_matrix[vertice1][0:vertice1:num_vertices-1] == 1):
                    break
            while True:
                vertice2 = random.randrange(0,num_vertices)
                if adjacency_matrix[vertice2][vertice1] == 0:
                    break    
            '''
        adjacency_matrix[vertice1][vertice2] = 1
        adjacency_matrix[vertice2][vertice1] = 1

        #renomear a variavel de indice para o nome mesmo
        vertice1 += 1
        vertice2 += 1

        if vertice1 in edges:
            edges[vertice1] = edges[vertice1] + [vertice2] 
        else:
            edges[vertice1] = [vertice2] 

        if vertice2 in edges:
            edges[vertice2] = edges[vertice2] + [vertice1] 
        else:
            edges[vertice2] = [vertice1] 

        #print(vertice1)
        #print(vertice2)
        #print(G.nodes)
        #G.add_edge(vertice1, vertice2)
        #print(G.nodes)

    np.savetxt("graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage_max_num_edges) + ".txt",adjacency_matrix, fmt="%1u", header=str(vertices))
    #nx.draw(G, with_labels=True, node_size=2000, edge_color='#eb4034', width=3, font_size=16, font_weight=500, arrowsize=20, alpha=0.8)
    #plt.savefig("graph_num_vertices_" + str(num_vertices) + "_percentage_" + str(percentage_max_num_edges) + ".png")

def create_vertices(vertices_num):
    vertices = {}

    for vertice_name in range(vertices_num):

        #To do: estabelecer que a distância entre dois vértices tem de ser superior a 1, se necessário use uma grelha maior, coordenadas (x,y) de 1 a 100 ou mesmo mais
        #n fazer no while true pode demorar em tempo
        while True:
            x = random.randint(MIN_VALUE_COORDINATE, MAX_VALUE_COORDINATE)
            y = random.randint(MIN_VALUE_COORDINATE, MAX_VALUE_COORDINATE)
            if (x,y) not in vertices.values():
                vertices[vertice_name + 1] = x,y
                break
    return vertices

def create_graphs(vertices_num_in_larger_graph):
    for vertices_num in range(2, vertices_num_in_larger_graph + 1):
        vertices = create_vertices(vertices_num)
        create_edges(0.125, vertices)
        create_edges(0.25, vertices)
        create_edges(0.50, vertices)
        create_edges(0.75, vertices)

def main():
    random.seed(98513)
    create_graphs(10)

if __name__ == "__main__":
    main()


# https://www.programiz.com/dsa/graph-adjacency-matrix