from crowd.project_management.project import Project
import os

project_name = "firstcustom"

my_project = Project()
creation_date = "11/08/2024"
info = "First test of CustomSimNetwork"

#create new project
#my_project.create_project(project_name, creation_date, info, "custom")
my_project.load_project(project_name)

def update_node_status(network, agent_id):
    if network.G.nodes[agent_id]["node"] == "Susceptible":
        network.G.nodes[agent_id]["node"] = "Infected"
    elif network.G.nodes[agent_id]["node"] == "Infected":
        network.G.nodes[agent_id]["node"] = "Recovered"

every_iteration_agent = [update_node_status]

my_project.lib_run_simulation(epochs=2, snapshot_period=1, every_iteration_agent=every_iteration_agent)