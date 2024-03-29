import os
import json
import subprocess
import math
import getopt
import sys
import argparse

# Extract solve times from output files, if they were solved
def parse_txt_file(file_path, rtime_attr, true_only=False):
    with open(file_path, "r") as file:
        lines = file.read().splitlines()

    #if  lines and "solve" in lines[-1]:
     #   solve_time = map(str.strip, lines[-1].split(":"))
    if not lines:
        return None
    
    lines = [l for l in lines if l]

    if "True" not in lines[-1] and "False" not in lines[-1]:
        return None
    
    if true_only and "True" not in lines[-1]:
        return None
    
    data = list(map(str.strip, lines[-1].split(";")))
    solveable = data[2]
    if solveable:
        return {
            "status": True,
            "rtime": float(data[rtime_attr]),
            "mempeak": "1 KiB"
        }
    else:
        return None
    
# initialize data for each run of demands. Demands are given in the names of the output files.
def init_data(data_directory):
    data = {}

    for root, graph_dirs,_ in os.walk(data_directory):
        for graph_dir in graph_dirs:
            directory_path = os.path.join(root, graph_dir)
            
            # Iterate through files in the subdirectory
            for output in os.listdir(directory_path):
                if output.endswith(".txt"):
                    number_of_demands = output.split("output")[1].split(".txt")[0]
                    data[str(number_of_demands)] = {"stats":{},"preamble":{},"meta":{}}
        break
    return data

# Extract running times for each graph for each demand
def extract_run_times(data_directory,data, rtime_attr=0, true_only=False):
    for root, graph_dirs, _ in os.walk(data_directory):
        instance = 0
        for graph_dir in graph_dirs:
            directory_path = os.path.join(root, graph_dir)
            for output in os.listdir(directory_path):
                instance += 1
                output_path = os.path.join(directory_path,output)
                number_of_demands = output.split("output")[1].split(".txt")[0]
                instance_name = os.path.splitext("instance"+str(instance))[0]
                instance_name = instance_name.replace("instance", "").zfill(10) + "_" + output_path.split('/')[-2]
                instance_data = parse_txt_file(output_path, rtime_attr, true_only)
               
                if instance_data is not None:
                    
                    if not str(number_of_demands) in data:
                        continue
                                        
                    data[str(number_of_demands)]["stats"][instance_name] = instance_data
                # else: #Remove comment to add timeout rtime for instances that did not complete
                #     data[str(number_of_demands)]["stats"][instance_name] = {"status": True, "rtime":3599, "mempeak": "1 KiB"}

# Define graphing metadata
def init_graph_metadata(data, label=""):
    for key, section in data.items():
        if not section["stats"]: #if all runs timed out
            continue

        y_min,y_max,x_min,x_max = math.inf,0,0,0
        for k,d in section.items():
            
            for j, l in d.items(): 
                if l["rtime"] > y_max : 
                    y_max = l["rtime"]
                if l["rtime"] < y_min : 
                    y_min = l["rtime"]
                x_max += 1

        meta_info = {
            "meta":{
                "y_min": y_min, 
                "y_max": y_max,
                "x_min": x_min,
                "x_max": x_max
            }
        }
        preamble_info = {
        "preamble": {
            "benchmark": "ttt" ,
            "prog_args": None,
            "program": "another-good-tool",
            "prog_alias": label
            }
        }
        section.update(preamble_info)
        section.update(meta_info)




if __name__ == "__main__":
    in_dirs = []

    parser = argparse.ArgumentParser("cactus")
    parser.add_argument("--dirs", type=str, default=[],nargs="+",)
    parser.add_argument("--legend", type=str, default=[],nargs="+")
    parser.add_argument("--xaxis", type=int, default=[], nargs="+")
    parser.add_argument("--savedest", type=str, default="cactus_graphs/")
    parser.add_argument("--select", type=int, default=[], nargs="+")
    parser.add_argument("--true_only", type=str, default="false")

    args = parser.parse_args()
    in_dirs=args.dirs
    legend_list=args.legend
    xaxis_list=args.xaxis
    demands_list=args.select
    true_only = args.true_only != "false"
    
    assert len(legend_list) == len(xaxis_list) and len(legend_list) == len(in_dirs) and (len(demands_list) == 0 or len(demands_list) == len(legend_list))

    print(in_dirs, legend_list, xaxis_list, demands_list)
    
    full_data = {}
    legend = {}
    rtime = {}
    #out_dirs = [f"{out}__{i}" for out in set(out_dirs) for i in range(out_dirs.count(out))]


    for i,k in enumerate(in_dirs):
        legend[k] = legend_list[i]
        rtime[k] = xaxis_list[i]

    print(legend, rtime)
    
    if len(demands_list) > 0:
        full_data['0'] = {}    


    for i, out in enumerate(in_dirs):
        data = {}
        data_directory = f"../../out/{out.split('__')[0]}" 
        data = init_data(data_directory)
        extract_run_times(data_directory, data, rtime[out], true_only)
        init_graph_metadata(data, legend[out])          # now we have the runtime for all demands for given experiment

        
        if len(demands_list) == 0:
            for demands, _ in data.items():
                if demands not in full_data:
                    full_data[demands] = {}
                    
                full_data[demands][out] = {}

            for demands, plot_data in data.items():
                file_name = f"json_folder/{demands}_{out}.json"
                with open(file_name, "w") as json_file:
                    json.dump(plot_data, json_file, indent=4)
                full_data[demands][out] = plot_data

        else:
            full_data['0'][out] = {}

            
            for demands, plot_data in data.items():            
                if int(demands) != int(demands_list[i]):
                    continue 
                
                file_name = f"json_folder/{0}_{out}.json"
                with open(file_name, "w") as json_file:
                    json.dump(plot_data, json_file, indent=4)
                
                full_data['0'][out] = plot_data

    for demand, in_dirs in full_data.items():
        xmax = 70
        ymax = 0
        ymin = 0
        xmin = 0
        
        
        stop = False
        for out in in_dirs:
            xmax = [in_dirs[out]["meta"]["x_max"] for out in in_dirs if in_dirs[out]["meta"]]
            ymax = [in_dirs[out]["meta"]["y_max"] for out in in_dirs if in_dirs[out]["meta"]]
            xmin = [in_dirs[out]["meta"]["x_min"] for out in in_dirs if in_dirs[out]["meta"]]
            ymin = [in_dirs[out]["meta"]["y_min"] for out in in_dirs if in_dirs[out]["meta"]]
            
            if not xmax or not ymax or not xmin or not ymin:
                stop = True
                continue
            xmax = max(xmax)
            ymax= min(3600, max(ymax))
            ymin = min(ymin)
            xmin = min(xmin)
        if stop:
            continue
        inputs = [f"./json_folder/{str(demand)}_{o}.json" for o in in_dirs if full_data[str(demand)][o]["stats"]]
        command = [
            'python3',      
            'mkplot.py',    
            '--legend', 'prog_alias',
            '-t', '1000000',
            '-b', 'svg',
            '--ylog',
            '--save-to', f'{args.savedest}demands'+str(demand) + '.svg',
            '--xmax', str(xmax),
            '--ymin', str(ymin),
            '--ymax', str(ymax + 50),
            '--lloc', 'lower right',
            '--lncol', '1',
            *inputs
        ]

        subprocess.run(command)


    

