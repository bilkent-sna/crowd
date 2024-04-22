import random
from crowd import node as n
from crowd import network as netw
import ndlib.models.ModelConfig as mc
from crowd.models import BaseDiffusion as bd
import ndlib.models.compartments as cpm
import networkx as nx
from ndlib.models.compartments.enums.NumericalType import NumericalType

class DiffusionNetwork(netw.Network):

    def __init__(self, conf_dict):
        super().__init__(conf_dict)

        #everything about configuration is stored at self.conf

        #get model status from conf to an array
        pd_conf = self.conf["definitions"]["pd-model"]
        node_types = pd_conf["nodetypes"] #this is a dictionary

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
        self.watch_methods = None

    def run(self, epochs, visualizers=None, snapshot_period=100, agility=1, digress=None):  
        # Simulation execution
        self.ndlib_model.set_initial_status(self.ndlib_config)

        # Iteration data dictionary
        simulation_data = {}

        for epoch in range(0, epochs): #for each epoch
            #execute one iteration with ndlib
            self.G, self.status_delta = self.ndlib_model.iteration(node_status=True)

            if (epoch % snapshot_period) == 0 or (epoch == epochs-1):
                print("Epoch:", epoch)
                if visualizers is not None:
                    for visualizer in visualizers:
                        visualizer.draw(self, epoch)

                if digress is not None:
                    digress.save_graph(str(epoch), self.G, 'graph.json')
                    digress.save_statusdelta(str(epoch), self.status_delta, 'statusdelta.json')
                    

                #save iteration data for parameters that user wants to track
                #in this case, we say that user can't pass any parameters to these functions
                for method in self.watch_methods:
                    #if method in self.predefined_models:
                    #call each method
                    #next line of code is assumed to be running the following way:
                    #simulation_data["percent_infected"][0] = percent_infected()
                    #print(method.__name__, type(method))
                    key_to_save = method.__name__ + " iteration " + str(epoch)
                    simulation_data[key_to_save] = method(self)
                
                
                    
            print(self.status_delta)

        if visualizers is not None:
            for visualizer in visualizers:
                visualizer.animate()

        if digress is not None and self.watch_methods is not None:
            digress.save_iteration_data(simulation_data, 'parameters.json')
            
        #trends = self.ndlib_model.build_trends(iterations)
                
    def add_node_parameters(self, pd_conf):
        #Setting node attribute if given
        if("node-parameters" in pd_conf):
            #set node parameters depending on the type
            
            #setting numerical node parameters if given
            if("numerical" in pd_conf["node-parameters"]):
                print("TO-DO: NOT COMPLETE")
                params = pd_conf["node-parameters"]["numerical"]
                for param_name, param_values in params.items():
                    #setting the numerical attribute randomly between 2 numbers
                    #we expect user to enter these 2 numbers in a list format
                    attr = {n: {param_name: random.choice(range(param_values[0], param_values[1]))} for n in self.G.nodes()}
                    nx.set_node_attributes(self.G, attr)

            #setting categorical node parameters if given
            if("categorical" in pd_conf["node-parameters"]):
                params = pd_conf["node-parameters"]["categorical"]
                for param_name, param_values in params.items():
                    #setting the categorical attribute randomly
                    #ndlib does not provide a method for this so we can add
                    #to conf file if user has any requirements
                    attr = {n: {param_name: random.choice(param_values)} for n in self.G.nodes()}
                    nx.set_node_attributes(self.G, attr)

    def add_edge_parameters(self, pd_conf):
       #Setting edge attribute if given
        if("edge-parameters" in pd_conf):
            #set edge parameters depending on the type
            if("numerical" in pd_conf["edge-parameters"]):
                params = pd_conf["edge-parameters"]["numerical"]
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
            
            if("categorical" in pd_conf["edge-parameters"]):
                params = pd_conf["edge-parameters"]["categorical"]
                for param_name, param_value in params.items():
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
            #for all type of compartments, except ConditionalComposition,
            #check if there is cascading composition
            if("composed" in compartment_values):
                composed = compartment_values["composed"]
            else:
                composed = None

            #NODE COMPARTMENTS
            #1. Node Stochastic
            if(compartment_values["type"] == "node-stochastic"):
                ratio = compartment_values["ratio"]
                #triggering status is not a mandatory field. So it may be empty.
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.NodeStochastic(ratio, triggering_status = triggering_status, composed = composed)
            #2. Node Categorical
            elif(compartment_values["type"] == "node-categorical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                compartments[compartment_name] = cpm.NodeCategoricalAttribute(attribute, value, probability, composed = composed)
            #3. Node Numerical Attribute
            elif(compartment_values["type"] == "node-numerical-attribute"):
                attribute = compartment_values["attribute"] #attribute name
                value = compartment_values["value"] #attribute testing value
                op = compartment_values["operator"] #logic operator
                #setting probability if valid
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                #setting trigerring status if given
                if("triggering_status" in compartment_values):
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
                if("value-type" in compartment_values):
                    value_type = self.setValueType(compartment_values["value-type"])
                else:
                    value_type = None
                op = compartment_values["operator"]
                #setting probability if valid
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                #setting trigerring status if given
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.NodeNumericalVariable(var, var_type, value, value_type, op, probability, triggering_status = triggering_status, composed = composed)
                
            #5. Node Treshold    
            elif(compartment_values["type"] == "node-treshold"):
                if("treshold" in compartment_values):
                    treshold = compartment_values["treshold"]
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
                treshold = compartment_values["treshold"]
                #triggering status is not a mandatory field. So it may be empty.
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeStochastic(treshold, triggering_status = triggering_status, composed = composed)
            #2. Edge Categorical
            elif(compartment_values["type"] == "edge-categorical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeCategoricalAttribute(attribute, value, triggering_status = triggering_status, probability = probability, composed = composed) 
            #3. Edge Numerical
            elif(compartment_values["type"] == "edge-numerical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                op = compartment_values["operator"]
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                    if(probability < 0 and probability > 1): #invalid probability
                        print("Invalid probability given: setting to 1")
                        probability = 1
                else:
                    probability = 1
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeNumericalAttribute(attribute=attribute, value=value, op=op, triggering_status = triggering_status, probability = probability, composed = composed)
            #EDGE COMPARTMENTS COMPLETE
                
            #TIME COMPARTMENTS
            #1. Count Down
            elif(compartment_values["type"] == "count-down"):
                name = compartment_values["name"]
                iterations = compartment_values["iteration-count"]
                compartments[compartment_name] = cpm.CountDown(name, iterations, composed = composed) #does composing other types with countdown make sense?
            #TIME COMPARTMENTS COMPLETE
                
            #CONDITIONAL COMPOSITION COMPARTMENT
            elif(compartment_values["type"] == "conditional-composition"):
                condition = compartment_values["condition"]
                first_branch = compartment_values["first-branch"]
                second_branch = compartment_values["second-branch"]
                compartments[compartment_name] = cpm.ConditionalComposition(compartments[condition], compartments[first_branch], compartments[second_branch])

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