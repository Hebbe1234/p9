import topology
from bdd import RWAProblem, pretty_print, BDD
from bdd_path_vars import RWAProblem as PRWAProblem, BDD as PBDD
from demands import Demand
from rsa.rsa_bdd import RSAProblem, BDD as RSABDD
import networkx as nx 
from itertools import permutations
import time

if __name__ == "__main__":
    G = nx.MultiDiGraph(nx.nx_pydot.read_dot("../dot_examples/four_node.dot"))
    G = nx.MultiDiGraph(nx.nx_pydot.read_dot("../dot_examples/simple_simple_net.dot"))
    G = nx.MultiDiGraph(nx.nx_pydot.read_dot("../dot_examples/simple_net.dot"))
    G = topology.get_nx_graph(topology.TOPZOO_PATH +  "/Uninett2011.gml")
    G = topology.get_nx_graph(topology.TOPZOO_PATH +  "/Twaren.gml")
    #G = topology.get_nx_graph(topology.TOPZOO_PATH +  "/HiberniaIreland.gml")
    
    if G.nodes.get("\\n") is not None:
        G.remove_node("\\n")
        
    demands = topology.get_gravity_demands(G, 4,seed=10)
    print("demands", demands)
    channels = topology.get_channels(demands, 64)
    overlapping, unique = topology.get_overlapping_channels(channels)
    

    #types = [BDD.ET.EDGE, BDD.ET.LAMBDA, BDD.ET.NODE, BDD.ET.DEMAND, BDD.ET.TARGET, BDD.ET.PATH,BDD.ET.SOURCE]
    rsa_types = [RSABDD.ET.EDGE, RSABDD.ET.CHANNEL, RSABDD.ET.NODE, RSABDD.ET.DEMAND, RSABDD.ET.TARGET, RSABDD.ET.PATH, RSABDD.ET.SOURCE]

    types = [PBDD.ET.EDGE, PBDD.ET.LAMBDA, PBDD.ET.NODE, PBDD.ET.DEMAND, PBDD.ET.TARGET, PBDD.ET.PATH, PBDD.ET.SOURCE]
    # types = [BDD.ET.EDGE, BDD.ET.LAMBDA, BDD.ET.NODE, BDD.ET.DEMAND, BDD.ET.TARGET, BDD.ET.PATH, BDD.ET.SOURCE]
    
    # forced_order = [BDD.ET.LAMBDA, BDD.ET.EDGE, BDD.ET.NODE]
    # ordering = [t for t in types if t not in forced_order]
    # p = permutations(ordering)

    # Increasing wavelengths
    # for w in range(1,5+1):
    #     print(f"w: {w}")
    #     rw1 = RWAProblem(G, demands, forced_order+[*ordering], w, group_by_edge_order =True, generics_first=False)
    #     if rw1.rwa.count() > 0:
    #         print(rw1.get_assignments(1)[0])
    #         break    

    # paths = topology.get_disjoint_simple_paths(G, demands, 1)  
    # cliques = topology.get_overlap_cliques(list(demands.values()), paths)
    # #print(paths)
    # exit()
    #print(paths)
    #overlapping_paths = topology.get_overlapping_simple_paths(paths)
    # rw1 = PRWAProblem(G, demands, paths, overlapping_paths, types, wavelengths=8, group_by_edge_order =True, generics_first=False, with_sequence=True, binary=True, \
    #      only_optimal=False, cliques=cliques)
    
    rsa = RSAProblem(G, demands, rsa_types, channels, unique, overlapping)
    print(rsa.rsa.count())
    # overlapping_paths = topology.get_overlapping_simple_paths(G, paths)
    # print(overlapping_paths)
    
    # Does not work when using i < j apparently. Seems to have impacted the runtime unfort.
    # rw1 = PRWAProblem(G, demands, paths, overlapping_paths, types, wavelengths=16, group_by_edge_order =True, generics_first=False, with_sequence=True, binary=True, \
    #         only_optimal=False)

    #pretty_print(rw1.base.bdd, rw1.rwa, true_only=True)
    #print(rw1.rwa.count())
    exit(0)    
    
    # for i,o in enumerate(p):
    #     print(f"ordering being checked: {o}")
    #     # rwa = RWAProblem(G, demands, [*o], 5, group_by_edge_order =False, generics_first=False)
    #     # rwa = RWAProblem(G, demands, [*o], 5, group_by_edge_order =False, generics_first=True)
    #     rwa = RWAProblem(G, demands, forced_order+[*o], 5, group_by_edge_order =True, generics_first=False)
    #     rwa = RWAProblem(G, demands, forced_order+[*o], 5, group_by_edge_order =True, generics_first=True)
    #     # print(rwa.rwa.count())
    
    #rwa.print_assignments(true_only=True, keep_false_prefix="l")