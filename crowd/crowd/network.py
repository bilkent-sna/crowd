import networkx as nx
import os
import importlib
import random
import sys
import csv
import pandas as pd
from crowd import node as n
from .visualization import visualizer as v
from .visualization import basic as bv

from crowd.confchecker import ConfChecker
from crowd.networkcreator import NetworkCreator
from crowd.digress import file_digress as fd

class Network:
    
    def __init__(self, network_file):
        conf_checker = ConfChecker(network_file)
        self.conf = conf_checker.get_conf()
        print("Got conf")
        if self.conf is not None:
            network_creator = NetworkCreator(self.conf)            
            self.G = network_creator.create_network()
            print("G-->")    
            print(self.G)
    """
    def create_random_edges(self):
        count = self.conf["info"]["total_count"]
        max_edges = (count-1)**2
        edge_count = random.randit(1, max_edges)

        for i in range(0, edge_count):
            self.G.add_edge()
    """
    
    def execute_action(self, nodenum, node, action):
        new_module = importlib.import_module(self.conf["definitions"]["source"], package=None)   
        cls = getattr(new_module, self.conf["definitions"]["source"])
        action_funct = getattr(cls, action)
        action_funct(nodenum, self)

    def select_nodes_for_action(self, count):
        indexes = range(0, count)
        new_module = importlib.import_module(self.conf["definitions"]["source"], package=None)   
        cls = getattr(new_module, self.conf["definitions"]["source"])
        if hasattr(cls, "select_nodes"):
            selection_funct = getattr(cls, "select_nodes")
            return selection_funct(self)
        else:
            return random.sample(indexes, k=count)
        
    def run_states(self, states_file, visualizers=None):
        
        try:
            df = pd.read_csv(states_file, sep='\t', header=0)
            nodes = df.ix[:,0]
            columns = df.columns
            for column in columns[1:,]:
                print(column)
                states = df[column]
                index = 0
                for i in range(len(states)):
                    nx.set_node_attributes(self.G, {nodes[i]:{"state":states[i]}})

                if visualizers is not None:
                    for visualizer in visualizers:
                        visualizer.draw(self, column)
            
            if visualizers is not None:
                for visualizer in visualizers:
                    visualizer.animate()
            print(self.G.nodes(data=True))
        except:
            raise ("Specified state file "+states_file+" not found")
        
    def run(self, 
            epochs, # no of iterations 
            visualizers=None, #  
            snapshot_period=100, # no of epochs the snapshot will be taken
            agility=1, # ratio of active nodes in the epoch, 1 means all nodes, 0 means single node
            digress=None
            ):
        print(self.conf)
        count = self.conf["info"]["total_count"]
        
        if agility == 0:
            selection_count = 1
        else:
            selection_count = count*agility
        
        for epoch in range(0, epochs): # for each epoch
            selected_nodes_for_action = self.select_nodes_for_action(selection_count)

            for nodenum in selected_nodes_for_action:
                actions = self.G.nodes[nodenum]['node'].select_actions(self.conf["definitions"]["node_actions"])
                for action in actions:
                    self.execute_action(nodenum, self.G.nodes[nodenum], action)
            
            if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                print("Epoch:", epoch)
                if visualizers is not None:
                    for visualizer in visualizers:
                        visualizer.draw(self, epoch)

                if digress is not None:
                    #":" changed to "-" since windows does not allow : in file names
                    digress.save(str(epoch) +"-"+str(self.run_function(self.conf["definitions"]["statfunctions"][0])))

                #for node, data in self.G.nodes.data():
                #    print(node, type(data["node"]))
        
        if visualizers is not None:
            for visualizer in visualizers:
                visualizer.animate()

    def run_function(self, function_name):

        new_module = importlib.import_module(self.conf["definitions"]["source"], package=None)   
        cls = getattr(new_module, self.conf["definitions"]["source"])    

        """
        new_module = importlib.import_module(self.conf["definitions"], package=None)   
        cls = getattr(new_module, self.conf["definitions"])
        """
        # // need to update this, as there may be many emit functions
        stat_function = getattr(cls, function_name)
        return stat_function(self)
        