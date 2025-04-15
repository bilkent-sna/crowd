Steps 1-3: Import libraries, create project and load datasets
=============================================================

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

The data files used for this example can be found `here <https://github.com/bilkent-sna/crowd/tree/master/crowd/docs/examples/generative_epidemic_agents/datasets>`_.

**Next:** Step 4: Modify configuration