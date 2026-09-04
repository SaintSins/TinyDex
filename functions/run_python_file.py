import os
import subprocess

def run_python_file( working_directory: str, file_path: str, args: list[str] | None = None) -> str:

    try:
        #Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        #Get absolute path of file
        file_path_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

         #Checks if file_path falls within working directory
        if os.path.commonpath([working_dir_abs, file_path_abs]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        #Checks if file_path is file or not
        if not os.path.isfile(file_path_abs):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        #Checks if file_path is a python file or not
        if not file_path_abs.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        #Command to run the file
        command = ["python", file_path_abs]

        #Checks additional args and add it to command list
        if args:
            command.extend(args)

        #Subprocess to run the the file
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        #Output string
        output: list[str] = []
        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")
        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"