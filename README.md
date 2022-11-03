# Algoritmos Avançados 1st Project — Exhaustive Search

## Introduction

Problem 20 – Find a minimum edge dominating set for a given undirected graph G(V, E), with n vertices and m edges. An edge dominating set of G is a subset D of edges, such that every edge not in D is adjacent to, at least, one edge in D. A minimum edge dominating set is an edge dominating set of smallest possible size.

Design and test an exhaustive search algorithm to solve the graph problem described above, as well as another method using a greedy heuristics.

Afterwards, analyze the computational complexity of the developed algorithms. To accomplish that:
* Perform a formal computational complexity analysis of the algorithms.
* Carry out a sequence of experiments, for successively larger problem instances, to register and analyze (1) the number of basic operations carried out, (2) the execution time and (3) the number of solutions / configurations tested.
* Compare the results of the experimental and the formal analysis.
* Determine the largest graph that you can process on your computer, without taking too much time.
* Estimate the execution time that would be required by much larger problem instances.
* Write a report (8 pages, max.).

## Graphs for the Computational Experiments

The graph instances used in the computational experiments should represent the following scenario:
* graph vertices are 2D points on the XOY plane, with integer valued coordinates between 1 and 20.
* graph vertices should neither be coincident nor too close.
* the number of edges sharing a vertex is randomly determined.

Generate successively larger random graphs, with 4, 5, 6, ... vertices, using your student number as seed.
Use 12.5%, 25%, 50% and 75% of the maximum number of edges for the number of vertices.

Suggestion: store each graph in a file to be used for the computational experiments.

Depending on the problem, it might be helpful to represent each graph by its adjacency matrix or by its incidence matrix.
It might also be useful to graphically visualize the graph instances and the computed solutions.

## How to run

### Start by installing the requeriments, creating a virtual environment for that:
```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip
pip install -r requeriments.txt
```

### CLI optional arguments 

## Author
Eva Bartolomeu, Nmec 98513