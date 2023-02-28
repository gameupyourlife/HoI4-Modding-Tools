import argparse
import os
import sys
import re
import collections
import networkx as nx
import matplotlib.pyplot as plt
import os
from pyvis.network import Network
import numpy as np
import random
import math

# Will go through all scripted effects, collect which effect declares wich variable. Than it will go throug once againg and will check which effect uses which variable and will add an edge between them. This will result in a graph where the nodes are the effects and the edges show which effect has do call which other effects because it uses its variables.
# CHANGE THIS TO YOUR PATH
directoryPath = "<your mod>/common/scripted_effects"
varPrefix = "<your prefix>"
###

G = nx.DiGraph()
effects = []

def is_not_commeted_out(line, search_for, search_for_secondary = "213rewt35434§$%Z&%/GHkdg<<llllfds"):
    if (line.find("{") == -1) & (line.find("{") == -1) & (line.find("#") != -1):
        return False
    return ((line.find("#") > line.find(search_for) & line.find(search_for_secondary)) | (line.find("#") == -1))

def add_effects_to_graph(effects):
    G.add_nodes_from(effects)

def is_not_a_log(line):
    return line.find("log") == -1

def read_effects_in_file(file):
    hirachy_level = 0
    var_setting_effect = []
    vars_set_in_effect = []
    current_effect = ""
    vars = []
    prev_line_had_set_var = False
    for line in file:
        index_of_character_with_clamp = line.count("{")
        hirachy_level += index_of_character_with_clamp
        set_var_index = line.rfind("set_variable")


        if (hirachy_level == 1) & (index_of_character_with_clamp != 0) & (is_not_commeted_out(line, "{", "}")):
            current_effect = line[:line.rfind("=")].strip()
        
        if ((set_var_index != -1) | (prev_line_had_set_var == True)) & (hirachy_level > 0) & (is_not_commeted_out(line, "{", "}")) & (is_not_a_log(line)):
            
            varBegin = line.find(varPrefix)
            curVar = line[varBegin:line.rfind("=", varBegin)].strip()
            # if prev_line_had_set_var:
            #     print("prev_line_had_set_var", curVar, line)
            # If the var is set on the right side of the equation we need to grab it from that side
            if curVar == "":
                curVar = line[varBegin:line.rfind("}")].strip()
            vars.append(curVar)
            prev_line_had_set_var = False

        if set_var_index != -1:
            prev_line_had_set_var = True
        # print(vars, hirachy_level, line)

        hirachy_level -= line.count("}")

        if (hirachy_level < 1) & (vars != []):
            # print("vars:", vars)
            vars_set_in_effect.append(vars)
            var_setting_effect.append(current_effect)
            vars = []

    return var_setting_effect, vars_set_in_effect
  
  

all_var_setting_effect = []
all_vars_set_in_effect = []

for filename in os.listdir(directoryPath):
    print("Now reading file: " + filename)
    path = os.path.join(directoryPath, filename)
    file = open(path, "r")
    all_var_setting_effect_read, all_vars_set_in_effect_read = read_effects_in_file(file)
    all_var_setting_effect = all_var_setting_effect + all_var_setting_effect_read
    all_vars_set_in_effect = all_vars_set_in_effect + all_vars_set_in_effect_read
# del all_vars_set_in_effect[0]
# add_effects_to_graph(effects)

# print(all_var_setting_effect)
# print("-------------------------")
# print(all_vars_set_in_effect[all_var_setting_effect.index("intrest_rate_graph_add_new_segment")-1])
# print(all_vars_set_in_effect[all_var_setting_effect.index("intrest_rate_graph_add_new_segment")])
# print(all_vars_set_in_effect[all_var_setting_effect.index("intrest_rate_graph_add_new_segment")+1])
# print("-------------------------")
# print(all_vars_set_in_effect)

# Go through all effects and add them to the graph
node_color_dict = {

}

# Function to Parse Hexadecimal Value
def parse_hex_color(string):
    if string.startswith("#"):
        string = string[1:]

    r = int(string[0:2], 16) # red color value
    g = int(string[2:4], 16) # green color value
    b = int(string[4:6], 16) # blue color value
    return r, g, b, 255

# Calculate distance btw two color
def color_similarity(base_col_val,oth_col_val):
    return math.sqrt(sum((base_col_val[i]-oth_col_val[i])**2 for i in range(3)))

def create_new_node_color():
    colors_are_similar = True
    while colors_are_similar:
        r = lambda: random.randint(0,255)
        g = lambda: random.randint(0,255)
        b = lambda: random.randint(0,255)
        nodeColor = '#%02X%02X%02X' % (r(),g(),b())
        nodeColor = '#%06X' % random.randint(0,256**3-1)
        print("new color", nodeColor)
        if node_color_dict != {}:
            for color in node_color_dict.values():
                if color_similarity(parse_hex_color(color),parse_hex_color(nodeColor)) < 75:
                    colors_are_similar = True
                    break
                else:
                    colors_are_similar = False
        else:
            colors_are_similar = False
    node_color_dict[filename] = nodeColor
    return nodeColor

def read_effects_in_file2(file, filename):
    hirachy_level = 0
    effect_calls_inside_effect = []
    for line in file:
        index_of_character_with_clamp = line.count("{")
        hirachy_level += index_of_character_with_clamp
        # if index_of_character_with_clamp != 0: # if the character is found
        if (hirachy_level == 1) & (index_of_character_with_clamp != 0) & (is_not_commeted_out(line, "{", "}")):
            effects.append(line[:line.rfind("=")].strip())
            # Find node color
            nodeColor = []
            try:
                nodeColor = node_color_dict[filename]
                print("Color is in dict")
            except:
                nodeColor = create_new_node_color()
            try:
                G.add_node(line[:line.rfind("=")].strip(), color=nodeColor)
            except:
                nodeColor = create_new_node_color()
                G.add_node(line[:line.rfind("=")].strip(), color=nodeColor)

        hirachy_level -= line.count("}")
    return effects

for filename in os.listdir(directoryPath):
    print("-------------------------")
    print("Now reading file: " + filename)
    path = os.path.join(directoryPath, filename)
    file = open(path, "r")
    # add_effects_to_graph(read_effects_in_file2(file))
    read_effects_in_file2(file, filename)


# Connect all effects with the effects which create the variables they use
def read_vars_used_in_effect_in_file(file):
    hirachy_level = 0
    current_effect = ""
    effects_using_vars_from_effect = []
    for line in file:
        index_of_character_with_clamp = line.count("{")
        hirachy_level += index_of_character_with_clamp
        printVars = False
        if (hirachy_level == 1) & (index_of_character_with_clamp != 0) & (is_not_commeted_out(line, "{", "}")) & (line.find("yes") == -1):
            current_effect = line[:line.rfind("=")].strip()
        # if current_effect == "total_expenses":
        #     printVars = True
        #     print("#################", line)
        varBegin = line.find(varPrefix)
        if( varBegin != -1) & (hirachy_level > 0) &  (is_not_commeted_out(line, "{", "}")) & (is_not_a_log(line)):
            curVar = line[varBegin:line.rfind("=", varBegin)].strip()
            if curVar.find(">") != -1:
                curVar = curVar[:curVar.find(">")].strip()
            if curVar.find("<") != -1:
                curVar = curVar[:curVar.find("<")].strip()
            if curVar.find("}") != -1:
                curVar = curVar[:curVar.find("}")].strip()
            # If the var is set on the right side of the equation we need to grab it from that side
            if curVar == "":
                curVar = line[varBegin:line.rfind("}")].strip()
            if printVars:
                print("curVar:", curVar)
            for x in range(len(all_vars_set_in_effect)):
                if curVar == "":
                    continue
                if (curVar in all_vars_set_in_effect[x]):
                    if printVars:
                        print("-----------------" + str(x), current_effect,  all_var_setting_effect[x] + "-----------------")
                    if current_effect == all_var_setting_effect[x]:
                        continue
                    if current_effect == "var_declariation":
                        continue
                    if all_var_setting_effect[x] == "var_declariation":
                        continue
                    G.add_edge(current_effect, all_var_setting_effect[x]) # add edge from current effect to effect
                    #                                      This effect needs -> this effect to work
                    effects_using_vars_from_effect.append((current_effect, all_var_setting_effect[x], ))
        # Go through right side
        varBegin = line.rfind(varPrefix)
        if( varBegin != -1) & (hirachy_level > 0) &  (is_not_commeted_out(line, "{", "}")) & (is_not_a_log(line)):
            curVar = line[varBegin:line.rfind("}", varBegin)].strip()
            # If the var is set on the right side of the equation we need to grab it from that side
            if curVar == "":
                curVar = line[varBegin:line.rfind("}")].strip()
            if printVars:
                print("curVar:", curVar)
            for x in range(len(all_vars_set_in_effect)):
                if curVar == "":
                    continue
                if (curVar in all_vars_set_in_effect[x]):
                    if printVars:
                        print("-----------------" + str(x), current_effect,  all_var_setting_effect[x] + "-----------------")
                    if current_effect == all_var_setting_effect[x]:
                        continue
                    if current_effect == "var_declariation":
                        continue
                    if all_var_setting_effect[x] == "var_declariation":
                        continue
                    G.add_edge( current_effect, all_var_setting_effect[x]) # add edge from current effect to effect
                    #                                      This effect needs -> this effect to work
                    effects_using_vars_from_effect.append((  current_effect, all_var_setting_effect[x] ))
                
        hirachy_level -= line.count("}")
    return effects_using_vars_from_effect

asdg = []
for filename in os.listdir(directoryPath):
    print("Now reading file: " + filename)
    path = os.path.join(directoryPath, filename)
    file = open(path, "r")
    asdg.append(read_vars_used_in_effect_in_file(file))

print(G.edges)

scale=2 # Scaling the size of the nodes by 10*degree
d = dict(G.degree)

#Updating dict
d.update((x, scale*y+10) for x, y in d.items())

#Setting up size attribute
nx.set_node_attributes(G,d,'size')



# Draw Graph
print("Files read, now drawing graph...")

net = Network(height="1200px", width="100%", bgcolor="#333333", font_color="white", select_menu=True, directed=True)
# net.show_buttons(filter_=['physics'])
net.from_nx(G)
net.set_options("""
    const options = {
    "physics": {
        "barnesHut": {
        "gravitationalConstant": -15000,
        "centralGravity": 0.1,
        "springLength": 220
        },
        "minVelocity": 0.75
    }
    }""")
net.show("graph.html")

# options = {
#     'node_color': 'blue',
#     'node_size': 10,
#     'width': 0.5,
#     "edge_color": "grey",
#     "font_size": 7,
# }
# nx.draw_networkx(G, with_labels = True ,**options)
# plt.show()

# print(G.edges)
    
