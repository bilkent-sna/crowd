import json
from . import egress as e
import networkx as nx
import os

class file_egress(e.egress):
    
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
        new_dict = {}
        if epoch_num is not None:
            new_dict = {"Iteration": epoch_num}

        if available_status:
            index = 0
            for status in available_status:
                new_dict[status] = data_dict[index]
                index += 1
        else:
            new_dict.update(data_dict)

        # if(epoch_num != 0):
        #     to_write = (",") + json.dumps(new_dict)
        # else:
        #     to_write = json.dumps(new_dict)
        # #self.save(to_write, file_name)
        path = os.path.join(self.artifact_path, 'parameters', file_name)
        # f = open(path, "a")
        # f.write(to_write)
        # # f.write(str(to_write))
        # f.close()
        # Step 1: Remove the trailing ']' from the file (if it exists)
        if os.path.exists(path):
            with open(path, 'r+') as f:
                f.seek(0, os.SEEK_END)  # Move to the end of the file
                f.seek(f.tell() - 1, os.SEEK_SET)  # Move one character back
                last_char = f.read(1)
                
                if last_char == ']':  # Check if the last character is ']'
                    f.seek(f.tell() - 1, os.SEEK_SET)  # Move back one character
                    f.truncate()  # Remove the closing bracket

                # Step 2: Write the new data
                with open(path, 'a') as f:
                    to_write = (",") + json.dumps(new_dict)
                    f.write(to_write)

            # Step 3: Add the closing bracket back
            with open(path, 'a') as f:
                f.write("]")  # Ensure the file always ends with ]
        else:
            with open(path, 'a') as f:
                to_write = json.dumps(new_dict)
                f.write("[\n" + to_write)

    def save_graph(self, epoch_num, current_graph, file_name):
        path = os.path.join(self.artifact_path, file_name)
        data = nx.node_link_data(current_graph, edges="links")

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
        #if file name given, save it as that. if not, network.gexf
        if file_name == None:
            file_name = "network.gexf"
        if not file_name.endswith(".gexf"):
            file_name += ".gexf"

        path = os.path.join(self.artifact_path, file_name)
        nx.write_gexf(graph, path)
    
    def save_as_edgelist(self, graph, file_name = None):
        #if file name given, save it as that, if not, network.edgelist
        if file_name == None:
            file_name = "network.edgelist"
        if not file_name.endswith(".edgelist"):
            file_name += ".edgelist"

        path = os.path.join(self.artifact_path, file_name)
        nx.write_edgelist(graph, path)

    def save_as_gml(self, graph, file_name = None):
        #if file name given, save it as that, if not, network.gml
        if file_name == None:
            file_name = "network.gml"
        if not file_name.endswith(".gml"):
            file_name += ".gml"

        path = os.path.join(self.artifact_path, file_name)
        nx.write_gml(graph, path)

    def save_as_graphml(self, graph, file_name = None):
        #if file name given, save it as that, if not, network.graphml
        if file_name == None:
            file_name = "network.graphml"
        if not file_name.endswith(".graphml"):
            file_name += ".graphml"

        path = os.path.join(self.artifact_path, file_name)
        nx.write_graphml(graph, path)

    def save_as_adjacency_list(self, graph, file_name = None):
        #if file name given, save it as that, if not, network.adjlist
        if file_name == None:
            file_name = "network.adjlist"
        if not file_name.endswith(".adjlist"):
            file_name += ".adjlist"

        path = os.path.join(self.artifact_path, file_name)
        nx.write_adjlist(graph, path)
    
    def save_as_json(self, graph, file_name = None):
        #if file name given, save it as that, if not, network.json
        if file_name == None:
            file_name = "network.json"
        if not file_name.endswith(".json"):
            file_name += ".json"

        path = os.path.join(self.artifact_path, file_name)
        data = nx.node_link_data(graph, edges="links")
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)

    def save_network_after_simulation(self, iteration_num, save_format):
        # loads graph.json which holds all iteration data
        path = os.path.join(self.artifact_path, "graph.json")
        graph_dict = json.load(path)

        #if we have "all" as the iteration number, then go one by one save them all
        if iteration_num == "all":
            for iter_data in graph_dict.values():
                nx_graph = nx.node_link_graph(iter_data)
                file_name = "network." + save_format
                self.save_graph_with_format(nx_graph, save_format, file_name)
        
        # else, just save the given iteration
        else:
            nx_graph = nx.node_link_graph(graph_dict[iteration_num])
            file_name = iteration_num + "." + save_format
            self.save_graph_with_format(nx_graph, save_format, file_name)
    
    def save_graph_with_format(self, graph, save_format, file_name):
        match save_format:
            case "gexf":
                self.save_as_gexf(graph, file_name)
            case "edgelist":
                self.save_as_edgelist(graph, file_name)
            case "gml":
                self.save_as_gml(graph, file_name)
            case "graphml":
                self.save_as_graphml(graph, file_name)
            case "adjacency_list":
                self.save_as_adjacency_list(graph, file_name)
            case "json":
                self.save_as_json(graph, file_name)