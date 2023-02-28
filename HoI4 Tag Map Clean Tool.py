import os

# Go through all files and gather all the tags who have a state as owner and put them in a list without duplicates. Then go through the states and remove all cores and claims of countrys who do not own a state.
# CHANGE THIS TO YOUR MOD PATH
directoryPath = "<your mod>/history/states/"
tags = []

for filename in os.listdir(directoryPath):
    path = os.path.join(directoryPath, filename)
    with open(path) as f:
        for line in f:
            if line.find("owner") != -1:
                tags.append(line[line.rfind("=")+1:line.rfind("#")].strip())
                break

# Sort the list by how often one tag appears in the list, remove duplicates and print the list
tags = sorted(tags, key=tags.count, reverse=True)
tags = list(dict.fromkeys(tags))
print(tags)


from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

for filename in os.listdir(directoryPath):
    path = os.path.join(directoryPath, filename)
    fh, abs_path = mkstemp()
    with fdopen(fh,'w') as new_file:
        with open(path) as old_file:
            for line in old_file:
                if line.find("add_core_of") != -1:
                    if line[line.rfind("=")+1:line.rfind("#")].strip() not in tags:
                        continue
                    else:
                        new_file.write(line)
                elif line.find("add_claim_by") != -1:
                    if line[line.rfind("=")+1:line.rfind("#")].strip() not in tags:
                        continue
                    else:
                        new_file.write(line)
                else:
                    new_file.write(line)
    #Copy the file permissions from the old file to the new file
    copymode(path, abs_path)
    #Remove original file
    remove(path)
    #Move new file
    move(abs_path, path)