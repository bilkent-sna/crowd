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
    
    def save_iteration_data(self, simulation_data):
        for key, value in simulation_data.items():
            file_name = f"{key.split()[0]}.json"  # Use the method name as the file name
            to_write = json.dumps(value, indent=2)
            self.save(to_write, os.path.join('parameters', file_name))
      

    def save_statusdelta(self, epoch_num, data_dict, file_name, available_status):
        new_dict = {"Iteration": epoch_num}
        index = 0
        for status in available_status:
            new_dict[status] = data_dict[index]
            index += 1

        if(epoch_num != 0):
            to_write = (",") + json.dumps(new_dict)
        else:
            to_write = json.dumps(new_dict)
        #self.save(to_write, file_name)
        path = os.path.join(self.artifact_path, 'parameters', file_name)
        f = open(path, "a")
        f.write(to_write)
        # f.write(str(to_write))
        f.close()


    def save_graph(self, epoch_num, current_graph, file_name):
        path = os.path.join(self.artifact_path, file_name)
        data = nx.node_link_data(current_graph)

        # Load existing data if the file already exists
        try:
            with open(path, 'r') as f:
                existing_data = json.load(f)
                # print(existing_data)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        # Add new data to the existing data
        existing_data[epoch_num] = data

        # Write back to file
        with open(path, 'w') as f:
            json.dump(existing_data, f, indent=4)

    def save_as_gexf(self, graph, file_name = None):
        #if file name given, save it as that. if not, either time or project.gexf
        print("TO-DO")