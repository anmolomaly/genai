%%writefile llm_engine.py
import ollama

def get_system_prompt(app_mode, output_length, current_tone):
    """Generates a system prompt based on the app mode, desired output length, and tone."""
    base_prompt = f"You are a helpful AI assistant. Respond in a {current_tone} tone."

    if app_mode == "Summarization":
        if output_length == "Short":
            return f"{base_prompt} Summarize the following text concisely, aiming for 1-2 sentences."
        elif output_length == "Medium":
            return f"{base_prompt} Summarize the following text into a paragraph of 3-5 sentences."
        else: # Long
            return f"{base_prompt} Provide a detailed summary of the following text, covering all key points."

    elif app_mode == "Grammar Correction":
        return f"{base_prompt} Correct any grammar, spelling, and punctuation errors in the following text. Do not change the meaning or intent."

    elif app_mode == "Creative Generation":
        return f'''{base_prompt} Generate creative content based on the following prompt. Ensure the response matches the specified tone and is appropriate for the given output length request (though creative generation can be more flexible).
If output length is Short, aim for a few sentences. If Medium, a paragraph or two. If Long, a more detailed piece of writing.'''
    return base_prompt # Fallback

def stream_llm_response(user_content, system_prompt, model="llama3"):
    """Streams responses from the Ollama chat model."""
    try:
        response = ollama.chat(
            model=model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_content},
            ],
            stream=True
        )
        for chunk in response:
            yield chunk['message']['content']
    except Exception as e:
        yield f"Error connecting to Ollama: {str(e)}. Please ensure Ollama server is running and the model '{model}' is available."
