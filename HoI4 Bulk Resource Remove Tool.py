import os
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

# INPUT
# This program will remove every resource owned by given country tag
country_tag = "GER" # Set to "ALL" to remove all resources
directoryPath = "<your-mod-path>/history/states/" # Replace <your-mod-path> with the path to your mod

def replace(file_path):
    #Create temp file
    fh, abs_path = mkstemp()
    is_searched_state = False
    is_in_resources = False

    if country_tag == "ALL":
        is_searched_state = True
    else:
        with open(file_path) as file:
            for line in file:
                if (line.find("owner") != -1):
                    if(line.find(country_tag) != -1):
                            is_searched_state = True
                            break

    with fdopen(fh,'w') as new_file:
            with open(file_path) as old_file:
                for line in old_file:
                    # Replace the owner and add_core_of lines with the new country tag
                
                    if (line.find("resources") != -1):
                        is_in_resources = True
                    if (line.find("}") != -1) & (is_in_resources):
                        is_in_resources = False
                        new_file.write("# " + line)
                    elif(is_in_resources):
                        new_file.write("# " + line)
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
