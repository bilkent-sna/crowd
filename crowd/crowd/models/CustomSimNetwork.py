from collections import defaultdict
import csv
import json
import os
import random
import networkx as nx
from crowd.networkcreator import NetworkCreator

class CustomSimNetwork:

    def __init__(self, conf, project_dir):
        self.conf = conf
        # print("Got conf")
        if self.conf is not None:
            # print("PASS1")
            network_creator = NetworkCreator(self.conf) 
            # print("PASS2")           
            self.G = network_creator.create_network(project_dir)
            self.project_dir = project_dir
            # print("G-->")    
            # print(self.G)

            # We allow users to define 4 kind of methods in the methods.py file in the project
            # We have default methods to read these, but user can override these methods if they want to read the methods from a different file 
            self.before_iteration_methods = None
            self.after_iteration_methods = None
            self.every_iteration_agent = None
            self.after_simulation_methods = None

            # If they exist in the conf file, node, edge and network level parameters will be added
            self.add_network_level_params(self.conf["definitions"])
            self.add_node_parameters(self.conf["definitions"])
            self.add_edge_parameters(self.conf["definitions"])

            # Access nodetypes from the conf
            self.node_types = self.conf["definitions"]["nodetypes"].keys()
            # print(self.node_types)

            self.prev_type_nums = None
            self.curr_type_nums = self.count_node_types()

            # User can write a method to early stop the simulation by changing this parameter
            self.early_stop = False


    def add_network_level_params(self, conf_part):
        # Setting network level parameters if given
        if "network-parameters" in conf_part:
            params = conf_part["network-parameters"]
            # if params is dict and params != {}:
            temp = type(params)
            if len(params) != 0:
                for param_name, param_value in params.items():
                    self.G.graph[param_name] = param_value

    def add_node_parameters(self, conf_part):
        #Setting node attribute if given
        if("node-parameters" in conf_part):
            #set node parameters depending on the type
            
            #setting numerical node parameters if given
            if("numerical" in conf_part["node-parameters"]):
                # print("TO-DO: is it possible to give user more options")
                params = conf_part["node-parameters"]["numerical"]
                if params != []: 
                    if type(params) == dict:
                        for param_name, param_values in params.items():
                            #setting the numerical attribute randomly between 2 numbers
                            #we expect user to enter these 2 numbers in a list format
                            attr = {n: {param_name: random.choice(range(int(param_values[0]), int(param_values[1])))} for n in self.G.nodes()}
                            nx.set_node_attributes(self.G, attr)
                    else:
                        # params is list type
                        for item in params:
                            for param_name, param_values in item.items():
                                attr = {n: {param_name: random.choice(range(int(param_values[0]), int(param_values[1])))} for n in self.G.nodes()}
                                nx.set_node_attributes(self.G, attr)


            #setting categorical node parameters if given
            if("categorical" in conf_part["node-parameters"]):
                params = conf_part["node-parameters"]["categorical"]
                if params != []:
                    if type(params) == dict:
                        for param_name, param_values in params.items():
                            #setting the categorical attribute randomly
                            #ndlib does not provide a method for this so we can add
                            #to conf file if user has any requirements
                            if type(param_values) == str:
                                    print("Param values before read_options:", param_values)
                                    param_values = self.read_options_file(param_values)
                                    print("Param values after setting as a list:", param_values)
                            attr = {n: {param_name: random.choice(param_values)} for n in self.G.nodes()}
                            nx.set_node_attributes(self.G, attr)
                    else:
                        for item in params:
                            for param_name, param_values in item.items():
                                if type(param_values) == str: # we should read the options from the file
                                    # param_values hold the name of the dataset
                                    # read the values from the data file and return a list
                                    # put this list into param_values
                                    print("Param values before read_options:", param_values)
                                    param_values = self.read_options_file(param_values)
                                    print("Param values after setting as a list:", param_values)
                                attr = {n: {param_name: random.choice(param_values)} for n in self.G.nodes()}
                                nx.set_node_attributes(self.G, attr)

    def read_options_file(self, path):
        # Read the .csv file
        path = os.path.join(self.project_dir, 'datasets', path)
        with open(path, 'r') as file:
            reader = csv.reader(file)
            return [row[0] for row in reader if row]
 

    def add_edge_parameters(self, conf_part):
         #Setting edge attribute if given
        if("edge-parameters" in conf_part):
            #set edge parameters depending on the type
            if("numerical" in conf_part["edge-parameters"]):
                params = conf_part["edge-parameters"]["numerical"]

                if params != []:
                    if type(params) == dict:
                        for param_name, param_value in params.items():
                            '''
                            ndlib's example:
                            attr = {(u, v): {"weight": int((u+v) % 10)} for (u, v) in g.edges()}
                            our case: we take "weight: int((u+v) % 10)" in the yaml file?  
                            '''
                            #would this work? param_values will be a string but we want it to be a calculation
                            #attr = {(u, v) : {param_name: param_values} for (u, v) in self.G.edges()}
                            attr = {(u, v) : {param_name: int((u+v) % 10)} for (u, v) in self.G.edges()}
                            nx.set_edge_attributes(self.G, attr)
                    else:
                        for item in params:
                            for param_name, param_value in item.items():
                                '''
                                ndlib's example:
                                attr = {(u, v): {"weight": int((u+v) % 10)} for (u, v) in g.edges()}
                                our case: we take "weight: int((u+v) % 10)" in the yaml file?  
                                '''
                                #would this work? param_values will be a string but we want it to be a calculation
                                #attr = {(u, v) : {param_name: param_values} for (u, v) in self.G.edges()}
                                attr = {(u, v) : {param_name: int((u+v) % 10)} for (u, v) in self.G.edges()}
                                nx.set_edge_attributes(self.G, attr)
                            
            
            if("categorical" in conf_part["edge-parameters"]):
                params = conf_part["edge-parameters"]["categorical"]
                if params != []:
                    if type(params) == dict:
                        for param_name, param_value in params.items():
                            #setting the categorical attribute randomly
                            #ndlib does not provide a method for this so we can add
                            #to conf file if user has any requirements
                            attr = {(u, v): {param_name: random.choice(param_value)} for (u, v) in self.G.edges()}
                            attr.update({(v, u): attr[(u, v)] for (u, v) in self.G.edges()})
                            nx.set_edge_attributes(self.G, attr)
                    else: 
                        for item in params:
                            for param_name, param_value in item.items():
                                #setting the categorical attribute randomly
                                #ndlib does not provide a method for this so we can add
                                #to conf file if user has any requirements
                                attr = {(u, v): {param_name: random.choice(param_value)} for (u, v) in self.G.edges()}
                                attr.update({(v, u): attr[(u, v)] for (u, v) in self.G.edges()})
                                nx.set_edge_attributes(self.G, attr)
                                    
    # Returns the change in the number of nodes each type
    def status_delta(self):
        if self.prev_type_nums is None:
            return {}  # or None

        # Calculate the delta for each node type
        status_delta = {node_type: self.curr_type_nums.get(node_type, 0) - self.prev_type_nums.get(node_type, 0)
                        for node_type in self.curr_type_nums}

        return status_delta


    def count_node_types(self):
        # Initialize a dictionary to store the counts
        type_counts = defaultdict(int)

        # Iterate over all nodes in the graph
        for node in self.G.nodes(data=True):
            node_type = node[1].get('node')  # Access the 'node' attribute
            
            # If the node type is in the list of node_types, count it
            if node_type in self.node_types:
                type_counts[node_type] += 1
        
        # Ensure all node types in node_types are represented, even if count is zero
        for node_type in self.node_types:
            type_counts[node_type] += 0

        return dict(type_counts)


    def run(self, 
            epochs, # no of iterations 
            visualizers=None, #  
            snapshot_period=100, # no of epochs the snapshot will be taken
            agility=1, # ratio of active nodes in the epoch, 1 means all nodes, 0 means single node
            digress=None
            ):
        
        # Iteration data dictionary
        simulation_data = {}

        # Holds how many epochs actually executed
        # Is updated if early stopping occurs
        actual_epochs = epochs

        for epoch in range(0, epochs): # for each epoch

            self.prev_type_nums = self.curr_type_nums
            
            if epoch != 0:
                # execute before iteration methods, which are to prepare for this iteration
                # and if any results returned, save them in simulation data dict
                if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                    simulation_data = self.execute_before_iteration(epoch, simulation_data)
                else:
                    self.execute_before_iteration(epoch, None)
                

                for node_id in self.G.nodes:
                    self.execute_every_iteration_agent(epoch, node_id)

                self.curr_type_nums = self.count_node_types()

            if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                # print("Epoch:", epoch)
                if visualizers is not None:
                    for visualizer in visualizers:
                        visualizer.draw(self, epoch)
                if digress is not None:
                    digress.save_graph(str(epoch), self.G, 'graph.json')

                #Add code here to store status delta to file
                # Available status is sent as None, because we have the nodetypes stored as it is given,
                # not 0, 1, 2... like NDLib uses. So, no need to convert in the save_statusdelta function.
                digress.save_statusdelta(epoch, self.status_delta(), 'status_delta.json', None)
                digress.save_statusdelta(epoch, self.curr_type_nums, 'count_node_types.json', None)
            
            if epoch != 0:
                # execute after iteration methods, which utilizes the new states of the agents
                # if any results returned, save in simulation data dict
                if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                    simulation_data = self.execute_after_iteration(epoch, simulation_data)
                else:
                    to_send = None
                    self.execute_after_iteration(epoch, to_send)

            if self.early_stop:
                # change epoch param and return it so it can be saved to simulation info
                # Ex: early_stop : true
                #     epoch: 20
                actual_epochs = epoch
                break
        
        # simulation is finished
        if visualizers is not None:
            for visualizer in visualizers:
                visualizer.animate()

        if digress is not None and len(simulation_data) != 0:
            digress.save_iteration_data(simulation_data)
        
        self.execute_after_simulation(digress)

        return self.early_stop, actual_epochs

    # This method will be called for all 4 types of user-entered methods
    def execute_methods(self, epoch, method_list, data_dict = None, agent_id = None):
        if method_list is not None:
            for method in method_list:
                #call each method
                if isinstance(method, list): #then it is a method with parameters
                    #first value in the list is the name of the function
                    #following ones are parameters
                    parameters = [self]
                    if agent_id is not None:
                        parameters.append(agent_id)
                    for i in range(1, len(method)):
                        parameters.append(method[i])
                    # print("Parameters:", parameters)
                    
                    if data_dict: # if it is not None, which means this is not agent method
                        key_to_save = method[0].__name__
                        if key_to_save not in data_dict:
                            data_dict[key_to_save] = []
                        if epoch is not None:
                            data_dict[key_to_save].append({
                                "Iteration": epoch,
                                "Value": method[0](*parameters)
                            })
                        else: # after simulation
                            data_dict[key_to_save] = method[0](*parameters)
                            # data_dict[key_to_save].append({
                            #     "Value": method[0](*parameters)
                            # })
                    else: # just run the method
                        method[0](*parameters)
                else:                    
                    if data_dict is not None:
                        key_to_save = method.__name__ 
                        if key_to_save not in data_dict:
                            data_dict[key_to_save] = []
                        if epoch is not None:    
                            data_dict[key_to_save].append({
                                "Iteration": epoch,
                                "Value":  method(self)
                            })
                        else: # after simulation
                            data_dict[key_to_save] = method(self)
                            # data_dict[key_to_save].append({
                            #     "Value": method(self)
                            # })
                    else:
                        if agent_id is not None:
                            method(self, agent_id)
                        else:
                            method(self)
        if data_dict is not None:
            return data_dict
    
    def execute_before_iteration(self, epoch, simulation_data):
        return self.execute_methods(epoch, self.before_iteration_methods, simulation_data)

    def execute_every_iteration_agent(self, epoch, agent_id):
        self.execute_methods(epoch, self.every_iteration_agent, None, agent_id)

    def execute_after_iteration(self, epoch, simulation_data):
        return self.execute_methods(epoch, self.after_iteration_methods, simulation_data)

    def execute_after_simulation(self, digress):
        data = {}

        self.execute_methods(epoch = None, method_list=self.after_simulation_methods, data_dict=data, agent_id=None)
        digress.save(json.dumps(data), 'parameters/after_simulation.json')

    