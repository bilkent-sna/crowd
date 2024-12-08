# Agent level methods
import random
from crowd.project_management.project import Project
import os
import networkx as nx

# don't need this rn
def has_changed_strategy_at_step(network, agent_id):
    curr_strategy = network.G.nodes[agent_id]["node"]
    prev_strategy = network.G.nodes[agent_id]["prev_strategy"]

    if curr_strategy != prev_strategy:
        return True
    else:
        return False
    
# call every iteration agent
def proportional_imitation(network, agent_id):
    
    # Get a list of the IDs of the current neighbor
    neighborsIDs = list(network.G.neighbors(agent_id))

    # If agent has neighbors, execute the logic
    if len(neighborsIDs) > 0:

        # Choose a random neigbor, j
        j = random.choice(neighborsIDs)

        neigh_payoff = network.G.nodes[j]["previous_payoff"]
        focal_agent_payoff = network.G.nodes[agent_id]["previous_payoff"]

        # max payoff is a network level parameter we have set previously
        # If neighbor's payoff is higher than the limit, set it back to max possible
        if neigh_payoff > network.G.graph["max_payoff"]:
            neigh_payoff = network.G.graph["max_payoff"]

        # Compare neighbor's agent current agent's payoffs in the previous step/epoch
        if neigh_payoff > focal_agent_payoff:
            
            # The neighbor's strategy was better so we change the strategy with a probability
            prob = (neigh_payoff - focal_agent_payoff) / (network.G.graph["max_payoff"] - network.G.graph["min_payoff"])

            # Generate a random number
            rand = random.random()

            # If number < probability, we current agent changes its strategy
            if rand < prob:

                # In this simulation, strategies are saved as the states of the agent, in other words, the current node type
                # So, we set the current state to neighbor agent's state
                network.G.nodes[agent_id]["node"] = network.G.nodes[j]["node"]
            
# Agent level helpers
def calculate_payoffs_with_neighbors(network, agent_id):
    
    # Get a list of the IDs of the current neighbor
    neighborsIDs = network.G.neighbors(agent_id)
    # We will count the nodetypes of neighbors
    count_I = 0
    count_T = 0
    count_U = 0

    for id in neighborsIDs:
        curr_agent_type = network.G.nodes[id]["node"]
        match curr_agent_type:
            case "I":
                count_I += 1
            case "T":
                count_T += 1
            case "U":
                count_U += 1
    
    # Add current agent's count as well
    curr_agent_type = network.G.nodes[agent_id]["node"]
    match curr_agent_type:
        case "I":
            count_I += 1
        case "T":
            count_T += 1
        case "U":
            count_U += 1

    curr_payoff = 0
    denom = count_T + count_U

    if denom > 0: # if there are any trustees
        R_T = network.G.graph["R_T"]
        R_U = network.G.graph["R_U"]

        match curr_agent_type:
                case "I":
                    curr_payoff = (R_T * (count_T / denom)) - 1
                case "T":
                    curr_payoff = R_T * (count_I / denom)
                case "U":
                    curr_payoff = R_U * (count_I / denom)
    
    # Set the curr_payoff
    network.G.nodes[agent_id]["current_payoff"] = curr_payoff
    
    return curr_payoff

# Model level methods
def calculate_statistics_after_iteration(network):
    # This is equivalent to setAnonymousAgentAposteriori
    # But agent counting and strategy change counting is excluded,
    # as it is done by the Custom Simulation Network automatically

    # Calculate global payoff
    global_payoff = 0

    # If graph type is well mixed population
        # calculate payoff with neighbors globally
    # But we are running scale free network in this example so it is not included
    # Else cases use "calculate payoff with neighbors"

    # Locally assign payoffs
    for id in range(network.G.number_of_nodes()):
        global_payoff += calculate_payoffs_with_neighbors(network, id)

        # update the previous payoff and strategies
        network.G.nodes[id]["previous_payoff"] = network.G.nodes[id]["current_payoff"]
        network.G.nodes[id]["prev_strategy"] = network.G.nodes[id]["node"]

    return global_payoff

# After simulation methods
def r_UT(network):
    # print("Inside r_ut", network.conf["definitions"]["network-parameters"]["r_UT"])
    return network.conf["definitions"]["network-parameters"]["r_UT"]

# This returns U count at the end
def R_T_6(network):
    #print("Inside rt6", network.curr_type_nums["U"])
    return network.curr_type_nums["U"]


# Helper for this file
def average_degree(G):
    return sum(dict(G.degree()).values()) / G.number_of_nodes() if G.number_of_nodes() > 0 else 0

def set_network_params(network, my_project):
    # Set some model parameters
    my_project.netw.G.graph["R_U"] = (1 + my_project.netw.G.graph["r_UT"]) * my_project.netw.G.graph["R_T"]
    my_project.netw.G.graph["max_payoff"] = average_degree(my_project.netw.G) * my_project.netw.G.graph["R_U"]


project_name = "firstcustom"

my_project = Project()
# creation_date = "11/08/2024"
# info = "First test of CustomSimNetwork"

#create new project
#my_project.create_project(project_name, creation_date, info, "custom")
my_project.load_project(project_name)

# Set some model parameters
my_project.netw.G.graph["R_U"] = (1 + my_project.netw.G.graph["r_UT"]) * my_project.netw.G.graph["R_T"]
my_project.netw.G.graph["max_payoff"] = average_degree(my_project.netw.G) * my_project.netw.G.graph["R_U"]


before_iteration = [[set_network_params, my_project]]
every_iteration_agent = [proportional_imitation]
after_iteration = [calculate_statistics_after_iteration]
after_simulation = [r_UT, R_T_6]

#my_project.lib_run_simulation(epochs=100, snapshot_period=20, every_iteration_agent=every_iteration_agent, after_iteration_methods=after_iteration, after_simulation_methods=after_simulation)
# print("Density of the graph:", nx.density(my_project.netw.G))
# print("Average clustering coefficient of the graph: ", nx.average_clustering(my_project.netw.G))

# # Calculate the average degree
# avg_degree = sum(dict(my_project.netw.G.degree()).values()) / my_project.netw.G.number_of_nodes()
# print("Average degree of the graph: ", avg_degree)

# my_project.run_lib_multiple_simulations(num_simulations=50, epochs=5000, snapshot_period=5000, before_iteration_methods=before_iteration, every_iteration_agent=every_iteration_agent, after_iteration_methods=after_iteration, after_simulation_methods=after_simulation)
my_project.run_lib_multiple_simulations(num_simulations=50, epochs=5000, snapshot_period=4999, before_iteration_methods=before_iteration, every_iteration_agent=every_iteration_agent, after_iteration_methods=after_iteration, after_simulation_methods=after_simulation)


