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
        return f'''{base_prompt} You are a strict grammar and spelling correction tool.
        
        TASK:
        - Correct all grammar, spelling, and punctuation errors.
        - Maintain the original meaning and intent exactly.
        - DO NOT provide explanations, headers, or notes.
        - DO NOT be conversational.
        - OUTPUT ONLY THE CORRECTED TEXT.'''

    elif app_mode == "Creative Generation":
        return f'''{base_prompt} Generate creative content based on the following prompt. 
        Length target: {output_length}. 
        Style/Tone: {current_tone}.'''
    
    return base_prompt

def stream_llm_response(user_content, system_prompt, model="llama3.2"):
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
            if 'message' in chunk and 'content' in chunk['message']:
                yield chunk['message']['content']
    except Exception as e:
        yield f"⚠️ Error: {str(e)}. (Model: {model})"
