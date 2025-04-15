Step 6: Define the helper methods
=================================

In the current version of Crowd, when we provide a list of options for categorical node parameters and one is chosen for node x, it is not deleted from the options for node y. 
In the context of agent names in this scenario, we prefer the names to be unique. Hence, we do not provide a list of names but use a custom method instead. This is planned to be added
to Crowd in the next versions. 

For this task, we use the *generate-names* method from the original study: 

.. code-block:: python

    # generate_names method directly taken from: GABM-Epidemic
    # https://github.com/bear96/GABM-Epidemic/blob/main/utils.py#L18

    def generate_names(n: int, s: int, country_alpha2='US'):
        '''
        Returns random names as names for agents from top names in the USA
        Used in World.init to initialize agents
        '''

        # This function will randomly selct n names (n/2 male and n/2 female) without
        # replacement from the s most popular names in the country defined by country_alpha2
        if n % 2 == 1:
            n += 1
        if s % 2 == 1:
            s += 1

        nd = NameDataset()
        male_names = nd.get_top_names(s//2, 'Male', country_alpha2)[country_alpha2]['M']
        female_names = nd.get_top_names(s//2, 'Female', country_alpha2)[country_alpha2]['F']
        if s < n:
            raise ValueError(f"Cannot generate {n} unique names from a list of {s} names.")
        # generate names without repetition
        names = random.sample(male_names, k=n//2) + random.sample(female_names, k=n//2)
        del male_names
        del female_names
        random.shuffle(names)
        return names


We call this method in *add_name_parameter*, which will give the selected names to graph's nodes in order:

.. code-block:: python

    def add_name_parameter(graph):
        names = generate_names(100, 200)
        attr = {}
        for n in graph.nodes():
            selected_name = random.choice(names)
            attr.update({n: {"name": selected_name}})
            names.remove(selected_name)

        nx.set_node_attributes(graph, attr)

By calling this *add_name_parameter* method, we conclude the initialization stage of our experiment:

.. code-block:: python

    add_name_parameter(my_project.netw.G)


In the introduction, we have explained how to define methods which will be executed at the chosen intervals. In the following code, we create lists denoting them for this case:

.. code-block:: python

    before_iteration_methods = [[decide_location, model, tokenizer]]
    after_iteration_methods = [
            compute_num_at_home, 
            compute_num_on_grid, 
            day_infected_is_4, 
            early_stopping_check
        ]
    after_simulation_methods = []

We will now define each of these methods. Note that in the code, the method definitions should be placed above these lists.

In the beginning of each iteration/day, agents decide to stay home or go out. Hence, it should be passed as a *before-iteration* method in Crowd.
See `this link <https://crowd.readthedocs.io/en/latest/introduction/custom_methods.html>`_ for more information regarding the user-defined method execution times in Crowd.

We pass this method as a small list on its own, which allows us to pass the parameters for *decide_location* this way. If we don't pass the model
and tokenizers initialized in this file, the simulation executor of Crowd will not have access to them and they cannot be called during the simulation.

.. code-block:: python

    # For each node/person/agent decide if staying home or not
    def decide_location(network, model, tokenizer):
        for n in network.G.nodes:
        response = ask_agent_stay_at_home(network, n, model, tokenizer)
        
        # Update agent's location wrt the response
        if response is True:
            network.G.nodes[n]['location'] = "home"
        else:
            network.G.nodes[n]['location'] = "grid"

*decide_location* calls another function, *ask_agent_stay_at_home*, which itself will call other helper functions. 
This structure is allowed not only in Crowd's library version, but also in the Method Lab of Crowd's GUI. 

.. code-block:: python

    # Used in decide_location method.
    # Returns True or False depending on whether agent wants to stay at home
    def ask_agent_stay_at_home(network, curr_node, model, tokenizer):

        reasoning, response = get_response_and_reasoning(network, curr_node, model, tokenizer)

        if reasoning is None:
            reasoning = f"{curr_node} did not give a reason."
            print("Reasoning was none-type.")

        response = response.lower()
        if "no" in response:
            return False
        elif "yes" in response:
            return True
        else:
            print(f"Response was something unexpected. Defaulting with assuming agent decided to not stay at home.\nResponse was '{response}'")
            return False

In the following method, we create the prompt by filling in the appropriate values for each node by accessing its node parameters. Here, we also use a method called *day_infected_is_4*, which gives
the number of nodes which are on their fourth day of infection. The definition of this method is given later in the example. 

By giving the percentage of infected people in the city, we allow the LLM to factor this into its decision. 

The prompt is placed into the instruction tag, beginning with "[INST]" and ending with "[\\INST]". We also include the format which we want the LLM to respond. 
If this is not provided, it is hard to get a direct and concise answer from the model. This prompt should also be adjusted to the needs of each simulation and LLM utilized. 

If the query to LLM fails, we retry after 10 seconds. 

Moreover, we parse the output sent by the LLM to extract the reasoning and response provided. We save these for all the nodes by calling the *save_current_agent_response* method. 
This allows the inspection of the answers provided by the LLM after the simulation. It is important for both modeling and analysis stages of a simulation. 

In the modeling stage, we evaluate these answers to determine their success at making a logical decision depending on the city's case numbers and personality traits. 
If the responses of LLM are not as expected, both the model settings (such as temperature) and prompt can be adjusted.

In the analysis stages, an example use can be to find connections between the agent's decisions and their personality traits. 

.. code-block:: python

    # Generate prompt accordingly and call the Generative AI model
    def get_response_and_reasoning(network, curr_node, model, tokenizer):
        
        name = network.G.nodes[curr_node]['name']

        question_prompt = f"""[INST]
            You are {name}. You are {network.G.nodes[curr_node]['age']} years old.

            Your traits are given below:
            {network.G.nodes[curr_node]['agreeableness']}
            {network.G.nodes[curr_node]['conscientiousness']}
            {network.G.nodes[curr_node]['surgency']}
            {network.G.nodes[curr_node]['emotional-stability']}
            {network.G.nodes[curr_node]['intellect']}

            Your basic bio is below:
            {name} lives in the town of Dewberry Hollow. {name} likes the town and has friends who also live there. {name} has a job and goes to the office for work everyday.

            I will provide {name}'s relevant memories here:
            {get_health_string(network, curr_node, name)}
            {name} knows about the Catasat virus spreading across the country. It is an infectious disease that spreads from human to human contact via an airborne virus. The deadliness of the virus is unknown. Scientists are warning about a potential epidemic.
            {name} checks the newspaper and finds that {(day_infected_is_4(network)*100)/network.G.number_of_nodes(): .1f}% of Dewberry Hollow's population caught new infections of the Catasat virus yesterday.
            {name} goes to work to earn money to support {name}'s self.

            Based on the provided memories, should {name} stay at home for the entire day? Please provide your reasoning.

            The format should be as follow:
            Reasoning: [explanation]
            Response: [Yes or No]

            Example response format:

            Reasoning: {name} is tired.
            Response: Yes

            It is important to provide Response in a single word. Pick either Yes or No, both not accepted.
            There should be 1 reasoning and 1 response section. If multiple reasonings exist, combine them into one.[/INST].
            """

        try:
            output = get_completion_from_messages(model = model,
                                                tokenizer = tokenizer,
                                                user_prompt = question_prompt)
        except Exception as e:
            print(f"{e}\nProgram paused. Retrying after 10s...")
            time.sleep(10)
            output = get_completion_from_messages(model = model,
                                                tokenizer = tokenizer,
                                                user_prompt = question_prompt)

        reasoning = ""
        response = ""
        try:
            # Split the string into parts using '\n' as the separator
            parts = output.split('\n')
           
            # Initialize variables to store the extracted values
            reasoning = ""
            response = ""

            # Loop through the parts and assign values to the variables
            for part in parts:
                if part.startswith("Reasoning:"):
                    reasoning = part[len("Reasoning: "):].strip()
                elif part.strip().startswith("Response:"):
                    response = part.strip()[len("Response: "):].strip()
                    # Remove the period at the end of response if it exists
                    if response.endswith('.'):
                        response = response[:-1]

            save_current_agent_response(curr_node, question_prompt, output, reasoning, response)
        except:
            print("Reasoning or response were not parsed correctly.")
            response = "No"
            reasoning = None
        return reasoning, response

    def get_health_string(network, curr_node, name):
        health_strings = [f"{name} feels normal.",
                            f"{name} has a light cough.",
                            f"{name} has a fever and a cough.",
                            ]

        node_state = network.G.nodes[curr_node]["node"]

        day_infected = 0

        if 'healing' in network.G.nodes[curr_node]:
            remaining_days = network.G.nodes[curr_node]['healing']
            day_infected = 6 - remaining_days

        if node_state == 0 or node_state == 2 or day_infected < 2:
            return health_strings[0]

        if day_infected == 3 or day_infected == 6:
            return health_strings[1]

        if day_infected == 4 or day_infected == 5:
            return health_strings[2]

    # Define a function to generate response using Hugging Face model
    def get_completion_from_messages(model, tokenizer, user_prompt, max_tokens=200, temperature=0.1):
        try:
            # Tokenize the input with padding
            inputs = tokenizer(user_prompt, return_tensors="pt", padding=True, truncation=True).to("cuda")

            # Generate text with attention mask and padding token set
            outputs = model.generate(
                inputs.input_ids,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=True,
                attention_mask=inputs["attention_mask"],
                pad_token_id= tokenizer.eos_token_id,  # Ensure the padding is handled
            )

            # Remove the input part from the output
            outputs = outputs[:, inputs.input_ids.shape[-1]:]

            # Decode the generated tokens to return the text
            return tokenizer.decode(outputs[0], skip_special_tokens=True)

        except Exception as e:
            print(f"Error generating text: {e}")
            return None

The following function uses Crowd's `file egress method save_statusdelta <https://github.com/bilkent-sna/crowd/blob/master/crowd/crowd/egress/file_egress.py#L22>`_ to write the response of current node to a file named *individual_agents_response.json*.
This function works as follows:

.. code-block:: python
    
    def save_statusdelta(self, epoch_num, data_dict, file_name, available_status):
        """
            Takes 4 parameters:
            1. epoch_num (current epoch number): If given (i.e. not None), this will be added to the 
                data_dict and written to file
            2. data_dict: The dictionary which holds the information we want to save
            3. file_name: Name of the JSON file
            4. available_status: Since this method is originally to save the number of nodes in each 
                iteration, it takes available node status and formats the data accordingly. If it is 
                None, no changes will be made to data dict.
            This method is preferred for cases where we write data to the end of a file without deleting
                or loading the previous content. The new content is just appended.
        """

[The code above is added for demonstration purposes. Do not add this function to your simulation. It is already in Crowd library.]

In our case, we want to save the current agent's response at the end of previous queries, so we prefer this method. 
Note that if we return the *simulation_data* dictionary, this will be automatically written to a file by Crowd. However, the 
data written this way are saved to a dictionary and written to a file at the end of the simulation. As we are making many queries
and they take a lot of space, it is unnecessary to keep them in the memory for the whole duration of the simulation. 
Hence, utilizing this method allows us to save some memory. 

We can access this *save_statusdelta* method through the *egress* object created in our Project instance. Since we have
created our project in the same file, we can access it directly. 

.. code-block:: python

    def save_current_agent_response(curr_node, question_prompt, output, reasoning, response):
        simulation_data = {
            "Node": curr_node,
            "Prompt": question_prompt,
            "Output": output,
            "Reasoning": reasoning,
            "Response": response
        }

        if my_project.egress is not None:
            try:
                my_project.egress.save_statusdelta(None, simulation_data, 'individual_agents_response.json', None)
            except Exception as e:
                print("Error occured", e.with_traceback)
        else:
            print("Egress is none, can't save current agent response.")


All of the methods we explained in this section are designed to be called before the execution of the infection logic. 
After that stage, we call the *after-iteration* methods, which we utilize for data collection and early stopping purposes. 

The data collection methods are defined as:

.. code-block:: python 

    def compute_num_on_grid(network):
        return sum([1 for n in network.G.nodes if network.G.nodes[n]['location'] == 'grid'])

    def compute_num_at_home(network):
        return sum([1 for n in network.G.nodes if network.G.nodes[n]['location'] == 'home'])

    def day_infected_is_4(network):
        # A temporary list which we will append True if it is the 4th day of being infected for the person
        # False otherwise
        is_day_4 = []

        for n in network.G.nodes:
            if 'healing' in network.G.nodes[n]:
                remaining_days = network.G.nodes[n]['healing']
                infected_days = 6 - remaining_days
                if infected_days == 4:
                    is_day_4.append(True)
                else:
                    is_day_4.append(False)
            else:
                is_day_4.append(False)

        # Total number of people who are infected at day 4 will be written to file
        return sum(is_day_4)

When there are no infected agents left, there will be no new infections in the city. 
Therefore, we do not need to continue the simulation. In this scenario, we wish to 
stop the simulation when there are no infected agents for two consecutive days. 

To implement this logic, we create a method named *early_stopping_check*, which will
be called after the simulation logic is completed in every iteration (i.e. *after-iteration method*). 

The number of nodes of each node type are saved automatically in Crowd, to a file named *count_node_types*. 
In the code below, we read the contents of this file. If there are more than 2 iterations, we can check for 
early stopping. We get the last two days' data. If they both have 0 infected nodes, we set *network*'s *early_stop*
variable as True. 

This variable is available in both CustomSimNetwork and DiffusionNetwork types. It is set to False by default, 
and the simulation keeps being executed until this variable is True or we reach the number of iterations 
input by the user. 

.. code-block:: python

    # If there are no infected agents for two consecutive days, stop the simulation
    def early_stopping_check(network):
        # Define the path to the JSON file containing node type counts
        path = os.path.join(network.egress.artifact_path, 'parameters', 'count_node_types.json')

        # Read the JSON data
        with open(path, 'r') as file:
            data = json.load(file)

        # Ensure there are at least 2 iterations to check
        if len(data) < 2:
            return  # Not enough data to check early stopping

        # Get the last two days' data
        last_two_days = data[-2:]

        # Check the "Infected" count for the last two days
        infected_last_day = last_two_days[1]['Infected']
        infected_second_last_day = last_two_days[0]['Infected']

        # If infected count is 0 for both days, stop the simulation
        if infected_last_day == 0 and infected_second_last_day == 0:
            network.early_stop = True

**Next:** Steps 7-8: Run the simulation and analyze the results