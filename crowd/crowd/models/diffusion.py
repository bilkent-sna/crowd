import random
from crowd import node as n
from crowd import network as netw
import ndlib.models.ModelConfig as mc
from crowd.models import BaseDiffusion as bd
import ndlib.models.compartments as cpm
import networkx as nx

class DiffusionNetwork(netw.Network):

    def __init__(self, network_file):
        super().__init__(network_file)

        #everything about configuration is stored at self.conf

        #get model status from conf to an array
        pd_conf = self.conf["definitions"]["pd-model"]
        node_types = pd_conf["nodetypes"]

        #Setting node attribute if given
        if("node-parameters" in pd_conf):
            #set node parameters depending on the type
            
            #setting numerical node parameters if given
            if("numerical" in pd_conf["node-parameters"]):
                #set 
                print("TO-DO")

            #setting categorical node parameters if given
            if("categorical" in pd_conf["node-parameters"]):
                params = pd_conf["node-parameters"]["categorical"]
                for param_name, param_values in params.items():
                    #setting the categorical attribute randomly
                    #ndlib does not provide a method for this so we can add
                    #to conf file if user has any requirements
                    attr = {n: {param_name: random.choice(param_values)} for n in self.G.nodes()}
                    nx.set_node_attributes(self.G, attr)

        #Setting edge attribute if given
        if("edge-parameters" in pd_conf):
            #set edge parameters depending on the type
            print("TODO")

        
        #ndlib model
        self.ndlib_model = bd.BaseDiffusion(self.G)
        
        #for each item in array
        for item in node_types:
            self.ndlib_model.add_status(item)

        print("Available Status For Custom Diffusion")
        print(self.ndlib_model.available_statuses)

        
        #create compartments dictionary
        compartments = {}
        for compartment_name, compartment_values in pd_conf["compartments"].items():
            #NODE COMPARTMENTS
            #1. Node Stochastic
            if(compartment_values["type"] == "node-stochastic"):
                ratio = compartment_values["ratio"]
                #triggering status is not a mandatory field. So it may be empty.
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.NodeStochastic(ratio, triggering_status)
            #2. Node Categorical
            elif(compartment_values["type"] == "node-categorical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                else:
                    probability = 1
                compartments[compartment_name] = cpm.NodeCategoricalAttribute(attribute, value, probability)
            #EDGE COMPARTMENTS
            #1. Edge Stochastic
            elif(compartment_values["type"] == "edge-stochastic"):
                treshold = compartment_values["treshold"]
                #triggering status is not a mandatory field. So it may be empty.
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeStochastic(treshold, triggering_status)
            #2. Edge Categorical
            elif(compartment_values["type"] == "edge-categorical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                else:
                    probability = 1
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeCategoricalAttribute(attribute, value, probability, triggering_status) 
            #3. Edge Numerical
            elif(compartment_values["type"] == "edge-numerical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                op = compartment_values["operator"]
                if("probability" in compartment_values):
                    probability = compartment_values["probability"]
                else:
                    probability = 1
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.EdgeNumericalAttribute(value, op, triggering_status, probability)

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


    def run(self, epochs, visualizers=None, snapshot_period=100, agility=1, digress=None):  
        # Simulation execution
        self.ndlib_model.set_initial_status(self.ndlib_config)
        iterations = self.ndlib_model.iteration_bunch(epochs)
        trends = self.ndlib_model.build_trends(iterations)
        return trends