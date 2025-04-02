import os
import pickle
import matplotlib.pyplot as plt
import json
from IPython.lib.pretty import pprint

# Get the current directory
current_directory = os.getcwd()

# List all folders in the current directory
folders = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]


# Plots dictionary
plots_names = {
    'InOut': '1',
    'Residuals': '2',
    'Residuals': '3',
    'Global': '4',
    'Residuals': '5',
    'Global': '6',
    'Courant': '7',
    'ReTau': '8',
}

# pickled_file = "Gnuplotting.analyzed/pickledPlots"
pickled_file = "Gnuplotting.analyzed/pickledStartData"
# pickled_file = "Decomposer.analyzed/pickledData"

# Iterate through each folder and check for the pickled file
for folder in folders:
    pickled_file_path = os.path.join(current_directory, folder, pickled_file)
    print(f"Checking folder: {folder}")
    print(f"Pickled file path: {pickled_file_path}")

    if folder[0].isdigit():
        try:
            with open(pickled_file_path, "rb") as file:
                data = pickle.load(file)


                pprint(data, max_seq_length=100)
                

        except KeyError as e:
            print(f"KeyError: {e} in folder: {folder}")
            
        
