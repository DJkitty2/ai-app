import ollama
import base64

with open("B:/pictures/IMG_7203(1).jpg", "rb") as f:
    image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')

# Send to a vision-capable model
client = ollama.Client(host=f"http://localhost:11434/")
response = client.chat(
    model='gemma3:12b',
    messages=[
        {
            'role': 'user',
            'content': 'What is in this image?',
            'images': [image_b64]
        }
    ]
)

print(response['message']['content'])
