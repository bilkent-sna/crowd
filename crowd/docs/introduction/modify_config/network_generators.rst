Network Generators
==================

The following network generators can be utilized in the configuration in the following format:

.. code-block:: yaml

    structure:
        random:
            type: 'conf-file-notation'
            parameter1: 100
            parameter2: 4
            ...


.. list-table::
   :header-rows: 1

   * - **Name**
     - **Conf. File Notation**
     - **Parameters**
   * - Random Regular Graph (NetworkX)
     - `random-regular`
     - - **degree** (int): The degree of each node.
       - **count** (int): The number of nodes in the graph.
   * - Erdős-Rényi Graph (NetworkX)
     - `erdos-renyi`
     - - **p** (float): Probability for edge creation.
       - **count** (int): The number of nodes in the graph.
   * - Barabási-Albert Graph (NetworkX)
     - `barabasi-albert`
     - - **m** (int): Number of edges to attach from a new node to existing nodes.
       - **count** (int): The number of nodes in the graph.
   * - Watts-Strogatz Graph (NetworkX)
     - `watts-strogatz`
     - - **k** (int): Number of nearest neighbors to be joined with for each node.
       - **p** (float): Rewiring probability.
       - **count** (int): The number of nodes in the graph.
   * - Connected Watts-Strogatz Graph (NetworkX)
     - `connected-watts-strogatz`
     - - **k** (int): Number of nearest neighbors to be joined with for each node.
       - **p** (float): Rewiring probability.
       - **tries** (int): Number of attempts to generate a connected graph.
       - **count** (int): The number of nodes in the graph.
   * - Newman-Watts-Strogatz Graph (NetworkX)
     - `newman-watts-strogatz`
     - - **k** (int): Number of nearest neighbors to be joined with for each node.
       - **p** (float): Rewiring probability.
       - **count** (int): The number of nodes in the graph.
   * - Powerlaw Cluster Graph (NetworkX)
     - `powerlaw-cluster-graph`
     - - **m** (int): Number of edges to add for each new node.
       - **p** (float): Probability of adding a triangle after adding a random edge.
       - **count** (int): The number of nodes in the graph.
   * - Forest Fire Graph (iGraph)
     - `forest-fire`
     - - **fw-prob** (float): Forward burning probability.
       - **bw-factor** (float): Backward burning ratio.
       - **count** (int): The number of nodes in the graph.
   * - Stochastic Block Model (iGraph)
     - `stochastic-block`
     - - **p-matrix** (list of lists): Preference matrix.
       - **block-sizes** (list of ints): Sizes of the blocks.
       - **include-loops** (bool): Whether loops are included (optional, defaults to `False`).
       - **count** (int): The number of nodes in the graph.
   * - LFR Benchmark Graph (NetworkX)
     - `LFR-benchmark`
     - - **tau1** (float): Power-law exponent for degree distribution.
       - **tau2** (float): Power-law exponent for community size distribution.
       - **mu** (float): Mixing parameter.
       - **avg-degree** (float): Average degree (optional).
       - **min-degree** (int): Minimum degree (optional).
       - **max-degree** (int): Maximum degree (optional).
       - **min-community** (int): Minimum community size (optional).
       - **max-community** (int): Maximum community size (optional).
       - **tolerance** (float): Tolerance for the community size (optional, defaults to `1e-07`).
       - **max-iterations** (int): Maximum iterations (optional, defaults to `500`).
       - **count** (int): The number of nodes in the graph.
   * - Geometric Random Graph (iGraph)
     - `geometric-random`
     - - **radius** (float): Distance threshold value.
       - **count** (int): The number of nodes in the graph.
   * - Configuration Model (iGraph)
     - `configuration`
     - - **degrees-path** (str): Path to file containing degree sequence.
       - **method** (str): Graph generation method (`configuration` or others, optional, defaults to `configuration`).
   * - Static Fitness Model (iGraph)
     - `static-fitness`
     - - **m** (int): Number of edges.
       - **fitness-path** (str): Path to file containing fitness values.
       - **include-loops** (bool): Whether loops are included (optional, defaults to `False`).


The following networks can be utilized in the configuration in the following format:

.. code-block:: yaml

    structure:
        from-library:
            type: 'conf-file-notation'
            if-parameter-exists: 100
            ...
    
.. list-table::
   :header-rows: 1

   * - **Name**
     - **Conf. File Notation**
     - **Information**
   * - Complete Graph (NetworkX)
     - `complete-graph`
     - Parameter **count** (int): The number of nodes in the graph.
   * - Zachary's Karate Club Graph (NetworkX)
     - `karate-club-graph`
     - A social network of friendships between 34 members of a karate club.
   * - Les Miserables Graph (NetworkX)
     - `les-miserables`
     - A coappearance network of characters in the novel Les Miserables.
    

**Next:** (Optional) Reading networks from file