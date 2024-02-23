import ndlib.models.CompositeModel as gc
import warnings
import future.utils
import numpy as np
from netdispatch import AGraph

class ConfigurationException(Exception):
    """Configuration Exception"""

class BaseDiffusion(gc.CompositeModel):

    def __init__(self, graph, seed=None):
        #from diffusion model
        np.random.seed(seed)
        self.discrete_state = True
        self.params = {"nodes": {}, "edges": {}, "model": {}, "status": {}}
        self.name = ""
        self.parameters = {"model": {}, "nodes": {}, "edges": {}}

        self.actual_iteration = 0
        self.graph = AGraph(graph)
        print(self.graph.nodes[0])
        self.status = {}
        for i in range(len(self.graph.nodes)):
            node_state = self.graph.nodes[i]['node'] #{node: Active}
            if(node_state == "Inactive"):
                self.status[i] = 0
            else:
                self.status[i] = 1
        #self.initial_status = {}
        self.initial_status = self.status

        #from composite model
        self.available_statuses = {}
        self.compartment = {}
        self.compartment_progressive = 0
        self.status_progressive = 0
    
    #override the configuration check function from Composite Model/Diffusion Model
    def __validate_configuration(self, configuration):
        """
        Validate the consistency of a Configuration object for the specific model

        :param configuration: a Configuration object instance
        """
        mdp = set(configuration.get_model_parameters().keys())

        # Checking initial simulation status
        if (
            self.discrete_state
            and len(mdp) == 0
        ):
            warnings.warn(
                "Initial configuration missing: a random sample of 5% of graph nodes will be set as active"
            )
            self.params["model"]["fraction_active"] = 0.05

    def set_initial_status(self, configuration):
        """
        Set the initial model configuration

        :param configuration: a ```ndlib.models.ModelConfig.Configuration``` object
        """

        self.__validate_configuration(configuration)

        nodes_cfg = configuration.get_nodes_configuration()
        # Set additional node information

        for param, node_to_value in future.utils.iteritems(nodes_cfg):
            if len(node_to_value) < len(self.graph.nodes):
                raise ConfigurationException(
                    {"message": "Not all nodes have a configuration specified"}
                )

            self.params["nodes"][param] = node_to_value

        edges_cfg = configuration.get_edges_configuration()
        # Set additional edges information
        for param, edge_to_values in future.utils.iteritems(edges_cfg):
            if len(edge_to_values) == len(self.graph.edges):
                self.params["edges"][param] = {}
                for e in edge_to_values:
                    self.params["edges"][param][e] = edge_to_values[e]

        # Set initial status
        model_status = configuration.get_model_configuration()

        for param, nodes in future.utils.iteritems(model_status):
            self.params["status"][param] = nodes
            for node in nodes:
                self.status[node] = self.available_statuses[param]

        # Set model additional information
        model_params = configuration.get_model_parameters()
        for param, val in future.utils.iteritems(model_params):
            self.params["model"][param] = val

        self.initial_status = self.status