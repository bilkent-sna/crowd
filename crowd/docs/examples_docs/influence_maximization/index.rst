Example 2: Influence maximization
=================================

Influence maximization is a vastly studied topic in the social networks research. 
It can be summarized to have 2 stages:

1. Selection of seed nodes
2. Simulation of influence/information spread

While the researchers actively introduce novel methodologies for the selection of seed
nodes, they commonly utilize simple algorithms for diffusion, such as Independent Cascade
(IC) or Linear Treshold (LT). 

To illustrate the effectiveness of their novel algorithms, researchers often conduct various 
experiments comparing their method's performance with the other available methods. 

This requires the stage 2 to be executed multiple times, while only the seed node selection varies.

With Crowd, we aim to simplify and fasten this progress with the features of the framework. 
We provide various methods to initialize the node types, as introduced in detail on our `Introduction to Crowd/Step 2:
Modify configuration/Initializing node types section <https://crowd.readthedocs.io/en/latest/introduction/modify_config/nodetype_init.html>`_.

To summarize, the initially "active" nodes which will spread the information to the "inactive" nodes can be selected
with the following options:

1. **Random with count**
2. **Random with weight**
3. Choose with metric
    - PageRank
    - Degree centrality
    - Betweenness centrality
    - Closeness centrality
    - Eigenvector centrality
    - Katz centrality
4. Load from file
    - Load the node IDs selected with the novel algorithms proposed by researchers in the CSV format

In the following pages, we provide an example code where we select the seed nodes with the metrics given in
option 3, and run the simulation using an IC model implemented with an agent-based approach. Following that, 
we visualize our results and compare each seed node selection method through the graphs we draw using Crowd's GUI.

The code in this tutorial provides can be utilized in influence maximization studies with only changing the initial node
selection method. 

**Next:** Step 1: Initialize the project and modify configuration

.. toctree::
    :hidden:
    :maxdepth: 1
        
    init_project_conf
    define_methods
    run_simulation
    merge_data_draw_charts