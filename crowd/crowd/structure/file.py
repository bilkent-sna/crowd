import csv
import pandas as pd
import networkx as nx
import importlib
import random
import math
import os
from .structure import Structure


class File(Structure):
    def __init__(self, structure, conf):
        super().__init__(structure)
        # super().__init__(structure)
        self.conf = conf
        #print("CONF FROM FILE", conf, "\n\n\n\n\n\n")

    def create(self):
        print("Creating file structure")

        _, file_extension = os.path.splitext(self.structure['path'])

        # Create nodes only network
        if self.structure["type"] == "nodes_only":
            try:
                # Read the network file
                header = 0 if self.structure["header"] else 1
                df = pd.read_csv(self.structure['path'], sep='\t', header=header)
                print(df)
                
                # Create the network with no nodes and edges
                self.G=nx.Graph()
                for row_dict in df.to_dict(orient="records"):
                    #print(row._asdict())
                    print(row_dict)
                    #row_dict = row._asdict()
                    self.G.add_node(row_dict['Id'])
                    nx.set_node_attributes(self.G, {row_dict['Id']:row_dict})
            except:
                raise("Specified network file "+self.structure["path"] +" does not exist")

        elif self.structure["type"] == "nodes_edges":
            try:
                # Read the network file
                header = 0 if self.structure["header"] else 1

                if file_extension == ".csv":
                    #df = pd.read_csv(self.structure['path'], sep='\t', header=header)
                    df = pd.read_csv(self.structure['path'], sep=',', header=header)
                    #print("The dataframe:", df.head())

                    #self.G = nx.read_edgelist(self.structure['path'], create_using = nx.Graph(), nodetype=int) 
                    if(header == 0):
                        headers = df.columns.tolist()
                        print("Headers of dataframe: ", headers)
                        self.G = nx.from_pandas_edgelist(df, source = headers[0], target = headers[1], create_using = nx.Graph()) 
                        print(self.G)
                
                elif file_extension == ".edgelist":
                    self.G = nx.read_edgelist(self.structure['path'], create_using = nx.Graph(), nodetype=int)
                    print("Printing an edgelist file info check: ", self.G)
                    
                #count = self.conf["info"]["total_count"]
                count = self.G.number_of_nodes()

                # if source or diffusion model not defined, don't do these steps
                if "source" in self.conf["definitions"] or "pd-model" in self.conf["definitions"]:
                    nodetype_counts = {}
                    for nodetype in list(self.conf["definitions"]["pd-model"]["nodetypes"].keys()):
                        nodetype_counts[nodetype] = 0
                        
                    print("FILE_PASS2")

                    #weights = [0.1, 0.1, 0.8]
                    #we should read weights from conf file instead
                    #weights = self.conf["definitions"]["pd-model"]["type-weights"]
                    #random_nodetypes = random.choices(list(self.conf["definitions"]["nodetypes"].keys()), cum_weights=[20,40,100], k=count)
                    
                    random_nodetypes = []
                    keys = list(self.conf["definitions"]["pd-model"]["nodetypes"].keys())
                    print("AFTER PASS2, KEYS LIST:", keys)
                    for i in range(0,len(keys)):
                        #random_nodetypes.extend([ keys[i] ] * int(math.ceil(weights[i]*count)))
                        curr_weight = float(self.conf["definitions"]["pd-model"]["nodetypes"][keys[i]]['initial-weight'])
                        print("AFTER PASS2, NO PROBLEM WITH WEIGHT")
                        random_nodetypes.extend([ keys[i] ] * int(math.ceil(curr_weight*count)))
                        print("RANDOM NODETYPES SET")
                    #if less than count nodetypes assigned, add 1 of last type
                    if len(random_nodetypes) < count:
                        print("AFTER PASS 2, IF1")
                        random_nodetypes.append(keys[len(keys) - 1])
                        print("AFTER PASS 2, IF2")
                    #if more than count nodetypes assigned, take out the last element
                    elif len(random_nodetypes) > count:
                        print("AFTER PASS 2, ELSE1")
                        random_nodetypes.pop() #pop removes the last by default
                        print("AFTER PASS 2, ELSE2")

                    random.seed(19)
                    
                    random.shuffle(random_nodetypes)
                    #random.shuffle(random_nodetypes)
                    #print(random.getstate())
                    print("--->", str(len(random_nodetypes)))

                    print("FILE_PASS3")

                    if "source" in self.conf["definitions"]:
                        new_module = importlib.import_module(self.conf["definitions"]["source"], package=None)
                        
                        for i in range(0, count):    
                            #random_nodetype = random.choices(list(self.conf["definitions"]["nodetypes"].keys()), weights=[20,20,60], k=1)[0]
                            #cls = getattr(new_module, definitions)
                            random_nodetype = random_nodetypes[i]
                            nodetype_counts[random_nodetype] +=1
                            nodetype = getattr(new_module, random_nodetype)
                            nodeobject = nodetype()
                            nx.set_node_attributes(self.G, {i:{"node": nodetype()}})
                    else:
                        
                        """
                        for i in range(0, count):
                            #random_nodetype = random.choice(list(self.conf["definitions"]["nodetypes"].keys()))
                            random_nodetype = random_nodetypes[i]
                            nodetype_counts[random_nodetype] +=1
                            nx.set_node_attributes(self.G, {i:{"node": random_nodetype}})
                        """
                        #some edge lists may not have node 0 and it results in an error here
                        #so it is better to loop through every node instead of 0 to count
                        #but we will still have i for random_nodetypes array

                        print("FILE_PASS4")
                        i = 0
                        for node in self.G.nodes:
                            #node variable here is not the node itself, but an int=c
                            #print("node", node) 
                            random_nodetype = random_nodetypes[i]
                            nodetype_counts[random_nodetype] +=1
                            nx.set_node_attributes(self.G, {node:{"node": random_nodetype}})
                            i += 1 #increment i for next iteration

                        print("FILE_PASS5")

            except:
                raise("Specified network file " + self.structure["path"] +" does not exist")
            
        #print("-- GRAPH DETAILS---->", nx.info(self.G)) => Networkx 3.0 removed info method
        print('Number of nodes', len(self.G.nodes))
        print('Number of edges', len(self.G.edges))
        degrees = [val for (node, val) in self.G.degree()]
        print(sum(degrees)/float(len(self.G.nodes)))
        print(self.G.nodes())
        return self.G
