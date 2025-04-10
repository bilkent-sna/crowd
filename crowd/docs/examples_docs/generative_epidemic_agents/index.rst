Example 1: Epidemic simulation with generative agents
=====================================================

This example is based on `GABM-Epidemic <https://github.com/bear96/GABM-Epidemic/tree/main>`_. We re-implement the paper and the code with our framework to show it simplifies and streamlines this process. Crowd eliminates the need to write any code for infection logic and visualization tasks for this study, only leaving the task-specific LLM prompting and data collection to the modelers.

We execute the example on Google Colab for GPU usage and faster inferences. It can be easily adopted to local environments by modifying the paths. The tutorial can also be followed on the `Colab notebook <https://github.com/bilkent-sna/crowd/blob/master/crowd/docs/examples/generative_epidemic_agents/gen_agents.ipynb>`_.

**Step 1: Import the necessary libraries and login to HuggingFace**

 .. code-block:: python

        import json
        import os
        import random
        import time
        from names_dataset import NameDataset
        import networkx as nx
        from crowd.project_management.project import Project
        from huggingface_hub import login
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

        login(token="your_hf_token")

**Step 2: Create or load project**

Crowd's Project structure holds previous simulations, datasets and project information. 
For each simulation, we can either create a new project or load a previous project. 

To create a new project, we must provide 4 values:

1. Name of the project (prefer no spaces between words)
2. Creation date (automatically given if project is created on GUI)
3. A short summary of project's purpose
4. "node" or "edge" values to denote which property is mainly changed in this project's simulations 

Projects are saved to "crowd_projects" folder which is created on system's current user directory by default. If we want to save this project to another directory, we can provide another parameter "selected_path".

.. code-block:: python

        project_name = "gabm_epidemic"

        my_project = Project()
        creation_date = "16/03/2025"
        info = "GABM-Epidemic example implementation with Crowd framework"

        # Create new project
        my_project.create_project(
            project_name = project_name, 
            creation_date = creation_date, 
            info = info, 
            nodeOrEdge = "node", 
            selected_path = "/content/drive/My Drive/Your_Directory_Name/"
            )

After *create_project* we don't need to call *load_project* again. It is used when we are opening up a previously created project. 

.. code-block:: python

        # OR load previous project
        my_project.load_project(project_name, "/content/drive/My Drive/Your_Directory_Name/")


**Step 3: Upload datasets**

In this simulation, each person has personality traits assigned randomly. 
These personality traits are grouped into 5 categories: agreeableness, conscientiousness, surgency, emotional-stability, intellect. 
Since each category includes many traits, instead of listing them all in the configuration file, we write them into csv files and put them into datasets folder of Crowd. 
Alternatively, we can use the "upload dataset" facility of Crowd's GUI. 

**Step 4: Modify configuration**

.. code-block:: yaml

    name: gabm-epidemic-case
    structure:
        random:
            count: 100
            degree: 5
            type: random-regular
    definitions:
        pd-model:
            compartments:
                c1:
                    attribute: location
                    probability: 0.1
                    type: node-categorical
                    value: grid
                c2:
                    type: count-down
                    name: healing
                    iteration-count: 6
            name: diffusion
            rules:
                r1:
                    - Susceptible
                    - Infected
                    - c1
                r2:
                    - Infected
                    - Recovered
                    - c2
            nodetypes:
                Susceptible:
                    random-with-count:
                    count: "98"
                Infected:
                    random-with-count:
                    count: "2"
                Recovered:
                    random-with-count:
                    count: "0"
            node-parameters:
                categorical:
                    location:
                        - grid
                    agreeableness: 
                        "agreeableness_options.csv"
                    conscientiousness: 
                        "conscientiousness_options.csv"
                    surgency: 
                        "surgency_options.csv"
                    emotional-stability: 
                        "emotional_stability_options.csv"
                    intellect: 
                        "intellect_options.csv"
                numerical:
                    age:
                    - 18
                    - 65



**Next:** Example 2: Influence maximization