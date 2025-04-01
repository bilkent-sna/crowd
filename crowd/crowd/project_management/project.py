from collections import defaultdict
import importlib
import os
import json
import yaml
from datetime import datetime
import networkx as nx
from itertools import product
from pathlib import Path


from crowd.visualization import visualizer as v
from crowd.visualization import basic as bv

from crowd.models.network_creator.confchecker import ConfChecker
from crowd.models.network import Network
from crowd.models.CustomSimNetwork import CustomSimNetwork
from crowd.models.EdgeSimNetwork import EdgeSimNetwork
from crowd.models.DiffusionNetwork import DiffusionNetwork
from crowd.egress import file_egress as fd

class Project:
    def __init__(self, project_name = None):
        if project_name:
            #load existing project with the given name
            self.load_project(project_name)
        else:
            #it is a new project, initialize everything to none
            #then create project method will be called
            self.project_name = None
            self.project_dir = None
            self.config_file = None
            self.methods_file = None
            self.results_dir = None
            self.parent_simulation_dir = None
            self.visualizers = None
            self.egress = None
            self.tracked_params = []

    def create_project(self, project_name, creation_date, project_info, nodeOrEdge, selected_path = None):
        
        self.project_name = project_name

        # Get the user's home directory
        user_home_dir = Path.home()
        if selected_path:
            user_home_dir = selected_path

        # A directory will be created for the project with the given project name
        self.project_dir = os.path.join(user_home_dir, 'crowd_projects', project_name)

        # Holds the path of conf file
        self.conf_file = os.path.join(self.project_dir, 'conf.yaml')

        # Holds the path of methods file
        self.methods_file = os.path.join(self.project_dir, 'methods.py')

        # Path of method_settings file
        self.method_settings_file = os.path.join(self.project_dir, 'method_settings.json')

        # A directory will be created for the results within the project folder
        self.results_dir = os.path.join(self.project_dir, 'results')

        # A directory will be created for the datasets within the project folder
        self.datasets_dir = os.path.join(self.project_dir, 'datasets')

        # Create project directory if not exists
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)

        # Create results directory if not exists
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)
        
        # Create datasets directory if not exists
        if not os.path.exists(self.datasets_dir):
            os.makedirs(self.datasets_dir)

        # Initialize configuration and basic info files 
        self.conf = self.init_conf()
        self.methods = self.init_methods() #also inits method_settings
        self.save_basic_info(project_name, creation_date, project_info, nodeOrEdge)

        # Initialize network for simulations
        # By default, it is set as a diffusion network, but it can be changed with methods
        if nodeOrEdge == 'node':
            self.netw = DiffusionNetwork(self.conf, self.project_dir)
        elif nodeOrEdge == 'edge':
            self.netw = EdgeSimNetwork(self.conf, self.project_dir)
        else:
            #default
            self.netw = CustomSimNetwork(self.conf, self.project_dir)

    def load_project(self, project_name, selected_path = None):

        # Using the project name provided, load the project
        # If does not exist, print error message
        self.project_name = project_name
        user_home_dir = Path.home()
        if selected_path:
            user_home_dir = selected_path
        self.project_dir = os.path.join(user_home_dir, 'crowd_projects', project_name)
        #print("This is the project dir:", self.project_dir)
        self.conf_file = os.path.join(self.project_dir, 'conf.yaml')
        self.methods_file = os.path.join(self.project_dir, 'methods.py')
        self.results_dir = os.path.join(self.project_dir, 'results')
        self.parent_simulation_dir = None

        if not os.path.exists(self.project_dir):
            raise FileNotFoundError("Project does not exist.")
        
        if not os.path.exists(self.conf_file):
            raise FileNotFoundError("Conf file does not exist.")

        #print("Before getting conf. The conf path:", self.conf_file)
        self.conf = self.get_conf()
        #print("After getting conf")

        # Initialize network for simulations
        if "definitions" in self.conf:
            if "pd-model" in self.conf["definitions"]:
                #print("PD model in load project")                
                self.netw = DiffusionNetwork(self.conf, self.project_dir)
            else:
                # print("Custom model in load project")
                self.netw = CustomSimNetwork(self.conf, self.project_dir)
        else:
            self.netw = EdgeSimNetwork(self.conf, self.project_dir)

        self.visualizers = None

    def change_network_type(self, isDiffusion):
        if isDiffusion:
            self.netw = DiffusionNetwork(self.conf, self.project_dir)
        else:
            self.netw = EdgeSimNetwork(self.conf, self.project_dir)


    def init_methods(self):
        toWrite = "#Use this area to write your own methods."
        try:
            with open(self.methods_file, 'w') as file:
                file.write(toWrite)
            #print(f"Methods initialized")
            with open(self.method_settings_file, 'w') as file:
                file.write(json.dumps({}))
            #print(f"Method settings initialized")
        except Exception as e:
            print(f"Error saving file: {e}")

    # Creates a default configuration 
    def init_conf(self):
        # Define the content of the YAML file
        config = {
            "name": "SIR-example",
            "info": {
                "total_count": 100
            },
            "definitions": {
                "pd-model": {
                    "name": "diffusion",
                    "nodetypes": {
                        "Susceptible": {
                            "random-with-weight": {
                                "initial-weight": 0.9
                            }
                        },
                        "Infected": {
                            "random-with-weight": {
                                "initial-weight": 0.1
                            }
                        },
                        "Recovered": {
                            "random-with-weight": {
                                "initial-weight": 0
                            }
                        }
                    },
                    "node-parameters": {
                        "numerical": {
                            "age": [0, 100],
                            "friends": [0, 50]
                        },
                        "categorical": {
                            "gender": ["male", "female"]
                        }
                    },
                    "edge-parameters": {
                        "numerical": {
                            "weight": "int((u+v) % 10)"
                        },
                        "categorical": {
                            "type": ["co-worker", "family"]
                        }
                    },
                    "compartments": {
                        "c1": {
                            "type": "node-stochastic",
                            "ratio": 0.5,
                            "triggering_status": "Infected"
                        }
                    },
                    "rules": {
                        "r1": ["Susceptible", "Infected", "c1"]
                    }
                }
            },
            "structure": {
                "random": {
                    "type": 'random-regular',
                    "degree": 4,
                    "count": 100
                }
            }
        }

   
        # Write the YAML content to the file
        with open(self.conf_file, "w") as file:
            yaml.dump(config, file, default_flow_style=False)

        #print(f"YAML configuration file created at {self.conf_file}")
            
        return config
    
    # Retrieves the configuration parameters from the configuration file
    def get_conf(self):
        conf_checker = ConfChecker(self.conf_file)
        return conf_checker.get_conf()
        ###print("Got conf")

    # Update configuration with new parameters
    def update_conf(self, new_conf):
        
        self.conf = new_conf

        # Save updated configuration to file
        with open(self.conf_file, 'w') as f:
            yaml.dump(self.conf, f)

        # We have to recreate the network object here
        # Because if we don't, NetworkCreater object is not called again
        # And even though the conf is changed, the graph itself is not affected by these changes
        if "definitions" in self.conf:
            if "pd-model" in self.conf["definitions"]:
                self.netw = DiffusionNetwork(self.conf, self.project_dir)
            else:
                self.netw = CustomSimNetwork(self.conf, self.project_dir)
        else:
            self.netw = EdgeSimNetwork(self.conf, self.project_dir)

    def update_conf_with_path(self, path):
        conf_checker = ConfChecker(path)
        new_conf = conf_checker.get_conf()   
        
        self.update_conf(new_conf)

    def run_edge_simulation(self, epochs, snapshot_period):
        # Running the simulation
        start_time = datetime.now()

        # Create the directory for this simulation
        simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M')}")
        if not os.path.exists(simulation_dir):
            os.makedirs(simulation_dir)

        self.egress = fd.file_egress(simulation_dir)
        #self.netw.egress = self.egress
        
        # Initialize empty dictionary in JSON files
        self.egress.save("{}", 'graph.json')
       
        # Take update method
        self.netw.update_method = self.load_methods()["update"]

        # Modify networks run method for new egress
        self.netw.run(epochs, self.visualizers, snapshot_period, agility=1, egress=self.egress)
        end_time = datetime.now()

      
        # Ensure the closing braces are added only if necessary
        simulation_params = {
            "date": start_time.strftime("%Y-%m-%d"),
            "name": self.conf["name"],
            "simulation_duration": str(end_time - start_time),  # end - start
            "start_time": start_time.isoformat(sep=' '),
            "end_time": end_time.isoformat(sep=' '),
            "epoch_num": epochs,
            "snapshot_period": snapshot_period,
            # Include other simulation params
        }

        # Save simulation results to a JSON file
        sim_info_file = os.path.join(simulation_dir, "simulation_info.json")
        with open(sim_info_file, 'w') as f:
            json.dump(simulation_params, f, indent=4)
        
    def lib_run_simulation(self, 
                           epochs, 
                           snapshot_period,
                           curr_batch = 1, 
                           before_iteration_methods = None, 
                           after_iteration_methods = None,
                           every_iteration_agent = None,
                           after_simulation_methods = None):
        if type(self.netw) == DiffusionNetwork:        
            self.netw.before_iteration_methods = before_iteration_methods
            self.netw.after_iteration_methods = after_iteration_methods
            self.netw.after_simulation_methods = after_simulation_methods

            self.run_simulation(epochs, snapshot_period, curr_batch, user_called = True)
        elif type(self.netw) == EdgeSimNetwork:
            self.run_edge_simulation(epochs, snapshot_period)
        
        elif type(self.netw) == CustomSimNetwork:
            self.netw.before_iteration_methods = before_iteration_methods
            self.netw.after_iteration_methods = after_iteration_methods
            self.netw.every_iteration_agent = every_iteration_agent
            self.netw.after_simulation_methods = after_simulation_methods
            
            self.run_simulation(epochs, snapshot_period, curr_batch, user_called = True)

    # Simulates the social network and saves the results in JSON format under the results directory
    def run_simulation(self, epochs, snapshot_period, curr_batch = 1, user_called = False):
        # Running the simulation
        start_time = datetime.now()

        if self.parent_simulation_dir is None:
            self.parent_simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M-%S-%f')[:-3]}")
        else:
            self.parent_simulation_dir = self.parent_simulation_dir

        if curr_batch == 1:
            # Create the parent directory
            if not os.path.exists(self.parent_simulation_dir):
                os.makedirs(self.parent_simulation_dir)

            # Save the current configuration as conf.yaml
            conf_file_path = os.path.join(self.parent_simulation_dir, "conf.yaml")

            # Modify SafeDumper to ignore aliases
            yaml.SafeDumper.ignore_aliases = lambda *args: True

            with open(conf_file_path, 'w') as conf_file:
                yaml.dump(self.conf, conf_file, default_flow_style=False, Dumper=yaml.SafeDumper)
        
        # Create the directory for this simulation
        simulation_dir = os.path.join(self.parent_simulation_dir, str(curr_batch))
        if not os.path.exists(simulation_dir):
            os.makedirs(simulation_dir)

        # Create the parameters directory for this simulation
        parameters_dir = os.path.join(simulation_dir, 'parameters')
        if not os.path.exists(parameters_dir):
            os.makedirs(parameters_dir)

        self.egress = fd.file_egress(simulation_dir)
        # #print("Artifact path:", self.egress.artifact_path)
        self.netw.egress = self.egress
        
        # Initialize empty dictionary in JSON files
        self.egress.save("{}", 'graph.json')

        # User gives the method a list of functions, which will be called every step of the simulation
        # These methods can be user-defined or predefined
        # As they are written in Python for now, we can just pass it by name
        if not user_called:
            self.netw.before_iteration_methods = self.get_before_iteration_methods()
            self.netw.after_iteration_methods = self.get_after_iteration_methods()
            self.netw.after_simulation_methods = self.get_after_simulation_methods()
            if type(self.netw) == CustomSimNetwork:
                self.netw.every_iteration_agent = self.get_every_iteration_agent_methods()

        # Removed
        # watch_methods_save = {str(method.__name__): str(method.__code__) for method in self.netw.watch_methods}
        
        # Modify networks run method for new egress
        early_stop, actual_epochs = self.netw.run(epochs, self.visualizers, snapshot_period, agility=1, egress=self.egress)
        end_time = datetime.now()

        # self.egress.save("]", os.path.join('parameters', 'status_delta.json'))
        # self.egress.save("]", os.path.join('parameters', 'count_node_types.json'))
        
        if type(self.netw) == DiffusionNetwork: 
            simulation_params = {
                "date": start_time.strftime("%Y-%m-%d"),
                "name": str(self.conf["name"] + '-' + str(curr_batch)),
                "simulation_duration": str(end_time - start_time),  # end - start
                "start_time": start_time.isoformat(sep=' '),
                "end_time": end_time.isoformat(sep=' '),
                "epoch_num": epochs,
                "early_stop": early_stop,
                "actual_epochs": actual_epochs,
                "snapshot_period": snapshot_period,
                "states": list(self.conf["definitions"]["pd-model"]["nodetypes"].keys()),
                "simulation_no": str(curr_batch),
                "directory_name":  os.path.basename(self.parent_simulation_dir)
                # "watch_methods": watch_methods_save
                # Include other simulation params
            }
        else: 
            simulation_params = {
                "date": start_time.strftime("%Y-%m-%d"),
                "name": str(self.conf["name"] + '-' + str(curr_batch)),
                "simulation_duration": str(end_time - start_time),  # end - start
                "start_time": start_time.isoformat(sep=' '),
                "end_time": end_time.isoformat(sep=' '),
                "epoch_num": epochs,
                "early_stop": early_stop,
                "actual_epochs": actual_epochs,
                "snapshot_period": snapshot_period,
                "states": list(self.conf["definitions"]["nodetypes"].keys()),
                "simulation_no": str(curr_batch),
                "directory_name":   os.path.basename(self.parent_simulation_dir)
            }

        # Save simulation results to a JSON file
        sim_info_file = os.path.join(simulation_dir, "simulation_info.json")
        # Read existing simulation info if file exists
        if os.path.exists(sim_info_file):
            with open(sim_info_file, "r") as f:
                simulation_info = json.load(f)
                simulation_params.update(simulation_info) #add the new settings    
            
        with open(sim_info_file, 'w') as f:
            json.dump(simulation_params, f, indent=4)
    
    def run_multiple_simulations(self, num_simulations, epochs, snapshot_period):
        # Check for model exploration
        if "model-exploration" in self.conf:
            # Run parameter exploration
            self.explore_parameters(num_simulations, 
                                    epochs, 
                                    snapshot_period,
                                    user_called=False)
        else:
            # Regular batch running
            start_time = datetime.now()
            self.parent_simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M-%S-%f')[:-3]}")

            for curr_batch in range(1, num_simulations + 1):
                self.run_simulation(epochs, 
                                    snapshot_period, 
                                    curr_batch, 
                                    user_called=False)

                # Reset the network for the next run
                if curr_batch != num_simulations:
                    self.reset_network()

    def run_lib_multiple_simulations(self, 
                                     num_simulations, 
                                     epochs, 
                                     snapshot_period, 
                                     before_iteration_methods = None, 
                                     after_iteration_methods = None,
                                     every_iteration_agent = None,
                                     after_simulation_methods = None):
        
        # Check for model exploration
        if "model-exploration" in self.conf:
            # Run parameter exploration
            self.explore_parameters(num_simulations, 
                                    epochs, 
                                    snapshot_period,
                                    before_iteration_methods, 
                                    after_iteration_methods, 
                                    every_iteration_agent,
                                    after_simulation_methods, 
                                    user_called=True)
        else:
            # Regular batch running
            start_time = datetime.now()
            self.parent_simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M-%S-%f')[:-3]}")

            for curr_batch in range(1, num_simulations + 1):
                self.lib_run_simulation(epochs, 
                                        snapshot_period, 
                                        curr_batch, 
                                        before_iteration_methods, 
                                        after_iteration_methods,
                                        every_iteration_agent,
                                        after_simulation_methods)

                # Reset the network for the next run
                if curr_batch != num_simulations:
                    self.reset_network()

    def explore_parameters(self, 
                           num_simulations, 
                           epochs, 
                           snapshot_period, 
                           before_iteration_methods=None, 
                           after_iteration_methods=None, 
                           every_iteration_agent=None, 
                           after_simulation_methods=None, 
                           user_called = False):

        # Get parameters to explore from the configuration
        # If "model-exploration" is not in conf, return empty dict
        sweep_config = self.conf.get("model-exploration", {})
    
        # Get parameter's path and values to explore from conf's model exploration section
        paths = [param["path"] for param in sweep_config.values()]
        values = [param["values"] for param in sweep_config.values()]
        
        # Generate combinations
        combinations = list(product(*values))
        
        # Update self.conf with current parameter values
        for comb_index, combination in enumerate(combinations):
            for i, path in enumerate(paths):
                self.set_conf_in_sweep(path, combination[i])

            # Reset the network to have the new conf
            if comb_index != 0:
                self.reset_network()

            # Create a parent directory for this parameter combination
            start_time = datetime.now()
            self.parent_simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M-%S-%f')[:-3]}")
            if not os.path.exists(self.parent_simulation_dir):
                os.makedirs(self.parent_simulation_dir)

            # Run num_simulations times for each parameter set
            for curr_batch in range(1, num_simulations + 1):

                # Create the directory for this simulation
                simulation_dir = os.path.join(self.parent_simulation_dir, str(curr_batch))
                if not os.path.exists(simulation_dir):
                    os.makedirs(simulation_dir)

                # Save the parameter set info in this simulation's directory
                simulation_info = {
                    "param_set_index": comb_index + 1,
                    "parameters": {paths[i]: combination[i] for i in range(len(paths))}
                }

                sim_info_path = os.path.join(simulation_dir, "simulation_info.json")
                with open(sim_info_path, "w") as f:
                    json.dump(simulation_info, f, indent=4)
                
                if user_called:
                    # Run a simulation with these settings
                    self.lib_run_simulation(epochs, 
                                            snapshot_period, 
                                            curr_batch,
                                            before_iteration_methods, 
                                            after_iteration_methods,
                                            every_iteration_agent,
                                            after_simulation_methods)
                else:
                    self.run_simulation(epochs, 
                                        snapshot_period,
                                        curr_batch,
                                        False)
                    
                # Reset the network after each run
                if curr_batch != num_simulations:
                    self.reset_network()


    # Set currently explored parameter's value with current combination
    def set_conf_in_sweep(self, path, value):
        """
            In the file, we get a path from the user to access the right parameter. 
            This prevents changing another parameter with the same name. 
            Example format to write the path in the conf file (dot-seperated path definition):
                path: definitions.pd-model.compartments.c1.ratio
            In this method, we access the parameter in the given location, then change its value.
        """
        keys_in_path = path.split(".")
        sub_dict = self.conf # Initially, we set sub dict as conf, then we iterate 

        # Iteratively get to the final sub_dict, exclude the parameter's name, given as the last key (ex:ratio)
        for key in keys_in_path[:-1]:
            if key in sub_dict:
                sub_dict = sub_dict[key]
            else:
                #print("Key ", key, " is not in the given path")
                Exception("Conf key does not exist")
        
        # We reached the last sub dict, now we set the value with the key
        sub_dict[keys_in_path[-1]] = value


    # Resets the network object based on its type
    def reset_network(self):
        if type(self.netw) == DiffusionNetwork:
            self.netw = DiffusionNetwork(self.conf, self.project_dir)
        elif type(self.netw) == CustomSimNetwork:
            self.netw = CustomSimNetwork(self.conf, self.project_dir)
        elif type(self.netw) == EdgeSimNetwork:
            self.netw = EdgeSimNetwork(self.conf, self.project_dir)
        else:
            self.netw = Network(self.conf, self.project_dir)


    # Saves the information passed by UI for project initialization
    def save_basic_info(self, name, date, info, nodeOrEdge):

        basic_info = {
            "name": name, 
            "date": date,
            "info": info,
            "nodeOrEdge": nodeOrEdge
        }

        basic_info_file = os.path.join(self.project_dir, "basic_info.json")
        with open(basic_info_file, 'w') as f:
            json.dump(basic_info, f, indent=4)
    
    def get_every_iteration_agent_methods(self):
        path = os.path.join(self.project_dir, 'method_settings.json')
        
        try:
            with open(path, 'r') as f:
                settings = json.load(f)
            
            all_methods = self.load_methods()
            agent_methods = []
            
            for method_name, setting in settings.items():
                if setting.get('every_iteration_agent', False):
                    agent_methods.append(all_methods[method_name])
            
            return agent_methods
        except:
            #print("Method settings file not found. Returning empty array.")
            return []
        
    def get_before_iteration_methods(self):
        path = os.path.join(self.project_dir, 'method_settings.json')
        
        try:
            with open(path, 'r') as f:
                settings = json.load(f)
            
            all_methods = self.load_methods()
            before_iteration_methods = []
            
            for method_name, setting in settings.items():
                if setting.get('before_iteration', False):
                    before_iteration_methods.append(all_methods[method_name])
            
            return before_iteration_methods
        except:
            #print("Method settings file not found. Returning empty array.")
            return []
        
    def get_after_iteration_methods(self):
        path = os.path.join(self.project_dir, 'method_settings.json')
        
        try:
            with open(path, 'r') as f:
                settings = json.load(f)
            
            all_methods = self.load_methods()
            after_iteration_methods = []
            
            for method_name, setting in settings.items():
                if setting.get('after_iteration', False):
                    after_iteration_methods.append(all_methods[method_name])
            
            return after_iteration_methods
        except:
            #print("Method settings file not found. Returning empty array.")
            return []
    
    def get_after_simulation_methods(self):
        path = os.path.join(self.project_dir, 'method_settings.json')
        
        try:
            with open(path, 'r') as f:
                settings = json.load(f)
                all_methods = self.load_methods()
                after_simulation_methods = []
                
                for method_name, setting in settings.items():
                    if setting.get('after_simulation', False):
                        after_simulation_methods.append(all_methods[method_name])
                
                return after_simulation_methods
        except:
            #print("Method settings file not found. Returning empty array.")
            return []
        
        

    def load_methods(self):
        file_path = os.path.join(self.project_dir, 'methods.py')
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"Methods file not found: {file_path}")
        
        spec = importlib.util.spec_from_file_location("methods", file_path)
        if spec is None:
            raise ImportError(f"Could not load spec from {file_path}")
        
        methods = importlib.util.module_from_spec(spec)
        if methods is None:
            raise ImportError(f"Could not create module from spec for {file_path}")
        
        spec.loader.exec_module(methods)
        return {name: func for name, func in methods.__dict__.items() if callable(func)}
    
    def merge_in_parent_simulation(self, curr_sim_directory, json_file_name, merge_method):
        parent_dir = os.path.dirname(curr_sim_directory)
        sim_dirs = [d for d in os.listdir(parent_dir) if os.path.isdir(os.path.join(parent_dir, d))]

        
        if json_file_name != 'after_simulation.json':
            # Collect data from all simulations
            data_to_merge = defaultdict(list)
            
            for sim_dir in sim_dirs:
                sim_path = os.path.join(parent_dir, sim_dir, 'parameters', json_file_name)
                if os.path.exists(sim_path):
                    with open(sim_path, 'r') as f:
                        sim_data = json.load(f)
                        for entry in sim_data:
                            iteration = entry['Iteration']
                            data_to_merge[iteration].append(entry)
            
            # Merge data based on the specified method
            if merge_method == "mean":
                merged_data = self.merge_same_sim_mean(data_to_merge)
            elif merge_method == "sum":
                merged_data = self.merge_same_sim_sum(data_to_merge)
            else:
                raise ValueError(f"Unknown merge method: {merge_method}")
            # Save the merged data to a new file
            output_file = os.path.join(curr_sim_directory, 'parameters', f"{json_file_name.split('.')[0]}_{merge_method}.json")
            with open(output_file, 'w') as f:
                json.dump(merged_data, f, indent=4)
            
        else: #if it is the after simulation file
            entries = []

            """ Create array in the following format: [
                {key1: number, key2: number},
                {key1: number, key2: number}
            ]
            """
            for sim_dir in sim_dirs:
                sim_path = os.path.join(parent_dir, sim_dir, 'parameters', json_file_name)
                if os.path.exists(sim_path):
                    with open(sim_path, 'r') as f:
                        sim_data = json.load(f)
                        entries.append(sim_data)
                    
           
            merged_entry = {}
            keys = entries[0].keys()
            
            for key in keys:
                values = [entry[key] for entry in entries]
                if merge_method == "mean":
                    merged_entry[key] = round(sum(values) / len(values), 3)
                elif merge_method == "sum":
                    merged_entry[key] = round(sum(values), 3)
                else:
                    raise ValueError(f"Unknown merge method: {merge_method}")
                
             # Save the merged data to a new file
            output_file = os.path.join(curr_sim_directory, 'parameters', f"{json_file_name.split('.')[0]}_{merge_method}.json")
            with open(output_file, 'w') as f:
                json.dump(merged_entry, f, indent=4)
                
    def merge_same_sim_mean(self, data_to_merge):
        merged_data = []
        
        for iteration, entries in data_to_merge.items():
            merged_entry = {"Iteration": iteration}
            keys = entries[0].keys()
            
            for key in keys:
                if key != "Iteration":
                    values = [entry[key] for entry in entries]
                    merged_entry[key] = round(sum(values) / len(values), 3)
            
            merged_data.append(merged_entry)
        
        # Sort by iteration
        merged_data.sort(key=lambda x: x["Iteration"])
        
        return merged_data
    
    def merge_same_sim_sum(self, data_to_merge):
        merged_data = []
        
        for iteration, entries in data_to_merge.items():
            merged_entry = {"Iteration": iteration}
            keys = entries[0].keys()
            
            for key in keys:
                if key != "Iteration":
                    values = [entry[key] for entry in entries]
                    merged_entry[key] = round(sum(values), 3)
            
            merged_data.append(merged_entry)
        
        # Sort by iteration
        merged_data.sort(key=lambda x: x["Iteration"])
        
        return merged_data

    def merge_with_other_simulation(self, simulation_dir, json_file_name, merge_dir_dict):
        merged_data = {}

        # Include the current simulation directory in the merging
        merge_dir_dict.insert(0, os.path.relpath(simulation_dir, self.results_dir))
 
        if json_file_name != 'after_simulation.json' and json_file_name != 'after_simulation_mean.json':
            for sim_path in merge_dir_dict:
                # Construct the full path to the JSON file
                full_sim_path = os.path.join(self.results_dir, sim_path, "parameters", json_file_name)
                sim_info_path = os.path.join(self.results_dir, sim_path, "simulation_info.json")
                
                if os.path.exists(full_sim_path) and os.path.exists(sim_info_path):
                    with open(sim_info_path, 'r') as sim_info_file:
                        sim_info = json.load(sim_info_file)
                        sim_name = sim_info['name']
                    
                    with open(full_sim_path, 'r') as json_file:
                        sim_data = json.load(json_file)
                        for entry in sim_data:
                            iteration = entry["Iteration"]
                            value = round(entry["Value"], 3)  # Round to 3 decimal places
                            
                            if iteration not in merged_data:
                                merged_data[iteration] = {}
                            
                            merged_data[iteration][sim_name] = value

            # Prepare the merged data in the required format
            merged_data_list = [{"Iteration": iteration, **values} for iteration, values in merged_data.items()]

            
        
        else: #if it is the after simulation file, create a list, not dict
            merged_data_list = []

            for sim_path in merge_dir_dict:
                # Construct the full path to the JSON file
                full_sim_path = os.path.join(self.results_dir, sim_path, "parameters", json_file_name)
                sim_info_path = os.path.join(self.results_dir, sim_path, "simulation_info.json")
                
                if os.path.exists(full_sim_path) and os.path.exists(sim_info_path):
                    with open(sim_info_path, 'r') as sim_info_file:
                        sim_info = json.load(sim_info_file)
                        sim_name = sim_info['name']
                    
                    with open(full_sim_path, 'r') as json_file:
                        sim_data = json.load(json_file)
                        merged_data_list.append(sim_data)

        # Get the current timestamp in a cross-platform format
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
        output_file_name = f"{json_file_name.split('.')[0]}_merged_{timestamp}.json"
        output_file_path = os.path.join(simulation_dir, "parameters", output_file_name)

        # Save the merged data to a new JSON file
        with open(output_file_path, 'w') as output_file:
            json.dump(merged_data_list, output_file, indent=4)



