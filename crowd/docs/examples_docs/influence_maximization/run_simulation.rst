Step 3: Run simulation
======================

We run the simulation using Crowd's Project method *lib_run_simulation*, for 20 iterations, collect data and save the graph in each iteration,
only once with the current settings. Moreover, we provide our custom methods as items in lists with respect to their execution times. 


.. code-block:: python

    my_project.lib_run_simulation(
        epochs=20, 
        snapshot_period=1, 
        curr_batch=1, 
        every_iteration_agent = [step],
        after_iteration_methods=[
            update_node_states, 
            calculate_total_active
        ]
    )


**Next:** Step 4: Merge data and draw charts