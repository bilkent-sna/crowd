from crowd.project_management.project import Project
import random

# Step 1: Create or load project
project_name = "influencemax_custom"
my_project = Project()

# my_project.create_project(project_name, "11/03/2025", "influence maximization use case implementation with customsimnetwork", "node")
my_project.load_project(project_name)

# Step 2: Set the edge parameter using in degree of nodes
# Using weighted cascade for probability assignment where
    # p(u, v) = 1/in_degree(v) or treshold/in_degree(v)
treshold = 1  
graph = my_project.netw.G
for u, v in graph.edges():
    graph[u][v]["activation_prob"] = treshold/graph.degree[v]

graph.graph["activated_agents"] = []


"""
    EVERY ITERATION AGENT METHODS
"""
def step(network, agent_id):

    if network.G.nodes[agent_id]['node'] == 2:
        neighbors = list(network.G.neighbors(agent_id))

        for v in neighbors:
            if network.G.nodes[v]['node'] == 0:
                if (agent_id, v) in network.G.edges():
                    activation_prob = network.G[agent_id][v]["activation_prob"]
                else:
                    activation_prob = network.G[v][agent_id]["activation_prob"]

                rand = random.random()
                if activation_prob >= rand:
                    network.G.graph["activated_agents"].append(agent_id)
                    return         
                
"""
    AFTER ITERATION METHODS
"""
def update_node_states(network):
    for node in network.G.nodes():
        curr_state = network.G.nodes[node]['node']
        if curr_state == 0:
            network.G.nodes[node]['node'] = 1
        elif curr_state == 2 and node in network.G.graph["activated_agents"]:
            network.G.nodes[node]['node'] = 0
    
    network.G.graph["activated_agents"] = []

# Returns the sum of active_spreader and active node counts
# Will be saved to file automatically
def calculate_total_active(network):
    return (network.curr_type_nums[1] + network.curr_type_nums[0])

my_project.lib_run_simulation(epochs=20, 
                              snapshot_period=1, 
                              curr_batch=1, 
                              every_iteration_agent = [step],
                              after_iteration_methods=[
                                  update_node_states, 
                                  calculate_total_active]
                            )

