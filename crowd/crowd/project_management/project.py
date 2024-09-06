import os
import json
from datetime import datetime
import shutil
import networkx as nx

from crowd.visualization import visualizer as v
from crowd.visualization import basic as bv

from crowd.confchecker import ConfChecker
from crowd.network import Network
from crowd.models.DiffusionNetwork import DiffusionNetwork
from crowd.digress import file_digress as fd



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
            self.results_dir = None
            self.visualizers = None
            self.digress = None
            self.tracked_params = []

    #Creates a new project
    def create_project(self, project_name, conf_directory = None):
        self.project_name = project_name

        # A directory will be created for the project with the given project name
        self.project_dir = os.path.join(os.getcwd(), project_name)

        # Holds the path of conf file
        # Initially conf.yaml file is used, user can change this with methods later
        self.conf_file = os.path.join(self.project_dir, 'conf.yaml')
        if(conf_directory != None): 
            # Save a copy of given conf file to our project
            shutil.copy(conf_directory, self.conf_file)

        # A directory will be created for the results within the project folder
        self.results_dir = os.path.join(self.project_dir, 'results')

        # Create project directory if not exists
        if not os.path.exists(self.project_dir):
            os.makedirs(self.project_dir)

        # Create results directory if not exists
        if not os.path.exists(self.results_dir):
            os.makedirs(self.results_dir)

        # Initialize configuration if not exists
        if not os.path.exists(self.conf_file):
            self.conf = self.init_conf()
        else:
            self.conf = self.get_conf() #when creating a new project, not expected to run
        #self.simulations = {} #this is a dictionary that holds different runs of simulations with their initiation time as the key
       
        # Initialize network for simulations
        if "pd-model" in self.conf["definitions"]:
            #it is a predefined model
            self.netw = DiffusionNetwork(self.conf)
        else:
            self.netw = Network(self.conf)

    def load_project(self, project_name):
        # Using the project name provided, load the project
        # If does not exist, print error message
        self.project_name = project_name
        self.project_dir = os.path.join(os.getcwd(), "/projects/" + project_name)
        self.conf_file = os.path.join(self.project_dir, 'conf.yaml')
        self.results_dir = os.path.join(self.project_dir, 'results')

        if not os.path.exists(self.project_dir):
            raise FileNotFoundError("Project does not exist.")
        
        if not os.path.exists(self.conf_file):
            raise FileNotFoundError("Conf file does not exist.")

        self.conf = self.get_conf()

        # Initialize network for simulations
        if "pd-model" in self.conf["definitions"]:
            #it is a predefined model
            self.netw = DiffusionNetwork(self.conf)
        else:
            self.netw = Network(self.conf)

        #self.tracked_params = self.conf["parameters-to-track"]
        self.visualizers = None

    #Creates a default configuration if not already present.
    def init_conf(self):
        # Default configuration
        config = {
            "fields": {
                "name": self.project_name
                # Add more parameters as needed
            }, 
            "structure": {
                "random": {
                    "seed" : 123, 
                    "degree": 4
                }
            }#,
            #"parameters-to-track": []
        }

        with open(self.conf_file, 'w') as f:
            json.dump(config, f, indent=4)
        
        return config
    
    #Retrieves the configuration parameters from the configuration file
    def get_conf(self):
        conf_checker = ConfChecker(self.conf_file)
        return conf_checker.get_conf()
        #print("Got conf")

    def update_conf(self, new_conf):
        # Update configuration with new parameters

        #how do we get the parameters? is new_conf a file? 
        #if it is a dictionary of conf, we can send it to validate conf
        #then write it to file
        #current_config = self.get_conf()
        #current_config["parameters"].update(new_conf)
        current_conf = new_conf

        # Save updated configuration to file
        with open(self.conf_file, 'w') as f:
            json.dump(current_conf, f, indent=4)
    
    # Simulates the social network and saves the results in JSON format under the results directory
    def run_simulation(self, epochs, snapshot_period, methods):
        # Running the simulation
        start_time = datetime.now()

        #data_in_iteration = {}

        # Create the directory for this simulation
        simulation_dir = os.path.join(self.results_dir, f"{start_time.strftime('%Y-%m-%d=%H-%M')}")
        if not os.path.exists(simulation_dir):
            os.makedirs(simulation_dir)

        self.digress = fd.file_digress(simulation_dir)
        self.digress.save("{", 'graph.json')

        self.digress.save("{", 'statusdelta.json')

        #user gives the method a list of functions, which will be called every step of the simulation
        #these methods can be user-defined or predefined
        #as they are written in Python for now, we can just pass it by name
        self.netw.watch_methods = methods
        watch_methods_save = {}
        #temp code
        for method in self.netw.watch_methods:
            watch_methods_save[str(method.__name__)] = str(method.__code__)

        
        #modify networks run method for new digress
        self.netw.run(epochs, self.visualizers, snapshot_period, agility=1, digress = self.digress)
        end_time = datetime.now()

        self.digress.save("}", 'graph.json')
        self.digress.save("\n}", 'statusdelta.json')

        simulation_params = {
            "date": start_time.strftime("%Y-%m-%d"),
            "simulation-duration": str(end_time - start_time), #end - start
            "start-time": start_time.isoformat(sep= ' '),
            "end-time": end_time.isoformat(sep= ' '),
            "epoch-num" : epochs,
            "snapshot-period": snapshot_period,
            "states": list(self.conf["definitions"]["pd-model"]["nodetypes"].keys()),
            "watch-methods": watch_methods_save 
            # Include other simulation params
        }

        #we save graph with run method digress?

        # Save simulation results to a JSON file
        sim_info_file = os.path.join(simulation_dir, "simulation_info.json")
        with open(sim_info_file, 'w') as f:
            json.dump(simulation_params, f, indent=4)
    
    
    #Retrieves all the simulation results stored in the results directory.
    def get_results(self):
        results = []
        for file_name in os.listdir(self.results_dir):
            if file_name.endswith('.json'):
                with open(os.path.join(self.results_dir, file_name), 'r') as f:
                    results.append(json.load(f))
        return results

    def run_multiple_simulations(self, num_simulations, epochs, snapshot_period, methods):
        for curr_batch in range(num_simulations):
            self.run_simulation(epochs, snapshot_period, methods, curr_batch)

    def delete_results(self):
        # Delete all simulation result files
        for file_name in os.listdir(self.results_dir):
            if file_name.endswith('.json'):
                os.remove(os.path.join(self.results_dir, file_name))
    
    #returns the results of the most recent simulation
    def get_latest_result(self):
        latest_result = max(os.listdir(self.results_dir))
        print("latest result", latest_result)
        with open(os.path.join(self.results_dir, latest_result), 'r') as f:
            return json.load(f)
        
    #retrieves simulation results for a specific date.
    def get_result_by_date(self, date):
        result_file = os.path.join(self.results_dir, f"{date}.json")
        if os.path.exists(result_file):
            with open(result_file, 'r') as f:
                return json.load(f)
        else:
            return None
    
    #returns a list of all dates for which simulation results are available
    def get_all_result_dates(self):
        result_dates = [filename.split('.')[0] for filename in os.listdir(self.results_dir)]
        return result_dates
    



    '''
    
    #related to UI
    def initialize_project_screen(self):
        pass

    #return the information of selected simulation - what kind of info are we returning?
    def load_selected_simulation(self, simulation_id):
        pass

    #calculate some metric e.g. avg degree
    def calculate_metric(self):
        pass
        
    '''