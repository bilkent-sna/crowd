import json
import time
import os
 
# This class provides methods which does not require creation of a Project object 
class GeneralMethods:
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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects'))
        for dir_name in os.listdir(base_dir):
            try:
                path = os.path.join(base_dir, dir_name, "basic_info.json")
        
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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects', project_name, 'results'))
       
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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects', project_name, 'datasets'))
       
        try:
            files = os.listdir(base_dir)
            return json.dumps(files)
        except Exception as e:
            return json.dumps("No datasets uploaded yet.")
        
    """
       given the current project name, uploaded file name and its content, saves the file into project's dataset collection
    """
    def save_dataset(self, project_name, file_name, file_content):
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects', project_name, 'datasets'))
       
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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects', project_name, 'results'))
       
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
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects', project_name, 'results'))
       
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
        Given the project name, returns the conf file in that project directory
    """
    def get_conf(self, project_name):
        return "The yaml file" 

class test:
    def __init__(self, input1, input2):
        self.input1 = input1
        self.input2 = input2

    def get_crowd_version(self):
        return "1.0.0"
    
    def get_values(self):
        values = {}
        values["input1"] = self.input1
        values["input2"] = self.input2
        return json.dumps(values)
    

class test2:
    def get_values(self, input1, input2):
        values = {}
        values["input1"] = input1
        values["input2"] = input2
        return json.dumps(values)
    
    def waitForX(self):
        time.sleep(10)

temp = GeneralMethods()
print(temp.list_all_projects())