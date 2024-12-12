import json
import os
from crowd.project_management.project import Project

# This class provides methods which are used to merge data
# In UI, it is called from the results section

class MergeMethods:
    def __init__(self):
        self.projects_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..','projects'))

    def merge_in_parent_sim(self, project_name, parent_simulation_dir, simulation_dir, json_file_name, merge_method):
        try:
            project = Project(project_name)
            simulation_dir = os.path.join(project.results_dir, parent_simulation_dir, simulation_dir)
            project.merge_in_parent_simulation(simulation_dir, json_file_name, merge_method)
            return "Data successfully merged"
        except:
            return "Error while merging"
        
    def merge_with_other_sim(self, project_name, parent_simulation_dir, simulation_dir, json_file_name, merge_dir_list):
        try:
            project = Project(project_name)
            simulation_dir = os.path.join(project.results_dir, parent_simulation_dir, simulation_dir)
            project.merge_with_other_simulation(simulation_dir, json_file_name, json.loads(merge_dir_list))
            return "Data successfully merged"
        except:
            return "Error while merging"
    