import os

def write_file(working_directory: str, file_path: str, content: str) -> str:

    try:
        #Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        #Get absolute path of file
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        #Checks if file_path falls within working directory
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        #Checks if file_path points to existing directory
        if os.path.isdir(file_path_abs):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        #Checks if all parent directories of file_path exists
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)

        #Opens the file_path and overwrites its contents
        with open(file_path_abs, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    
    except Exception as e:
        return f"Error: writing to file: {e}"