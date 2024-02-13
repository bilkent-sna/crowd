import csv
import pandas as pd
import networkx as nx
import importlib
import random
import math
from .structure import Structure


class File(Structure):
    def __init__(self, structure, conf):
        super().__init__(structure)
        super().__init__(structure)
        self.conf = conf

    def create(self):
        print("Creating file structure")

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
                df = pd.read_csv(self.structure['path'], sep='\t', header=header)

                self.G = nx.read_edgelist(self.structure['path'], create_using = nx.Graph(), nodetype=int) 

                count = self.conf["info"]["total_count"]
                nodetype_counts = {}
                for nodetype in list(self.conf["definitions"]["nodetypes"].keys()):
                    nodetype_counts[nodetype] = 0
                    
                weights = [0.1, 0.1, 0.8]
                #random_nodetypes = random.choices(list(self.conf["definitions"]["nodetypes"].keys()), cum_weights=[20,40,100], k=count)
                
                random_nodetypes = []
                keys = list(self.conf["definitions"]["nodetypes"].keys())
                for i in range(0,len(keys)):
                    random_nodetypes.extend([keys[i]]*int(math.ceil(weights[i]*count)))

                #if len(random_nodetypes) < count:

                random.seed(19)
                
                random.shuffle(random_nodetypes)
                #random.shuffle(random_nodetypes)
                print(random.getstate())
                print("--->", str(len(random_nodetypes)))

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
                    
                    for i in range(0, count):
                        #random_nodetype = random.choice(list(self.conf["definitions"]["nodetypes"].keys()))
                        random_nodetype = random_nodetypes[i]
                        nodetype_counts[random_nodetype] +=1
                        nx.set_node_attributes(self.G, {i:{"node": random_nodetype}})


            except:
                raise("Specified network file "+self.structure["path"] +" does not exist")
            
        print("-- GRAPH DETAILS---->", nx.info(self.G))
        degrees = [val for (node, val) in self.G.degree()]
        print(sum(degrees)/float(len(self.G)))
        return self.G
