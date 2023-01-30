import os
import pathlib

import pandas as pd


def get_parent_dir(path: pathlib.WindowsPath) -> str:
    """returns path of parent directory"""

    root = os.getcwd().replace("\\", "/").split("/")[-1]
    if path == ".":
        # if it is the current working directory
        return root
    return (root / path).as_posix()


def get_extension(file_extensions: str) -> str:
    """returns the extension of the file"""

    return "".join([ext for ext in file_extensions])


def get_name(file_name: str) -> str:
    """returns the name without the extension"""

    if file_name.startswith(".") or file_name.find(".") == -1:  # if it is a dotfile
        return file_name
    return file_name[:file_name.find(".")]


def get_info(file: pathlib.WindowsPath) -> tuple[str, str, str]:

    file_name = get_name(file.name)
    parent_dir = get_parent_dir(file.parent)
    extension = get_extension(file.suffixes)
    return (parent_dir, file_name, extension)


if __name__ == "__main__":

    # get current working directory
    root = os.getcwd()
    glob = pathlib.Path(".").glob('**/*')
    
    
    # comment if the script needs to ignore .git folder
    glob = [path for path in glob if not any(part.startswith('.git') for part in path.parts)]
    
    files = []

    for file in glob:
        if not file.is_dir():
            files.append(
                get_info(file))

    # creating a table
    df = pd.DataFrame(files)
    # index starts from 1
    df.index += 1

    # saving to a file
    with pd.ExcelWriter("results.xlsx", engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, 'results', header=False)
