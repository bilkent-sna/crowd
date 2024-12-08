import networkx as nx
import igraph as ig
import importlib
import random

import pandas as pd
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
            return int(self.conf["structure"]["random"]["degree"])
        except Exception as ex:
            return 4
            
    def create(self):
        # print("Creating random structure")

        if "count" in self.conf["structure"]["random"]:
            count = int(self.conf["structure"]["random"]["count"])
        else:
            # not all models require node count, so we set it to 0 initially
            # then update after generating the network.
            count = 0  

        # print("Count at random.create: ", count)
        # print("conf at random", self.conf)

        graph_type = self.conf["structure"]["random"]["type"]

        self.G = None
        if "preprocessing" not in self.conf:
            
            if graph_type == 'random-regular':
                print("Creating random regular graph")
                degree = int(self.conf["structure"]["random"]["degree"])
                self.G = nx.random_regular_graph(degree, count, seed=None)
            elif graph_type == 'erdos-renyi':
                prob = float(self.conf["structure"]["random"]["p"]) # probability for edge creation
                self.G = nx.erdos_renyi_graph(count, prob, seed = None)
            elif graph_type == 'barabasi-albert':
                m = int(self.conf["structure"]["random"]["m"]) # number of edges to attach from a new node to existing nodes
                self.G = nx.barabasi_albert_graph(count, m, seed = None, initial_graph=None)
            elif graph_type == 'watts-strogatz':
                k = int(self.conf["structure"]["random"]["k"]) # each node is joined with its k nearest neighbors in a ring topology
                prob = float(self.conf["structure"]["random"]["p"]) # probability of rewiring each edge
                self.G = nx.watts_strogatz_graph(count, k, prob, seed = None)
            elif graph_type == 'connected-watts-strogatz':
                k = int(self.conf["structure"]["random"]["k"]) # each node is joined with its k nearest neighbors in a ring topology
                prob = float(self.conf["structure"]["random"]["p"]) # probability of rewiring each edge
                tries = int(self.conf["structure"]["random"]["tries"]) # number of attempts to generate a connected graph
                self.G = nx.connected_watts_strogatz_graph(count, k, prob, tries, seed = None)
            elif graph_type == 'newman_watts_strogatz':
                k = int(self.conf["structure"]["random"]["k"]) # each node is joined with its k nearest neighbors in a ring topology
                prob = float(self.conf["structure"]["random"]["p"]) # probability of rewiring each edge
                self.G = nx.newman_watts_strogatz_graph(count, k, prob, seed = None)
            elif graph_type == 'powerlaw-cluster-graph':
                m = int(self.conf["structure"]["random"]["m"]) # the number of random edges to add for each new node
                prob = float(self.conf["structure"]["random"]["p"]) # probability of adding a triangle after adding a random edge
                self.G = nx.powerlaw_cluster_graph(count, m, prob, seed = None)
            elif graph_type == 'forest-fire':
                fw_prob = float(self.conf["structure"]["random"]["fw-prob"]) # forward burning probability
                bw_fact = float(self.conf["structure"]["random"]["bw-factor"]) # backward burning ratio
                forest_fire_graph = ig.Graph.Forest_Fire(fw_prob = fw_prob, bw_factor = bw_fact, n = count, directed = False)
                self.G = forest_fire_graph.to_networkx()
            elif graph_type == 'stochastic-block': # Also exists in networkX, but we chose igraph as it is faster
                matrix = self.conf["structure"]["random"]["p-matrix"]
                blocks = self.conf["structure"]["random"]["block-sizes"]
                if "include-loops" in self.conf["structure"]["random"]:
                    include_loops = bool(self.conf["structure"]["random"]["include-loops"])
                else:
                    include_loops = False
                stochastic_block_graph = ig.Graph.SBM(n = count, pref_matrix = matrix, block_sizes = blocks, directed = False, loops = include_loops)
                self.G = stochastic_block_graph.to_networkx()
            elif graph_type == 'LFR-benchmark':
                settings = self.conf["structure"]["random"]
                tau1 = float(settings["tau1"])
                tau2 = float(settings["tau2"])
                mu = float(settings["mu"])
                if "avg-degree" in settings:
                    avg_degree = float(settings["avg-degree"])
                else:
                    avg_degree = None
                if "min-degree" in settings:
                    min_degree = int(settings["min-degree"])
                else:
                    min_degree = None
                if "max-degree" in settings:
                    max_degree = int(settings["max-degree"])
                else:
                    max_degree = None
                if "min-community" in settings:
                    min_comm = int(settings["min-community"])
                else:
                    min_comm = None
                if "max-comunity" in settings:
                    max_comm = int(settings["max-community"])
                else: 
                    max_comm = None
                if "tolerance" in settings:
                    tol = float(settings["tolerance"])
                else:
                    tol = 1e-07
                if "max-iterations" in settings:
                    max_iters = int(settings["max-iterations"])
                else:
                    max_iters = 500
                self.G = nx.LFR_benchmark_graph(count, tau1, tau2, mu, avg_degree, min_degree, max_degree, min_comm, max_comm, tol, max_iters)
            elif graph_type == 'geometric-random':
                radius = float(self.conf["structure"]["random"]["radius"])
                self.G = ig.Graph.GRG(count, radius).to_networkx()
            elif graph_type == 'configuration':
                file_path = self.conf["structure"]["random"]["degrees-path"]
                degrees_list = pd.read_csv(file_path, header=None).iloc[:, 0].tolist()
                if "method" in self.conf["structure"]["random"]:
                    method = self.conf["structure"]["random"]["method"]
                else:
                    method = 'configuration'
                self.G = ig.Graph.DegreeSequence(out = degrees_list, method = method).to_networkx()
                count = self.G.number_of_nodes()
            elif graph_type == 'static-fitness':
                m = int(self.conf["structure"]["random"]["m"]) # number of edges
                if "include-loops" in self.conf["structure"]["random"]:
                    include_loops = bool(self.conf["structure"]["random"]["include-loops"])
                else:
                    include_loops = False
                fitness_path = self.conf["structure"]["random"]["fitness-path"]
                fitness_list = pd.read_csv(fitness_path, header=None).iloc[:, 0].tolist()
                self.G = ig.Graph.Static_Fitness(
                    m = m,
                    fitness_out = fitness_list,
                    loops = include_loops,
                    multiple = False
                ).to_networkx()
                count = self.G.number_of_nodes()


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
    
        
