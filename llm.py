from ollama import ChatResponse, chat
import ollama
import pyautogui

def type_text(text):
    pyautogui.write(text, 1)
    return "text written"

def add_two_numbers(a: int, b: int) -> int:
  """
  Add two numbers

  Args:
    a (int): The first number
    b (int): The second number

  Returns:
    int: The sum of the two numbers
  """

  # The cast is necessary as returned tool call arguments don't always conform exactly to schema
  # E.g. this would prevent "what is 30 + 12" to produce '3012' instead of 42
  return int(a) + int(b)


def subtract_two_numbers(a: int, b: int) -> int:
  """
  Subtract two numbers
  """

  # The cast is necessary as returned tool call arguments don't always conform exactly to schema
  return int(a) - int(b)


# Tools can still be manually defined and passed into chat
subtract_two_numbers_tool = {
  'type': 'function',
  'function': {
    'name': 'subtract_two_numbers',
    'description': 'Subtract two numbers',
    'parameters': {
      'type': 'object',
      'required': ['a', 'b'],
      'properties': {
        'a': {'type': 'integer', 'description': 'The first number'},
        'b': {'type': 'integer', 'description': 'The second number'},
      },
    },
  },
}

type_text_tool = {
    "name": "type_text",
    "description": "Types the specified text on the user's keyboard.",
    "parameters": {
        "type": "object",
        "properties": {
            "text": {
                "type": "string",
                "description": "The text to type."
            }
        },
        "required": ["text"]
    }
}

messages = [
    {
        "role": "system",
        "content": """
You can use the following tools:
- add_two_numbers: adds two numbers.
- subtract_two_numbers: subtracts two numbers.
- type_text: types text on the user's keyboard.

When using a tool, reply with a tool call and arguments.
"""
    },
    {'role': 'user', 'content': 'can you use the text typing tool to type hello world?'}
]
print('Prompt:', messages[0]['content'])

available_functions = {
  'add_two_numbers': add_two_numbers,
  'subtract_two_numbers': subtract_two_numbers,
  'type_text': type_text,
}

client = ollama.Client(host="http://192.168.0.147:11434")
response = client.chat(
  'llama3.1',
  messages=messages,
  tools=[add_two_numbers, subtract_two_numbers_tool, type_text_tool],
)

if response.message.tool_calls:
  # There may be multiple tool calls in the response
  for tool in response.message.tool_calls:
    # Ensure the function is available, and then call it
    if function_to_call := available_functions.get(tool.function.name):
      print('Calling function:', tool.function.name)
      print('Arguments:', tool.function.arguments)
      output = function_to_call(**tool.function.arguments)
      print('Function output:', output)
    else:
      print('Function', tool.function.name, 'not found')

# Only needed to chat with the model using the tool call results
if response.message.tool_calls:
  # Add the function response to messages for the model to use
  messages.append(response.message)
  messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

  # Get final response from model with function outputs
  final_response = client.chat('llama3.1', messages=messages)
  print('Final response:', final_response.message.content)

else:
  print('No tool calls returned from model')