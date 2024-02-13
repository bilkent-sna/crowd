import random
from crowd import node as n
from crowd import network as netw
import ndlib
import ndlib.models.ModelConfig as mc
import ndlib.models.CompositeModel as gc
import ndlib.models.compartments as cpm

class DiffusionNetwork(netw.Network):

    def __init__(self, network_file):
        super().__init__(network_file)

        #ndlib model
        self.ndlib_model = gc.CompositeModel(self.G)

        #everything about configuration is stored at self.conf

        #get model status from conf to an array
        fields = self.conf["definitions"]["pd-model"]["diffusion"]["fields"]
        node_types = fields["nodetypes"]

        #for each item in array
        for item in node_types:
            self.ndlib_model.add_status(item)

        print("Available Status For Custom Diffusion")
        print(self.ndlib_model.available_statuses)
        #create compartments dictionary
        compartments = {}
        for compartment_name, compartment_values in fields["compartments"].items():
            if(compartment_values["type"] == "node-stochastic"):
                ratio = compartment_values["ratio"]
                #triggering status is not a mandatory field. So it may be empty.
                if("triggering_status" in compartment_values):
                    triggering_status = compartment_values["triggering_status"]
                else:
                    triggering_status = None
                compartments[compartment_name] = cpm.NodeStochastic(ratio, triggering_status)
            elif(compartment_values["type"] == "node-categorical"):
                attribute = compartment_values["attribute"]
                value = compartment_values["value"]
                probability = compartment_values["probability"]
                
        #create rules and add them to model
        for rule in fields["rules"].values():
            self.ndlib_model.add_rule(rule[0], rule[1], compartments[rule[2]])          

        #model initial status configuration
        self.ndlib_config = mc.Configuration()

        #get it from conf / change this
        self.ndlib_config.add_model_parameter('fraction_infected', self.conf["info"]["fraction_infected"])


    def run(self, epochs, visualizers=None, snapshot_period=100, agility=1, digress=None):  
        # Simulation execution
        self.ndlib_model.set_initial_status(self.ndlib_config)
        iterations = self.ndlib_model.iteration_bunch(epochs)
        trends = self.ndlib_model.build_trends(iterations)
        return trends