Step 4: Modify configuration
============================

We first enter a *name* for this simulation, to differentiate this experiment with others, followed with the *structure* section where we describe
the network as a *random regular network* with a degree of 5. This creates a network where all the nodes have a degree of 5. 

In each simulation step, agents interact with their neighbors instead of random agents. 

We utilize Crowd's Diffusion Network in this study. Since it is a predefined model, in the *definitions* section, we include the keyword *pd-model* and put
the simulation settings inside it. To select which predefined model we want to use, *name* parameter in this part should be set to *diffusion*. 

While the order of the keyword-item pairs in this section (or in any section) does not matter (since they are just dictionary/hashmaps), we will first explain the nodetypes in this example:

1. *Susceptible*: 98 nodes/agents are set as Susceptible. Both *98* as an integer or *"98"* as a string is supported as an input.
2. *Infected*: 2 nodes/agents are initially infected and will be spreading the disease to others.
3. *Recovered*: No nodes are initially in this state. After a node is healed, they will switch to this state and be immune to infection. 

In the scenario description, we have stated that the agents only take part in the diffusion process when they go out (i.e. node.location = grid). 
To facilitate this, we include a categorical node parameter named *location*. We want all the nodes to be initially on *grid*, so we only provide that
as an option, and set *location* to *home* only when the agent (with the help of LLM queries) decides to stay home.

The categorical node parameters are set randomly from the list given. Hence, the personality traits will also be determined randomly for each category from the
options given in the files. Note that the traits can also be given as a list in this section; however, as the lengths of the lists increase, separating them to
another file allows more clean and easy-to-follow YAML configuration.

Numerical node parameters take *start* and *end* values to define a range, and set that parameter for each node as a random number between that range. 
In this case, we are setting the *age* of each agent/node randomly between 18 and 65. 

To define the simulation settings of diffusion simulations, we will utilize *compartments* and *rules* in the configuration file. We will utilize 2 compartments and 2 rules for this example, which can be explained as follows:

- **c1** is a node categorical compartment, which means that the node will pass from state 1 to state 2 if the categorical condition is satisfied. 
- **r1**, which uses *c1* can be translated as: 
    - If a node’s location is grid, with 0.1 probability, Susceptible nodes will transfer to Infected.     
- When a node is infected, it takes 6 days to recover. We implement this as rule *r2*. 
- **r2** uses a count-down compartment *c2*, which holds a variable called healing for the infected agent when that person is infected (starting with the value of 6) and decreases this number every day, and the agent will go to the Recovered state when this number reaches 0.

.. code-block:: yaml

    name: gabm-epidemic-case
    structure:
        random:
            count: 100
            degree: 5
            type: random-regular
    definitions:
        pd-model:
            name: diffusion
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
            rules:
                r1:
                    - Susceptible
                    - Infected
                    - c1
                r2:
                    - Infected
                    - Recovered
                    - c2

**Next:** Step 5: Import and initialize the LLM