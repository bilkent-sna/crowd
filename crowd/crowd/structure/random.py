import networkx as nx
import importlib
import random
from .structure import Structure
import math

class Random(Structure):
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
        # count = self.conf["info"]["total_count"]
        count = self.conf["structure"]["random"]["count"]
        print("Count at random.create: ", count)
        print("conf at random", self.conf)

        self.G = None
        if "preprocessing" not in self.conf:
            #if "random" in self.structure:
            print("Creating random regular graph")
            self.G = nx.random_regular_graph(self.get_degree_count(), count, seed=None)
            #else:
            #    self.G = nx.read_edgelist(self.structure, create_using = nx.Graph(), nodetype=int)            

            #else still needs to be changed bc we changed the conf file 
            if("definitions" in self.conf):
                if "pd-model" in self.conf["definitions"]: #if it is a predefined model
                    print("random.py - inside pd-model")
                    if(self.conf["definitions"]["pd-model"]["name"] == "diffusion"): #if it is a diffusion model
                        if(self.conf["definitions"]["pd-model"]["nodetypes"] != None): #if nodetypes are defined
                            nodetype_counts = {}
                            #take out [pd-model] if code works like this
                            nodetype_dict = self.conf["definitions"]["pd-model"]["nodetypes"]
                            keys = list(nodetype_dict.keys())
                            
                            for nodetype in keys:
                                nodetype_counts[nodetype] = 0
                            
                            #fill the weights array with the numbers given in the conf file
                            weights = []
                            for element in nodetype_dict.values():
                                weights.append(float(element['initial-weight']))
                            
                            #weights = self.conf["definitions"]["pd-model"]["type-weights"]
                        
                            random_nodetypes = []
                            #keys = list(self.conf["definitions"]["nodetypes"].keys())
                    
                            for i in range(0,len(keys)):
                                random_nodetypes.extend([ keys[i] ] * int(math.ceil(weights[i]*count)))

                            #if less than count nodetypes assigned, add 1 of last type
                            if len(random_nodetypes) < count:
                                random_nodetypes.append(keys[len(keys) - 1])
                            #if more than count nodetypes assigned, take out the last element
                            elif len(random_nodetypes) > count:
                                random_nodetypes.pop() #pop removes the last by default

                            random.seed(19)
                                
                            random.shuffle(random_nodetypes)
                            #random.shuffle(random_nodetypes)
                            #print(random.getstate())
                            print("--->", str(len(random_nodetypes)))
                            
                            '''
                            for i in range(0, count):
                                #deleted [].keys() here
                                    
                                random_nodetype = random.choice(list(self.conf["definitions"]["pd-model"]["nodetypes"]))
                                nodetype_counts[random_nodetype] +=1
                                nx.set_node_attributes(self.G, {i:{"node": random_nodetype}})
                            '''
                                
                            i = 0
                            for node in self.G.nodes:
                                #node variable here is not the node itself, but an int
                                #print("node", node) 
                                random_nodetype = random_nodetypes[i]
                                nodetype_counts[random_nodetype] +=1
                                nx.set_node_attributes(self.G, {node:{"node": random_nodetype}})
                                i += 1 #increment i for next iteration
                            print("NODE COUNTS-->", nodetype_counts) 
                        else:
                            print("Nodetypes not defined in the configuration file.")
                    else:
                        print("It is not defined as a diffusion model. You may want to check the configuration file.")

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