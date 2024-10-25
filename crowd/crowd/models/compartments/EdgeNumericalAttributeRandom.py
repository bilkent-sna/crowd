"""
    This compartment is an extension of the Edge Numerical Compartment of NDLib. Original code by Giulio Rossetti. 
    In the original compartment, we compare the attribute value with a constant value. 
    In this compartment, we compare the attribute value with a random value, picked between the treshold given by the user. 
    An example use case for this compartment: 
    When using edge stochastic, we can't compare the generated value with an edge attribute. When implementing Independent 
        Cascade Model, we need the generated value to be larger than an edge attribute for a node to be activated. 
    If value is entered as "random [0,1]" we call this compartment instead of EdgeNumericalAttribute.
    Note: This doesn't allow IN operation.
"""


import random
from ndlib.models.compartments.Compartment import Compartiment
import networkx as nx
import numpy as np
import operator


class EdgeNumericalAttributeRandom(Compartiment):
    def __init__(
        self,
        attribute,
        range=None,
        op=None,
        triggering_status=None,
        probability=1,
        **kwargs
    ):
        super(self.__class__, self).__init__(kwargs)
        self.__available_operators = {
            "==": operator.__eq__,
            "<": operator.__lt__,
            ">": operator.__gt__,
            "<=": operator.__le__,
            ">=": operator.__ge__,
            "!=": operator.__ne__
        }

        self.attribute = attribute
        self.trigger = triggering_status
        self.attribute_range = range
        self.probability = probability
        self.operator = op

        if self.attribute_range is None:
            raise ValueError("A valid attribute range must be provided")

        if self.operator is not None and self.operator in self.__available_operators:
            if not isinstance(self.attribute_range[0], int) and not isinstance(self.attribute_range[1], int):
                if not isinstance(self.attribute_range[0], float) and not isinstance(self.attribute_range[1], float):
                    raise ValueError(
                        "Ranges should be provided as numeric values"
                    )
        else:
            raise ValueError("The operator provided '%s' is not valid" % operator)

    def execute(self, node, graph, status, status_map, *args, **kwargs):

        if isinstance(graph, nx.DiGraph):
            neighbors = list(graph.predecessors(node))
        else:
            neighbors = list(graph.neighbors(node))

        edge_attr = graph.get_edge_attributes(self.attribute)

        # triggered = []

        generated_number = random.uniform(self.attribute_range[0], self.attribute_range[1])

        if self.trigger is not None:
            for v in neighbors:
                if status[v] == status_map[self.trigger]:
                    if((node, v) in edge_attr):
                        val = edge_attr[(node, v)]
                    else:
                        val = edge_attr[(v, node)]
                    
                    if self.__available_operators[self.operator](
                        val, generated_number
                    ):
                        # triggered.append(v)
                        p = np.random.random_sample()

                        if p <= self.probability:
                            return self.compose(node, graph, status, status_map, kwargs)
        else:
            for v in neighbors:
                if((node, v) in edge_attr):
                    val = edge_attr[(node, v)]
                else:
                    val = edge_attr[(v, node)]
                
                if self.__available_operators[self.operator](
                    val, generated_number
                ):
                    # triggered.append(v)
                    p = np.random.random_sample()

                    if p <= self.probability:
                        return self.compose(node, graph, status, status_map, kwargs)
        

        # for _ in triggered:
        #     p = np.random.random_sample()

        #     test = p <= self.probability

        #     if test:
        #         return self.compose(node, graph, status, status_map, kwargs)

        return False