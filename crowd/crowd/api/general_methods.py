import json
from pathlib import Path
# import time
import os
from crowd.egress.file_egress import file_egress as fe

# This class provides methods which does not require creation of a Project object 
class GeneralMethods:

    def __init__(self):
        user_home_dir = Path.home()
        self.projects_dir = os.path.abspath(os.path.join(user_home_dir, 'crowd_projects'))

        # Create project directory if not exists
        if not os.path.exists(self.projects_dir):
            os.makedirs(self.projects_dir)

    """
        reads projects directory and returns 
        {
            name: "project_name",
            date_created: "06/06/2024",
            info: "This is a short explanation of what the project does."
        }
        for each project
    """
    def list_all_projects(self):
        projects = []
        for dir_name in os.listdir(self.projects_dir):
            try:
                path = os.path.join(self.projects_dir, dir_name, "basic_info.json")
        
                with open(path, 'r') as f:
                    projects.append(json.load(f))
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Cannot find the required project file in {path}") from e
            except Exception as e:
                raise Exception(f"An error occurred while listing projects: {str(e)}") from e
            
        # print(projects)        
        return json.dumps(projects)
    
    
    """
        reads the current project directory and returns info about all simulations 
        {
            "date": "2024-08-22",
            "name": "n-player-r-ut-1-2",
            "simulation_duration": "0:00:23.896975",
            "start_time": "2024-08-22 15:06:47.092203",
            "end_time": "2024-08-22 15:07:10.989178",
            "epoch_num": 5000,
            "snapshot_period": 5000,
            "states": ["I","T","U"]
        }
        for each simulation
    """
    def list_all_simulations(self, project_name):
        simulations = []
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))

        for dir_name in os.listdir(base_dir):
            try:
                path = os.path.join(base_dir, dir_name, "1", "simulation_info.json")
                with open(path, 'r') as f:
                    sim_info = json.load(f)
                    
                # Count the number of sub-directories (child simulations) in this directory
                child_sim_count = len(os.listdir(os.path.join(base_dir, dir_name))) - 1 # minus one for conf file

                # Add the child_sim_count to the simulation info dictionary
                sim_info['child_sim_count'] = child_sim_count

                simulations.append(sim_info)

            except FileNotFoundError as e:
                raise FileNotFoundError(f"Cannot find the required simulation file in {path}") from e
            except Exception as e:
                raise Exception(f"An error occurred while listing simulations: {str(e)}") from e

        return json.dumps(simulations)
    
    """
        Lists the parent simulation file names and number of simulations within each
        Returns dictionary of {simulation_name: count}
    """
    def list_sim_and_count(self, project_name):
        simulations = {}
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))
       
        for dir_name in os.listdir(base_dir):
            try:
                child_sim_count = len(os.listdir(os.path.join(base_dir, dir_name))) - 1 # minus one for conf
                simulations.update({dir_name: child_sim_count})
            except FileNotFoundError as e:
                raise FileNotFoundError(f"Cannot find the simulation directory in {dir_name}") from e
            except Exception as e:
                raise Exception(f"An error occurred while listing simulations and their sub-simulation counts: {str(e)}") from e
            
        print("List sim and count print:", simulations)      
        return json.dumps(simulations)  

    """
        reads the current datasets directory and returns a list of the names of all files in there
    """
    def list_all_datasets(self, project_name):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'datasets'))
       
        try:
            files = os.listdir(base_dir)
            return json.dumps(files)
        except Exception as e:
            raise Exception(f"An error occurred while listing datasets: {str(e)}") from e
        
    """
       given the current project name, uploaded file name and its content, saves the file into project's dataset collection
    """
    def save_dataset(self, project_name, file_name, file_content):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'datasets'))
       
        try:
            with open(os.path.join(base_dir, file_name), 'wb') as file:
                file.write(bytes(file_content))
            print(f"File {file_name} saved successfully")
        except Exception as e:
            raise Exception(f"Error saving file: {e}")

    """
        Given the project name and simulation directory name, 
        returns the contents of the first simulation's simulation_info file in JSON format
    """
    def load_simulation_info(self, project_name, simulation_directory):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))
       
        try:
            path = os.path.join(base_dir, simulation_directory, "1\simulation_info.json")
            with open(path, 'r') as f:
                return json.dumps(json.load(f))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Cannot find the simulation info in {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while loading simulation info: {str(e)}") from e
        

    """
        Given the project name and simulation directory name, 
        returns the contents of all child simulation's simulation_info file in JSON format
    """
    def get_subsimulations_info(self, project_name, simulation_directory):
        simulations = {}
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results', simulation_directory))
        child_sim_count = len(os.listdir(base_dir)) - 1 # minus one for conf.yaml
        try:
            for i in range(1, child_sim_count+1):
                path = os.path.join(base_dir, str(i), "simulation_info.json")
                # print(path)
                with open(path, 'r') as f:
                    simulations.update({i: json.load(f)})
            
            return json.dumps(simulations)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Cannot find the sub-simulation info in {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while loading sub-simulation info: {str(e)}") from e
    
    """
        Given the project name and simulation directory name, 
        returns the networkx graph used in simulation, saved in each snapshot period
        in JSON format
    """
    def load_simulation_graph(self, project_name, simulation_directory):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))
       
        try:
            path = os.path.join(base_dir, simulation_directory, "1\graph.json")
            # return json.dumps(path)
            with open(path, 'r') as f:
                return json.dumps(json.load(f))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Cannot find the simulation graph in {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while loading the simulation graph: {str(e)}") from e
        
    """
        Given the project name and simulation directory name, 
        returns the added edges in simulation, saved in each iteration?
        in JSON format
    """
    def load_added_edges(self, project_name, simulation_directory):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))
       
        try:
            path = os.path.join(base_dir, simulation_directory, "new_addition.json")
            # return json.dumps(path)
            with open(path, 'r') as f:
                return json.dumps(json.load(f))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Cannot find the added edges file in {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while loading the added edges: {str(e)}") from e

    """
        reads the current parameters directory and returns a list of the names of all files in there
    """
    def list_all_parameters(self, project_name, simulation_directory):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results', simulation_directory, '1\parameters'))
       
        try:
            files = os.listdir(base_dir)
            return json.dumps(files)
        except Exception as e:
            raise Exception(f"An error occurred while listing all parameters: {str(e)}") from e
        
    """
        Given the project name, simulation directory and requested file name,
        returns the requested parameter file
    """
    def load_parameter_file(self, project_name, simulation_directory, file_name):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results', simulation_directory, '1\parameters'))
       
        try:
            path = os.path.join(base_dir, file_name)
            # return json.dumps(path)
            with open(path, 'r') as f:
                return json.dumps(json.load(f))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Cannot find the parameter file in {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while loading the parameter file: {str(e)}") from e
        
    """
        Given the project name, returns the methods file
    """
    def load_methods_file(self, project_name):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name))
       
        try:
            path = os.path.join(base_dir, 'methods.py')
            with open(path, 'r') as f:
                file_content = f.read()
                return json.dumps({'content': file_content})
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Cannot find the methods file in {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while loading the methods file: {str(e)}") from e

    """
        Saves the given methods to a python file, which will be used for the simulation
    """    
    def save_methods(self, project_name, file_content):
        path = os.path.abspath(os.path.join(self.projects_dir, project_name, 'methods.py'))
        try:
            with open(path, 'w') as file:
                file.write(file_content)
            print(f"Methods saved successfully")
        except Exception as e:
            raise Exception(f"Error saving methods file: {e}")
    

    def save_methods_list_view(self, project_name, file_content):
        path = os.path.abspath(os.path.join(self.projects_dir, project_name, 'method_settings.json'))
        try:
            with open(path, 'w') as file:
                file.write(file_content)
            print(f"Methods settings saved successfully")
        except Exception as e:
            raise Exception(f"Error saving the method settings file: {e}")
            

        
    """
        Given the project name, returns the conf file in that project directory
    """
    def get_conf(self, project_name):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name))
       
        try:
            path = os.path.join(base_dir, 'conf.yaml')
            with open(path, 'r') as f:
                file_content = f.read()
                return json.dumps(file_content)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Cannot find the configuration file in {path}") from e
        except Exception as e:
            raise Exception(f"An error occurred while loading the configuration file: {str(e)}") from e

    """
        Given the project name and file content, save the new content to project conf file
    """    
    def save_conf(self, project_name, file_content):
        path = os.path.abspath(os.path.join(self.projects_dir, project_name, 'conf.yaml'))
        try:
            with open(path, 'w') as file:
                file.write(file_content)
            print(f"Conf saved successfully")
        except Exception as e:
            raise Exception(f"Error saving the configuration file: {e}")
    
    
    """
        Given the project name, simulation directory, iteration number and file format, save the graph without the need to re-run the simulation
    """
    def save_network_after_simulation(self, project_name, simulation_directory, iteration_num, save_format):
        # Create file egress object
        path = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results', simulation_directory))
        saver = fe(path)
        # Call file egress' save network after simulation method        
        try:
            saver.save_network_after_simulation(iteration_num, save_format)
            print(f"Network file saved successfully")
        except Exception as e:
            raise Exception(f"Error saving network file after simulation: {e}")