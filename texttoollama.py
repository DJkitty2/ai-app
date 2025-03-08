import ollama
import os
import json

# Conversation history to maintain context (limit to 20 messages for memory control)
conversation_history = []
MAX_HISTORY = 20

# File to store conversation history
HISTORY_FILE = "conversation_history.json"

# Load previous conversation history if available
def load_conversation_history():
    global conversation_history
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            conversation_history = json.load(file)

# Save the last 5 exchanges
def save_conversation_history():
    with open(HISTORY_FILE, "w") as file:
        json.dump(conversation_history[-10:], file, indent=4)  # Save last 5 questions + 5 responses

# Add a system prompt for guidance
def get_llama_response(text, system_prompt=None):
    """Send text to Ollama and return the AI-generated response."""
    global conversation_history

    # Load previous history on startup
    if not conversation_history:
        load_conversation_history()

    # Use provided system prompt or default to environment variable
    system_prompt = system_prompt or os.getenv("OLLAMA_SYSTEM_PROMPT", "You are a helpful assistant.")

    # Add system prompt if starting fresh
    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt})

    # Append user message to history
    conversation_history.append({"role": "user", "content": text})

    # Trim conversation history to prevent excessive memory usage
    if len(conversation_history) > MAX_HISTORY:
        conversation_history = [conversation_history[0]] + conversation_history[-(MAX_HISTORY-1):]

    # Send conversation history to Ollama
    client = ollama.Client(host="http://localhost:11434")
    response = client.chat(model="deepseek-r1:14b", messages=conversation_history)

    # Extract and append AI response to maintain context
    response_text = response["message"]["content"]
    conversation_history.append({"role": "assistant", "content": response_text})

    # Save updated conversation history
    save_conversation_history()

    return response_text

# Only run this if the script is executed directly
if __name__ == "__main__":
    example_text = "Hello, how are you?"
    print(get_llama_response(example_text))
