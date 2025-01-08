Step 1: Create or load a project
================================

**Library**

In Crowd, simulation settings, datasets and results are stored in a Project structure. As the first step, we import the Project class from the project_management module.

.. code-block:: python

   from crowd.project_management.project import Project

To start defining a simulation, we can either create a new project or load an existing one. Creating a project requires entering a name, a date, and a quick summary about the project's topic.

Last parameter node denotes that this is a simulation where we are interested in the changes of nodes. The other option is edge, which denotes simulations where edges are modified.

.. code-block:: python

   project_name = "simplediffusion"
   creation_date = "19/10/2024"
   info = "Diffusion of a virus on a random network"

   my_project = Project()

   # Create a new project
   my_project.create_project(project_name, creation_date, info, "node")

   # OR load previous project 
   #my_project.load_project(project_name) 

**App**

Alternatively, we can use Crowd's GUI to configure and run our simulations. The project creation screen is provided below.

.. image:: SIR_example_images/project_creation.png
   :alt: Project creation in Crowd GUI
   :width: 400px
   :align: center

|

**Next:** Step 2: Modify configuration