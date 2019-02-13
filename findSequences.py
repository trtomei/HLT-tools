from __future__ import print_function

# AlCAMenuChecker.py
# Purpose: check that the HLT menu has all the AlCa mandatory paths
# and that the paths are correctly seeded.
# Author: Thiago Tomei
# Date: 2017-11-02

import sys
import os
import fnmatch
import networkx as nx
import matplotlib.pyplot as plt

RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

HLTMenuName="dumpedHLT.py"

# Parse the HLT menu
### Usually, blindly executing an external file is a security hazard... 
execfile(HLTMenuName)

print (process.process)
pathnames = process.paths.viewkeys()
sequencenames = list(process.sequences.viewkeys())

# Find base
# Add to DAG

### LOOP
# Find parents
# Add to DAG
print (sequencenames)
G = nx.DiGraph()

### First add the base nodes to the DAG
print(len(sequencenames))
for seqnamea in sequencenames:
    base_sequence = True
    seqa = getattr(process,seqnamea)
    for seqnameb in sequencenames:
        seqb = getattr(process,seqnameb)
        if seqa.contains(seqb):
            #print("\t"+seqnamea+" contains "+seqnameb)
            base_sequence = False
    if base_sequence is True:
        print(seqnamea+" is base")
        G.add_node(seqnamea)

print("\n"+"="*16)
print(len(sequencenames))
print(len(G.nodes))        
print("="*16+"\n")

for base_seq in list(G.nodes):
    sequencenames.remove(base_seq)

print("\n"+"="*16)
print("Still not in the graph:")
print(sequencenames)
print("="*16+"\n")

### Now iteratively find the direct parents
while (len(sequencenames) is not 0):
    print("Still missing",len(sequencenames),"sequences")
    
    # Clear relationships
    new_edges = dict()
    
    # Traverse the graph ### FIXME:is there any way to get only nodes that have no parents?
    for seqname in G.nodes:
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
            new_edges[seqname] = "process"

    # At this point, new_edges should have all the new parent-child relationships
    # Add the newfound parents to the graph
    for key,value in new_edges.items():
        #print("New relation:",value,"is the parent of",key)
        G.add_edge(key,value)
        # Remove the newfound parents from the sequencenames
        #print("Try to remove",value)
        try:
            sequencenames.remove(value)
        except ValueError:
            #print("Already removed",value)
            continue

### At this point, all information should be in the graph!
# It hsould have all the sequences + 1 (the process)
print(nx.info(G))
print(list(nx.bfs_tree(G,"process",reverse=True).edges()))
