import networkx as nx
import matplotlib.pyplot as plt 
import numpy as np
import time
import collections
from scipy.optimize import curve_fit

def power_law(x, a, b):
    return a*np.power(x, b)

if __name__ == '__main__':   
    #Keep track of our dates 
    dates = []
    #Get our edges data from temporalnetwork.csv
    edges = []
    #Get our edges for the day being looked at
    curDay = []
    #Open the file
    with open('temporalnetwork.csv', 'r') as f:
        next(f)
        lines = f.readlines()
    for line in lines:
        data = line.split(',')
        #Get the day
        day = time.strftime('%Y-%m-%d', time.localtime(int(data[2].rstrip())))
        #If this is a new day
        if day not in dates:
            #Add it to our dates list
            dates.append(day)
            #Append the current list of edges to our edges list
            edges.append(curDay[:])
            #Reset the curDay list
            curDay.clear()
        #Add the edge to curDay list
        curDay.append((data[0], data[1])) 

    #Add the final day to our edge list 
    edges.append(curDay)
    #Pop the first element (first new day will create blank list)
    edges.pop(0)
    
    #Create our graph
    G = nx.DiGraph()
    componentSize = []
    
    #For each day we calculate the largest component size and add it to our list of sizes
    for i in range(len(dates)):
        G.add_edges_from(edges[i])
        components = ([len(c) for c in sorted(nx.weakly_connected_components(G), key=len, reverse=True)])
        componentSize.append(components.pop(0))
    
    #Get the ratios for graphing    
    totalSize = len(G.nodes)
    ratios = []
    for component in componentSize:
        ratios.append(component / totalSize)
        
    plt.title("Evolution of the relative size of the largest weakly connected component ")
    plt.xlabel("Days Past")
    plt.ylabel("Ratio")
    plt.plot(range(len(ratios)), ratios)
    plt.show()
    
    #4-Week lifespan
    #Create our graph
    G4WK = nx.DiGraph()
    componentSize4Week = []
    
    #For each day we calculate the largest component size and add it to our list of sizes
    j = 1
    for i in range(len(dates)):
        if (j>27):
            G4WK.clear()
            j = 1
        G4WK.add_edges_from(edges[i])
        components = ([len(c) for c in sorted(nx.weakly_connected_components(G4WK), key=len, reverse=True)])
        componentSize4Week.append(components.pop(0))
        j = j + 1
    
    #Get the ratios for graphing    
    ratios4Wk = []
    for component in componentSize4Week:
        ratios4Wk.append(component / totalSize)
        
    plt.title("Evolution of the relative size of the largest weakly connected component (4 & 8 week lifespan)")
    plt.xlabel("Days Past")
    plt.ylabel("Ratio")
    plt.plot(range(len(ratios4Wk)), ratios4Wk, label="4 Week Span")
    
    #8-Week lifespan
    #Create our graph
    G8WK = nx.DiGraph()
    componentSize8Week = []
    
    #For each day we calculate the largest component size and add it to our list of sizes
    j = 1
    for i in range(len(dates)):
        if (j>55):
            G8WK.clear()
            j = 1
        G8WK.add_edges_from(edges[i])
        components = ([len(c) for c in sorted(nx.weakly_connected_components(G8WK), key=len, reverse=True)])
        componentSize8Week.append(components.pop(0))
        j = j + 1
    
    #Get the ratios for graphing    
    ratios8Wk = []
    for component in componentSize8Week:
        ratios8Wk.append(component / totalSize)
        
    plt.xlabel("Days Past")
    plt.ylabel("Ratio")
    plt.plot(range(len(ratios8Wk)), ratios8Wk, label="8 Week Span")
    plt.legend()
    plt.show()
    
    '''
    For each day, fit a power–law function to the 
    degree distribution, and plot the evolution of the 
    exponent of these functions over time assuming that
    social relationships cannot dissolve. 
    '''
    #Clear our network
    G.clear()
    #Hold the degree distribution for each day
    degreeDist = []
    #For each day get the degrees
    for i in range(len(dates)):
        G.add_edges_from(edges[i])
        degrees = dict(G.degree())
        #sort the dictionaries numerically
        degrees_values = sorted(degrees.values())
        #get frequencies
        freqdegrees = collections.Counter(degrees_values) 
        x = np.array(list(freqdegrees.keys()))
        y = np.array(list(freqdegrees.values()))
        #create the distribution
        y = y / (len(degrees))
        degreeDist.append((x,y))
      
    #Create a list to store each power law 
    powerLaw = []
    #Calculate the power law for progressive distributions
    for distributions in degreeDist:
        try:
            pars, cov = curve_fit(f=power_law, xdata=distributions[0], ydata=distributions[1], p0=[0, 0], bounds=(-np.inf, np.inf))
            powerLaw.append(pars[1])
        #We'll have an error for the first point so skip it
        except:
            continue
    
    #Plot the graph  
    plt.title("Evolution of the power law exponent over time")
    plt.xlabel("Days Past")
    plt.ylabel("Power Law Exponent")
    plt.plot(range(len(powerLaw)), powerLaw)
    plt.show()

    '''
    Draw a figure to show the evolution of the average
    geodesic distance over time when social relationships 
    are assumed to persist indefinitely.
    '''
    #Clear our network
    G.clear()
    #Hold the average geodesic distance for each day
    geodesicDist = []
    #For each day get the geodesic distance
    for i in range(len(dates)):
        G.add_edges_from(edges[i])
        #Get the largest weakly connected component nodes
        largest_g = max(nx.weakly_connected_components(G), key=len)
        #Create a subgraph and get its geodesic
        l = G.subgraph(largest_g)
        geodesic = nx.average_shortest_path_length(l)
        geodesicDist.append(geodesic)
    
    #Plot the graph    
    plt.title("Evolution of the average geodesic distance over time")
    plt.xlabel("Days Past")
    plt.ylabel("Average Geodesic Distance")
    plt.plot(range(len(geodesicDist)), geodesicDist)
    plt.show()    
    
    pass