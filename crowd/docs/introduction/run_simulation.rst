Step 4: Run Simulation
======================

**Library**

Project class provides 2 methods to execute a simulation within Python code:

1. **lib_run_simulation**: This function runs the simulation only 1 time
2. **lib_run_multiple_simulations**: This function allows batch running and model exploration.

**batch run**: Running the simulation with the same settings multiple times, determined by the modeler. This helps reducing the impact of stochasticity on the results.

**model exploration**: Running the simulation with different settings to observe the impact of independent variables on dependent variables. In Crowd, model exploration constructs a grid of parameter combinations and only one value differs in each combination. It is not possible to explore different node type initializations as it would require the change of other types of nodes for the total to be 100 nodes again.

In this introductory example, we use the first method, lib_run_simulation. We run the simulation for 50 iterations (epochs), save the graph and data collectors every 5 iterations (snapshot period), for one time (curr batch number).

.. code-block:: python

    my_project.lib_run_simulation(epochs=50,
                                  snapshot_period=5,
                                  curr_batch=1,
                                  after_iteration_methods=[get_percentage_infected])
   
**App**

After selecting the configuration using selectors and saving these settings, simulation can be run by clicking the provided button as explained in step 2. 

**Next:** Step 5: Inspect results with network visualization