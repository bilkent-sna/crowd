.. crowd documentation master file, created by
   sphinx-quickstart on Thu Dec 19 14:46:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Getting Started
===================
.. Add your content using ``reStructuredText`` syntax. See the
.. `reStructuredText <https://www.sphinx-doc.org/en/master/usage/restructuredtext/index.html>`_
.. documentation for details.


**What is an agent-based social network simulation?** 

Agent-based social network simulation is a methodology commonly adopted by the computational social scientists to study how the individual entities (agents) influence the system through interactions with the other agents and the environment (network).

Examining the interaction between the agents in this structured environment provides insight into issues such as information diffusion, trust dynamics, and disease spread, which can be leveraged to prevent negative outcomes or achieve positive ones. 

In a network simulation, an agent typically represents a person, but may also represent an animal, an organization, or any other individual entity. A link between two nodes represents the existence of a relationship between two agents, and there may exist different kinds of relationships (e.g. family, coworker, or possibility of coordination between two organizations). Nodes interact with their neighbors, and the actions and state of these neighbors play a crucial role. For instance,  while modeling the spread of information in simulations, the information is carried to an agent from its neighbors.

**How does Crowd simplify conducting social network simulations?**

While various general-purpose agent-based simulators allow social network simulations, they are not designed with a focus on social networks, and the effort required to model a complex networked system increases.

For this purpose, Crowd provides:

1. 15+ network generators and commonly used networks integrated into the framework (e.g., Erdos-Renyi, Barabasi-Albert, Forest Fire models; complete graphs, Zachary's Karate Club graph)
2. Network models that:

   - Automatically collect data
   - Allow execution of user-defined Python methods in selected simulation stages
   - Minimizes the code needed to write by the modeler
3. Graphical user interface:

   - Easy to navigate structure with different simulations and projects
   - Defining simulation settings with selectors and dropdowns
   - Interactive network visualization
   - Chart generation and data aggregation with simple selections
   - Interactive line, bar, area, scatter charts
4. Access to all frameworks and libraries in Python environment, including TensorFlow, PyTorch and HuggingFace Transformers to integrate generative agents into simulations
5. Execution of simulations within Jupyter notebooks

.. toctree::
   :hidden:
   :maxdepth: 1

   installation