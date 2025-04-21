Step 2: Define custom methods
=============================

In general-purpose agent-based simulation frameworks such as Mesa or MASON, *step* methods are created to be executed in
each iteration of the simulation. In this tutorial, we name our *every-iteration-agent* method as *step* for the 
possible familiarity for the readers, though it can have any chosen name that is allowed by Python. This step function
corresponds to a step function implemented in extensions of Mesa's Agent classes or MASON's Steppable classes.  

*every-iteration-agent* methods take in 2 parameters by default (which can be extended, for more information check the Introduction
section): network and agent_id. 

We utilize these two parameters in our custom function to access the states of the current agent, get its neighbors, and if a neighbor is 
an Active Spreader, to get the activation probability of the edge between them. 

As explained in the previous step, when an Active_Spreader node tries to 
activate an Inactive node, a random number is generated. If the activation probability of 
the edge between these two nodes is larger than or equal to this random number, the Inactive
node is activated. 

In this implementation, we don't want to change the state of the newly activated nodes immediately. 
We want them to start activating the other nodes in the next iteration. Therefore, instead of 
setting their nodetype directly to "Active_Spreader", we add them to our "activated_agents" list, 
which was saved as a network parameter in the previous step. 

Modelers can use this notation when they wish to access the following parameters:

- node-level:
    network.G.nodes[agent_id]['parameter-name']
- state of the node (which is also node-level):
    network.G.nodes[agent_id]['node']
- edge-level:
    network.G[source_node][target_node]
- network-level:
    network.G.graph['parameter-name']
 

.. code-block:: python
        
        """
            EVERY ITERATION AGENT METHODS
        """
        def step(network, agent_id):

            if network.G.nodes[agent_id]['node'] == "Inactive":
                neighbors = list(network.G.neighbors(agent_id))

                for v in neighbors:
                    if network.G.nodes[v]['node'] == "Active_Spreader":
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
            # For each node
            for node in network.G.nodes():
                # Get the current state of the node
                curr_state = network.G.nodes[node]['node']
                # Move Active Spreaders -> Active
                if curr_state == "Active_Spreader":
                    network.G.nodes[node]['node'] = "Active"
                # Move Inactive nodes which just got activated -> Active Spreader
                elif curr_state == "Inactive" and node in network.G.graph["activated_agents"]:
                    network.G.nodes[node]['node'] = "Active_Spreader"
            
            # Reset the activated agents list for the next iteration
            network.G.graph["activated_agents"] = []

        # Returns the sum of active_spreader and active node counts
        # Will be saved to file automatically
        def calculate_total_active(network):
            return (network.curr_type_nums["Active"] + network.curr_type_nums["Active_Spreader"])

After the main diffusion logic is completed for an iteration (i.e. when all the agent-level methods are executed), Crowd will run the user-defined *after-iteration* methods.
We define two methods:

1. Update node states
    - Current Active Spreader nodes will switch to Active 
    - Newly activated nodes will switch to Active Spreader
2. Calculate total active
    - Data collection method 
    - We will use the results to draw charts and compare this method with others

**Next:** Step 3: Run simulation