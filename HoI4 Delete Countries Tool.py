import os
from tempfile import mkstemp
from shutil import move, copymode
from os import fdopen, remove

# INPUT
# This program will change the owner and core of the states with the given ids to the given country tag
country_tags = ["GER"] # States will be owned by this country
directoryPath = "C:/Users/cedri/Documents/GitHub/HoI4-Modding-Tools/events"

def replace(file_path):
    #Create temp file
    fh, abs_path = mkstemp()


    with fdopen(fh,'w') as new_file:
        with open(file_path) as old_file:
            lines = old_file.readlines()
            for i in range(len(lines)):
                line = lines[i]
                # Check whether the line contains one of the tags
                for tag in country_tags:
                    tagIndex = line.find(tag)
                    if tagIndex != -1:
                        indices = [line.find("target"), line.find("id"), line.find("owner"), line.find("controller"), line.find("scope"), line.find("tag")]
                        indices.sort()
                        commentIndex = line.find("#")

                        # If tag found in line and is not in a comment
                        if indices[-1] != -1 and ((commentIndex > indices[-1]) or (commentIndex == -1)):
                            openingBracketIndex = line.find("{")
                            localcommentIndex = line.find("#")
                            while (openingBracketIndex == -1) and ((localcommentIndex > openingBracketIndex) or (localcommentIndex == -1)):
                                i -= 1
                                line = lines[i]
                                openingBracketIndex = line.find("{")
                                localcommentIndex = line.find("#")
                            line, lines, i = CommentOutLineInsideBracketIndex(lines, i)

                        elif isInLineAndNoteCommeted(line, "{"):
                            line, lines, i = CommentOutLineInsideBracketIndex(lines, i)

                        else:
                            lines[i] = "# " + lines[i]

                indices = [line.find("ai_chance"), line.find("ai_will_do")]
                indices.sort()
                if indices[-1] != -1:
                    line, lines, i = CommentOutLineInsideBracketIndex(lines, i)

                
            new_file.writelines(lines)

                
                    

    #Copy the file permissions from the old file to the new file
    copymode(file_path, abs_path)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)

def isInLineAndNoteCommeted(line, search_term):
    # Check whether the line contains the search term and is not in a comment
    index = line.find(search_term)
    commentIndex = line.find("#")
    if index != -1 and ((commentIndex > index) or (commentIndex == -1)):
        return True
    return False


def CommentOutLineInsideBracketIndex(lines, index):
    nestIndex = 0
    line = lines[index]
    while nestIndex > 0:
        line = lines[index]
        lines[index] = "# " + lines[index]
        if isInLineAndNoteCommeted(line, "{"):
            nestIndex += 1
        if  isInLineAndNoteCommeted(line, "}"):
            nestIndex -= 1
        index += 1
    return (line, lines, index)

for filename in os.listdir(directoryPath):
    path = os.path.join(directoryPath, filename)
    replace(path)


# Go through all files and gather all the tags who have a state as owner and put them in a list without duplicates. Then go through the states and remove all cores and claims of countrys who do not own a state.
