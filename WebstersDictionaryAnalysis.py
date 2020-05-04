'''
Analysis of Webster's Unabridged Dictionary with NetworkX
'''
import networkx as nx
import matplotlib.pyplot as plt
import json
import numpy as np
import collections 

def plot_degree_dist(degrees, typeName):
    #create a dictionary from the degrees
    degrees = dict(degrees)
    
    #sort the dictionaries numerically
    degrees_values = sorted(degrees.values())
    
    #get frequencies
    freqdegrees = collections.Counter(degrees_values) 
    
    x = np.array(list(freqdegrees.keys()))
    y = np.array(list(freqdegrees.values()))
        
    #get the least–square regression line for each and coefficients
    coefDegree = np.polyfit(x, y, 1)
    
    #plot on log-log
    plt.loglog(x, y, label=typeName) 
    plt.plot(x, np.polyval(coefDegree, x), '--', label=(coefDegree))

    #legend the graph
    plt.legend()
    
#Gets triangles in adjacency matrix
def countTriangle(g): 
    nodes = len(g) 
    triangles = 0 
    for i in range(nodes): 
        for j in range(nodes): 
            for k in range(nodes): 
                if( i!=j and i !=k and j !=k and 
                        g[i][j] and g[j][k] and g[k][i]): 
                    triangles += 1
    return triangles/3
    
if __name__ == '__main__':
    #create our graph
    G = nx.Graph()
    
    #import JSON data as dictionary
    f = open('webstersdictionary.json')
    data = json.load(f)
    f.close()
    
    #Create our directed graph
    G = nx.DiGraph(data)
        
    #Get total number of nodes and edges
    print ("Number of nodes: ", G.number_of_nodes())        
    print ("Number of edges: ", G.number_of_edges())
    
    #To find bidirectional edges we will create a undirected graph and then find the difference in edge count
    H = nx.Graph()
    H.add_edges_from(G.edges)
    print ("Number of bidirectional edges: ", G.number_of_edges() - H.number_of_edges()) 
    
    #Get triangles from three cliques of the directed graph that removed edges that aren't bidirectional
    threeCycle = [c for c in nx.cycle_basis(H) if len(c)==3]
    print("Number of triangles: ", len(threeCycle))
    
    #Create the graph
    plot_degree_dist(G.degree(), 'degree')
    plot_degree_dist(G.in_degree(), 'in-degree')
    plot_degree_dist(G.out_degree(), 'out-degree')
    
    #Show graph
    plt.show()
    
    pass