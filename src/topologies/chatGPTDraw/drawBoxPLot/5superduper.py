import os
import shutil
import json
source_dir = "FIXED_FAILOVER_MUCH_INFO"
pathToData =  source_dir #CHANGES ACCORDING TO WHAT DATA YOU LOOKING AT. 

#1splitIntoFolder.py
####ONLY SPLITS THE THINGS FROM THE RESULT FOLDER, INTO 4 FOLDERS
def split_into_folder_BDD(): 
    # Define the source and destination directories
    
    source_dir2 = source_dir + '/results'
    kanto_dynamic_dir = source_dir+'/kantoAnds'
    kanto_failover_dir = source_dir+ '/kantoEdgeTop'
    dt_dynamic_dir = source_dir +'/dtAnds'
    dt_failover_dir = source_dir+'/dtEdgeTop'

    # Ensure destination directories exist
    os.makedirs(kanto_dynamic_dir, exist_ok=True)
    os.makedirs(kanto_failover_dir, exist_ok=True)
    os.makedirs(dt_dynamic_dir, exist_ok=True)
    os.makedirs(dt_failover_dir, exist_ok=True)

    # Iterate through each file in the source directory
    for filename in os.listdir(source_dir2):
        if filename.endswith('.json'):
            filepath = os.path.join(source_dir2, filename)

            # Read the content of the JSON file
            with open(filepath, 'r') as file:
                data = json.load(file)
                data = data[0]
                # Check the content of the file and copy it to the appropriate folder
                if 'kanto11' in data["filename"]:
                    if 'failover_dynamic_query' in data["experiment"]:
                        shutil.copy(filepath, os.path.join(kanto_dynamic_dir, filename))
                    elif 'failover_failover_query' in data["experiment"]:
                        shutil.copy(filepath, os.path.join(kanto_failover_dir, filename))
                elif 'dt' in data["filename"]:
                    if 'failover_dynamic_query' in data["experiment"]:
                        shutil.copy(filepath, os.path.join(dt_dynamic_dir, filename))
                    elif 'failover_failover_query' in data["experiment"]:
                        shutil.copy(filepath, os.path.join(dt_failover_dir, filename))

    print("Files have been copied to the respective folders.")


# def process_json_file(file_path):
#     with open(file_path, 'r') as f:
#         data = json.load(f)
    
#     for item in data:
#         time_points = item['time_points']
#         usage_times = item['usage_times']
        
#         # Subtract usage_times from time_points elementwise
#         time_points_2 = [
#             [tp - ut for tp, ut in zip(tp_list, ut_list)]
#             for tp_list, ut_list in zip(time_points, usage_times)
#         ]
        
#         # Add the new key to the item
#         item['time_points_2'] = time_points_2

#     with open(file_path, 'w') as f:
#         json.dump(data, f, indent=4)

# def process_folder(folder_path):
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.json'):
#             file_path = os.path.join(folder_path, filename)
#             process_json_file(file_path)

# def split_into_folder(): 

#     # Use the function
#     folder_path = 'FAILOVER_MUCH_INFO/kantoAnds'
#     folder_path = 'FAILOVER_MUCH_INFO/kantoEdgeTop'

#     folder_path = 'FAILOVER_MUCH_INFO/dtEdgeTop'
#     folder_path = 'FAILOVER_MUCH_INFO/dtAnds'
#     process_folder(folder_path)



# graphName = "dt"
# name = graphName + "EdgeTop"
# name = graphName + "Ands"
# data_folder = '5k_FAILURES_ILP/'+name
# data_folder = 'FAILOVER_MUCH_INFO/'+name

graphNames = ["dt","kanto"]
queryOptions = ["Ands","EdgeTop"]

def extract():
    for graphname in graphNames:
        for queryType in queryOptions: 
            name = graphname + queryType
            output_file = name+'.json'
            data_folder = pathToData + "/" + name  #Filepath direclty to the json. 
            outfolder = name

            # Initialize lists to store demands and all_times values
            demands_and_all_times = []

            # Iterate over each JSON file in the Data folder
            for filename in os.listdir(data_folder):
                if filename.endswith('.json'):
                    file_path = os.path.join(data_folder, filename)
                    
                    # Open the JSON file and load its content
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                    data = data[0]
                    # Extract demands and all_times values from the loaded data

                    demands = data.get('demands')
                    # all_times = data.get('all_times')
                    all_times = data.get('time_points')
                    subtree_times = data.get('subtree_times')
                    
                    # Append demands and all_times to the list
                    demands_and_all_times.append({
                        'demands': demands,
                        'all_times': all_times,
                        'subtree_times': subtree_times
                    })

                                # Write the extracted data to a new JSON file
            with open(output_file, 'w') as f:
                json.dump(demands_and_all_times, f, indent=4)

            # Iterate through each set of all_times
            # for i in range(5): #CHANGE IF THERE IS MORE OR LESS THEN 5 edgeafilver 
            #     new_data = []
            #     for item in data:
            #         new_item = {
            #             "demands": item["demands"],
            #             "all_times": [item["all_times"][i]],
            #             "subtree_times": [item["subtree_times"][i]]
            #         }
            #         new_data.append(new_item)
                
            #     # Write new data to a new JSON file in the json2 folder
            #     with open(outfolder+f'/EdgeFailover_{i+1}.json', 'w') as outfile:
            #         json.dump(new_data, outfile, indent=4)

def extractToMany():
    for graphname in graphNames:
        for queryType in queryOptions: 
            name = graphname + queryType
            output_file = name+'.json'
            data_folder = pathToData + "/" + name  #Filepath direclty to the json. 
            outfolder = name
            # Create a folder if it doesn't exist
            if not os.path.exists(outfolder):
                os.makedirs(outfolder)

            with open(output_file, 'r') as f:
                data = json.load(f)

            # Iterate through each set of all_times
            for i in range(5):
                new_data = []
                for item in data:
                    new_item = {
                        "demands": item["demands"],
                        "all_times": [item["all_times"][i]],
                        "subtree_times": [item["subtree_times"][i]]

                    }
                    new_data.append(new_item)
                
                # Write new data to a new JSON file in the json2 folder
                with open(outfolder+f'/EdgeFailover_{i+1}.json', 'w') as outfile:
                    json.dump(new_data, outfile, indent=4)


split_into_folder_BDD()
import time
time.sleep(1)
extract()
time.sleep(1)
extractToMany()

