from texttoollama import get_llama_response

def get_response(username: str, user_input: str, channel: str) -> str: 
    lowered: str = user_input.lower()    
    try:
        response = get_llama_response(f"{username} said {user_input} in {channel} on discord")
        return response
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't process your request at the moment."