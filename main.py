import os
import argparse
import json

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from tools import tools


def main() -> None:

    # Loads .env
    load_dotenv()
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if api_key is None:
        raise RuntimeError('API Key is missing')

    #Initialize the CLI parser and define its description
    parser = argparse.ArgumentParser(description='TinyDex')
    parser.add_argument('user_prompt', type=str, help='User prompt') #Define required positional argument
    parser.add_argument('--verbose', action='store_true', help='Enable verbose ouput') #Define optional argument; store_true will parse this as boolean value of True if flag is set otherwise False
    args = parser.parse_args() #Processes CLI input and packages them into 'args' obj
    prompt = args.user_prompt #Access the input via its attribute name
    verbose = args.verbose #Access the boolean value via its attribute name

    #Creates a client obj
    client = OpenAI(
        base_url='https://openrouter.ai/api/v1',
        api_key=api_key,
    )

    #List of messages with role and content to build a conversation history
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}]

    #Calls function to generate the response by passing the messages, client obj, verbose flag
    generate_content(client, messages, verbose)

#Function to generate the response
def generate_content(client:OpenAI, messages: list, verbose:bool = False) -> None:
    #Creates a response obj
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=tools,
        )
    #Checks the flag for enabling verbose output
    if verbose:
        #Checks for usage property in response obj
        if response.usage is None:
            raise RuntimeError("Failed to fetch response.usage")
        print(f'User prompt: {messages[0]["content"]}\nPrompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}') #Prints user_prompt, prompt_token and completion_token

    #Extracts the message obj from returned response
    response_message = response.choices[0].message

    # Check if the model decided to execute tools or reply directly
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.type == "function":
                function_args = json.loads(tool_call.function.arguments or "{}")
                print(f"Calling function: {tool_call.function.name}({function_args})")
    else:
        print(response_message.content)
    


if __name__ == "__main__":
    main()
