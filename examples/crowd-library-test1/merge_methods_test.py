from crowd.api.merge_methods import MergeMethods

mrg = MergeMethods()

# Testing merge in parent simulation, where we will take the avg of all count_node_types in the parent folder
# And write the results to current simulation's folder
# The results can be used to draw charts in the results page of Crowd
#mrg.merge_in_parent_sim("simplediffusion", "2024-08-18=20-56", "1", "statusdelta.json", "mean")

# Testing merge across simulations
# mrg.merge_with_other_sim("firstcustom", "2024-08-15=11-56", "1", 'calculate_statistics_after_iteration.json',
#                          ['2024-08-15=12-00/1'])

#mrg.merge_with_other_sim("simplediffusion", "2024-08-21=14-55", "1", 'after_simulation.json', ['2024-08-21=14-55/2'])

# # Simulation 0
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=10-35", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=10-35", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=10-35", "1", "count_node_types.json", "mean")

# # Simulation 0.1
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=11-05", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=11-05", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=11-05", "1", "count_node_types.json", "mean")

# # Simulation 0.2
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=11-33", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=11-33", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=11-33", "1", "count_node_types.json", "mean")

# # Simulation 0.3
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-01", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-01", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-01", "1", "count_node_types.json", "mean")

# # Simulation 0.4
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-28", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-28", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-28", "1", "count_node_types.json", "mean")

# # Simulation 0.5
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-50", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-50", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=12-50", "1", "count_node_types.json", "mean")

# # Simulation 0.6
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=13-26", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=13-26", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=13-26", "1", "count_node_types.json", "mean")

# # Simulation 0.7
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=13-50", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=13-50", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=13-50", "1", "count_node_types.json", "mean")

# # Simulation 0.8
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=14-17", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=14-17", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=14-17", "1", "count_node_types.json", "mean")

# # Simulation 0.9
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=14-43", "1", "after_simulation.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=14-43", "1", "calculate_statistics_after_iteration.json", "mean")
# mrg.merge_in_parent_sim("firstcustom", "2024-08-22=14-43", "1", "count_node_types.json", "mean")

# Simulation 1
mrg.merge_in_parent_sim("firstcustom", "2024-08-22=15-06", "1", "after_simulation.json", "mean")
mrg.merge_in_parent_sim("firstcustom", "2024-08-22=15-06", "1", "calculate_statistics_after_iteration.json", "mean")
mrg.merge_in_parent_sim("firstcustom", "2024-08-22=15-06", "1", "count_node_types.json", "mean")

mrg.merge_with_other_sim("firstcustom", "2024-08-22=10-35", "1", 'after_simulation_mean.json', 
                        [
                            '2024-08-22=11-05/1',
                            "2024-08-22=11-33/1",
                            "2024-08-22=12-01/1",
                            "2024-08-22=12-28/1",
                            "2024-08-22=12-50/1",
                            "2024-08-22=13-26/1",
                            "2024-08-22=13-50/1",
                            "2024-08-22=14-17/1",
                            "2024-08-22=14-43/1",
                            "2024-08-22=15-06/1"
                        ])


mrg.merge_with_other_sim("firstcustom", "2024-08-22=10-35", "1", 'calculate_statistics_after_simulation_mean.json', 
                        [
                            '2024-08-22=11-05/1',
                            "2024-08-22=11-33/1",
                            "2024-08-22=12-01/1",
                            "2024-08-22=12-28/1",
                            "2024-08-22=12-50/1",
                            "2024-08-22=13-26/1",
                            "2024-08-22=13-50/1",
                            "2024-08-22=14-17/1",
                            "2024-08-22=14-43/1",
                            "2024-08-22=15-06/1"
                        ])

mrg.merge_with_other_sim("firstcustom", "2024-08-22=10-35", "1", 'count_node_types.json', 
                        [
                            '2024-08-22=11-05/1',
                            "2024-08-22=11-33/1",
                            "2024-08-22=12-01/1",
                            "2024-08-22=12-28/1",
                            "2024-08-22=12-50/1",
                            "2024-08-22=13-26/1",
                            "2024-08-22=13-50/1",
                            "2024-08-22=14-17/1",
                            "2024-08-22=14-43/1",
                            "2024-08-22=15-06/1"
                        ])