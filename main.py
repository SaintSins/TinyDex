import os
import argparse
import sys

from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from tools import tools, call_function
from config import MAX_ITERS


def main() -> None:

    # Loads .env
    load_dotenv()
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if api_key is None:
        raise RuntimeError('API Key is missing')

    #Initialize the CLI parser and define its description
    parser = argparse.ArgumentParser(description='TinyDex')
    parser.add_argument('user_prompt', type=str, nargs="?", help='Optional user prompt for single tasks') #Define  optional positional argument
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
    messages = [{"role": "system", "content": system_prompt}]

    #Checks for prompt in argument if true the ReAct loop will be executed with single response
    if prompt:
        if verbose:
            print(f'User prompt: {prompt}')
        messages.append({"role": "user", "content": prompt})
        answer = run_react_cycle(client, messages, verbose)
        if answer:
            print("\nFinal Response:")
            print(answer)
        else:
            sys.exit(1)
    #Launches interactive REPL session in terminal
    else:
        run_interactive_session(client, messages, verbose)
    
#Function to generate the response
def generate_content(client:OpenAI, messages: list, verbose:bool = False) -> str | None:

    #Creates a response obj
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=tools,
            temperature=0
        )
    
    #Checks the flag for enabling verbose output
    if verbose:
        #Checks for usage property in response obj
        if response.usage is None:
            raise RuntimeError("Failed to fetch response.usage")
        print(f'Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}') #Prints user_prompt, prompt_token and completion_token

    #Extracts the message obj from returned response
    response_message = response.choices[0].message

    #After each call response_message is appened to messages list for context history
    messages.append(response_message)

    #Checks if the model decided to execute tools or reply directly
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            if tool_call.type == "function":
                result_message = call_function(tool_call, verbose)
                if not result_message.get("content"):
                    raise RuntimeError(f"Empty function response for {tool_call.function.name}")
                if verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        return None
    else:
        return response_message.content

#ReAct tool loop
def run_react_cycle (client: OpenAI, messages: list, verbose: bool = False) -> str | None:
    #Calls function to generate the response by passing the messages, client obj, verbose flag
        for iteration in range(1,MAX_ITERS+1):
            try:
                final_response = generate_content(client, messages, verbose)
                if final_response:
                    return final_response
            except Exception as e:
                print(f"Error during iteration {iteration}: {e}", file=sys.stderr)
                return None
    
        print(f"Maximum iterations ({MAX_ITERS}) reached without resolution.", file=sys.stderr)
        return None

#Interactive terminal loop
def run_interactive_session(client: OpenAI, messages: list, verbose: bool = False) -> None:
    print("\nTinyDex Interactive Session (type 'exit' or 'quit' to end)")
    print("-" * 58)

    while True:
        try:
            #Pause and wait for user input in the terminal
            user_input = input("\nYou > ").strip()
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "q"}:
                print("Ending session.")
                break

            #Append the new message to persistent memory
            messages.append({"role": "user", "content": user_input})

            #Let the ReAct engine run its tool cycles
            answer = run_react_cycle(client, messages, verbose)
            if answer:
                print(f"\nTinyDex > {answer}")

        except (KeyboardInterrupt, EOFError):
            print("\nEnding session.")
            break

if __name__ == "__main__":
    main()
