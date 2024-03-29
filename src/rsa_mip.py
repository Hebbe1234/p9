#!/usr/bin/env python

import pulp
import pulp.apis
import networkx as nx
from networkx import digraph
from networkx import MultiDiGraph
from demands import Demand
import topology
import argparse
import time
import os

os.environ["TMPDIR"] = "/scratch/rhebsg19/"

def SolveRSAUsingMIP(topology: MultiDiGraph, demands: list[Demand], paths, channels, slots: int):    
    demand_to_paths = {i : [j for j,p in enumerate(paths) if p[0][0] == d.source and p[-1][1] == d.target] for i, d in enumerate(demands)}
    demand_to_channels = {i : [j for j, c in enumerate(channels) if len(c) == d.size] for i, d in enumerate(demands)}
    
    def y_lookup(path : int, channel : int):
        return "p"+str(path)+"_"+"c"+str(channel)

    def z_lookup(slot : int):
        return "s"+str(slot)

    def gamma(channel: int, slot: int):
        return slot in channels[channel]
    
    def delta(path: int, edge):
        return edge in paths[path]
       
    start_time_constraint = time.perf_counter()

    y_var_dict = pulp.LpVariable.dicts('y',
                                       [("p"+str(p) + "_" + "c"+str(c))
                                        for p  in range(len(paths))
                                        for c in range(len(channels))], lowBound=0, upBound=1, cat="Integer")
    
    z_var_dict = pulp.LpVariable.dicts('z',
                                       [("s"+str(s))
                                        for s in range(slots)], lowBound=0, upBound=1, cat="Integer")
    
    # Define the PuLP problem and set it to minimize 
    prob = pulp.LpProblem('RSA:)', pulp.LpMinimize)

    # Define the objective function to minimize the sum of z_var_dict values
  
    # Add the objective function to the problem
    prob += (pulp.lpSum(z_var_dict[z_lookup(s)] for s in range(slots) ))

    #16
    for d in range(len(demands)) :
        sum_ = 0
        for p in demand_to_paths[d]:
            for c in demand_to_channels[d]:
                sum_ += y_var_dict[y_lookup(p,c)]
        
        prob += sum_ == 1

    #17
    for edge in topology.edges(keys=True):
        for s in range(slots):
            sum_ = 0
            for d in range(len(demands)):
                for p in demand_to_paths[d]:
                    for c in demand_to_channels[d]:
                        sum_ += y_var_dict[y_lookup(p,c)] * gamma(c, s) * delta(p, edge)
            
            prob += sum_ <= 1

    # custom constraint
    for s in range(slots):
        sum_ = 0
        for d in range(len(demands)):
            for p in demand_to_paths[d]:
                for c in demand_to_channels[d]:
                    prob += y_var_dict[y_lookup(p,c)] * gamma(c, s) <= z_var_dict[z_lookup(s)]

    end_time_constraint = time.perf_counter()
    status = prob.solve(pulp.PULP_CBC_CMD(msg=False))
    
    optimal_number = int(sum(z_var_dict[z_lookup(s)].value() for s in range(slots) ))

    solved=True
    if pulp.constants.LpStatusInfeasible == status:
        print("Infeasable :(")
        optimal_number = slots
        solved = False
    
    # Print the results
    # print([(i, p[0][0], p[-1][1]) for i, p in enumerate(paths)])
    # print([(i, c) for i, c in enumerate(channels)])
    
    # for var in prob.variables():
    #     if var.varValue == 0.0:
    #         continue
    #     print(f"{var.name} = {var.varValue}")


    
    return start_time_constraint, end_time_constraint, solved, optimal_number

def main():
    if not os.path.exists("/scratch/rhebsg19/"):
        os.makedirs("/scratch/rhebsg19/")

    parser = argparse.ArgumentParser("mainrsa_mip.py")
    parser.add_argument("--filename", default="./topologies/topzoo/Ai3.gml", type=str, help="file to run on")
    parser.add_argument("--slots", default=320, type=int, help="number of slots")
    parser.add_argument("--demands", default=10, type=int, help="number of demands")
    parser.add_argument("--wavelengths", default=10, type=int, help="number of wavelengths")
    parser.add_argument("--experiment", default="default", type=str, help="default")
    parser.add_argument("--paths", default=2, type=int, help="how many paths")

    args = parser.parse_args()

    G = topology.get_nx_graph(args.filename)
    if G.nodes.get("\\n") is not None:
        G.remove_node("\\n")

    demands = topology.get_gravity_demands2_nodes_have_constant_size(G, args.demands, seed=10, offset=0)
    paths = topology.get_simple_paths(G, demands, args.paths, shortest=False)
    demand_channels = topology.get_channels(demands, args.slots, limit=False)
    _, channels = topology.get_overlapping_channels(demand_channels)
    
    demands = list(demands.values())
    
    print(demands)
    solved = False
    start_time_constraint = time.perf_counter()
    end_time_constraint = time.perf_counter()

    
    if args.experiment == "default":
        start_time_constraint, end_time_constraint, solved, optimal_number = SolveRSAUsingMIP(G, demands, paths, channels, args.slots)
   
    end_time_all = time.perf_counter()

    solve_time = end_time_all - end_time_constraint
    constraint_time = end_time_constraint - start_time_constraint

    print("solve time;constraint time;all time;satisfiable;demands;slots")
    print(f"{solve_time};{constraint_time};{solve_time + constraint_time};{solved};{args.demands};{args.slots}")
    # print(f"{solve_time + constraint_time};{solve_time};{solved};{args.demands};{args.wavelengths}")




if __name__ == "__main__":
    main()

