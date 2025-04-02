import os
import pickle
import matplotlib.pyplot as plt
import json
from IPython.lib.pretty import pprint

# Get the current directory
current_directory = os.getcwd()

# List all folders in the current directory
folders = [name for name in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, name))]

# Print the folder names
print(folders)


# Create a simple matplotlib figure
fig, ax = plt.subplots()
ax.set_title("Sample Plot")
ax.set_xlabel("Time")
ax.set_ylabel("Ret")

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

# Iterate through each folder and check for the pickled file
for folder in folders:
    pickled_file_path = os.path.join(current_directory, folder, "Gnuplotting.analyzed/pickledPlots")
    print(f"Checking folder: {folder}")
    print(f"Pickled file path: {pickled_file_path}")

    if folder[0].isdigit() and os.path.exists(pickled_file_path):
        try:
            with open(pickled_file_path, "rb") as file:
                data = pickle.load(file)

            

                ret = data[plots_names['ReTau']]['values']['avg']
                times = data[plots_names['ReTau']]['times']


                ax.plot(times, ret, label=folder)
                

        except KeyError as e:
            print(f"KeyError: {e} in folder: {folder}")
            
        
plt.legend()
plt.show()
