import networkx as nx
from math import factorial as fac
import numpy as np
import collections
import matplotlib.pyplot as plt 
import random 

def binomial(x, y):
    try:
        binom = fac(x) // fac(y) // fac(x - y)
    except ValueError:
        binom = 0
    return binom

def plot_degree_dist(degrees, typeName):
    #create a dictionary from the degrees
    degrees = dict(degrees)
    #sort the dictionaries numerically
    degrees_values = sorted(degrees.values())
    #get frequencies
    freqdegrees = collections.Counter(degrees_values) 
    x = np.array(list(freqdegrees.keys()))
    y = np.array(list(freqdegrees.values()))
    #create the distribution
    y = y / (len(degrees))
    #plot on log-log
    plt.loglog(x, y, label=typeName) 
    #legend the graph
    plt.legend()
    
if __name__ == '__main__':
    #PART A
    #load in our data
    g = nx.read_adjlist(path="collaboration_network.txt", delimiter="\t", comments="#", create_using=nx.DiGraph(), nodetype=None, encoding="utf-8")
    #generate Erdos-Renyi random graph n=5,242 and p = n / (n 2)
    er = nx.erdos_renyi_graph(5242, 5242 / (binomial(5242, 2)))
    #generate a Watts-Strogatz "small world" graph
    sw = nx.Graph()
    #create the nodes
    nodes = list(range (5242))
    #generate edges between nodes, their neighbors, and their neighbor's neighbors
    edges = []
    for node in nodes:
        if node!=5241 and node!=5240:
            edges.append([nodes[node], nodes[node+1]])
            edges.append([nodes[node], nodes[node+2]])
        if node==5240:
            edges.append([nodes[node], nodes[node+1]])
            edges.append([nodes[node], nodes[0]])            
        if node==5241:
            edges.append([nodes[node], nodes[0]])
            edges.append([nodes[node], nodes[1]])
    #randomize 4k edges
    for i in range(4000):
        #select a random edge
        randomSelection = random.randrange(5242)
        #select a random node to change in the edge and update the edge
        randomNode = random.randrange(5242)
        edges[randomSelection][1] = randomSelection
    sw.add_edges_from(edges)
    
    #PART B
    #Plot all three degree distributions on log log
    plot_degree_dist(g.degree(), 'Collaboration Network')
    plot_degree_dist(er.degree(), 'ER Network')
    plot_degree_dist(sw.degree(), 'Small World')
    #Show the final graph
    plt.title("Log-log distribution of collaboration, ER, Small World")
    plt.show()
    
    #PART C
    #Create an undirected graph of the collaboration network with randomly assigned "trust/distrust" relations
    edgesCollab = []
    #Read the dataset
    readFile = open("collaboration_network.txt", "r")
    #Remove all newlines
    readFile = readFile.read().splitlines()
    #For each line we create an edge with either positive or negative relation
    for line in readFile:
        if line[0] == '#':
            continue
        parts = line.split('\t')
        edgesCollab.append((parts[0], parts[1]))
    h = nx.Graph()
    for x in edgesCollab:
        posOrNeg = random.randint(0, 1)
        if posOrNeg == 0:
            h.add_edge(x[0], x[1], data = "trust")
        if posOrNeg == 1:
            h.add_edge(x[0], x[1], data = "distrust")
        
    #Get the number of triangles of each type
    #Type A is 3 positive, type B is 2 Positive, Type C is 1 Positive, Type D is no Positives
    A = 0 
    B = 0 
    C = 0 
    D = 0
    triangles = [c for c in nx.cycle_basis(h) if len(c)==3]
    for triEdges in triangles:
        positive = 0
        if h[triEdges[0]][triEdges[1]]['data'] == "trust":
            positive = positive + 1
        if h[triEdges[1]][triEdges[2]]['data'] == "trust":
            positive = positive + 1
        if h[triEdges[2]][triEdges[0]]['data'] == "trust":
            positive = positive + 1
        if positive == 3:
            A = A+1
        if positive == 2:
            B = B+1
        if positive == 1:
            C = C+1
        if positive == 0:
            D = D+1
    
    print("Triangles of type A: ", A)
    print("Triangles of type B: ", B)
    print("Triangles of type C: ", C)
    print("Triangles of type D: ", D)
    
    #Get the fraction of positive and negative edges        
    positive = 0.00
    total = 0.00
    for u,v,data in h.edges(data=True):
        if data["data"] == "trust":
            positive = positive+1
        total = total + 1
    print("Fraction of positive edges: ", positive/total)
    print("Fraction of negative edges: ", (total-positive)/total)
    
    #Get the probability of each type of triangle
    #Input probabilities, rp, and rn is always equal to 1-rp
    rp = .30
    rn = 1-rp
    #Create an undirected graph of the collaboration network with randomly assigned "trust/distrust" relations based on rp and rn
    edgesCollab = []
    #Read the dataset
    readFile = open("collaboration_network.txt", "r")
    #Remove all newlines
    readFile = readFile.read().splitlines()
    #For each line we create an edge with either positive or negative relation
    for line in readFile:
        if line[0] == '#':
            continue
        parts = line.split('\t')
        edgesCollab.append((parts[0], parts[1]))
    z = nx.Graph()
    for x in edgesCollab:
        posOrNeg = random.random()
        if posOrNeg <= rp:
            z.add_edge(x[0], x[1], data = "trust")
        if posOrNeg > rp:
            z.add_edge(x[0], x[1], data = "distrust")
            
    #Get the number of triangles of each type
    #Type A is 3 positive, type B is 2 Positive, Type C is 1 Positive, Type D is no Positives
    A = 0 
    B = 0 
    C = 0 
    D = 0
    triangles = [c for c in nx.cycle_basis(z) if len(c)==3]
    for triEdges in triangles:
        positive = 0
        if z[triEdges[0]][triEdges[1]]['data'] == "trust":
            positive = positive + 1
        if z[triEdges[1]][triEdges[2]]['data'] == "trust":
            positive = positive + 1
        if z[triEdges[2]][triEdges[0]]['data'] == "trust":
            positive = positive + 1
        if positive == 3:
            A = A+1
        if positive == 2:
            B = B+1
        if positive == 1:
            C = C+1
        if positive == 0:
            D = D+1
    
    print("Probabilities  with rp = ", rp, " and rn = ", rn)
    print("Probability of triangles of type A: ", A/(A+B+C+D))
    print("Probability of triangles of type B: ", B/(A+B+C+D))
    print("Probability of triangles of type C: ", C/(A+B+C+D))
    print("Probability of triangles of type D: ", D/(A+B+C+D))
    pass