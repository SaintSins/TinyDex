import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse

# Loads .env
load_dotenv()
api_key = os.environ.get('OPENROUTER_API_KEY')
if api_key is None:
    raise RuntimeError('API Key is missing')

#Initialize the CLI parser and define its description
parser = argparse.ArgumentParser(description='TinyDex')
parser.add_argument('user_prompt', type=str, help='User prompt') #Define required positional argument
args = parser.parse_args() #Processes CLI input and packages them into 'args' obj
prompt = args.user_prompt #Access the input via its attribute name

#Creates a client obj
client = OpenAI(
    base_url='https://openrouter.ai/api/v1',
    api_key=api_key,
)

#Creates a response obj
response = client.chat.completions.create(
    model="openrouter/free",
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
)

#Checks for usage property in response obj and returns prompt_tokens and completion_tokens
if response.usage is None:
    raise RuntimeError("Failed to fetch response.usage")
print(f'Prompt tokens: {response.usage.prompt_tokens}\nResponse tokens: {response.usage.completion_tokens}')

#Prints the exact answer to prompt
print(response.choices[0].message.content)

def main():
    pass

if __name__ == "__main__":
    main()
