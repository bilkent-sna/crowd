Step 1: Initialize the project and modify configuration
=======================================================

Similar to the previous examples, we start the experiment by initializing our project with a name, creation date, 
a short summary, and "node" to denote this will be a node-based simulation where the changes in the states of the 
nodes will be the main focus of our project.  


.. code-block:: python

        from crowd.project_management.project import Project
        import random

        # Step 1: Create or load project
        project_name = "influencemax_custom"
        my_project = Project()

        my_project.create_project(
            project_name, 
            "11/03/2025", 
            "influence maximization use case implementation with customsimnetwork", 
            "node"
        )
        # my_project.load_project(project_name)

For this example, we will first conduct the experiment with the PageRank algorithm for the seed node selection.
Hence, we named this simulation as "pagerank-1", as it can be seen from the YAML block below. 

We utilize a `Facebook ego networks dataset <https://snap.stanford.edu/data/ego-Facebook.html>`_, which can be found on 
`Stanford Network Analysis Project (SNAP) <https://snap.stanford.edu/index.html>`_ platform. Modelers can utilize SNAP's 
`Large Network Dataset Collection <https://snap.stanford.edu/data/index.html>`_ to conduct simulations of various scenarios.

Since we will be using a real-world dataset for this simulation, we initialize the *struct* block to read from a file. 
The file "facebook_combined.txt" stores the edges, denoted as "0 1" where there is an edge from node 0 to node 1, or from node 1 to node 0.
As it is an undirected network, both nodes can be defined as source or target nodes. 

We use the keyword "nodes_edges" for the files where we provide the network's edges. Moreover, we use "header: false" to denote this file
does not have any headers that defines the contents of the columns. 

Inside the *definitions* block, we first specify that we will be using the CustomSimNetwork using "name:custom". Then, with only few lines, 
and by writing no code, we initialize the node types. Node that the network has 4099 nodes and the total count of all node types should be 
equal to that. A mistake in this part results in an unsuccessful simulation. 

We only want each node to try to spread information once, so we have an extra state named as *Active_Spreader*. After an iteration (i.e. one 
try to spread information), the *Active_Spreader* nodes become *Active* and cannot activate any nodes/agents anymore. 

.. code-block:: yaml
    
    name: pagerank-1
    structure:
        file:
            header: "false"
            path: "path-to\\facebook_combined.txt"
            type: nodes_edges
    definitions:
        name: custom
        nodetypes:
            Active_Spreader:
                choose-with-metric:
                    metric: pagerank
                    count: 100
            Active:
                random-with-count:
                    count: 0
            Inactive:
                random-with-count:
                    count: 3999


The Independent Cascade (IC) model works as the following: When an Active_Spreader node tries to 
activate an Inactive node, a random number is generated. If the activation probability of 
the edge between these two nodes is larger than or equal to this random number, the Inactive
node is activated. 

For this purpose, we need to initialize the activation probability of the edges before the diffusion
simulation begins. 

Weighted cascade is commonly utilized for this purpose where the probability is assigned as:

.. code-block:: python

    p(u, v) = 1/in_degree(v) or treshold/in_degree(v)

where u is the source node and v is the target node. We store this variable as an edge parameter. 

Following that, we define a network parameter called *activated_agents* and initialize it to 
an empty array, which we will use in our custom methods on the next step. 

.. code-block:: python

        # Step 2: Set the edge parameter using in degree of nodes
        # Using weighted cascade for probability assignment where
            # p(u, v) = 1/in_degree(v) or treshold/in_degree(v)
        treshold = 1  
        graph = my_project.netw.G
        for u, v in graph.edges():
            graph[u][v]["activation_prob"] = treshold/graph.degree[v]

        graph.graph["activated_agents"] = []




**Next:** Step 2: Define custom methods