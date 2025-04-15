Step 5: Import and initialize the LLM
=====================================

This step can be adjusted with respect to the model and settings you prefer to use. Note that for this type of simulations where we ask 
the model for an answer instead of text completion, it is recommended to use instruct models which are fine tuned to reply to queries. 
Some models may already have that despite not having "instruct" in their name. It is important to confirm this to get meaningful results 
as answers for the scenario you wish to simulate. 

In this scenario, we only want "Yes/No" as the response and a sentence of reasoning for this response from the LLM. If the model does not
provide the answer in the format we need, all node's locations will be set as "grid" by default, which will not be any different from a regular
SIR simulation.  

.. code-block:: python

    model_name = "mistralai/Mistral-7B-Instruct-v0.3"

    # Load the tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    # Define configuration for 8-bit quantization
    bnb_config = BitsAndBytesConfig(
        load_in_8bit_fp32_cpu_offload=True
    )

    # Load the model with quantization and a manual device map
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,  # Use quantization for 8-bit loading
        device_map="auto"  # Automatically allocate layers to devices
    )

    # Set the EOS token for both the tokenizer and the model
    tokenizer.pad_token = tokenizer.eos_token
    model.config.pad_token_id = tokenizer.eos_token_id

    # Now you can proceed with using the model for inference

**Next:** Step 6: Define the helper methods