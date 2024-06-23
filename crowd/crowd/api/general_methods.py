import json
import time
import os
 
# This class provides methods which does not require creation of a Project object 
class GeneralMethods:

    def __init__(self):
        self.projects_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects'))

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
            except: 
                return "Cannot find project"
            
        # print(projects)        
        return json.dumps(projects)
    
    
    """
        reads the current project directory and returns info about all simulations 
        {
           UPDATE THESE
        }
        for each simulation
    """
    def list_all_simulations(self, project_name):
        simulations = []
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))
       
        for dir_name in os.listdir(base_dir):
            try:
                path = os.path.join(base_dir, dir_name, "simulation_info.json")
                with open(path, 'r') as f:
                    simulations.append(json.load(f))
            except: 
                return "Cannot find simulation"
            
        # print(projects)        
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
            return json.dumps("No datasets uploaded yet.")
        
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
            print(f"Error saving file: {e}")

    """
        Given the project name and simulation directory name, 
        returns the contents of the simulation_info file in JSON format
    """
    def load_simulation_info(self, project_name, simulation_directory):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))
       
        try:
            path = os.path.join(base_dir, simulation_directory, "simulation_info.json")
            with open(path, 'r') as f:
                return json.dumps(json.load(f))
        except: 
            return "Cannot find simulation"
    
    """
        Given the project name and simulation directory name, 
        returns the networkx graph used in simulation, saved in each snapshot period
        in JSON format
    """
    def load_simulation_graph(self, project_name, simulation_directory):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results'))
       
        try:
            path = os.path.join(base_dir, simulation_directory, "graph.json")
            # return json.dumps(path)
            with open(path, 'r') as f:
                return json.dumps(json.load(f))
        except Exception as e: 
            # Print the exception details
            print(f"Exception occurred: {e}")
            return "Cannot find simulation"

    """
        reads the current parameters directory and returns a list of the names of all files in there
    """
    def list_all_parameters(self, project_name, simulation_directory):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results', simulation_directory, 'parameters'))
       
        try:
            files = os.listdir(base_dir)
            return json.dumps(files)
        except Exception as e:
            return json.dumps("No parameters saved yet.")
        
    """
        Given the project name, simulation directory and requested file name,
        returns the requested parameter file
    """
    def load_parameter_file(self, project_name, simulation_directory, file_name):
        base_dir = os.path.abspath(os.path.join(self.projects_dir, project_name, 'results', simulation_directory, 'parameters'))
       
        try:
            path = os.path.join(base_dir, file_name)
            # return json.dumps(path)
            with open(path, 'r') as f:
                return json.dumps(json.load(f))
        except Exception as e: 
            # Print the exception details
            print(f"Exception occurred: {e}")
            return "Cannot find parameter file"
        
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
        except Exception as e: 
            # Print the exception details
            print(f"Exception occurred: {e}")
            return json.dumps({'error': "Cannot find methods file"})

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
            print(f"Error saving file: {e}")
    

    def save_methods_list_view(self, project_name, file_content):
        path = os.path.abspath(os.path.join(self.projects_dir, project_name, 'method_settings.json'))
        try:
            with open(path, 'w') as file:
                file.write(file_content)
            print(f"Methods settings saved successfully")
        except Exception as e:
            print(f"Error saving file: {e}")
            

        
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
        except Exception as e: 
            # Print the exception details
            print(f"Exception occurred: {e}")
            return json.dumps({'error': "Cannot find conf file"})
        
    def save_conf(self, project_name, file_content):
        path = os.path.abspath(os.path.join(self.projects_dir, project_name, 'conf.yaml'))
        try:
            with open(path, 'w') as file:
                file.write(file_content)
            print(f"Conf saved successfully")
        except Exception as e:
            print(f"Error saving file: {e}")
    