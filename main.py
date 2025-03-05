from voicetotext import transcribe_audio
from texttoollama import get_llama_response

# Step 1: Get transcribed text
text = transcribe_audio("audio.mp3")

# Step 2: Send it to Ollama
response = get_llama_response(text)

# Step 3: Print or use the response
print("Ollama's Response:", response)
