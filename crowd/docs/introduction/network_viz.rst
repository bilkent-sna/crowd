Step 5: Inspect results with network visualization
==================================================

In this step, for both library and app options followed previously, we continue from the app. 

As mentioned in the previous section, the graph files are saved automatically in the simulation directory. 

If a simulation is called from the library, we can reach the corresponding network visualization by selecting that simulation from the project page, and clicking "Go".

For simulations called from app, we will be directed to the Network page automatically. 

.. image:: SIR_example_images/networkViz3.png
   :alt: Network visualization page
   :width: 400px
   :align: center

In this page, we can interact with the network by zooming in and out, move the nodes and see their IDs when hovered over. 

When hovered over, the current node and its neighbors will be fully visible, while the others become more transparent. 

The iteration we inspect can be changed with forward and backward buttons, or with a slider. Simulation can be played and stopped with the "run/pause" buttons.

The current iteration can be downloaded in PNG, SVG and JPEG formats, and a playable image can be downloaded as a GIF. 

The colors of nodes can be changed by clicking on *Edit node style* button and choosing desired options.

Detailed information about each node and edge can be obtained from the *Inspect nodes* section. By searching for a node with its ID,
its node type and all parameters will be displayed, along with the edges connecting the node to its neighbors. For edge searches, both source and target node's IDs should be entered.


.. image:: SIR_example_images/inspect_nodes.png
   :alt: Inspecting nodes
   :width: 300px
   :align: center


**Next:** Step 6: Data Merge (Optional)

