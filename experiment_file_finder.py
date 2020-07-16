import os
from typing import Union

def file_finder(directory: str, file_extension: Union[str, tuple] = "") -> list:
    """Generate a list containing both the name and path of each file with the specified extension in the directory.

    Parameters
    ----------
    directory : str
        Directory where you want to get the files.
    file_extension : Union[str, tuple], optional
        The file extension or extensions you want to include in your list, by default "" (includes all files)

    Returns
    -------
    file_names: list
        List containing both the name and the path of each file in the specified directory.
    """

    file_names = []
    for file_name in os.listdir(directory):
        if file_name.endswith(file_extension):
            file_path = os.path.join(directory, file_name)
            file_names.append([file_name, file_path])

    return file_names

print(file_finder("test files"))