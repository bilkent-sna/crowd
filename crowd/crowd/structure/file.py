import csv
import pandas as pd
import networkx as nx
import importlib
import random
import math
import os
from .structure import Structure


class File(Structure):
    def __init__(self, structure, conf, project_dir):
        super().__init__(structure, project_dir)
        # super().__init__(structure)
        self.conf = conf
        #print("CONF FROM FILE", conf, "\n\n\n\n\n\n")

    def create(self):
        # print("Creating file structure")

        _, file_extension = os.path.splitext(self.structure['path'])

        # Create nodes only network
        if self.structure["type"] == "nodes_only":
            try:
                # Read the network file
                header = 0 if self.structure["header"] else 1
                df = pd.read_csv(self.structure['path'], sep='\t', header=header)
                print(df)
                
                # Create the network with no nodes and edges
                self.G=nx.Graph()
                for row_dict in df.to_dict(orient="records"):
                    #print(row._asdict())
                    print(row_dict)
                    #row_dict = row._asdict()
                    self.G.add_node(row_dict['Id'])
                    nx.set_node_attributes(self.G, {row_dict['Id']:row_dict})
            except:
                raise("Specified network file "+self.structure["path"] +" does not exist")

        elif self.structure["type"] == "nodes_edges":
            try:
                # Read the network file
                header = 0 if self.structure["header"] else 1

                if file_extension == ".csv":
                    #df = pd.read_csv(self.structure['path'], sep='\t', header=header)
                    df = pd.read_csv(self.structure['path'], sep=',', header=header)
                    # print("The dataframe:", df.head())

                    #self.G = nx.read_edgelist(self.structure['path'], create_using = nx.Graph(), nodetype=int) 
                    if(header == 0):
                        headers = df.columns.tolist()
                        print("Headers of dataframe: ", headers)
                        self.G = nx.from_pandas_edgelist(df, source = headers[0], target = headers[1], create_using = nx.Graph()) 
                        # print(self.G)
                
                elif file_extension == ".edgelist":
                    self.G = nx.read_edgelist(self.structure['path'], create_using = nx.Graph(), nodetype=int)
                    # print("Printing an edgelist file info check: ", self.G)
                    
                #count = self.conf["info"]["total_count"]
                count = self.G.number_of_nodes()

                # if source or diffusion model not defined, don't do these steps
                if "source" in self.conf["definitions"] or "pd-model" in self.conf["definitions"] or self.conf["definitions"]["name"] == 'custom':
                    self.G = self.set_nodetypes(self.G, self.conf, count)

            except:
                raise("Specified network file " + self.structure["path"] +" does not exist")
            
        #print("-- GRAPH DETAILS---->", nx.info(self.G)) => Networkx 3.0 removed info method
        # print('Number of nodes', len(self.G.nodes))
        # print('Number of edges', len(self.G.edges))
        # degrees = [val for (node, val) in self.G.degree()]
        # print(sum(degrees)/float(len(self.G.nodes)))
        # print(self.G.nodes())
        return self.G
