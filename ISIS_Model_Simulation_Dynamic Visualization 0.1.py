# Author: Joe Shaheen
#Used Python 2.7 on Windows 8.1

import networkx as nx
import random
import numpy
import time

class sim:

    """def __init__(self, size, probability, iterations, entry_iterations, sim_number): #Intialize the Model
        self.iterations = iterations
        self.entry_iterations = entry_iterations
        origin_network = nx.erdos_renyi_graph(size, probability, directed=False, seed=1234567 ) # used seed=1234567 for testing
        i = 0
        iteration = 0
        self.entry_method(origin_network, iteration, sim_number)"""

    def entry_method(self, size, probability, iteration, entry_iterations, sim_number):
        origin_network = nx.erdos_renyi_graph(size, probability, directed=False, seed=1234567)
        runs = 0
        while len(nx.nodes(origin_network)) < max_size: #Defining the Entry Method by entering new nodes into the network
            #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$---starting entry method---$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            i = 1
            node_list = nx.nodes(origin_network) # create a list of nodes from the network
            #print ("This is the node_list list before the entry_iterations classmethod loop", node_list)

            while i <= entry_iterations and len(node_list) < max_size :
                node_list = nx.nodes(origin_network)
                #print ("This is the node_list list in the entry loop class method loop", node_list)

                random_name = str(time.time()) + '_' + str(random.random()) # Give each node a new random name. Used for verification
                origin_network.add_node(random_name) # Add the node to the network
                new_node = origin_network.node[random_name]
                random_node = numpy.random.choice(node_list)
                if random.uniform(0,1) < 0.95: # IF this test succeeds connect the node to a random node in the network
                    origin_network.add_edge(random_name, random_node)
                i += 1
                #print(i)
                #print (nx.get_node_attributes(self.origin_network, 'node_DC'),"<---this is the new node", "and the length is ", len(node_list))
            #print("______________________________________________________________________________________________________________________________________________________________")
            #output_file(origin_network, 1, iteration, sim_number)

            #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$---starting triadic reproduction---$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
            node_list = nx.nodes(origin_network)
            #print ("**Triadic Method** This is the node_list list before the entry to the loop", node_list)

            i = 1
            while i <= iterations: # This loop starts the triadic closure
                #print ("**Triadic Method** This is the node_list list AFTER the entry to the loop", node_list)
                #print node_list
                random_node = numpy.random.choice(nx.nodes(origin_network)) # picka random node
                #print ("This is the TM random node", random_node)
                #print origin_network
                if nx.is_isolate(origin_network, random_node) == True or origin_network.degree(random_node) == 0: # if it's an isolate find go back to the start of the loop and  find another node
                    i += 1
                    #print (" This node is an isolate or has no neighbors:", origin_network.neighbors(random_node), "on turn", i)
                    continue
                else:
                    try:
                        Neighb = origin_network.neighbors(random_node)
                    except nx.NetworkXError:
                        #print ("node is not in graph")
                        i +=1
                        continue

                    #print ("**Triadic Method** These are the neighbors for random node", origin_network.neighbors(random_node))

                    if len(origin_network.neighbors(random_node)) <= 1: #if the neighbor has no neighbors then go back to the start of the loop
                        #print ("The neighbor has no additional neighbors", "on turn", i)
                        #random_neighb = Neighbs[0]
                        i+=1
                        continue
                    else:
                        random_neighb = numpy.random.choice(origin_network.neighbors(random_node)) # if it has 1 or more neighbors, pick a random one
                        try:
                            neighbs_of_neighb = origin_network.neighbors(random_neighb)
                        except nx.NetworkXError:
                            print ("error")
                            continue
                    # if the neighbor has a neighbor and the random test is passed connect ego node to the friend of my friend
                    if len(neighbs_of_neighb) == 1:
                        #print ("This neighbor has only the original neighbor on turn", i)
                        random_NofN = neighbs_of_neighb[0]
                        if random.uniform(0,1) < 0.95:
                            origin_network.add_edge(random_node, random_NofN)
                    else:
                        random_NofN = numpy.random.choice(neighbs_of_neighb)
                        if random.uniform(0,1) < 0.95:
                            origin_network.add_edge(random_node, random_NofN)
                        #print "success"

                i += 1
                #print(i)
            #print("______________________________________________________________________________________________________________________________________________________________")
            #output_file(origin_network, 2, iteration, sim_number)
            i = 0
            while i < iterations: # Creat random edges to increase desnity
                if random.uniform(0,1) < 0.05:
                    origin_network.add_edge(numpy.random.choice(origin_network.nodes()),numpy.random.choice(origin_network.nodes()))
                i +=1
            #output_file(origin_network, 3, iteration, sim_number)

            i=0
            #nx.set_node_attributes(origin_network, 'Degree', nx.degree(origin_network))
            while i < entry_iterations: # Cumulative growth function. If a node meets a random node and the random node has more friends, after passing
                                             # the random test, connect to it. This is a preferntial attachment without the ridiculous assumptions
                node_a = numpy.random.choice(nx.nodes(origin_network))
                node_b = numpy.random.choice(nx.nodes(origin_network))
                #print ("This is node a", node_a, "with a degree of", origin_network.degree(node_a))
                #print ("This is node B:" , node_b, "with a degree of", origin_network.degree(node_b))
                #print origin_network.node[node_a]['Degree']
                if origin_network.degree(node_a) < origin_network.degree(node_b) and random.uniform(0,1) < 0.25:
                    origin_network.add_edge(node_a, node_b)
                i += 1


            runs += 1
        print ("It took this many runs to reach max size", runs)
        #output_file(origin_network, 666 , iteration, sim_number)
        nx.write_gexf(origin_network, "sim_" + str(sim_number) + "_run_" + str(iteration) + "_iter_" + str(time.time()) + ".gexf")
        return origin_network

# running the model and setting the parameters
if __name__ == '__main__':

    Simulation_times = 1 # how many times would you like to run the simulation
    probability = 0.003 # intializing probability of the erdos renyi network
    global max_size
    max_size = 100 # set this value to set all other relevant parameters. The model will ouput a network roughly at this size
    size = 50 # Initial size of the network
    iterations = 10 * size # used to iterating while loops for all actions except entry actions
    entry_iterations = int(iterations * 0.3) # used to iterate actions for entry only.

n = 1
while n <= Simulation_times:

    print ("simulation starts...")

    A = sim() #iterations is always set at 2 for now

    A.entry_method(size, probability, iterations, entry_iterations, n)

    print("just ran the output function from main")
    n += 1








