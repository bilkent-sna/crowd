import json
import os
from pathlib import Path
from crowd.project_management.project import Project

# This class provides methods which are used to merge data
# In UI, it is called from the results section

class MergeMethods:
    def __init__(self):
        user_home_dir = Path.home()
        self.projects_dir = os.path.abspath(os.path.join(user_home_dir, 'crowd_projects'))
    
    def merge_in_parent_sim(self, project_name, parent_simulation_dir, simulation_dir, json_file_name, merge_method):
        try:
            project = Project(project_name)
            simulation_dir = os.path.join(project.results_dir, parent_simulation_dir, simulation_dir)
            project.merge_in_parent_simulation(simulation_dir, json_file_name, merge_method)
            return json.dumps("Data successfully merged")
        except Exception as e:
            raise Exception(f"An error occurred while merging in parent simulation: {str(e)}") from e
        
    def merge_with_other_sim(self, project_name, parent_simulation_dir, simulation_dir, json_file_name, merge_dir_list):
        try:
            project = Project(project_name)
            simulation_dir = os.path.join(project.results_dir, parent_simulation_dir, simulation_dir)
            project.merge_with_other_simulation(simulation_dir, json_file_name, json.loads(merge_dir_list))
            return json.dumps("Data successfully merged")
        except Exception as e:
            raise Exception(f"An error occurred while merging with other simulation: {str(e)}") from e
    