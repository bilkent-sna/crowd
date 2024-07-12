import csv
import math
import os
import networkx as nx
import importlib
import random
from crowd.preprocessing import preprocessor as p
from crowd.preprocessing import communitydetection as com

class Structure:

    def __init__(self, structure, project_dir):
        self.structure = structure
        self.project_dir = project_dir

    def create(self):
        Exception("Create not implemented in Structure")

    def set_nodetypes(self, graph, conf, count):
        print("Inside set nodetypes")
        # Set the nodetypes as described in conf
        if "pd-model" in conf["definitions"]:
            if conf["definitions"]["pd-model"]["nodetypes"] != None:
                nodetype_counts = {}
                nodetype_dict = self.conf["definitions"]["pd-model"]["nodetypes"]
                keys = list(nodetype_dict.keys())

                random_nodetypes = []
                total_assigned = 0

                for nodetype in keys:
                    nodetype_counts[nodetype] = 0
                    print("Currently setting nodetype ", nodetype)
                    if "random-with-count" in nodetype_dict[nodetype]:
                        print("Inside random with count")
                        count_to_add = int(nodetype_dict[nodetype]["random-with-count"]["count"])
                        random_nodetypes.extend([ nodetype ] * int(count_to_add))
                        total_assigned += count_to_add
                    elif "random-with-weight" in nodetype_dict[nodetype]:
                        print("Inside random with weight")
                        initial_weight = float(nodetype_dict[nodetype]["random-with-weight"]["initial-weight"])
                        count_to_add = int(math.ceil(initial_weight*count))
                        random_nodetypes.extend([ nodetype ] * count_to_add)
                        total_assigned += count_to_add
                    elif "choose-with-metric" in nodetype_dict[nodetype]:
                        print("Inside choose with metric")
                        algo = nodetype_dict[nodetype]["choose-with-metric"]["metric"]
                        print("Choosen metric for choosing k nodes:", algo)
                        k = int(nodetype_dict[nodetype]["choose-with-metric"]["count"])
                        # Choose which nodes are selected for influence maximization
                        # And set node's attribute as this nodetype
                        graph = self.choose_nodes_with_centrality(algo, k, graph, nodetype)
                        # We don't out this nodetype to random_nodetypes
                        # Because we won't assign these randomly
                        nodetype_counts[nodetype] = k
                        total_assigned += k
                    elif "from-file" in nodetype_dict[nodetype]:
                        print("Inside from file")
                        path = nodetype_dict[nodetype]["from-file"]["path"]
                        path = os.path.join(self.project_dir, 'datasets', path)
                        # path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', conf["name"], 'datasets')
                        print("This is the path we send", path)
                        graph, node_count = self.set_nodes_from_file(graph, path, nodetype)
                        nodetype_counts[nodetype] = node_count
                        total_assigned += node_count
                    else:
                        print("Invalid node type initialization choice")
            
                #if less than count nodetypes assigned, add 1 of last type
                if total_assigned < count:
                    random_nodetypes.append(keys[len(keys) - 1])
                #if more than count nodetypes assigned, take out the last element
                elif total_assigned > count:
                    random_nodetypes.pop() #pop removes the last by default

                random.seed(123)
                random.shuffle(random_nodetypes)

                print("--->", str(len(random_nodetypes)))

                i = 0
                for node in graph.nodes:
                    #node variable here is not the node itself, but an int
                    #print("node", node) 
                    # if node is not already set
                    # print("i", i)
                    if 'node' not in graph.nodes[node]:
                        random_nodetype = random_nodetypes[i]
                        nodetype_counts[random_nodetype] +=1
                        nx.set_node_attributes(self.G, {node:{"node": random_nodetype}}) 
                        i += 1 #increment i for next iteration     

                print("NODE COUNTS-->", nodetype_counts)

        return graph

    def choose_nodes_with_centrality(self, metric, k, graph, nodetype):    
        print("Inside choose nodes with centrality")
        # Step 1: Choose k nodes        
        if metric == 'degree':
            centrality = nx.degree_centrality(graph)
        elif metric == 'pagerank':
            print("Before pagerank")
            centrality = nx.pagerank(graph)
            # print("Page rank results", centrality)
        elif metric == 'betweenness':
            centrality = nx.betweenness_centrality(graph)
        elif metric == 'closeness':
            centrality = nx.closeness_centrality(graph)
        elif metric == 'eigenvector':
            centrality = nx.eigenvector_centrality(graph)
        elif metric == 'katz':
            centrality = nx.katz_centrality(graph)
        else:
            print("Unknown metric", metric)
            raise ValueError(f"Unknown metric: {metric}")

        print("Before sorted nodes")
        sorted_nodes = sorted(centrality.items(), key=lambda item: item[1], reverse=True)
        print("sorted nodes", sorted_nodes)
        top_k_nodes = [node for node, _ in sorted_nodes[:k]]

        print("Top k nodes:", top_k_nodes)

        # Step 2: Add the nodetype to these k nodes
        for node in top_k_nodes:
            nx.set_node_attributes(graph, {node:{"node": nodetype}}) 

        # Return the resulting graph    
        return graph
    
    def set_nodes_from_file(self, graph, path, nodetype):
        node_count = 0
    
        # Read the .csv file
        with open(path, 'r') as file:
            reader = csv.reader(file)
            
            #print("reading file rn")
            for row in reader:
                #print("row", row)
                for node_id in row:
                    #print("nodeid before", node_id)
                    node_id = node_id.strip()
                    #print("nodeid after", node_id)
                    if node_id.isdigit():
                        node_id = int(node_id)
                        #print("digit", node_id)
                        if node_id in graph.nodes:
                            nx.set_node_attributes(graph, {node_id: {"node": nodetype}})
                            node_count += 1
                            
        return graph, node_count
        

