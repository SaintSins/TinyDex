import os
from config import MAX_CHARS

def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        #Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        #Get absolute path of file
        file_path_abs = os.path.normpath(
            os.path.join(working_dir_abs, file_path)
        )

        #Checks if file_path falls within working directory
        if (
            os.path.commonpath([working_dir_abs, file_path_abs])
            != working_dir_abs
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        #Checks if file_path is file or not
        if not os.path.isfile(file_path_abs):
            return (
                f'Error: File not found or is not a regular file: "{file_path}"'
            )

        #Read the file and return its contents as a string
        with open(file_path_abs, "r", encoding="utf-8") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return content

    except Exception as e:
        return f'Error reading file "{file_path}": {e}'