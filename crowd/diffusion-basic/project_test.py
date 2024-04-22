from crowd.models import DiffusionNetwork as n
from crowd.visualization import basic as bv
import os
from crowd.project_management.project import Project

'''
yaml_path = os.path.join(os.path.dirname(__file__), 'compartments-test.yaml')
mysimplenetwork = n.DiffusionNetwork(yaml_path)
visualizer = bv.Basic(os.path.join(os.path.dirname(__file__), 'artifacts'))

mysimplenetwork.run(10, visualizers=[visualizer], snapshot_period=2)
'''

# Create a new project
project_name = "test1"

'''
my_project = Project()
yaml_path = os.path.join(os.path.dirname(__file__), 'conf.yaml')
my_project.create_project(project_name, yaml_path)
my_project.run_simulation(10, 2)


'''
# Load an existing project
existing_project_name = "test1"
my_project = Project(existing_project_name)
#print("All result dates:\n", my_project.get_all_result_dates())

#print("\n\n\nGet result by date:\n", my_project.get_result_by_date("2024-04-13=23-06"))

#print("\n\n\n\n\nGet latest result:", my_project.get_latest_result())

#returns the status of node 0 in every snapshot
def get_node_status(network):
    return network.ndlib_model.status[0]

#returns the percentage of infected nodes in every snapshot
def get_percentage_infected(network):
    return network.status_delta[1] / network.G.number_of_nodes()

methods = [get_node_status, get_percentage_infected]

my_project.run_simulation(10, 2, methods)
