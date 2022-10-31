import json
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
    sorted_edges = dict(sorted(edges.items(), key = lambda entry: len(entry[1]), reverse=True))
    sorted_edges = { key:sorted(value, key = lambda vertice: list(sorted_edges.keys()).index(vertice)) for key,value in sorted_edges.items() }
    result = set()

    while sorted_edges:
        vertice1_max_adjacency = list(sorted_edges.keys())[0]
        vertice1_adjacency_list = sorted_edges[vertice1_max_adjacency]
        vertice2_max_adjacency = vertice1_adjacency_list[0]
        vertice2_adjacency_list = []
        
        result.add((vertice1_max_adjacency, vertice2_max_adjacency))
        del sorted_edges[vertice1_max_adjacency]
    
        if vertice2_max_adjacency in sorted_edges.keys():
            vertice2_adjacency_list = sorted_edges[vertice2_max_adjacency]
            del sorted_edges[vertice2_max_adjacency]

        for vertice in vertice1_adjacency_list:
            if vertice in sorted_edges.keys():
                lst = sorted_edges[vertice] 
                lst.remove(vertice1_max_adjacency)
                if len(lst) != 0:
                    sorted_edges[vertice] = lst
                else:
                    del sorted_edges[vertice]

        for vertice in vertice2_adjacency_list:
            if vertice in sorted_edges.keys():
                lst = sorted_edges[vertice] 
                lst.remove(vertice2_max_adjacency)
                if len(lst) != 0:
                    sorted_edges[vertice] = lst
                else:
                    del sorted_edges[vertice]
                
    return result

def main():
    solutions = []
    for vertices_num in range(2, 11):
        for percentage in [0.125, 0.25, 0.50, 0.75]:
            vertices, edges = read_graph(vertices_num, percentage)
            print("Vertices num: ", str(vertices_num), " percentage: " + str(percentage) )
            solution_edges = min_edge_dominating_set(vertices, edges)
            print(solution_edges)
            solutions.append((vertices, solution_edges, vertices_num, percentage))
    
    print("Criar imagens...")
    for solution in solutions:
        create_graphic_image(*solution)

if __name__ == "__main__":
    main()