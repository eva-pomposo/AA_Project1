import itertools
import json
import networkx as nx
import matplotlib.pyplot as plt

VERTICES_NUM_LAST_GRAPH = 10

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
    max_num_edges = []
    edges_set = set()
    for vertice1 in edges:
        max_num_edges.append(len(edges[vertice1]))
        for vertice2 in edges[vertice1]:
            if (vertice2, vertice1) not in edges_set:
                edges_set.add((vertice1, vertice2))

    max_num_edges = int(sum(max_num_edges) / 2)

    for num_edges in range(1,max_num_edges):
        subsets = list(itertools.combinations(edges_set, num_edges))

        for subset in subsets:
            subset = set(subset)
            is_solution = True
            edges_not_in_subset = edges_set - subset
            for edge in edges_not_in_subset:
                #if all(edge[0] not in i for i in subset) and all(edge[1] not in i for i in subset):
                if all(edge[0] not in i and edge[1] not in i for i in subset):
                    is_solution = False
                    break
            if is_solution:
                return subset
    return edges_set

def main():
    solutions = []
    for vertices_num in range(2, VERTICES_NUM_LAST_GRAPH + 1):
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