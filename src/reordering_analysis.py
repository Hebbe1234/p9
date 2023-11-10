from matplotlib import axes
import pandas as pd
import matplotlib.pyplot as mp
from itertools import permutations
import itertools
import matplotlib.pyplot as plt

from itertools import chain, combinations
def all_subsets(ss):
    return chain(*map(lambda x: combinations(ss, x), range(0, len(ss)+1)))


if __name__ == "__main__":

    
    # results = pd.read_csv("../out/Reordering_csvs/results.csv", delimiter=";")
    # results.to_pickle("../out/Reordering_csvs/results.pkl")
    df = pd.read_pickle("../out/Reordering_csvs/results.pkl")
    df.columns = ["File", "ID", "Other_Order", "Generics_First", "Order", "Mult_combined", "Size"]

    #df = pd.read_pickle("../out/Reordering_csvs/df_small.pkl")
    
    result_count_by_file = df.groupby(["File"], as_index=False).count()
    print(result_count_by_file.head(20))   
     
     
    completed_files = result_count_by_file[result_count_by_file["ID"] == 322560]
    print(completed_files.shape)
    
    completed = df[df["File"].isin(completed_files["File"])]
    
    completed["Mult_combined"] = completed["Mult_combined"].str.replace(r"\(|\)|,|\'","", regex=True).str.split('').apply(sorted).str.join('')
    
    sizes = completed[["Other_Order", "Generics_First", "Order", "Size"]].groupby(["Other_Order", "Generics_First", "Order"], as_index=False).mean()
    sizes.reset_index(inplace=True, drop=True)
    
    
    sorted = sizes.sort_values(["Size"])
    sorted.reset_index(inplace=True, drop=True)
    # print(sorted.head(100000))

    cols = ["green", "red", "blue", "orange"]
    
    # Plotting
    ax = None
    for b1 in [True, False]:
        for b2 in [True, False]:
            print(b1, b2)
            tt = sorted[(sorted["Other_Order"].str.strip() == str(b1)) & (sorted["Generics_First"].str.strip()  == str(b2)) ]
        
            print(tt.head())
            # ff.drop(columns=['index_0'])
            tt.reset_index(inplace=True, drop=True)
            
            if ax is None:
                ax = tt.plot(y=["Size"], kind="line", figsize=(9, 8), color=cols[0])
            else:
                tt.plot(y=["Size"],  kind="line", figsize=(9, 8), color=cols[0], ax=ax)
                
            cols = cols[1:]

            tt_min = tt.iloc[0]["Size"]
            
            print(tt[tt["Size"] > tt_min].head(100))
          
    if ax is not None:  
        ax.legend(["True, True", "True, False", "False, True", "False, False"])
        
    mp.show()

    # Try to find patterns in the two groups of variable orders
    best_bool_comb_df = sorted[(sorted["Other_Order"].str.strip() == str(False)) & (sorted["Generics_First"].str.strip() == str(False)) ]
    best_bool_comb_df["Order"] = best_bool_comb_df["Order"].str.replace(r"\(|\)|,|\'|\s","", regex=True).str.split('').str.join('')
    best_size = best_bool_comb_df.iloc[0]["Size"]
    
    best_perms = best_bool_comb_df[best_bool_comb_df["Size"] == best_size]
    worst_perms = best_bool_comb_df[best_bool_comb_df["Size"] != best_size]
    
    positions = {}
    
    for p, perms in enumerate([best_perms, worst_perms]):
        for index, row in perms.iterrows():
            for i, c in enumerate([*row["Order"]]):
                if not c in positions:
                    positions[c] = []
                
                positions[c].append(i)

        avg_positions = {key: 0.0 for key in positions}
        for c in positions:
            avg_positions[c] = sum(positions[c]) / len(positions[c])
    
        print(["Best", "Worst"][p], avg_positions)
    
    # print(sizes[(sizes["Order"] == sorted.iloc[0]["Order"]) &\
    #         (sizes["Mult_combined"] == sorted.iloc[0]["Mult_combined"]) &\
    #     #   (sizes["Mult_combined"] == sorted.iloc[0]["Mult_combined"]) &\
    #       (sizes["Other_Order"] == sorted.iloc[0]["Other_Order"]) &\
    #       (sizes["Generics_First"] == sorted.iloc[0]["Generics_First"])].head(1000))
    
    