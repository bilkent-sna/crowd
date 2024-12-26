Crowd's Models
==============

In the current version of Crowd (v0.9), we provide two base classes of network, **Network**, and **CustomSimNetwork**, as well as two extensions of them: 
**DiffusionNetwork** and **EdgeSimNetwork**. 

**Note:** More information regarding Network and EdgeSimNetwork will be added soon. For now, please prefer CustomSimNetwork and DiffusionNetwork, supported by the UI and explained in detail in all examples.

**1. Network class**

The base Network class of Crowd is useful for researchers who want to implement all low-level details of the simulation, such as the selection of nodes for action and execution of
a simulation. It is possible to define a simulation by creating model and agent classes, similar to Mesa and Mason, with this Network type. 

The source file where these definitions reside, the name and some parameters for node type (agent) classes, as well as the methods to call are listed in a YAML file.

**2. EdgeSimNetwork class**

We extend the Network class for a use case of edgebased simulation where we add links to the network in every iteration of the simulation, depending on the update method
provided by the user for the selection. We save the new links in JSON format for further analysis and visualization. This EdgeSimNetwork illustrates the extensible nature of Crowd
and how data savers and visualizers can be utilized in custom networks created by the modelers.


**3. CustomSimNetwork class**

CustomSimNetwork provides notably more functionalities compared to previous types while not requiring the modeler to implement any extensions of other classes.  This class:

- handles the addition of network, node, and edge parameters, 
- counts node types and the change in each iteration to save to a file in each snapshot,
- holds and runs user-defined methods before an iteration, after an iteration, and after a simulation. 

The details regarding user-defined methods are given in the next step.

**4. DiffusionNetwork class**

Crowd facilitates simplified diffusion simulations where the simulation logic is defined in the configuration file using the compartment structure from NDLib.
This allows NDLib to provide all functionalities related to the diffusion, while the modeler needs to only write methods for data collection purposes. 

This is provided by using DiffusionNetwork, an extension of the CustomSimNetwork class, hence extending all its functionalities, except agent methods, as we
leave the iteration logic to the execution of compartment-based rules.


**Next:** Step 3: Define custom methods