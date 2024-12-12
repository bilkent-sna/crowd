import os
import json
from crowd.models.EdgeSimNetwork import EdgeSimNetwork
from crowd.project_management.project import Project


class ProjectFunctions:
    def create_project(self, name: str, date: str, info: str, nodeOrEdge: str):
        """
        Creates a new project.

        :param name: The name of the project.
        :param date: The date when the project is first created (DD/MM/YYYY) format
        :param info: A short explanation of the project.
        """
        
        # Initialize the project object
        new_project = Project()

        # Create a new project with the given parameters
        # A directory will be created for this object with the most basic files
        try:
            new_project.create_project(name, date, info, nodeOrEdge)
        except Exception as e:
            print(f"An error occurred: {e.with_traceback}")

        print(f"Creating project: {name} with info: {info}")

    
    def get_conf_and_run(self, data, project_name, epochs, snapshot_period, num_simulations):
        try:
            data_dict = json.loads(data)
            print(f"Received data successfully")
           
            # Initialize the project object
            new_project = Project()

            print("Before loading project")
            new_project.load_project(project_name)
            print("After loading project")
            
            conf = self.parseConf(data_dict, new_project.project_dir)

            print("Before updating conf")
            new_project.update_conf(conf)
            print("After updating conf")

            new_project.run_multiple_simulations(num_simulations, epochs, snapshot_period)

            simulation_directory = max(os.listdir(new_project.results_dir))
            print("Simulation directory:", simulation_directory)                                                                                                      
      
            return json.dumps(simulation_directory)
        
            # Process the data as needed
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except TypeError as e:
            print(f"Type error: {e}")
        except KeyError as e:
            print(f"Key error: {e}")
    
    def edge_conf_run(self, data, project_name, epochs, snapshot_period):
        try:
            data_dict = json.loads(data)
            print(f"Received data successfully")
           
            # Initialize the project object
            new_project = Project()

            print("Before loading project")
            new_project.load_project(project_name)
            print("After loading project")
            
            conf = self.parse_custom_sim_conf(data_dict, new_project.project_dir)

            print("Before updating conf")
            new_project.update_conf(conf)
            print("After updating conf")

            if type(new_project.netw) != EdgeSimNetwork:
                new_project.change_network_type(False)

            new_project.run_edge_simulation(epochs, snapshot_period)
            
            simulation_directory = max(os.listdir(new_project.results_dir))
            print("Simulation directory:", simulation_directory)                                                                                                      
      
            return json.dumps(simulation_directory)
        
            # Process the data as needed
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        except TypeError as e:
            print(f"Type error: {e}")
        except KeyError as e:
            print(f"Key error: {e}")

    def init_and_run_simulation(self, project_name, epochs, snapshot_period, num_simulations):
        try:
            # Initialize the project object
            new_project = Project()

            print("Before loading project")
            new_project.load_project(project_name)
            print("After loading project")

            new_project.run_multiple_simulations(num_simulations, epochs, snapshot_period)

            simulation_directory = max(os.listdir(new_project.results_dir))
            print("Simulation directory:", simulation_directory)                                                                                                      
      
            return json.dumps(simulation_directory) #will this return the parent directory or the last one

        except TypeError as e:
            print(f"Type error: {e}")
        except KeyError as e:
            print(f"Key error: {e}")

    def edge_sim_run(self, project_name, epochs, snapshot_period):
        try:
            # Initialize the project object
            new_project = Project()

            print("Before loading project")
            new_project.load_project(project_name)
            print("After loading project")

            if type(new_project.netw) != EdgeSimNetwork:
                new_project.change_network_type(False)

            new_project.run_edge_simulation(epochs, snapshot_period)

            simulation_directory = max(os.listdir(new_project.results_dir))
            print("Simulation directory:", simulation_directory)                                                                                                      
      
            return json.dumps(simulation_directory)

        except TypeError as e:
            print(f"Type error: {e}")
        except KeyError as e:
            print(f"Key error: {e}")

    def parse_custom_sim_conf(self, data_dict, project_dir):
        conf = {
                "name": data_dict["name"]
            }
    
        #data source/structure part
        if "file" in data_dict["dataSource"]["structure"]["fileOrRandom"]:
            item_to_add = {
                "structure": {
                    "file": data_dict["dataSource"]["structure"]["fileOrRandom"]["file"]
                }
            }

            curr_path = item_to_add["structure"]["file"]["path"]
            item_to_add["structure"]["file"]["path"] = os.path.join(project_dir, 'datasets', curr_path)
        
        else:
            generate_type = data_dict["dataSource"]["structure"]["fileOrRandom"]["generateType"]
            print("Generate type:", generate_type)
            item_to_add = {
                "structure": {
                    generate_type: {
                        "degree": data_dict["dataSource"]["structure"]["fileOrRandom"]["degree"],
                        "count": data_dict["dataSource"]["structure"]["fileOrRandom"]["count"]
                    }
                }
            }

         # Directly set the structure key at the top level
        conf["structure"] = item_to_add["structure"]

        print('CONF --->', conf)

        return conf


    def parseConf(self, data_dict, project_dir):

        conf = {
                "name": data_dict["name"]
            }
        
        definitions = {
            "definitions": {
                    "pd-model": {
                        "name": "diffusion"
                    }
                }
        }
    
        #nodetype 
        nodetypes_dict = data_dict["nodeTypes"]
        temp = {}

        for type in nodetypes_dict:
            key_name = type["name"]
            init_type = type["init"]
            init_dict = {}
            if init_type == 'random-with-count':
                init_dict = {
                    "count": type[init_type]["count"]
                }
            elif init_type == 'random-with-weight':
                init_dict = {
                    "initial-weight": type[init_type]["weight"]
                }
            elif init_type == 'choose-with-metric':
                init_dict = {
                    "metric": type[init_type]["metric"],
                    "count": type[init_type]["count"]
                }
            elif init_type == 'from-file':
                init_dict = {
                    "path": type[init_type]["path"]
                }

            #type's format: {name: .., weight: ...}
            temp.update( {
                key_name: {
                    init_type: init_dict
                }
            } )
        
        item_to_add = {
            "nodetypes" : temp
        }

        definitions["definitions"]["pd-model"].update(item_to_add)


        #node parameters 
        if "nodeParameters" in data_dict:
            params_dict = data_dict["nodeParameters"]["numerical"]
            temp = []

            for type in params_dict:
                key_name = type["name"]
                #type's format: {name: .., weight: ...}
                temp.append( {
                    key_name: type["range"]
                } )
            
            params_dict = data_dict["nodeParameters"]["categorical"]
            temp2 = []

            for type in params_dict:
                key_name = type["name"]
                #type's format: {name: .., weight: ...}
                temp2.append( {
                    key_name: type["options"]
                } )
            
            item_to_add = {
                "node-parameters": {
                    "numerical" : temp,
                    "categorical": temp2
                }
            }

            definitions["definitions"]["pd-model"].update(item_to_add)

        #edge parameters 
        if "edgeParameters" in data_dict:
            params_dict = data_dict["edgeParameters"]["numerical"]
            temp = []

            for type in params_dict:
                key_name = type["name"]
                #type's format: {name: .., weight: ...}
                temp.append( {
                    key_name: type["weight"]
                } )
            
            params_dict = data_dict["edgeParameters"]["categorical"]
            temp2 = []

            for type in params_dict:
                key_name = type["name"]
                #type's format: {name: .., options: ...}
                temp2.append( {
                    key_name: type["options"]
                } )
            
            item_to_add = {
                "edge-parameters": {
                    "numerical" : temp,
                    "categorical": temp2
                }
            }
            definitions["definitions"]["pd-model"].update(item_to_add)

        #compartments 
        compartments_dict = data_dict["compartments"]
        temp = {}

        for type in compartments_dict:
            key_name = type["name"]
            #type's format: {name: .., weight: ...}
            temp.update( {
                key_name:  type["content"]
            } )
        
        item_to_add = {
            "compartments" : temp
        }

        definitions["definitions"]["pd-model"].update(item_to_add)

        #rules 
        rules_dict = data_dict["rules"]
        temp = {}

        for type in rules_dict:
            key_name = type["name"]
            #type's format: {name: .., weight: ...}
            temp.update( {
                key_name: type["content"]
            } )
        
        item_to_add = {
            "rules" : temp
        }

        definitions["definitions"]["pd-model"].update(item_to_add)
        
        #data source/structure part
        if "file" in data_dict["dataSource"]["structure"]["fileOrRandom"]:
            item_to_add = {
                "structure": {
                    "file": data_dict["dataSource"]["structure"]["fileOrRandom"]["file"]
                }
            }

            curr_path = item_to_add["structure"]["file"]["path"]
            item_to_add["structure"]["file"]["path"] = os.path.join(project_dir, 'datasets', curr_path)
        
        else:
            generate_type = data_dict["dataSource"]["structure"]["fileOrRandom"]["generateType"]
            print("Generate type:", generate_type)
            item_to_add = {
                "structure": {
                    "random": {
                        "degree": data_dict["dataSource"]["structure"]["fileOrRandom"]["degree"],
                        "count": data_dict["dataSource"]["structure"]["fileOrRandom"]["count"],
                        "type": generate_type
                    }
                }
            }

         # Directly set the structure key at the top level
        conf["structure"] = item_to_add["structure"]
        conf["model-exploration"] = data_dict["model-exploration"]

        print('CONF BEFORE ADDING DEFINITIONS: PLS WORK --->', conf)

        conf["definitions"] = definitions["definitions"]
       

        print("HELLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOO WE ARE HERE")
        print('LATEST CONF', conf)

        return conf
    


