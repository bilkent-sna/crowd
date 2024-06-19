import os
import json
from crowd.project_management.new_project import NewProject


class ProjectFunctions:
    def create_project(self, name: str, date: str, info: str):
        """
        Creates a new project.

        :param name: The name of the project.
        :param date: The date when the project is first created (DD/MM/YYYY) format
        :param info: A short explanation of the project.
        """
        
        # Initialize the project object
        new_project = NewProject()

        # Create a new project with the given parameters
        # A directory will be created for this object with the most basic files
        try:
            new_project.create_project(name, date, info)
        except Exception as e:
            print(f"An error occurred: {e.with_traceback}")

        print(f"Creating project: {name} with info: {info}")

    
    def get_conf_and_run(self, data, project_name, epochs, snapshot_period):
        try:
            data_dict = json.loads(data)
            print(f"Received data successfully")
           
            # Initialize the project object
            new_project = NewProject()

            print("Before loading project")
            new_project.load_project(project_name)
            print("After loading project")
            
            conf = self.parseConf(data_dict, new_project.project_dir)

            print("Before updating conf")
            new_project.update_conf(conf)
            print("After updating conf")

            #remove this later and actually read the methods file
            methods = []
            new_project.run_simulation(epochs, snapshot_period, methods)

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
            #type's format: {name: .., weight: ...}
            temp.update( {
                key_name: {
                    "initial-weight": type["weight"]
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
            conf["definitions"]["pd-model"].update(item_to_add)

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
            generate_type = next(iter(data_dict["dataSource"]["structure"]["fileOrRandom"]))
            item_to_add = {
                "structure": {
                    generate_type: {
                        "degree": data_dict["dataSource"]["structure"]["fileOrRandom"][generate_type]["degree"]
                    }
                }
            }

         # Directly set the structure key at the top level
        conf["structure"] = item_to_add["structure"]

        print('CONF BEFORE ADDING DEFINITIONS: PLS WORK --->', conf)

        conf["definitions"] = definitions["definitions"]
       

        print("HELLLLLLLLLLLLLLLLOOOOOOOOOOOOOOOO WE ARE HERE")
        print('LATEST CONF', conf)

        return conf