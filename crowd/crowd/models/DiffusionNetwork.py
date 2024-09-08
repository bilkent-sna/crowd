import random
from crowd.networkcreator import NetworkCreator
from .CustomSimNetwork import CustomSimNetwork
import ndlib.models.ModelConfig as mc
from crowd.models import BaseDiffusion as bd
import ndlib.models.compartments as cpm
import networkx as nx
from ndlib.models.compartments.enums.NumericalType import NumericalType

class DiffusionNetwork(CustomSimNetwork):

    def __init__(self, conf_dict, project_dir):
        self.conf = conf_dict
        # print("Got conf")
        if self.conf is not None:
            # print("PASS1")
            network_creator = NetworkCreator(self.conf) 
            # print("PASS2")           
            self.G = network_creator.create_network(project_dir)
            self.project_dir = project_dir
            # print("G-->")    
            # print(self.G)

            #everything about configuration is stored at self.conf

            #get model status from conf to an array
            pd_conf = self.conf["definitions"]["pd-model"]
            node_types = pd_conf["nodetypes"] #this is a dictionary

            #DEBUG: Print the configurations to verify their structure
            print("Initial configuration:", pd_conf)
            
            self.add_node_parameters(pd_conf)

            self.add_edge_parameters(pd_conf)

            #ndlib model
            self.ndlib_model = bd.BaseDiffusion(self.G, self.conf)
            
            #for each item in array
            for item in node_types.keys():
                self.ndlib_model.add_status(item)

            print("Available Status For Custom Diffusion")
            print(self.ndlib_model.available_statuses)

            #create compartments dictionary
            compartments = self.add_compartments(pd_conf)
                    
            #create rules and add them to model
            for rule in pd_conf["rules"].values():
                print("Processing rule", rule[0])
                self.ndlib_model.add_rule(rule[0], rule[1], compartments[rule[2]])          

    
            #model initial status configuration
            self.ndlib_config = mc.Configuration()

            #Setting model parameters if given
            if("model-parameters" in pd_conf):
                for parameter, value in pd_conf["model-parameters"].items():
                    print(parameter, value)
                    self.ndlib_config.add_model_parameter(parameter, value)

            #initialize the watch methods to None
            #this variable will hold a list of method names that will be called in every iteration of the simulation
            #to record the values of user-requested parameters or do a certain calculation with them
            self.before_iteration_methods = None
            self.after_iteration_methods = None
            self.after_simulation_methods = None

            # user can write a method to early stop the simulation by changing this parameter
            self.early_stop = False

    def run(self, epochs, visualizers=None, snapshot_period=100, agility=1, digress=None):  
        # Simulation execution
        self.ndlib_model.set_initial_status(self.ndlib_config)
        actual_epochs = epochs

        # Iteration data dictionary
        simulation_data = {}

        for epoch in range(0, epochs): #for each epoch

            #execute before iteration methods
            if epoch != 0:
                # execute before iteration methods, which are to prepare for this iteration
                # and if any results returned, save them in simulation data dict
                if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                    simulation_data = self.execute_before_iteration(epoch, simulation_data)
                else:
                    self.execute_before_iteration(epoch, None)

            #execute one iteration with ndlib
            self.G, self.node_count, self.status_delta = self.ndlib_model.iteration(node_status=True)

            if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                print("Epoch:", epoch)
                if visualizers is not None:
                    for visualizer in visualizers:
                        visualizer.draw(self, epoch)

                if digress is not None:
                    digress.save_graph(str(epoch), self.G, 'graph.json')
                    digress.save_statusdelta(epoch, self.node_count, 'count_node_types.json', self.ndlib_model.available_statuses)
                    digress.save_statusdelta(epoch, self.status_delta, 'status_delta.json', self.ndlib_model.available_statuses)
                    
            #save iteration data for parameters that user wants to track
            if epoch != 0:
                # execute after iteration methods, which utilizes the new states of the agents
                # if any results returned, save in simulation data dict
                if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                    simulation_data = self.execute_after_iteration(epoch, simulation_data)
                else:
                    self.execute_after_iteration(epoch, None)
                
            if self.early_stop:
                actual_epochs = epoch
                break

            # print(self.status_delta)

        if visualizers is not None:
            for visualizer in visualizers:
                visualizer.animate()

        if digress is not None and len(simulation_data) != 0:
            digress.save_iteration_data(simulation_data)
        
        self.execute_after_simulation(digress)
        return self.early_stop, actual_epochs
        
        #trends = self.ndlib_model.build_trends(iterations)
                
    def add_node_parameters(self, pd_conf):
        #Setting node attribute if given
        if("node-parameters" in pd_conf):
            #set node parameters depending on the type
            
            #setting numerical node parameters if given
            if("numerical" in pd_conf["node-parameters"]):
                print("TO-DO: is it possible to give user more options")
                params = pd_conf["node-parameters"]["numerical"]
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
            if("categorical" in pd_conf["node-parameters"]):
                params = pd_conf["node-parameters"]["categorical"]
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
                                if type(param_values) == str:
                                    print("Param values before read_options:", param_values)
                                    param_values = self.read_options_file(param_values)
                                    print("Param values after setting as a list:", param_values)
                            
                                attr = {n: {param_name: random.choice(param_values)} for n in self.G.nodes()}
                                nx.set_node_attributes(self.G, attr)
        
    def add_edge_parameters(self, pd_conf):
       #Setting edge attribute if given
        if("edge-parameters" in pd_conf):
            #set edge parameters depending on the type
            if("numerical" in pd_conf["edge-parameters"]):
                params = pd_conf["edge-parameters"]["numerical"]

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
                            
            
            if("categorical" in pd_conf["edge-parameters"]):
                params = pd_conf["edge-parameters"]["categorical"]
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
                                    

    def add_compartments(self, pd_conf):
        #create compartments dictionary
        compartments = {}
        for compartment_name, compartment_values in pd_conf["compartments"].items():
            
             #DEBUG: Print compartment details
            print("Processing compartment:", compartment_name, compartment_values)
            
            #for all type of compartments, except ConditionalComposition,
            #check if there is cascading composition
            if("composed" in compartment_values and compartment_values["composed"] != ''):
                composed = compartment_values["composed"]
            else:
                composed = None

            #NODE COMPARTMENTS
            #1. Node Stochastic
            if(compartment_values["type"] == "node-stochastic"):
                ratio = float(compartment_values["ratio"])
                #triggering status is not a mandatory field. So it may be empty.
                if("triggering_status" in compartment_values
                   and compartment_values["triggering_status"] != ''):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.NodeStochastic(ratio, triggering_status = triggering_status, composed = composed)
            #2. Node Categorical
            elif(compartment_values["type"] == "node-categorical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                if("probability" in compartment_values 
                   and compartment_values["probability"] != ''):
                    probability = float(compartment_values["probability"])
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                compartments[compartment_name] = cpm.NodeCategoricalAttribute(attribute, value, probability, composed = composed)
            #3. Node Numerical Attribute
            elif(compartment_values["type"] == "node-numerical-attribute"):
                attribute = compartment_values["attribute"] #attribute name
                value = int(compartment_values["value"]) #attribute testing value
                op = compartment_values["operator"] #logic operator
                #setting probability if valid
                if("probability" in compartment_values
                   and compartment_values["probability"] != ''):
                    probability = float(compartment_values["probability"])
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                #setting trigerring status if given
                if("triggering_status" in compartment_values
                   and compartment_values["triggering_status"] != ''):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.NodeNumericalAttribute(attribute, value, op, probability, triggering_status = triggering_status, composed = composed)     
            #4. Node Numerical Variable
                '''
                The difference between node numerical attribute and node numerical variable is that 
                you can compare the attribute's value with a variable
                    ex: node numerical attribute: if age > 18
                        node numerical variable: if age > friends where friends is a variable that holds an integer value
                ''' 
            elif(compartment_values["type"] == "node-numerical-variable"):
                var = compartment_values["variable"]
                #in ndlib variable type is mandatory but we can have a default in the future
                #e.g. if user doesn't type it we default to integer
                var_type = self.setValueType(compartment_values["variable-type"])
                #when operator is IN, "value" is expected to be a tuple of two elements identifying a closed interval
                value = compartment_values["value"]
                #value-type does not have to be specified. if not specified, ndlib takes it as number
                if("value-type" in compartment_values
                   and compartment_values["value-type"] != ''):
                    value_type = self.setValueType(compartment_values["value-type"])
                else:
                    value_type = None
                op = compartment_values["operator"]
                #setting probability if valid
                if("probability" in compartment_values
                   and compartment_values["probability"] != ''):
                    probability = float(compartment_values["probability"])
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                #setting trigerring status if given
                if("triggering_status" in compartment_values
                   and compartment_values["triggering_status"] != ''):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.NodeNumericalVariable(var, var_type, value, value_type, op, probability, triggering_status = triggering_status, composed = composed)
                
            #5. Node Treshold    
            elif(compartment_values["type"] == "node-treshold"):
                if("treshold" in compartment_values
                   and compartment_values["treshold"] != ''):
                    treshold = float(compartment_values["treshold"])
                    if(treshold < 0 or treshold > 1):
                        #it is not a valid treshold
                        print("Given treshold value is not valid. Setting it to 1.")
                        treshold = 1
                else:
                    treshold = None
                triggering_status = compartment_values["triggering_status"]
                compartments[compartment_name] = cpm.NodeThreshold(treshold, triggering_status = triggering_status, composed = composed)
            #NODE COMPARTMENTS COMPLETE

            #EDGE COMPARTMENTS
            #1. Edge Stochastic
            elif(compartment_values["type"] == "edge-stochastic"):
                treshold = float(compartment_values["treshold"])
                #triggering status is not a mandatory field. So it may be empty.
                if("triggering_status" in compartment_values
                   and compartment_values["triggering_status"] != ''):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeStochastic(treshold, triggering_status = triggering_status, composed = composed)
            #2. Edge Categorical
            elif(compartment_values["type"] == "edge-categorical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                if("probability" in compartment_values
                   and compartment_values["probability"] != ''):
                    probability = float(compartment_values["probability"])
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                if("triggering_status" in compartment_values
                   and compartment_values["triggering_status"] != ''):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeCategoricalAttribute(attribute, value, triggering_status = triggering_status, probability = probability, composed = composed) 
            #3. Edge Numerical
            elif(compartment_values["type"] == "edge-numerical"):
                attribute = compartment_values["attribute"]
                value = int(compartment_values["value"])
                op = compartment_values["operator"]
                if("probability" in compartment_values
                   and compartment_values["probability"] != ''):
                    probability = float(compartment_values["probability"])
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                if("triggering_status" in compartment_values
                   and compartment_values["triggering_status"] != ''):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeNumericalAttribute(attribute=attribute, value=value, op=op, triggering_status = triggering_status, probability = probability, composed = composed)
            #EDGE COMPARTMENTS COMPLETE
                
            #TIME COMPARTMENTS
            #1. Count Down
            elif(compartment_values["type"] == "count-down"):
                name = compartment_values["name"]
                iterations = int(compartment_values["iteration-count"])
                compartments[compartment_name] = cpm.CountDown(name, iterations, composed = composed) #does composing other types with countdown make sense?
            #TIME COMPARTMENTS COMPLETE
                
            #CONDITIONAL COMPOSITION COMPARTMENT
            elif(compartment_values["type"] == "conditional-composition"):
                condition = compartment_values["condition"]
                first_branch = compartment_values["first-branch"]
                second_branch = compartment_values["second-branch"]
                compartments[compartment_name] = cpm.ConditionalComposition(compartments[condition], compartments[first_branch], compartments[second_branch])

         #DEBUG: Print all compartments after processing
        # print("All compartments:", compartments)
        
        #all compartments added, return the dictionary        
        return compartments

    def setValueType(self, value):
        if(value == "attribute"):
            value = NumericalType.ATTRIBUTE
        elif(value == "status"):
            value = NumericalType.STATUS
        else:
            print("Invalid value type. Set to attribute by default.")
            value = NumericalType.ATTRIBUTE
        return value