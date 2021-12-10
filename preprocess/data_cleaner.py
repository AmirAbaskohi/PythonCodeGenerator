import os
from curtsies.fmtfuncs import red, green, on_blue, yellow, blue, cyan

REPOS_DIR = "repos"

def is_python_file(path):
    return path.split('.')[-1] == 'py'

for dirpath, dirnames, filenames in os.walk(REPOS_DIR):

    for filename in filenames:
        full_path = os.path.join(dirpath, filename)
        if is_python_file(full_path):
            print(green(f"Keeping {full_path}"))
        else:
            print(red(f"Deleting {full_path}"))

            if REPOS_DIR in full_path:
                os.remove(full_path)
            else:
                print(yellow(f"Something Went Wrong"))