import networkx as nx
import matplotlib.pyplot as plt 
import random
import numpy as np

def SIModel(filename, highestDegree):
    #Get our edges data from interactionsnetwork.csv
    edges = []
    with open(filename, 'r') as f:
        next(f)
        lines = f.readlines()
    for line in lines:
        data = line.split(',')
        #Add the edge to edges list
        edges.append((data[0], data[1]))
        
    '''
    Initial chance of infecting a neighbor is 10%
    Each infected node has 1 chance to infect its 
    each of its neighboring nodes
    We will be measuring the average epidemic size
    with 100 simulation runs of each infection percentage
    as well as the epidemic length, we will do this for many p
    (slowly increasing from 10% to 90%) and graph results
    '''
    infectPercentage = 0.1
    #List for the number of infected nodes at the end of each trial
    infected = []
    #List for the average number of infected nodes at the end of each trial after 100 trials
    infectedAvg = []
    #List for the total amount of days each trial lasts
    days = []
    #List for the average total amount of days each trial lasts after 100 trials
    daysAvg = []
    #List to keep track of our infect percentage value
    infectPercentageTracker = []
    '''
    Keep track of edges because if by the end of a cycle 
    edge count is the same we know the epidemic is now over
    '''
    #Create our graph
    G = nx.Graph()
    G.add_edges_from(edges)
    #Get our total node size
    totalNodes = len(G.nodes)
    #Set our total trials for each infect percentage
    totalTrials = 100
    
    while infectPercentage < 0.95:
        for i in range(totalTrials):
            #Set all nodes to not infected
            nx.set_node_attributes(G, False, 'contagion')
            '''
            Keep track of newly infected nodes and nodes that have been 
            infected the previous day, as newly infected nodes will be the infectors
            for the next day while nodes that were infected the previous day
            are the infectors for the current day
            This will also prevent nodes from trying to infect other nodes twice
            '''
            newlyInfected = []
            previousDayInfected = []
            #If highest degree is true assign the highest degree node to infected status to begin
            if highestDegree == True:
                sortedNodes = sorted(G.degree, key=lambda x: x[1], reverse=True)
                highest = sortedNodes[0]
                G.nodes[highest[0]]['contagion'] = True
                previousDayInfected.append(highest[0])
            #If not, assign one single random node the infected status to begin
            else:
                v = random.choice(list(G.nodes.keys()))
                G.nodes[v]['contagion'] = True
                previousDayInfected.append(v)
            #Start with day 0 and 1 infected node
            daysCounter = 0
            infectedCounter = 1
            #Checks to make sure if on each day we have the same amount of infections
            newDayInfected = 1
            while(True):
                #Go through all nodes that were infected during the previous day
                for u in previousDayInfected:
                    #Go through all neighbors of u
                    for neighbor in G.neighbors(u):
                        #Check to make sure they are not already infected
                        if G.nodes[neighbor]['contagion'] == False:
                            #At percentage chance change the neighbor to infected
                            if random.random() < infectPercentage:
                                G.nodes[neighbor]['contagion'] = True
                                #Increment infected counter
                                infectedCounter = infectedCounter + 1
                                newlyInfected.append(neighbor)
                        
                #If no one got infected we are done with the epidemic
                if (infectedCounter == newDayInfected):
                    break
                #If someone got infected we update our edges counter and continue to the next time step
                else:
                    newDayInfected = infectedCounter
                
                #Increment days by 1 before starting a new day
                daysCounter = daysCounter + 1
                #Clear the previous day infected list and replace it with newly infected
                previousDayInfected.clear()
                previousDayInfected = newlyInfected[:]
                newlyInfected.clear()

            #Record our results and clear our graph to start a new trial
            days.append(daysCounter)
            infected.append(infectedCounter/totalNodes)
        
        '''
        Once completed the trial for the current infection percentage
        We store the averages of days and infected percentage
        and then increment infectPercentage by another 10% and start
        the next trial until we've reach an infectPercentage of 90%  
        '''
        daysAvg.append(sum(days) / len(days))
        infectedAvg.append(sum(infected) / len(infected))
        infectPercentageTracker.append(infectPercentage)
        infectPercentage = infectPercentage + 0.1
        days.clear()
        infected.clear()
    
    return infectPercentageTracker, infectedAvg, daysAvg, totalNodes
    
if __name__ == '__main__':
    #Get SI Network data from interactionsnetwork.csv, RandNet1.csv, and RandNet2.csv
    infectPercentageTracker, infectedAvg, daysAvg, totalNodes = SIModel("interactionsnetwork.csv", False)
    infectPercentageTrackerRand1, infectedAvgRand1, daysAvgRand1, totalNodesRand1 = SIModel("RandNet1.csv", False)
    infectPercentageTrackerRand2, infectedAvgRand2, daysAvgRand2, totalNodesRand2 = SIModel("RandNet2.csv", False)
    
    #Get SI Network data from interactionsnetwork.csv, RandNet1.csv, and RandNet2.csv with the highest degree node as the initial infected
    infectPercentageTrackerHighest, infectedAvgHighest, daysAvgHighest, totalNodes = SIModel("interactionsnetwork.csv", True)
    infectPercentageTrackerRand1Highest, infectedAvgRand1Highest, daysAvgRand1Highest, totalNodesRand1Highest = SIModel("RandNet1.csv", True)
    infectPercentageTrackerRand2Highest, infectedAvgRand2Highest, daysAvgRand2Highest, totalNodesRand2Highest = SIModel("RandNet2.csv", True)
    
    '''
    Plot of our data which includes average epidemic size
    over infect rate(p) and average epidemic length over infect rate(p)
    '''
    plt.title("SI Model Average Epidemic Size with varying p, single node start at random")
    plt.xlabel("Infect Percentage (p)")
    plt.ylabel("Average Epidemic Size (s/|V\)")
    plt.plot(infectPercentageTracker, infectedAvg, label="Interactions Network", color="b")
    plt.plot(infectPercentageTrackerRand1, infectedAvgRand1, label="Random Network 1", color="y")
    plt.plot(infectPercentageTrackerRand2, infectedAvgRand2, label="Random Network 2", color="r")
    plt.legend()
    plt.show()
    
    plt.title("SI Model Average Epidemic Length with varying p, single node start at random")
    plt.xlabel("Infect Percentage (p)")
    plt.ylabel("Average Epidemic Length (l)")
    plt.plot(infectPercentageTracker, daysAvg, label="Interactions Network", color="b")
    plt.plot(infectPercentageTrackerRand1, daysAvgRand1, label="Random Network 1", color="y")
    plt.plot(infectPercentageTrackerRand2, daysAvgRand2, label="Random Network 2", color="r")
    plt.axhline(y=np.log(totalNodes), linestyle='-', label="log(|V|) - Interactions", color="b")
    plt.axhline(y=np.log(totalNodesRand1), linestyle='-', label="log(|V|) - Rand 1", color="y")
    plt.axhline(y=np.log(totalNodesRand2), linestyle='-', label="log(|V|) - Rand 2", color="r")
    plt.legend()
    plt.show()
    
    '''
    Plot for data starting with highest degree node as infected
    '''
    plt.title("SI Model Average Epidemic Size with varying p, single node start at highest degree node")
    plt.xlabel("Infect Percentage (p)")
    plt.ylabel("Average Epidemic Size (s/|V\)")
    plt.plot(infectPercentageTrackerHighest, infectedAvgHighest, label="Interactions Network", color="b")
    plt.plot(infectPercentageTrackerRand1Highest, infectedAvgRand1Highest, label="Random Network 1", color="y")
    plt.plot(infectPercentageTrackerRand2Highest, infectedAvgRand2Highest, label="Random Network 2", color="r")
    plt.legend()
    plt.show()
    
    plt.title("SI Model Average Epidemic Length with varying p, single node start at highest degree node")
    plt.xlabel("Infect Percentage (p)")
    plt.ylabel("Average Epidemic Length (l)")
    plt.plot(infectPercentageTrackerHighest, daysAvgHighest, label="Interactions Network", color="b")
    plt.plot(infectPercentageTrackerRand1Highest, daysAvgRand1Highest, label="Random Network 1", color="y")
    plt.plot(infectPercentageTrackerRand2Highest, daysAvgRand2Highest, label="Random Network 2", color="r")
    plt.axhline(y=np.log(totalNodes), linestyle='-', label="log(|V|) - Interactions", color="b")
    plt.axhline(y=np.log(totalNodesRand1), linestyle='-', label="log(|V|) - Rand 1", color="y")
    plt.axhline(y=np.log(totalNodesRand2), linestyle='-', label="log(|V|) - Rand 2", color="r")
    plt.legend()
    plt.show()
    pass