import os
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

# INPUT
# This program will change the owner and core of the states with the given ids to the given country tag
states_to_alter = [665, 458]
country_tag = "<TAG>" # States will be owned by this country
directoryPath = "<your mod>/history/states/"

def replace(file_path):
    #Create temp file
    fh, abs_path = mkstemp()
    is_searched_state = False
    core_found = False

    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                # If the file has the right id, set the flag to true and proceed to alter the file
                # If the file has the wrong id, set the flag to false and return to save time and look for the right file
                if line.find("id") != -1:
                    curId = int(line[line.rfind("=")+1:line.rfind("#")].strip())
                    if curId in states_to_alter:
                        is_searched_state = True
                    else:
                        return
                # Replace the owner and add_core_of lines with the new country tag
                if (line.find("owner") != -1) & (is_searched_state):
                        new_file.write("        owner = " + country_tag + "\n")
                # Remove any cores other than that of the country tag
                elif (line.find("add_core_of") != -1) & (is_searched_state) & (core_found):
                    continue
                elif (line.find("add_core_of") != -1) & (is_searched_state):
                        new_file.write("        add_core_of = " + country_tag + "\n")
                        core_found = True
                # If we do not have to alter the line we won't do anything
                else:
                    new_file.write(line)
    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

for filename in os.listdir(directoryPath):
    path = os.path.join(directoryPath, filename)
    replace(path)


# Go through all files and gather all the tags who have a state as owner and put them in a list without duplicates. Then go through the states and remove all cores and claims of countrys who do not own a state.
