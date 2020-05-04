import networkx as nx
import random
import matplotlib.pyplot as plt 

if __name__ == '__main__':
    #Get our node data from nodeslist.csv
    nodes = []
    with open('nodeslist.csv', 'r') as f:
        next(f)
        lines = f.readlines()
    for line in lines:
        data = line.split(',')
        nodes.append([data[0], data[2].rstrip()])    
    
    #Get our edges data from nodeslist.csv
    edges = []
    with open('edgelist.csv', 'r') as f:
        next(f)
        lines = f.readlines()
    for line in lines:
        data = line.split(',')
        edges.append([data[0], data[1]])    
    
    #Add nodes and edges to our directed graph
    G = nx.DiGraph()
    for node in nodes:
        G.add_node(node[0], data=node[1])
    G.add_edges_from(edges)

    #Randomize our list of nodes for testing our heuristic
    random.shuffle(nodes)
    #Create our graph basis
    plt.xlabel('Fraction of labels observed')
    plt.ylabel('Accuracy of heuristic')
    plt.title('Political Blogs Heuristic')
    #For each node we check the types of the nodes it directs to 
    #Then we check the majority typing and see if it matches the original node's type
    #If yes, our heuristic is correct and we plot that with our current sample size
    #If no, our heuristic is not correct and we plot that with our current sample size
    #Note: liberal = 0, conservative = 1
    totalChecked = 0.00
    totalCorrect = 0.00
    totalNodes = len(nodes)
    fraction = []
    accuracy = []
    for u,v in nodes:
        #Counters for each type and total
        liberal = 0
        conservative = 0
        #Get the amount of each neighbor
        for neighbor in G.neighbors(u):
            libOrCons = G.nodes[neighbor]["data"]
            if (libOrCons == '0'):
                liberal = liberal + 1
            if (libOrCons == '1'):
                conservative = conservative + 1
                
        #If there are more liberal neighbors check if the original node is liberal       
        if (liberal > conservative):
            #If it matches, heuristic is correct
            if (v == '0'):
                totalChecked = totalChecked + 1.00
                totalCorrect = totalCorrect + 1.00
            #If it doesn't match, heuristic is incorrect
            if (v == '1'):
                totalChecked = totalChecked + 1.00
                
        #If there are more liberal neighbors check if the original node is conservative   
        if (conservative > liberal):
            #If it doesn't match, heuristic is incorrect
            if (v == '0'):
                totalChecked = totalChecked + 1.00
            #If it matches, heuristic is correct
            if (v == '1'):
                totalChecked = totalChecked + 1.00 
                totalCorrect = totalCorrect + 1.00
         
        fraction.append(totalChecked/totalNodes)    
        accuracy.append(totalCorrect / totalChecked)
    
    #plot from our collected data
    plt.plot(fraction, accuracy)
    #Show final plot
    plt.show()      
    pass