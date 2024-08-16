import networkx as nx
import importlib
import random
from .structure import Structure
from ..preprocessing import communitydetection as com
import math

class CombinedRandom(Structure):
    def __init__(self, structure, conf, project_dir, seed=123):
        super().__init__(structure, project_dir)
        self.seed = seed
        self.conf = conf

    # REWRITE NEEDED
    def get_degree_count(self):
        try:
            return self.conf["structure"]["random"]["degree"]
        except Exception as ex:
            return 4
            
    def create(self):
        print("Creating random structure")
        count = self.conf["structure"]["random"]["count"]
        print("Count at random.create: ", count)
        print("conf at random", self.conf)

        graph_type = self.conf["structure"]["random"]["type"]

        self.G = None
        if "preprocessing" not in self.conf:
            
            if graph_type == 'random-regular':
                print("Creating random regular graph")
                degree = self.conf["structure"]["random"]["degree"]
                self.G = nx.random_regular_graph(degree, count, seed=None)
            elif graph_type == 'erdos-renyi':
                prob = self.conf["structure"]["random"]["p"] # probability for edge creation
                self.G = nx.erdos_renyi_graph(count, prob, seed = None)
            elif graph_type == 'barabasi-albert':
                m = self.conf["structure"]["random"]["m"] # number of edges to attach from a new node to existing nodes
                self.G = nx.barabasi_albert_graph(count, m, seed = None, initial_graph=None)
            elif graph_type == 'watts-strogatz':
                k = self.conf["structure"]["random"]["k"] # each node is joined with its k nearest neighbors in a ring topology
                prob = self.conf["structure"]["random"]["p"] # probability of rewiring each edge
                self.G = nx.watts_strogatz_graph(count, k, prob, seed = None)
            elif graph_type == 'connected-watts-strogatz':
                k = self.conf["structure"]["random"]["k"] # each node is joined with its k nearest neighbors in a ring topology
                prob = self.conf["structure"]["random"]["p"] # probability of rewiring each edge
                tries = self.conf["structure"]["random"]["tries"] # number of attempts to generate a connected graph
                self.G = nx.connected_watts_strogatz_graph(count, k, prob, tries, seed = None)
            elif graph_type == 'newman_watts_strogatz':
                k = self.conf["structure"]["random"]["k"] # each node is joined with its k nearest neighbors in a ring topology
                prob = self.conf["structure"]["random"]["p"] # probability of rewiring each edge
                self.G = nx.newman_watts_strogatz_graph(count, k, prob, seed = None)
            elif graph_type == 'powerlaw-cluster-graph':
                m = self.conf["structure"]["random"]["m"] # the number of random edges to add for each new node
                prob = self.conf["structure"]["random"]["p"] # probability of adding a triangle after adding a random edge
                self.G = nx.powerlaw_cluster_graph(count, m, prob, seed = None)


            #else still needs to be changed bc we changed the conf file 
            if("definitions" in self.conf):
                if "pd-model" in self.conf["definitions"] or self.conf["definitions"]["name"] == 'custom': #if it is a predefined model
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