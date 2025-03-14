import openfoamparser as Ofpp
import numpy as np
import sys
import os
import matplotlib.pyplot as plt 
import pathlib
import re

def get_directories(directory):
    # Regex to match valid decimal folder names (e.g., 0.99, 1.12, 3.0, etc.)
    number_pattern = re.compile(r'^\d+(\.\d+)?$')

    # Get folders with valid decimal names and sort them numerically
    folders = [
        f for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f)) and number_pattern.match(f) and f != '0'
    ]

    # Sort by numeric value
    return sorted(folders, key=lambda x: float(x))

def plot_ret(parsed_data, current_path):

    # Path
    current_path = str(current_path)
    print(f"Current path: {current_path}")

    # Parameters
    H2 = parsed_data["H"]/2
    nu = 1/parsed_data["Re_lam"]
    ret = []

    directories_list = get_directories(current_path)
    directories_list.pop(0)

    for i in directories_list:
        w = Ofpp.parse_boundary_field(f'{current_path}/{i}/wallShearStress')
        top_values = w[b"top"][b"value"]
        bot_values = w[b"bottom"][b"value"]

        tau = np.abs(np.average(top_values+bot_values))

        ut = np.sqrt(tau)

        ret.append(ut*H2/nu)

    print(f"Re_tau values: {list(enumerate([float(i) for i in ret]))}")


    plt.plot(ret)
    plt.xlabel('Time step')
    plt.ylabel('Re_tau')
    plt.title('Re_tau evolution')
    plt.show()

if __name__ == "__main__":

    parent_path = pathlib.Path().resolve().parent # Get parent path
    sys.path.append(str(parent_path)) # Add to python path to access scripts folder

    # Now import the scripts folder
    from scripts.common import parsing
    
    current_path = os.path.dirname(os.path.realpath(__file__))
    parsed_data = parsing.parse_foam_file(f"{current_path}/default.parameters")
    plot_ret(parsed_data, current_path)
