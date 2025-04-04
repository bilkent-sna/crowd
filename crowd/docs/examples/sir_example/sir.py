from crowd.project_management.project import Project

# 1. Project creation
project_name = "simplediffusion"
creation_date = "19/10/2024"
info = "Diffusion of a virus on a random network"

my_project = Project()
#my_project.create_project(project_name, creation_date, info, "node")

# OR load previous project 
my_project.load_project(project_name)

# 2. Define the custom methods you wish to run

# returns the percentage of infected nodes in every snapshot
def get_percentage_infected(network):
    print(network.node_count)
    return (network.node_count[1] /network.G.number_of_nodes()) * 100

# 3. Run the simulation
my_project.lib_run_simulation(epochs=50,
                              snapshot_period=5,
                              curr_batch=1,
                              after_iteration_methods=[get_percentage_infected])
