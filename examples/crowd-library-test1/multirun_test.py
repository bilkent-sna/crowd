from crowd.project_management.new_project import NewProject
import os

project_name = "simplediffusion"

my_project = NewProject()
# creation_date = "11/08/2024"
# info = "First test of CustomSimNetwork"

#create new project
#my_project.create_project(project_name, creation_date, info, "custom")
my_project.load_project(project_name)

def i_count(network):
    return network.status_delta[0]

def s_count(network):
    return network.status_delta[1]

#my_project.lib_run_simulation(epochs=4, snapshot_period=1, )
after_simulation_methods = [i_count, s_count]

my_project.run_lib_multiple_simulations(3, 3, 1, [], [], [], after_simulation_methods=after_simulation_methods)

