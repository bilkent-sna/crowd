import ndlib.models.CompositeModel as gc
import warnings
import future.utils
import numpy as np
from netdispatch import AGraph

class ConfigurationException(Exception):
    """Configuration Exception"""

class BaseDiffusion(gc.CompositeModel):

    def __init__(self, graph, conf, seed=None):
        #from diffusion model
        np.random.seed(seed)
        self.discrete_state = True
        self.params = {"nodes": {}, "edges": {}, "model": {}, "status": {}}
        self.name = ""
        self.parameters = {"model": {}, "nodes": {}, "edges": {}}

        self.actual_iteration = 0
        self.graph = AGraph(graph)

        self.status = {}

        self.conf = conf
        self.possible_node_states = list(conf['definitions']['pd-model']['nodetypes'].keys()) #get nodetypes dict
        for node in self.graph.nodes:
            node_state = self.graph.nodes[node]['node']
            self.status[node] = self.possible_node_states.index(node_state)
            """
            #print("node", node)
            #print("node-type", type(node))
            node_state = self.graph.nodes[node]['node']
            if(node_state == "Inactive" or node_state == "Susceptible"):
                self.status[node] = 0
            elif(node_state == "Active" or node_state == "Infected"):
                self.status[node] = 1
            else:
                self.status[node] = 2
            #print("Done current") """
        """
        for i in range(len(self.graph.nodes)):
            node_state = self.graph.nodes[i]['node'] #{node: Active}
            if(node_state == "Inactive"):
                self.status[i] = 0
            else:
                self.status[i] = 1
        """
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

        #self.__validate_configuration(configuration)

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


    def iteration(self, node_status=True):
        """
        Execute a single model iteration

        Originally :return: Iteration_id, Incremental node status (dictionary node->status)
        Currently :return: Graph, node_count
        """
        self.clean_initial_status(list(self.available_statuses.values()))
        actual_status = {node: nstatus for node, nstatus in future.utils.iteritems(self.status)}

        if self.actual_iteration == 0:
            self.actual_iteration += 1
            delta, node_count, status_delta = self.status_delta(actual_status)
            if node_status:
                '''
                return {"iteration": 0, "status": actual_status.copy(),
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}
                '''
                return self.graph.graph, node_count.copy(), status_delta.copy()
            else:
                return {"iteration": 0, "status": {},
                        "node_count": node_count.copy(), "status_delta": status_delta.copy()}

        for u in self.graph.nodes:
            u_status = self.status[u]
            for i in range(0, self.compartment_progressive):

                if u_status == self.available_statuses[self.compartment[i][0]]:
                    rule = self.compartment[i][2]
                    test = rule.execute(node=u, graph=self.graph, status=self.status,
                                        status_map=self.available_statuses, params=self.params)
                    if test:
                        actual_status[u] = self.available_statuses[self.compartment[i][1]]
                        self.graph.nodes[u]['node'] = self.possible_node_states[actual_status[u]]
                        '''
                        if(actual_status[u] == 0):
                            self.graph.nodes[u]['node'] = 'Susceptible'
                        elif(actual_status[u] == 1):
                            self.graph.nodes[u]['node'] = 'Infected'
                        else:
                            self.graph.nodes[u]['node'] = 'Removed'
                        break
                        '''

        delta, node_count, status_delta = self.status_delta(actual_status)
        self.status = actual_status
        self.actual_iteration += 1

        # print("delta:", delta)
        # print("node count:", node_count)
        # print("status_delta: ", status_delta)
        if node_status:
            '''return {"iteration": self.actual_iteration - 1, "status": delta.copy(),
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}'''
            return self.graph.graph, node_count.copy(), status_delta.copy()
        else:
            return {"iteration": self.actual_iteration - 1, "status": {},
                    "node_count": node_count.copy(), "status_delta": status_delta.copy()}
    