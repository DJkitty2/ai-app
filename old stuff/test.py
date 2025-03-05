import ollama
import customtkinter as ctk
import tkinter as tk
import threading
import customtkinter

# Set appearance and theme
ctk.set_appearance_mode("System")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# Initialize main application window
root = ctk.CTk()
root.title("Ollama Test Chat App")

# Create an entry widget
entry = ctk.CTkEntry(root, placeholder_text="Enter message here")
entry.pack(pady=20, fill=tk.X, padx=20)

# Create a frame for the text widget and scrollbar
text_frame = tk.Frame(root)
text_frame.pack(pady=20, fill=tk.BOTH, expand=True)

# Create a text widget with a scrollbar
text_widget = tk.Text(text_frame, wrap=tk.WORD, bg="gray")
text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = tk.Scrollbar(text_frame, command=text_widget.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_widget.config(yscrollcommand=scrollbar.set)

# Define a function to handle the ollama chat interaction
def call_ollama():
    A = entry.get()  # Get text from entry widget
    response = ollama.chat(model='llama3.1', messages=[
        {
            'role': 'user',
            'content': f'{A}',
        },
    ])
    print(response['message']['content'])
    text_widget.delete(1.0, tk.END)  # Clear previous content
    text_widget.insert(tk.END, response['message']['content'])  # Insert new content

# Create a button to trigger the chat
def on_button_click():
    # Use threading to avoid freezing the GUI
    thread = threading.Thread(target=call_ollama)
    thread.start()

button = ctk.CTkButton(root, text="Send", command=on_button_click)
button.pack(pady=10)

# Start the GUI loop
root.mainloop()
