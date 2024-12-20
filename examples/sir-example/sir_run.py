from crowd.project_management.project import Project
from crowd.egress.file_egress import file_egress 

# 1. Project creation
project_name = "simplediffusion2"
creation_date = "19/10/2024"
info = "Diffusion of a virus on a random network"

my_project = Project()
my_project.create_project(project_name, creation_date, info, "node")


# OR load previous project 
# my_project.load_project(project_name)

# 2. Define the custom methods you wish to run

# returns the percentage of infected nodes in every snapshot
def get_percentage_infected(network):
    print(network.node_count)
    return (network.node_count[1] /network.G.number_of_nodes()) * 100

def save_graph_in_various_formats(network, my_project):
    my_project.egress.save_as_gexf(network.G)
    my_project.egress.save_as_edgelist(network.G)
    my_project.egress.save_as_gml(network.G)
    my_project.egress.save_as_graphml(network.G)
    my_project.egress.save_as_adjacency_list(network.G)

# 3. Run the simulation
my_project.lib_run_simulation(epochs=5,
                              snapshot_period=1,
                              curr_batch=1,
                              after_iteration_methods=[get_percentage_infected],
                              after_simulation_methods=[[save_graph_in_various_formats, my_project]])
