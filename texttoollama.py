import ollama

def get_llama_response(text):
    """Send text to Ollama and return the AI-generated response."""
    client = ollama.Client(host="http://localhost:11434")
    response = client.chat(model="llama3.2", messages=[{"role": "user", "content": text}])
    return response["message"]  # Return Ollama's response

# Only run this if the script is executed directly
if __name__ == "__main__":
    example_text = "Hello, how are you?"
    print(get_llama_response(example_text))
