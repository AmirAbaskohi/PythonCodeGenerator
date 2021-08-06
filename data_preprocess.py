import os
from curtsies.fmtfuncs import red, green, on_blue, yellow, blue, cyan
import time
import re

def remove_comments(string):
    string = re.sub(re.compile("\'\'\'.*?\'\'\'",re.DOTALL ) ,"" ,string)
    string = re.sub(re.compile("\"\"\".*?\"\"\"",re.DOTALL ) ,"" ,string)
    string = re.sub(re.compile("#.*?\n" ) ,"" ,string)
    return string

MAX_CHAR_LENGTH = 512
MIN_CHAR_LENGTH = 256

NEWLINE_CHAR = "<N>"

full_paths = []
for dirpath, dirnames, filenames in os.walk("repos"):
    for f in filenames:
        full_path = os.path.join(dirpath, f)
        full_paths.append(full_path)


with open("data.txt", "a") as df:
    for path in full_paths:

        try:
            file = open(path, "r").read()
        except:
            continue

        file = remove_comments(file)
        f = file.replace("\n", NEWLINE_CHAR)

        if 100 < len(file) <= MAX_CHAR_LENGTH:
            df.write(f + '\n')

        elif len(file) > MAX_CHAR_LENGTH:
            sd = f.split(f"{NEWLINE_CHAR}")
            sub_str = ""
            for split in sd:
        
                sub_str += split + f"{NEWLINE_CHAR}{NEWLINE_CHAR}"
                if MIN_CHAR_LENGTH <= len(sub_str) <= MAX_CHAR_LENGTH:
            
                    df.write(sub_str + '\n')
                    sub_str = ""

        else:
            print(red("Not enough length to consider"))
        
        