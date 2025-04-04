import networkx as nx
import importlib
import random
from .structure import Structure
from ..preprocessing import communitydetection as com
import math

class FromLibrary(Structure):
    def __init__(self, structure, conf, project_dir, seed=123):
        super().__init__(structure, project_dir)
        self.seed = seed
        self.conf = conf

    def get_degree_count(self):
        try:
            return self.conf["structure"]["random"]["degree"]
        except Exception as ex:
            return 4
            
    def create(self):
        conf_part = self.conf["structure"]["from-library"]
        graph_type = conf_part["type"]

        self.G = None
        if "preprocessing" not in self.conf:
            
            if graph_type == 'complete-graph':
                count = conf_part["count"]
                self.G = nx.complete_graph(count)
            elif graph_type == 'karate-club-graph':
                self.G = nx.karate_club_graph()
            elif graph_type == 'davis-southern-woman':
                self.G = nx.davis_southern_women_graph()
            elif graph_type == 'florentine-families':
                self.G = nx.florentine_families_graph()
            elif graph_type == 'les-miserables':
                self.G = nx.les_miserables_graph()

            #else still needs to be changed bc we changed the conf file 
            if("definitions" in self.conf):
                if "pd-model" in self.conf["definitions"]: #if it is a predefined model
                    self.G = self.set_nodetypes(self.G, self.conf, count)
                #if not a diffusion model
                # else:
                elif "source" in self.conf["definitions"]: 
                    print("random.py - source")
                    nodetype_counts = {}
                    for nodetype in list(self.conf["definitions"]["nodetypes"].keys()):
                        nodetype_counts[nodetype] = 0
                        
                    if "source" in self.conf["definitions"]:
                        new_module = importlib.import_module(self.conf["definitions"]["source"], package=None)
                        
                        weights = [0.1, 0.1, 0.8]
                        #random_nodetypes = random.choices(list(self.conf["definitions"]["nodetypes"].keys()), cum_weights=[20,40,100], k=count)
                        
                        random_nodetypes = []
                        keys = list(self.conf["definitions"]["nodetypes"].keys())
                        for i in range(0,len(keys)):
                            random_nodetypes.extend([keys[i]]*int(weights[i]*count))

                        random.seed(12)
                        random.shuffle(random_nodetypes)
                        #print("--->", random_nodetypes)
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
                            random_nodetype = random.choice(list(self.conf["definitions"]["nodetypes"].keys()))
                            nodetype_counts[random_nodetype] +=1
                            nx.set_node_attributes(self.G, {i:{"node": random_nodetype}})
                    
                    print("NODE COUNTS-->", nodetype_counts)   
            
            # if source not in conf file and not a diffusion model
            # in edge simulations, we will execute this part
            else:
                #just create the network. no need to set nodetypes into anything.
                print("Creating random regular graph")
                print("IN ELSE")
                self.G = nx.random_regular_graph(self.get_degree_count(), count, seed=None)

            
        else:
            preprocessing = self.conf["preprocessing"]
            print(preprocessing)
            for op in preprocessing:
                # new_module = importlib.import_module(op)
                if op == "communitydetection":
                    
                    if structure is None:
                        
                        self.G = nx.random_regular_graph(self.get_degree_count(), count, seed=None)
                        degrees = self.G.degree()
                        degree = sum([ x[1] for x in degrees]) / self.G.number_of_nodes()
                        print("average_degree :"+ str(degree))
                        cd  = com.CommunityDetection()
                        while not cd.process(self, preprocessing[op]):
                            self.G = nx.random_regular_graph(self.get_degree_count(), count, seed=None)
                    else:
                        self.G = nx.read_edgelist(structure, create_using = nx.Graph(), nodetype=int) 
                        cd  = com.CommunityDetection()
                        cd.process(self, preprocessing[op])
        print("Returning G-->", self.G)    
        return self.G