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