from openai.types.chat import ChatCompletionToolUnionParam
from collections.abc import Callable
from config import WORKING_DIR
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

import json

#Tool definition schema for get_files_info
schema_get_files_info: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}

#Tool definition schema for get_file_content
schema_get_file_content: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads and returns the text content of a specified file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to read, relative to the working directory.",
                },
            },
            "required": ["file_path"],
        },
    },
}

#Tool definition schema for write_file
schema_write_file: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes or overwrites text content to a specified file relative to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the file to write, relative to the working directory.",
                },
                "content": {
                    "type": "string",
                    "description": "The text content to write into the target file.",
                },
            },
            "required": ["file_path", "content"],
        },
    },
}

#Tool definition schema for run_python_file
schema_run_python_file: ChatCompletionToolUnionParam = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a Python script relative to the working directory with optional command-line arguments and returns the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the Python file to execute, relative to the working directory.",
                },
                "args": {
                    "type": "array",
                    "items": {
                        "type": "string",
                    },
                    "description": "Optional list of command-line arguments to pass to the Python script.",
                },
            },
            "required": ["file_path"],
        },
    },
}


#List of available schemas
tools: list[ChatCompletionToolUnionParam] = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
    ]

#Dispatch map
tool_map: dict[str, Callable[..., str]] = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

#Calls the requested function
def call_function(tool_call, verbose: bool = False) -> dict:

    #Extracts the name and argument(s) from tool_call 
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments or "{}")

    if verbose:
        print(f" - Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")

    #Fallback for failed calls
    if function_name not in tool_map:
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": f"Error: Unknown function: {function_name}",
        }

    #Injecting working directory as argument
    function_args["working_directory"] = WORKING_DIR
    result = tool_map[function_name](**function_args)

    #Payload
    return {
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": result,
    }