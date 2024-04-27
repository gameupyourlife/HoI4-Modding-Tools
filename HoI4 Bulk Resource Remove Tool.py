import os
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

# INPUT
# This program will remove every resource owned by given country tag
country_tag = "ALL" # Set to "ALL" to remove all resources
directoryPath = "C:/Users/cedri/Documents/GitHub/HoI4-Modding-Tools" # Replace <your-mod-path> with the path to your mod
remove_factory = True # Set to True to remove factories as well

def replace(file_path):
    #Create temp file
    fh, abs_path = mkstemp()
    is_searched_state = False
    has_to_be_removed = False

    if country_tag == "ALL":
        is_searched_state = True
    else:
        with open(file_path) as file:
            for line in file:
                if (line.find("owner") != -1):
                    if(line.find(country_tag) != -1):
                            is_searched_state = True
                            break

    if is_searched_state:
        with fdopen(fh,'w') as new_file:
            lines = []
            with open(file_path) as old_file:
                lines = old_file.readlines()
                for i in range(len(lines)):
                    line = lines[i]
                    # Replace the owner and add_core_of lines with the new country tag
                    if isInLineAndNoteCommeted(line, "buildings") and (remove_factory):
                        has_to_be_removed = True
                    if isInLineAndNoteCommeted(line, "resources"):
                        has_to_be_removed = True
                    
                    if(has_to_be_removed):
                        CommentOutLineInsideBracketIndex(lines, i)
                        has_to_be_removed = False

            new_file.writelines(lines)


    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def CommentOutLineInsideBracketIndex(lines, index):
    nestIndex = 0
    line = lines[index]
    lines[index] = "# " + lines[index]
    if isInLineAndNoteCommeted(line, "{"):
        nestIndex += 1
    if  isInLineAndNoteCommeted(line, "}"):
        nestIndex -= 1
    index += 1
    while nestIndex > 0:
        line = lines[index]
        lines[index] = "# " + lines[index]
        if isInLineAndNoteCommeted(line, "{"):
            nestIndex += 1
        if  isInLineAndNoteCommeted(line, "}"):
            nestIndex -= 1
        index += 1
    return (line, lines, index)

def isInLineAndNoteCommeted(line, search_term):
    # Check whether the line contains the search term and is not in a comment
    index = line.find(search_term)
    commentIndex = line.find("#")
    if index != -1 and ((commentIndex > index) or (commentIndex == -1)):
        return True
    return False


directoryPath = os.path.join(directoryPath, "history/states")
for filename in os.listdir(directoryPath):
    path = os.path.join(directoryPath, filename)
    replace(path)


# Go through all files and gather all the tags who have a state as owner and put them in a list without duplicates. Then go through the states and remove all cores and claims of countrys who do not own a state.
