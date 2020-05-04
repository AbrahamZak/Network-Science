import networkx as nx
import matplotlib.pyplot as plt 

if __name__ == '__main__':
    #load in our data
    g = nx.read_adjlist(path="frienship_network.txt", delimiter=" ", comments="#", create_using=None, nodetype=None, encoding="utf-8")
    #print the connected components
    print("Number of connected components: ", nx.number_connected_components(g))
    #print the nodes and edges
    print ("Number of nodes: ", nx.number_of_nodes(g))
    print ("Number of edges: ", nx.number_of_edges(g))
    #get a dictionary of all degrees
    deg_dict = dict(g.degree)
    #get the average neighbor degrees
    avg_neighbor = (nx.average_neighbor_degree(g))
    #get the ratio (degree of node u divided by the average neighbor degree of node u)
    ratio = dict((k, float(deg_dict[k]) / avg_neighbor[k]) for k in deg_dict)
    #plot the ratio in scatter
    keys = list(ratio.keys())
    x = []
    for item in keys:
        x.append(float(item))
    y = list(ratio.values())
    plt.title("Degree of node u divided by the average neighbor degree of node u")
    plt.xlabel("Node u")
    plt.ylabel("Ratio")
    plt.scatter(x,y, marker='.')
    plt.show()