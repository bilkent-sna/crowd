import networkx as nx
import importlib
import random
from crowd.preprocessing import preprocessor as p
from crowd.preprocessing import communitydetection as com

class Structure:

    def __init__(self, structure):
        self.structure = structure

    def create(self):
        Exception("Create not implemented in Structure")
