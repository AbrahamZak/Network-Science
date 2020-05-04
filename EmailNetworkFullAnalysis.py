import networkx as nx
import matplotlib.pyplot as plt 
import numpy as np
import collections
from scipy.stats import lognorm
from scipy import stats
from time import ctime
from datetime import date 

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
    #get the least–square regression line for each and coefficients
    coefDegree = np.polyfit(x, y, 1)
    #plot on log-log
    plt.loglog(x, y, label=typeName) 
    plt.plot(x, np.polyval(coefDegree, x), '--', label=(coefDegree))
    #legend the graph
    plt.legend()

def powerfit(x, y):
    k, m = np.polyfit(np.log(x), np.log(y), 1)
    yres = np.exp(m) * x**(k)
    print("Sum of squared difference (power law): ", np.sum((y-yres)**2))
    return yres

def expFit(x,xo,a):
    f= xo*np.exp(a*x)
    return(f)

def exp(x, y):
    ylin = np.log(y)
    [a,b,r,p,sterr] = stats.linregress(x,ylin) 
    yres= expFit(x,np.exp(b),a)
    print("Sum of squared difference (exponential): ", np.sum((y-yres)**2))
    return yres

def lognormal(x, y):
    s, loc, scale = lognorm.fit(x)
    xmin = x.min()
    xmax = x.max()
    x = np.linspace(xmin, xmax, len(x))
    pdf = lognorm.pdf(x, s, scale=scale)
    yres = pdf
    print("Sum of squared difference (log-normal): ", np.sum((y-yres)**2))
    return yres

def plot_degree_dist_compare(degrees):
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
    plt.loglog(x, y, 'b.', label="degree distribution") 
    #fitted power law
    ypw = powerfit(x, y)
    plt.loglog(x, ypw, 'k-', label="power-law", linestyle='dashed')
    #exponential
    yexp = exp(x, y)
    plt.loglog(x, yexp, label="exponential")
    #log-normal
    yln = lognormal(x, y)
    plt.loglog(x, yln, label="log-normal")
    #legend the graph
    plt.legend()
    
if __name__ == '__main__':
    #Create a list for our edges
    edges = []
    #Read the dataset
    readFile = open("532projectdataset.txt", "r")
    #Remove all newlines
    readFile = readFile.read().splitlines()
    #For each line enter the from and to email addresses into our edges list
    for line in readFile:
        parts = line.split(' ')
        #Filter out weekends
        day = ctime(int(parts[0]))
        dateSplit = day.split(' ')
        if dateSplit[0] in ('Mon', 'Tue', 'Wed', "Thu", 'Fri'):
            edges.append((parts[1], parts[2]))
        
    #Add weights to our list
    edges = list(collections.Counter(edges).items())
    #Create our directed graph using our edges and weights list
    g = nx.DiGraph()
    for x,y in edges:
        g.add_edge(x[0], x[1], weight = y)

    #Summary Statistics
    #Number of nodes
    print ("Number of nodes: ", nx.number_of_nodes(g))
    #Number of edges
    print ("Number of edges: ", nx.number_of_edges(g))
    #Number of bidirectional edges
    #To find bidirectional edges we will create an undirected graph and then find the difference in edge count
    h = nx.Graph()
    h.add_edges_from(g.edges)
    print ("Number of bidirectional edges: ", g.number_of_edges() - h.number_of_edges()) 
    #Min, max, and average number of other addresses each email address has interacted with (both in–, out– and total degree)
    in_degrees = list(g.in_degree)
    in_degrees_values = []
    for x,y in in_degrees:
        in_degrees_values.append(y)
    print ("Minimum in degree: ", min(in_degrees_values))
    print ("Average in degree: ", np.mean(in_degrees_values))
    print ("Maximum in degree: ", max(in_degrees_values))
    out_degrees = list(g.out_degree)
    out_degrees_values = []
    for x,y in out_degrees:
        out_degrees_values.append(y)
    print ("Minimum out degree: ", min(out_degrees_values))
    print ("Average out degree: ", np.mean(out_degrees_values))
    print ("Maximum out degree: ", max(out_degrees_values))
    degrees = list(g.degree)
    degrees_values = []
    for x,y in degrees:
        degrees_values.append(y)
    print ("Minimum total degree: ", min(degrees_values))
    print ("Average total degree: ", np.mean(degrees_values))
    print ("Maximum total degree: ", max(degrees_values))
    #Diameter of the network
    #Get the largest strongly connected component nodes
    largest_g = max(nx.strongly_connected_components(g), key=len)
    #Create a subgraph and find its diameter
    l = g.subgraph(largest_g)
    #print(*l.edges(data=True), sep='\n')
    #Uncomment to calculate diameter below - Long run time (30+ mins) 
    #Result is 11
    #print("Diameter: ", nx.distance_measures.diameter(l))
    
    #Plot
    #Distribution of degree, in-degree, out-degree
    plot_degree_dist(g.degree(), 'degree')
    plot_degree_dist(g.in_degree(), 'in-degree')
    plot_degree_dist(g.out_degree(), 'out-degree')
    #Show the final graph
    plt.title("Log-log distribution of degrees, in–degrees, and out–degrees and regression")
    plt.show()
    
    #Comparing the fitted power law for the degree distribution to the exponential and log-normal distributions
    plot_degree_dist_compare(g.degree())
    plt.title("Comparing the fitted power law for the degree distribution to the exponential and log-normal distributions")
    plt.show()    
    
    pass
