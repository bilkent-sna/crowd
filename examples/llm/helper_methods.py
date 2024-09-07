
import time


def decide_location(network, model):
    # For each node/person/agent decide if staying home or not
    # In the original implementation, it was called for each agent separately in their prepare_step function
    # We don't allow such structure, but this implementation basically does the same thing
    for n in network.G.nodes:
        response = ask_agent_stay_at_home(network, n, model)

        # Update agent's location wrt the response
        if response is True:
            network.G.nodes[n]['location'] = "home"
        else:
            network.G.nodes[n]['location'] = "grid"
    
    

def get_health_string(network, curr_node):
    # Instead of node's name, we have node's id for now
    health_strings = [f"{curr_node} feels normal.",
                        f"{curr_node} has a light cough.",
                        f"{curr_node} has a fever and a cough.",
                        ]
    
    node_state = network.G.nodes[curr_node]["node"]

    day_infected = 0

    if 'healing' in network.G.nodes[curr_node]:
        remaining_days = network.G.nodes[curr_node]['healing'] 
        day_infected = 6 - remaining_days

    if node_state == "Susceptible" or node_state == "Recovered" or day_infected < 2:
        return health_strings[0]
    
    if day_infected == 3 or day_infected == 6:
        return health_strings[1]
    
    if day_infected == 4 or day_infected == 5:
        return health_strings[2]
   
def ask_agent_stay_at_home(network, curr_node, model):
    #Used in decide_location method.
    # Returns True or False depending on whether agent wants to stay at home

    reasoning, response = get_response_and_reasoning(network, curr_node, model)
    # save_current_agent_response(curr_node, reasoning, response)

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


def get_response_and_reasoning(network, curr_node, model):
    # Generate propmt accordingly and call the Generative AI model

    question_prompt = f"""[INST]
        You are {curr_node}. You are {network.G.nodes[curr_node]['age']} years old. 
       
        Your traits are given below:
        {network.G.nodes[curr_node]['agreeableness']}
        {network.G.nodes[curr_node]['conscientiousness']}
        {network.G.nodes[curr_node]['surgency']}
        {network.G.nodes[curr_node]['emotional-stability']}
        {network.G.nodes[curr_node]['intellect']}
        
        Your basic bio is below:
        {curr_node} lives in the town of Dewberry Hollow. {curr_node} likes the town and has friends who also live there. {curr_node} has a job and goes to the office for work everyday.
        
        I will provide {curr_node}'s relevant memories here:
        {get_health_string(network, curr_node)}
        {curr_node} knows about the Catasat virus spreading across the country. It is an infectious disease that spreads from human to human contact via an airborne virus. The deadliness of the virus is unknown. Scientists are warning about a potential epidemic.
        {curr_node} checks the newspaper and finds that {(day_infected_is_4(network)*100)/network.G.number_of_nodes(): .1f}% of Dewberry Hollow's population caught new infections of the Catasat virus yesterday.
        {curr_node} goes to work to earn money to support {curr_node}'s self.
       
        Based on the provided memories, should {curr_node} stay at home for the entire day? Please provide your reasoning.

        
        The format should be as follow:
        Reasoning: [explanation]
        Response: [Yes or No]

        Example response format:

        Reasoning: {curr_node} is tired.
        Response: Yes

        It is important to provide Response in a single word. Pick either Yes or No, both not accepted. 
        There should be 1 reasoning and 1 response section. If multiple reasonings exist, combine them into one.[/INST].
        """
    
    try:
        print("Prompt:" , question_prompt)
        output = get_completion_from_messages(model, question_prompt, temperature=0)
        print("Output for node", curr_node, ":", output)
    except Exception as e:
        print(f"{e}\nProgram paused. Retrying after 10s...")
        time.sleep(10)
        output = get_completion_from_messages(model, question_prompt, temperature=0)

    reasoning = ""
    response = ""
    try:
        # intermediate  = output.split("Reasoning:",1)[1]
        # reasoning, response = intermediate.split("Response:")
        # response = response.strip().split(".",1)[0]
        # reasoning = reasoning.strip()
        # Split the string into parts using '\n' as the separator
        parts = output.split('\n')
        print("parts:", parts)
        # Initialize variables to store the extracted values
        reasoning = ""
        response = ""

        # Loop through the parts and assign values to the variables
        for part in parts:
            if part.startswith("Reasoning:"):
                reasoning = part[len("Reasoning: "):].strip()
            elif part.strip().startswith("Response:"):
                print("response part:", part)
                response = part.strip()[len("Response: "):].strip()
                # Remove the period at the end of response if it exists
                if response.endswith('.'):
                    response = response[:-1]


        # # Print the extracted values
        # print("Reasoning:", reasoning)
        # print("Response:", response)
        # 
        # print(reasoning, response)
        save_current_agent_response(curr_node, question_prompt, output, reasoning, response)
    except:
        print("Reasoning or response were not parsed correctly.")
        response = "No"
        reasoning = None
    return reasoning, response

def save_current_agent_response(curr_node, question_prompt, output, reasoning, response):
    print("Inside save 1")
    # Iteration data dictionary
    simulation_data = {
        "save_current_agent_response": {
            "Node": curr_node,
            "Prompt": question_prompt,
            "Output": output,
            "Reasoning": reasoning,
            "Response": response
        }
    }
    print("Inside save2")
    if my_project.digress is not None:
        print("Inside save not none")
        try:
            my_project.digress.save_iteration_data(simulation_data)
        except Exception as e:
            print("Error occured", e.with_traceback)
    else:
        print("Digress is none, can't save current agent response.")


def get_completion_from_messages(model, user_prompt, max_tokens=200, temperature=0.1, top_p=0.5, echo=False):
    try:
        # Define the parameters
        model_output = model(
            user_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            echo=echo,
        )
        print("Model output generated.")
        return model_output["choices"][0]["text"].strip()
    except Exception as e:
        print(f"Error generating text: {e}")
        return None

# Statistic methods
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