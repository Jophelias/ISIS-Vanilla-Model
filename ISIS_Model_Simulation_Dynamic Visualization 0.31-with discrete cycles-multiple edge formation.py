# Author: Joe Shaheen
#Used Python 2.7 on Windows 8.1

import networkx as nx
import random
import numpy
import time

class sim:
    def entry_method(self, size, probability, iteration, entry_iterations, sim_number):

        origin_network = nx.erdos_renyi_graph(size, probability, directed=False, seed=1234567)
        runs = 0
        for nodes in origin_network.nodes():
            nx.set_node_attributes(origin_network, 'Time', 0)
            nx.set_node_attributes(origin_network, 'connected_this_turn', 1)
        for edges in origin_network.edges():
            nx.set_edge_attributes(origin_network, 'Time', 0)
            nx.set_edge_attributes(origin_network, 'Type', "ER")
        name = size + 1

        while len(nx.nodes(origin_network)) < max_size: #Defining the Entry Method by entering new nodes into the network
            nx.set_node_attributes(origin_network, 'connected_this_turn', 0)

            i = 1
            node_list = nx.nodes(origin_network) # create a list of nodes from the network
            while i <= entry_iterations and len(node_list) < max_size :
                name +=1 
                node_list = nx.nodes(origin_network)
                random_name = str(name)         # Give each node a new random name. Used for verification
                origin_network.add_node(random_name, Time = runs + 1, connected_this_turn = 0)               # Add the node to the network

                new_node = origin_network.node[random_name]
                random_node = numpy.random.choice(node_list)

                if random.uniform(0,1) < 0.95:                                      # If this test succeeds connect the node to a random node in the network
                    origin_network.add_edge(random_name, random_node, Time = runs + 1, Type = "entry_edge")
                    origin_network.node[random_name]['connected_this_turn'] = 0
                i += 1
            node_list = nx.nodes(origin_network)

            i = 1
            while i <= iterations: # This loop starts the triadic closure
                random_node = numpy.random.choice(nx.nodes(origin_network)) # pick a random node
                if nx.is_isolate(origin_network, random_node) == True or origin_network.degree(random_node) == 0: # if it's an isolate find go back to the start of the loop and find another node
                    i += 1
                    #continue
                else:
                    try:
                        node_neighbors = origin_network.neighbors(random_node) #pick the neighbors of the first node
                        random_neighbor_of_node = numpy.random.choice(node_neighbors)  #choose one of those neighbors to evaluate for triadic closure
                        if len(origin_network.neighbors(random_neighbor_of_node)) >= 2: # Does the neighbor node have more than two connecting nodes?
                            neighb_nodes = set(origin_network.neighbors(random_neighbor_of_node))
                            neighb_nodes_excluding_the_original_node = neighb_nodes.difference_update(neighb_nodes)
                            third_node = numpy.random.choice(neighb_nodes_excluding_the_original_node)
                            if random.uniform(0,1) < 0.95:
                                origin_network.add_edge(random_node, third_node, Time=runs + 1, Type="triadic_edge")
                    except nx.NetworkXError:
                        print "error"



                    """"#try:
                    #   Neighb = origin_network.neighbors(random_node)
                    #except nx.NetworkXError:
                        #i +=1
                        #continue
                    if : #if the neighbor has no neighbors then go back to the start of the loop
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
                            origin_network.add_edge(random_node, random_NofN, Time = runs + 1, Type = "triadic_edge")
                    else:
                        random_NofN = numpy.random.choice(neighbs_of_neighb)
                        if random.uniform(0,1) < 0.95:
                            origin_network.add_edge(random_node, random_NofN, Time = runs + 1, Type = "triadic_edge")"""
                        #print "success"
                # Cumulative growth function. If a node meets a random node and the random node has more friends, after passing
                # the random test, connect to it. This is a preferential attachment without the ridiculous assumptions
                node_a = numpy.random.choice(nx.nodes(origin_network))
                node_b = numpy.random.choice(nx.nodes(origin_network))
                if origin_network.degree(node_a) < origin_network.degree(node_b) and random.uniform(0,1) < 0.1:
                    origin_network.add_edge(node_a, node_b, Time = runs + 1, Type = "preferential_edge")
                i += 1
            runs += 1
        print ("It took this many runs to reach max size", runs)
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








