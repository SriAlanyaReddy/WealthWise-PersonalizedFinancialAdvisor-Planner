from langchain_community.llms import CTransformers

def ask_llama(query: str):
    """
    Generate an answer using the Llama model.
    """
    try:
        # Load the model (replace with the path to your .bin file)
        model_path = "model/llama-2-7b-chat.ggmlv3.q8_0.bin"
        llm = CTransformers(
            model=model_path,
            model_type="llama",  # Specify the model type
            max_new_tokens=256,  # Adjust as per your requirements
        )

        # Generate the response
        response = llm(query)
        print("Query:", query)
        print("Response:", response)

    except Exception as e:
        print(f"Error during generation: {e}")

# Provide your query here
query = "What is the capital of France?"
ask_llama(query)
