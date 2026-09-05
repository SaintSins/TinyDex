from functions.get_files_info import get_files_info
from openai.types.chat import ChatCompletionToolUnionParam

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

#List of available schemas
tools: list[ChatCompletionToolUnionParam] = [schema_get_files_info]