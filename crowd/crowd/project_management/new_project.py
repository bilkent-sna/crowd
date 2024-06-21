import importlib
import os
import json
from crowd.models.EdgeSimNetwork import EdgeSimNetwork
import yaml
from datetime import datetime
import shutil
import networkx as nx

from crowd.visualization import visualizer as v
from crowd.visualization import basic as bv

from crowd.confchecker import ConfChecker
from crowd.network import Network
from crowd.models.DiffusionNetwork import DiffusionNetwork
from crowd.digress import file_digress as fd

class NewProject:
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
            self.visualizers = None
            self.digress = None
            self.tracked_params = []

    def create_project(self, project_name, creation_date, project_info):
        
        self.project_name = project_name

        # A directory will be created for the project with the given project name
        self.project_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', project_name)

        # Holds the path of conf file
        self.conf_file = os.path.join(self.project_dir, 'conf.yaml')

        # Holds the path of methods file
        self.methods_file = os.path.join(self.project_dir, 'methods.py')

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
        self.methods = self.init_methods()
        self.save_basic_info(project_name, creation_date, project_info)

        # Initialize network for simulations
        # By default, it is set as a diffusion network, but it can be changed with methods
        self.netw = DiffusionNetwork(self.conf)

    def load_project(self, project_name):

        # Using the project name provided, load the project
        # If does not exist, print error message
        self.project_name = project_name
        self.project_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'projects', project_name)
        self.conf_file = os.path.join(self.project_dir, 'conf.yaml')
        self.methods_file = os.path.join(self.project_dir, 'methods.py')
        self.results_dir = os.path.join(self.project_dir, 'results')

        if not os.path.exists(self.project_dir):
            raise FileNotFoundError("Project does not exist.")
        
        if not os.path.exists(self.conf_file):
            raise FileNotFoundError("Conf file does not exist.")

        self.conf = self.get_conf()
        
        # Initialize network for simulations
        # By default, it is set as a diffusion network, but it can be changed with methods
        self.netw = DiffusionNetwork(self.conf)

        self.visualizers = None

    def change_network_type(self, isDiffusion):
        if isDiffusion:
            self.netw = DiffusionNetwork(self.conf)
        else:
            self.netw = EdgeSimNetwork(self.conf)


    def init_methods(self):
        toWrite = "#Use this area to write your own methods."
        try:
            with open(self.methods_file, 'w') as file:
                file.write(toWrite)
            print(f"Methods initialized")
        except Exception as e:
            print(f"Error saving file: {e}")

    # Creates a default configuration 
    def init_conf(self):
        # Define the content of the YAML file
        config = {
            "name": "SIR-example-with-all-compartment-types",
            "info": {
                "total_count": 200
            },
            "definitions": {
                "pd-model": {
                    "name": "diffusion",
                    "nodetypes": {
                        "Susceptible": {
                            "initial-weight": 0.9,
                            "color": "blue"
                        },
                        "Infected": {
                            "initial-weight": 0.1,
                            "color": "red"
                        },
                        "Recovered": {
                            "initial-weight": 0,
                            "color": "green"
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
                    "degree": 4
                }
            }
        }

   
        # Write the YAML content to the file
        with open(self.conf_file, "w") as file:
            yaml.dump(config, file, default_flow_style=False)

        print(f"YAML configuration file created at {self.conf_file}")
            
        return config
    
    # Retrieves the configuration parameters from the configuration file
    def get_conf(self):
        conf_checker = ConfChecker(self.conf_file)
        return conf_checker.get_conf()
        #print("Got conf")

    # Update configuration with new parameters
    def update_conf(self, new_conf):
        
        self.conf = new_conf

        # We have to recreate the network object here
        # Because if we don't, NetworkCreater object is not called again
        # And even though the conf is changed, the graph itself is not affected by these changes
        self.netw = DiffusionNetwork(self.conf)

        # Save updated configuration to file
        with open(self.conf_file, 'w') as f:
            yaml.dump(self.conf, f)

    def run_edge_simulation(self, epochs, snapshot_period):
        # Running the simulation
        start_time = datetime.now()

        # Create the directory for this simulation
        simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M')}")
        if not os.path.exists(simulation_dir):
            os.makedirs(simulation_dir)

        self.digress = fd.file_digress(simulation_dir)
        
        # Initialize empty dictionary in JSON files
        self.digress.save("{}", 'graph.json')
       
        # Take update method
        self.netw.update_method = self.load_methods()["update"]

        # Modify networks run method for new digress
        self.netw.run(epochs, self.visualizers, snapshot_period, agility=1, digress=self.digress)
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

    
    # Simulates the social network and saves the results in JSON format under the results directory
    def run_simulation(self, epochs, snapshot_period):
        # Running the simulation
        start_time = datetime.now()

        # Create the directory for this simulation
        simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M')}")
        if not os.path.exists(simulation_dir):
            os.makedirs(simulation_dir)

        # Create the parameters directory for this simulation
        parameters_dir = os.path.join(simulation_dir, 'parameters')
        if not os.path.exists(parameters_dir):
            os.makedirs(parameters_dir)

        self.digress = fd.file_digress(simulation_dir)
        
        # Initialize empty dictionary in JSON files
        self.digress.save("{}", 'graph.json')
        self.digress.save("[", os.path.join('parameters', 'statusdelta.json'))

        # User gives the method a list of functions, which will be called every step of the simulation
        # These methods can be user-defined or predefined
        # As they are written in Python for now, we can just pass it by name
        self.netw.every_iteration_methods = self.get_every_iteration_methods()
        self.netw.after_methods = self.get_after_simulation_methods()

        # Removed
        # watch_methods_save = {str(method.__name__): str(method.__code__) for method in self.netw.watch_methods}
        
        # Modify networks run method for new digress
        self.netw.run(epochs, self.visualizers, snapshot_period, agility=1, digress=self.digress)
        end_time = datetime.now()

        self.digress.save("]", os.path.join('parameters', 'statusdelta.json'))

        # Ensure the closing braces are added only if necessary
        simulation_params = {
            "date": start_time.strftime("%Y-%m-%d"),
            "name": self.conf["name"],
            "simulation_duration": str(end_time - start_time),  # end - start
            "start_time": start_time.isoformat(sep=' '),
            "end_time": end_time.isoformat(sep=' '),
            "epoch_num": epochs,
            "snapshot_period": snapshot_period,
            "states": list(self.conf["definitions"]["pd-model"]["nodetypes"].keys()),
            # "watch_methods": watch_methods_save
            # Include other simulation params
        }

        # Save simulation results to a JSON file
        sim_info_file = os.path.join(simulation_dir, "simulation_info.json")
        with open(sim_info_file, 'w') as f:
            json.dump(simulation_params, f, indent=4)

    # Saves the information passed by UI for project initialization
    def save_basic_info(self, name, date, info):

        basic_info = {
            "name": name, 
            "date": date,
            "info": info
        }

        basic_info_file = os.path.join(self.project_dir, "basic_info.json")
        with open(basic_info_file, 'w') as f:
            json.dump(basic_info, f, indent=4)
    
    def get_every_iteration_methods(self):
        path = os.path.join(self.project_dir, 'method_settings.json')
        with open(path, 'r') as f:
            settings = json.load(f)
        
        all_methods = self.load_methods()
        every_iteration_methods = []
        
        for method_name, setting in settings.items():
            if setting.get('every_iteration', False):
                every_iteration_methods.append(all_methods[method_name])
        
        return every_iteration_methods
    
    def get_after_simulation_methods(self):
        path = os.path.join(self.project_dir, 'method_settings.json')
        with open(path, 'r') as f:
            settings = json.load(f)
        
        all_methods = self.load_methods()
        after_simulation_methods = []
        
        for method_name, setting in settings.items():
            if setting.get('after_simulation', False):
                after_simulation_methods.append(all_methods[method_name])
        
        return after_simulation_methods

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
    

# pr = NewProject()
# pr.load_project("customsimulation")
# pr.change_network_type(False) #change network type to edge
# pr.run_edge_simulation(2, 1)
# print("Simulation completed")

