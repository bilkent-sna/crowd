
# IF TYYPE OF NETWORK IS WELL MIXED POPULATION
# after iteration method
def calculate_payoff_with_the_neighbors_globally(network):
    # We exclude tv from the formulation because it is set as 1 in all simulations given in paper 
    R_T = network.G.graph["R_T"]
    R_U = network.G.graph["R_U"]
    denom = network.curr_type_nums["T"] + network.curr_type_nums["U"]
    global_payoffs = 0 # Stores the global payoff for this iteration

    # For each agent, calculate current wealth
    for i in range(network.G.number_of_nodes()):
        curr_agent_type = network.G.nodes[i]["node"]
        agent_wealth = 0

        if denom > 0: # if there are any trustees
            match curr_agent_type:
                case "I":
                    agent_wealth = (R_T * (network.curr_type_nums["T"] / denom)) - 1
                case "T":
                    agent_wealth = R_T * (network.curr_type_nums["I"] / denom)
                case "U":
                    agent_wealth = R_U * (network.curr_type_nums["I"] / denom)
                case _:
                    print("Undefined agent type")

        #else agent wealth stays as 0

        # Save the calculated agent wealth
        network.G.nodes[i]["current_payoff"] = agent_wealth

        # Add to the global payoff
        global_payoffs += agent_wealth

    
    # Return the global payoff of this iteration so that its value will be saved to results file
    # With the iteration number
    return global_payoffs