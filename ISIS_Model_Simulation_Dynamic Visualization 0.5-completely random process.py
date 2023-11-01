# Author: Joe Shaheen
#Used Python 2.7 on Windows 8.1
#Date: 07/27/2017

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
            nx.set_node_attributes(origin_network, 'connected_this_turn', 0)
            nx.set_node_attributes(origin_network, 'time_order', 0)
        for edges in origin_network.edges():
            nx.set_edge_attributes(origin_network, 'Time', 0)
            nx.set_edge_attributes(origin_network, 'Type', "ER")
            nx.set_edge_attributes(origin_network, 'time_order', 0)
        name = size + 1
        time_count= size + 1

        while len(nx.nodes(origin_network)) < max_size: #Defining the Entry Method by entering new nodes into the network
            nx.set_node_attributes(origin_network, 'connected_this_turn', 1 )

            i = 1
            node_list = nx.nodes(origin_network) # create a list of nodes from the network
            while i <= entry_iterations and len(node_list) < max_size :
                name +=1 
                node_list = nx.nodes(origin_network)
                random_name = name         # Give each node a new random name. Used for verification
                origin_network.add_node(random_name, Time = runs + 1, connected_this_turn = 0, time_order = time_count)               # Add the node to the network

                new_node = origin_network.node[random_name]
                random_node = numpy.random.choice(node_list)

                if random.uniform(0,1) < 0.5:                                      # If this test succeeds connect the node to a random node in the network
                    origin_network.add_edge(random_name, random_node, Time = runs + 1, Type = "entry_edge", time_order = time_count)
                    origin_network.node[random_name]['connected_this_turn'] = 0
                time_count += 1
                i += 1
            node_list = nx.nodes(origin_network)

            #This is a totally random connecting function. Only to be used in the random version of the simulation

            i = 1
            while i < iterations:
                node_a = random.choice(nx.nodes(origin_network))
                # print("node a is ", type(node_a))
                node_b = random.choice(nx.nodes(origin_network))
                if random.uniform(0,1) <= 0.5 and origin_network.node[node_a]['connected_this_turn'] == 1:
                    origin_network.add_edge(node_a, node_b, Time=runs + 1, Type="random_edge", time_order = time_count)
                    origin_network.node[node_a]['connected_this_turn'] = 0
                time_count += 1
                i += 1

                #Now for transitivity

                node_a = random.choice(nx.nodes(origin_network))
                # print("node a is ", type(node_a))
                Neighbors = origin_network.neighbors(node_a)
                if len(Neighbors) > 2:
                    node_b = random.choice(Neighbors)
                    Neighbors.pop(node_b)
                    node_c = random.choice(Neighbors)
                    if random.uniform(0, 1) <= 0.5 and origin_network.node[node_b]['connected_this_turn'] == 1 and origin_network.node[node_c]['connected_this_turn'] == 1:
                        origin_network.add_edge(node_b, node_c, Time=runs + 1, Type="triadic_edge", time_order=time_count)
                        origin_network.node[node_b]['connected_this_turn'] = 0
                        origin_network.node[node_c]['connected_this_turn'] = 0
                time_count += 1
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
    max_size = 150000 # set this value to set all other relevant parameters. The model will ouput a network roughly at this size
    size = 50 # Initial size of the network
    iterations = 100 * size # used to iterating while loops for all actions except entry actions
    entry_iterations = int(iterations * 0.3) # used to iterate actions for entry only.

n = 1
while n <= Simulation_times:

    print ("simulation starts...")

    A = sim() #iterations is always set at 2 for now

    A.entry_method(size, probability, iterations, entry_iterations, n)

    print("just ran the output function from main")
    n += 1








