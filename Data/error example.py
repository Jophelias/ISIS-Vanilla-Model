import networkx as nx
import random

origin_network = nx.erdos_renyi_graph(150, 0.003, directed=False, seed=1234567)

iterations = 10
print('This is hello')


i = 1
while i <= iterations: # This loop starts the triadic closure
    random_node = random.choice(nx.nodes(origin_network)) # pick a random node
    if nx.is_isolate(origin_network, random_node) == True or origin_network.degree(random_node) == 0: # if it's an isolate find go back to the start of the loop and find another node
            i += 1
            continue
        else:
            try:
                Neighb = origin_network.neighbors(random_node)
            except nx.NetworkXError:
                i +=1
                continue
            if len(origin_network.neighbors(random_node)) <= 1: #if the neighbor has no neighbors then go back to the start of the loop
                i+=1
                continue
            else:
                random_neighb = random.choice(origin_network.neighbors(random_node)) # if it has 1 or more neighbors, pick a random one
                try:
                    neighbs_of_neighb = origin_network.neighbors(random_neighb)
                except nx.NetworkXError:
                    print ("error")
                    continue
            # if the neighbor has a neighbor and the random test is passed connect ego node to the friend of my friend
            if len(neighbs_of_neighb) == 1:
                #print ("This neighbor has only the original neighbor on turn", i)
                random_NofN = neighbs_of_neighb[0]
                random_NofN = str(random_NofN)
                random_node = str(random_node)
                #print(random_NofN)
                #print(type(random_NofN))
                are_nodes_connected = nx.get_node_attributes(origin_network, 'connected_this_turn')
                print(are_nodes_connected)
                is_node_connected = are_nodes_connected[random_node]
                print ("node connection status ", is_node_connected)
                if random.uniform(0,1) < 0.95 and origin_network.node[random_node]['connected_this_turn'] == 1:
                    origin_network.add_edge(random_node, random_NofN, Time = runs + 1, Type = "triadic_edge")
                    origin_network.node[random_node]['connected_this_turn'] = 0
            else:
                random_NofN = random.choice(neighbs_of_neighb)
                random_node = str(random_node)
                random_NofN = str(random_NofN)
                are_nodes_connected = nx.get_node_attributes(origin_network, 'connected_this_turn')
                is_node_connected = are_nodes_connected[random_node]
                print ("node connection status 2 ", is_node_connected)

                if random.uniform(0,1) < 0.95 and origin_network.node[random_node]['connected_this_turn'] == 1:
                    origin_network.add_edge(random_node, random_NofN, Time = runs + 1, Type = "triadic_edge")
                    origin_network.node[random_node]['connected_this_turn'] = 0
                #print "success"
        i += 1
