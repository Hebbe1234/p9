import argparse
import time
from topology import get_demands
from topology import get_nx_graph
from bdd_edge_encoding import RWAProblem, BDD



def baseline(G, order, demands, wavelengths):
    start_time_rwa = time.perf_counter()
    rwa = RWAProblem(G,demands,order,wavelengths,group_by_edge_order=True)
    return (start_time_rwa, rwa)

def wavelength_constraint(G,order,demands,wavelengths):
    start_time_rwa = time.perf_counter()
    rwa = RWAProblem(G,demands,order,wavelengths,group_by_edge_order=True, generics_first=False, wavelength_constrained=True)
    return (start_time_rwa,rwa)

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser("mainbdd.py")
    parser.add_argument("--filename", type=str, help="file to run on")
    parser.add_argument("--wavelengths", default=10, type=int, help="number of wavelengths")
    parser.add_argument("--demands", default=10, type=int, help="number of demands")
    parser.add_argument("--experiment", default="baseline", type=str, help="baseline, ")
    args = parser.parse_args()

    G = get_nx_graph(args.filename)
    if G.nodes.get("\\n") is not None:
        G.remove_node("\\n")

    demands = get_demands(G, args.demands, 1)
    types =  [BDD.ET.DEMAND, BDD.ET.SOURCE, BDD.ET.EDGE, BDD.ET.NODE, BDD.ET.PATH, BDD.ET.TARGET]

    
    solved = False
    start_time_all = time.perf_counter()
    start_time_rwa = time.perf_counter() #bare init. Bliver sat i metoden

    if args.experiment == "baseline":
        (start_time_rwa, rwa) = baseline(G, types, demands, args.wavelengths)
    elif args.experiment == "wavelength_constraint":
        (start_time_rwa, rwa) = wavelength_constraint(G,types,demands,args.wavelengths)
    else:
        raise Exception("Invalid Argument")
    
    end_time_all = time.perf_counter()  

    solve_time = end_time_all - start_time_rwa
    all_time = end_time_all - start_time_all

    print("solve time;all time;satisfiable;demands;wavelengths")
    print(f"{solve_time};{all_time};{rwa.rwa != rwa.base.bdd.false};{len(rwa.base.bdd)};-1;{args.demands};{args.wavelengths}")
