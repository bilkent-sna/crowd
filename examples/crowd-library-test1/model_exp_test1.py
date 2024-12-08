from crowd.project_management.project import Project
import os

project_name = "libtest"

my_project = Project()
creation_date = "28/06/2024"
info = "First test of library"

#create new project
# my_project.create_project(project_name, creation_date, info, "node")

#OR load previous
my_project.load_project(project_name)

# returns the status of node 0 in every snapshot
def get_node_status(network):
    return network.ndlib_model.status[0]

# #returns the percentage of infected nodes in every snapshot
# def get_percentage_infected(network):
#     return network.node_counts[1] /network.G.number_of_nodes()

# def greet(network):
#     return "Hello"

# every_iteration_methods = [get_node_status, get_percentage_infected]
# after_methods = [greet]

# my_project.lib_run_simulation(2, 1, every_iteration_methods, after_methods)
my_project.run_lib_multiple_simulations(num_simulations=2, 
                                        epochs=3, 
                                        snapshot_period=1)
