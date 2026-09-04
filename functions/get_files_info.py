import os

def get_files_info(working_directory: str, directory: str = ".") -> str:

    try:

        #Get absolute path of working directory
        working_dir_abs = os.path.abspath(working_directory)

        #Generates a full path to target directory
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        #Checks if target_dir falls within working_dir_abs
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')

        #Checks if directory argument is directory or not
        if not os.path.isdir(target_dir):
            return (f'Error: "{directory}" is not a directory')

        #Getting the files info
        files_info: list[str] = []
        for filename in os.listdir(target_dir):
            filepath = os.path.join(target_dir,filename)
            size = os.path.getsize(filepath)
            is_dir = os.path.isdir(filepath)
            files_info.append(f"- {filename}: file_size={size} bytes, is_dir={is_dir}")
        return "\n".join(files_info)

    except Exception as e:
        return(f'Error listing files: {e}')



