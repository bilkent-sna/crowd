Step 3: Define custom methods
=============================

To describe additional simulation logic or data collection functions, we can define methods and pass them to simulation. These methods will be called at the simulation stage determined by the modeler.

DiffusionNetwork simulations in Crowd can execute custom methods at 3 intervals:

- Simulation execution begins
- In each epoch:
    - Before iteration methods are executed (interval 1)
    - NDlib runs rules and compartments
    - After iteration methods are executed (interval 2)
- After running all epochs:
    - After simulation methods are executed (interval 3)


Despite the execution time, all methods are required to follow two rules:

1. Take network as the parameter
2. To save a value in every iteration, return the result. It will be automatically saved in a file, named as function_name.json, in every snapshot period.

**snapshot period**: Denotes the "period" which the network and results of the custom methods will be written to files. If snapshot period is 1, data will be saved in each iteration.

More information regarding custom methods:

- Any library installed in user's computer can be imported and used.
- Helper methods do not have to be passed to "run simulation" method.
- Methods can take parameters other than network.

    - Method with no parameters passed as:
        .. code-block:: python

            after_iteration = [my_method]

    - Method with parameters:
        .. code-block:: python

            after_iteration = [my_method, parameter1, parameter2]

.. code-block:: python

    # returns the percentage of infected nodes in every snapshot
    def get_percentage_infected(network):
        print("Node counts", network.node_count)
        return (network.node_count[1] /network.G.number_of_nodes()) * 100

In the code above, we first reach the node counts of each node type through the network object. To see all class variables, see DiffusionNetwork model.

The node_count variable holds a dictionary in the following format:

.. code-block:: python 

    {nodetype1: count1, nodetype2: count2, nodetype3: count3}

NDLib converts the nodetypes to numbers in the order we defined them. Therefore, when we print the node_count dictionary in the first iteration we see the following output:

.. code-block:: python 

    {0: 86, 1: 14, 2: 0}

where {0: Susceptible, 1: Infected, 2: Recovered} nodes.

In this method, we want to save the percentage of infected nodes. Hence, we access *node_count[1]* and divide it to total number of nodes. network.G is the NetworkX object which stores all network information. Numerous functions provided by NetworkX can be reached through this object.

Finally, we return the computed number to be saved to "get_percentage_infected.json" in the following format:

.. code-block:: json

    {
        "Iteration": 1, 
        "Value": 14
    }

**App**

Alternatively, we can use the Method Lab of GUI:

.. figure:: SIR_example_images/methodlab.png
   :alt: Method Lab Crowd GUI
   :width: 95%
   :align: center

   Diffusion simulation Method Lab 

**Next**: Step 4: Run simulation