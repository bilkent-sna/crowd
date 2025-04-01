.. crowd documentation master file, created by
   sphinx-quickstart on Thu Dec 19 14:46:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Examples
========
.. Add your content using ``reStructuredText`` syntax. See the
.. `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
.. documentation for details.


In this section, we include examples of Crowd's usage in different scenarios, utilizing various features of the framework. 

Navigate directly to an example: 

1. `Epidemic simulation with generative agents: <generative_epidemic_agents/index.html>`_

   - Network (model) type: Diffusion Network
   - Utilizes LLM inference for agent decisions
   - Can be used as a template for any type of generative agents experiment with Crowd


2. `Influence maximization: <influence_maximization/index.html>`_

   - Network (model) type: Custom Simulation Network
   - Provides a template for basic custom simulations with Crowd
   - Can be directly used to compare different seed node selection methodologies without modifying any of this example code (more details given in the example).

3. `Networked trust game: <networked_trust_game/index.html>`_

   - Network (model) type: Custom Simulation Network
   - Provides the basis to implement N-player cooperative games with Crowd
   - Utilizes various user-implemented methods
   - Shows how to utilize batch run and model exploration functionalities of Crowd (batch run: run the simulation with the same settings, model exploration/parameter sweep: run the simulation with different settings - each combination only has one varying parameter)


As we continue to develop Crowd, more examples will be added.  

**Next:** Example 1: Epidemic simulation with generative agents

.. toctree::
   :hidden:
   :maxdepth: 2

   generative_epidemic_agents/index
   influence_maximization/index
   networked_trust_game/index
