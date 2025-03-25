from ollama import ChatResponse, chat
import os

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

def get_os():
    return {"os_name": os.name}

available_functions = {
    'add_two_numbers': add_two_numbers,
    'subtract_two_numbers': subtract_two_numbers,
    'get_os': get_os,
}

def get_llama_response(messages):
    response: ChatResponse = chat(
        'qwen2.5:3b',
        messages=messages,
        tools=[add_two_numbers, subtract_two_numbers, get_os],
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

        # Add the function response to messages for the model to use
        messages.append(response.message)
        messages.append({'role': 'tool', 'content': str(output), 'name': tool.function.name})

        # Get final response from model with function outputs
        final_response = chat('qwen2.5:3b', messages=messages)
        print('Final response:', final_response.message.content)

    else:
        print('No tool calls returned from model')


if __name__ == "__main__":
    messages = [{'role': 'user', 'content': 'What is my os?'}]
    print('Prompt:', messages[0]['content'])
    get_llama_response(messages)
