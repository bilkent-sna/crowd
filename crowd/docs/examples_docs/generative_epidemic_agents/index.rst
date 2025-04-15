Example 1: Epidemic simulation with generative agents
=====================================================

This example is based on `GABM-Epidemic <https://github.com/bear96/GABM-Epidemic/tree/main>`_. We re-implement the paper and the code with our framework to show it simplifies and streamlines this process. Crowd eliminates the need to write any code for infection logic and visualization tasks for this study, only leaving the task-specific LLM prompting and data collection to the modelers.

The scenario can be briefly described as follows: 

1. Agents reside on a network and contact with their neighbors every day
2. At the beginning of each day, each agent decides whether to stay home or go out, depending on the information provided such as:
    
    - personality traits
    - age
    - agent's health information
    - the percentage of new cases in the city to the total population

3. The decision of staying home or going out is made by an LLM of choice. A personalized query is sent for each agent. 
4. If an agent decides to stay home, they will not interact with any other agents
5. Infected agents who did not stay home (i.e. agent.location = grid) can spread the disease with a 0.1 probability on every contact to their Susceptible neighbors
6. Infected agents are healed in 6 days, which means they will switch to Recovered state

We execute the example on Google Colab for GPU usage and faster inferences. It can be easily adopted to local environments by modifying the paths. The tutorial can also be followed on the `Colab notebook <https://github.com/bilkent-sna/crowd/blob/master/crowd/docs/examples/generative_epidemic_agents/gen_agents.ipynb>`_.

.. toctree::
    :hidden:
    :maxdepth: 1
        
    steps_1_to_3
    modify_config
    init_llm
    define_methods
    run_simulation

**Next:** Steps 1-3: Import libraries, create project and load datasets