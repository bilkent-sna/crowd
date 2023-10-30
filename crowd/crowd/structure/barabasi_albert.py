import networkx as nx
import importlib
import random
from .structure import Structure

class BarabasiAlbert(Structure):
    def __init__(self, structure, conf, seed=123):
        super().__init__(structure)
        self.seed = seed
        self.conf = conf

    def get_degree_count(self):
        try:
            return self.conf["structure"]["random"]["degree"]
        except Exception as ex:
            return 4
            
    def create(self):
        print("Creating random structure")
        count = self.conf["info"]["total_count"]
        self.G = None
        if "preprocessing" not in self.conf:
            #if "random" in self.structure:
            print("Creating random regular graph")
            #self.G = nx.random_regular_graph(self.get_degree_count(), count, seed=None)
            self.G = nx.barabasi_albert_graph(count, self.get_degree_count() )
            #else:
            #    self.G = nx.read_edgelist(self.structure, create_using = nx.Graph(), nodetype=int)            

            nodetype_counts = {}
            for nodetype in list(self.conf["definitions"]["nodetypes"].keys()):
                nodetype_counts[nodetype] = 0
                
            if "source" in self.conf["definitions"]:
                new_module = importlib.import_module(self.conf["definitions"]["source"], package=None)
                
                for i in range(0, count):    
                    random_nodetype = random.choices(list(self.conf["definitions"]["nodetypes"].keys()), weights=[20,20,60], k=1)[0]
                    #cls = getattr(new_module, definitions)
                    nodetype_counts[random_nodetype] +=1
                    nodetype = getattr(new_module, random_nodetype)
                    nodeobject = nodetype()
                    nx.set_node_attributes(self.G, {i:{"node": nodetype()}})
            else:
                
                for i in range(0, count):
                    random_nodetype = random.choice(list(self.conf["definitions"]["nodetypes"].keys()))
                    nodetype_counts[random_nodetype] +=1
                    nx.set_node_attributes(self.G, {i:{"node": random_nodetype}})
            
            print(nodetype_counts)   
            
        else:
            preprocessing = self.conf["preprocessing"]
            print(preprocessing)
            for op in preprocessing:
                # new_module = importlib.import_module(op)
                if op == "communitydetection":
                    
                    if structure is None:
                        
                        #self.G = nx.random_regular_graph(self.get_degree_count(), count, seed=None)
                        self.G = nx.barabasi_albert_graph(count, self.get_degree_count() )
                        degrees = self.G.degree()
                        degree = sum([ x[1] for x in degrees]) / self.G.number_of_nodes()
                        print("average_degree :"+ str(degree))
                        cd  = com.CommunityDetection()
                        while not cd.process(self, preprocessing[op]):
                            #self.G = nx.random_regular_graph(self.get_degree_count(), count, seed=None)
                            self.G = nx.barabasi_albert_graph(count, self.get_degree_count() )
                    else:
                        self.G = nx.read_edgelist(structure, create_using = nx.Graph(), nodetype=int) 
                        cd  = com.CommunityDetection()
                        cd.process(self, preprocessing[op])
        print("Returning G-->", self.G)    
        return self.G