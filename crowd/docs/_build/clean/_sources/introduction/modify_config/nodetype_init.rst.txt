Initializing Node Types
=======================

In the modifying configuration section, we have utilized 'random with weight' initialization method of Crowd. In this section, we explain the details of all 4 initalization methods.

With all initialization types, the total node count should be equal to network's node count, or if setting with weights, to 1.

**1. Random with count**

For this initialization type, the exact number of nodes for each type is entered by the modeler. The node type will be chosen randomly for each node.

.. code-block:: yaml

    nodetypes:
        Susceptible:
            random-with-count:
                count: 90
        Infected:
            random-with-count:
                count: 10
        Recovered:
            random-with-count:
                count: 0


**2. Random with weight**

For this initialization type, a weight for each type is entered by the modeler. Node count for each type will be calculated by (node_count * weight_of_that_type).

The node type will be chosen randomly for each node.

.. code-block:: yaml

    nodetypes:
        Susceptible:
            random-with-weight:
                initial-weight: 0.9
        Infected:
            random-with-weight:
                initial-weight: 0.1
        Recovered:
            random-with-weight:
                initial-weight: 0

**3. Choose with metric**

Various social network analysis (SNA) metrics can also be utilized to choose node types. 

.. list-table::
   :header-rows: 1

   * - **Metric**
     - **Conf. File Notation**
   * - PageRank
     - `pagerank`
   * - Degree centrality
     - `degree`
   * - Betweenness centrality
     - `betweenness`
   * - Closeness centrality
     - `closeness`  
   * - Eigenvector centrality
     - `eigenvector`  
   * - Katz centrality
     - `katz` 

With these metrics, top k (count) nodes can be selected as the spreader. In the influence maximization simulations where researchers wish to compare their novel algorithms with the existing methods, centrality metrics are often chosen as a baseline.

With Crowd, researchers can simply rerun their simulations with the same settings by only changing the initialization method in the configuration file. Reading from file option, explained in the following subsection, can be used to load the seed nodes
determined with the researchers' own algorithm, or other methods to compare that are not provided by Crowd. 

An example configuration is given below:

.. code-block:: yaml

    nodetypes:
        Active:
            choose-with-metric:
                metric: pagerank
                count: 10
        Inactive:
            random-with-count:
                count: 90



**4. Load from file**

With this option, modelers can utilize the node lists saved previously to the project's datasets. 
This file can simply be copied to the project's datasets folder or uploaded through the user interface. 

Important: The file should only include the integers representing node IDs. Each number should be separated with comma or new line. Only CSV file format is accepted.

.. code-block:: yaml

    nodetypes:
        Active:
            from-file:
                path: 'name-of-file'
        Inactive:
            random-with-count:
            count: 90


**Next:** (Optional) Crowd's network models