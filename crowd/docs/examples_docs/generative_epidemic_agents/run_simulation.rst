Steps 7-8: Run the simulation and analyze the results
=====================================================

**Step 7: Run the simulation**

Following the definition of custom methods, we can now execute the simulation
using the *lib_run_simulation* method of the Project class for 10 iterations (epochs),
saving the data and the graph to files in every iteration (snapshot_period = 1),
and run the simulation with the same settings for 1 time only (curr_batch = 1).


.. code-block:: python

    my_project.lib_run_simulation(
        epochs = 10, 
        snapshot_period = 1, 
        curr_batch = 1, 
        before_iteration_methods = before_iteration_methods, 
        after_iteration_methods = after_iteration_methods, 
        after_simulation_methods = after_simulation_methods
    )

**Step 8: Analyze the results** 

**Option 1:** 
If executed on Google Colab, download the project files and move them to crowd_projects folder on the local device. 
From Crowd GUI, select the simulation. Inspect the network visualization, draw charts and download visualizations.

**Option 2:**
Conduct data analysis with Python libraries by loading the generated JSON files. 

**Next:** Example 2: Influence maximization