from crowd.project_management.project import Project
import os

project_name = "libtest"

my_project = Project()
creation_date = "28/06/2024"
info = "First test of library"

#create new project
my_project.create_project(project_name, creation_date, info, "node")

#OR load previous
#my_project.load_project(project_name)

#conf_path = "C:/Users/SERIF/Desktop/nese/dyn and soc netw/simulation tool/netsim/examples/crowd-library-test1/conf.yaml"
conf_path = os.path.join(os.path.dirname(__file__), 'conf.yaml')
my_project.update_conf_with_path(conf_path)

# returns the status of node 0 in every snapshot
def get_node_status(network):
    return network.ndlib_model.status[0]

#returns the percentage of infected nodes in every snapshot
def get_percentage_infected(network):
    return network.status_delta[1] /network.G.number_of_nodes()

def greet(network):
    return "Hello"

every_iteration_methods = [get_node_status, get_percentage_infected]
after_methods = [greet]

my_project.lib_run_simulation(2, 1, every_iteration_methods, after_methods)

