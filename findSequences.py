from __future__ import print_function

# findSequences.py
# Purpose: make a graph of all the sequences
# in a given HLT path. Format is "dot"
# Author: Thiago Tomei
# Date: 2019-02-13

import sys
import os
import fnmatch
import networkx as nx

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

HLTMenuName = "dumpedHLT.py"
mother_path_name = "HLT_Mu50_v13"

# Parse the HLT menu
### Usually, blindly executing an external file is a security hazard... 
execfile(HLTMenuName)

print (process.process)
pathnames = process.paths.viewkeys()
sequencenames = set(process.sequences.viewkeys())
G = nx.DiGraph()

### Define function to find leaves
def find_leaves(sequencenames, process):
    base_sequences = set()
    #print(len(sequencenames))
    for seqnamea in sequencenames:
        base_sequence = True
        seqa = getattr(process,seqnamea)
        for seqnameb in sequencenames:
            seqb = getattr(process,seqnameb)
            if seqa.contains(seqb):
                #print("\t"+seqnamea+" contains "+seqnameb)
                base_sequence = False
        if base_sequence is True:
            print(seqnamea+" is leaf")
            base_sequences.add(seqnamea)
    return base_sequences

### Define function to find parents
def find_parents(children, sequencenames, process):
    new_edges = dict()
    for seqname in children:
        seq_child = getattr(process,seqname)
        distance = 9999
        seq_parent = cms.Sequence()
        # Do you have parents?
        for possible_parent in sequencenames:
            seq_pp = getattr(process,possible_parent)
            if (seq_pp.contains(seq_child) and len(seq_pp.moduleNames()) < distance):
                # Okay, found a shorter parent
                seq_parent = seq_pp
                distance = len(seq_pp.moduleNames())
        # At this point, we should have the shortest parent
        if(distance < 9999):
            #print(seq_parent.label()+" is the direct parent of "+seqname)
            new_edges[seqname] = seq_parent.label()
        else:
            #print(seqname+" has no parents")
            new_edges[seqname] = mother_path_name
    return new_edges

### We iterate finding:
# 1) All leaves
# 2) All remaining sequences (i.e., the ones that are not leaves)
# 3) Edges between leaves and remaining sequences

current_leaves = set()
remaining_sequences = sequencenames

while(len(remaining_sequences) is not 0):
    current_leaves = find_leaves(remaining_sequences, process)
    remaining_sequences = remaining_sequences.difference(current_leaves) 
    new_edges = find_parents(current_leaves,remaining_sequences,process)
    print("\n"+"="*16+"\n")
    print(current_leaves)
    print("\n"+"="*16+"\n")
    for key,value in new_edges.items():
        print(key,"is child of",value)
    print("\n"+"="*16+"\n")
    for key,value in new_edges.items():
        G.add_edge(key,value)

### At this point, all information should be in the graph!
# It should have all the sequences + 1 (the process)
print(nx.info(G))
prelim_edges = list(nx.bfs_tree(G,mother_path_name,reverse=True).edges())
print("strict graph {")
print('node [fontname = "helvetica",shape="rectangle"];')
print('edge [color = "red"];')
for edge in prelim_edges:
    print(edge[0],"--",edge[1])
print("}")
