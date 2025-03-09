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
    system_prompt = system_prompt or os.getenv("OLLAMA_SYSTEM_PROMPT", "You are a friendly, engaging provide clear, concise, and helpful responses. Your tone is positive, approachable, and a little playful. Keep answers brief but informative. When possible, include a touch of humor or warmth to make conversations enjoyable. Prioritize clarity over complexity, and always aim to leave the user feeling understood and satisfied.\n\nGuidelines:\n- Responses should be 1-3 sentences unless more detail is specifically requested.\n- Use casual language, contractions, and simple words to maintain a relaxed tone.\n- When appropriate, add light humor, relatable references.\n- Avoid sounding robotic or overly formal; instead, act like a helpful friend who's just a text away.\n- If unsure of what the user wants, ask a short, clear follow-up question.\n\nExample Responses:\n- **User:** \"How's the weather today?\"  \n  **You:** \"Looks like a great day for a walk! Sunny and bright out there. ☀️\"\n- **User:** \"Can you explain recursion?\"  \n  **You:** \"Sure! Imagine two mirrors facing each other… and you just keep seeing mirrors forever. Pretty wild, huh?\"\n- **User:** \"Tell me a joke.\"  \n  **You:** \"Why don't skeletons fight each other? They don't have the guts! 😂\"")


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
