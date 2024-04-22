import json
from . import digress as d
import networkx as nx
import os

class file_digress(d.digress):
    
    def save(self, input, file_name, append=True):
        # save
        path = os.path.join(self.artifact_path, file_name)
        f = open(path, "a")
        f.write(str(input)+"\n")
        f.close()
    
    def save_iteration_data(self, data_dict, file_name):
        to_write = json.dumps(data_dict)
        self.save(to_write, file_name)

    def save_statusdelta(self, epoch_num, data_dict, file_name):
        if(epoch_num != "0"):
            to_write = (",\n\"" + epoch_num + "\": ") + json.dumps(data_dict)
        else:
            to_write = ("\"" + epoch_num + "\": ") + json.dumps(data_dict)
        #self.save(to_write, file_name)
        path = os.path.join(self.artifact_path, file_name)
        f = open(path, "a")
        f.write(str(to_write))
        f.close()


    def save_graph(self, epoch_num, current_graph, file_name):
        data = nx.node_link_data(current_graph)
        data = json.dumps(data)

        # Remove single quotes from the beginning and end of the data string
        data = data[1:-1]
        #print("data: ", data)
        #print(("\"" + epoch_num + "\""))
        data = data.replace(',', ',\n')
        to_write = ("\"" + epoch_num + "\": ") + "{\n" + data + "},"

        '''
        save the graph to file in the format: 
        {
            "1" : { 
                "nodes": [
                    {"id": "Myriel", "group": 1},
                    ...}
                ],
                "links": [
                    {"source": "Napoleon", "target": "Myriel", "value": 1},
                    ...}
                ]
            } 
        '''
        self.save(to_write, file_name)
    
    def save_as_gexf(self, graph, file_name = None):
        #if file name given, save it as that. if not, either time or project.gexf
        print("TO-DO")