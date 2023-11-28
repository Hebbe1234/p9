import os
import networkx as nx
from topology import get_demands
from topology import get_nx_graph
from networkx import digraph
from networkx import MultiDiGraph

graphs = []
for subdirs, dirs, files in os.walk("./topologies/topzoo"):
    for f in files:
        G = get_nx_graph(subdirs+"/"+f)
        if G.nodes.get("\\n") is not None:
            G.remove_node("\\n")
        graphs.append((f,len(G.edges)))

graphs.sort(key=lambda f: f[1])
graphs = [f + "\n" for (f,size) in graphs if size >= 20][:19]

with open("topologies/over20.txt", "w") as f:
    f.writelines(graphs)