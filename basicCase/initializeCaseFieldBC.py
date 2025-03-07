import os
import pathlib
import sys
import argparse

current_path = Path.cwd() # Get current path
sys.path.append(current_path) # Add to python path to access scripts folder

# Now import the scripts folder
from scripts import parsing, temporal_inlet_conditions, initial_field_conditions

# Parse CLI commands
parser = argparse.ArgumentParser(description="Initialization Python script for the planeChannel turbulent transition case")
parser.add_argument("type", type=str, help="Type of initialization: either inletBC or initialField")
parser.add_argument("parameters_file", type=str, help="Parameters file name", required=False)
args = parser.parse_args()

# Parse data from a .parameters file
if args.parameters_file:
    parameters_file_name = f"{args.parameters_file}.parameters"
else:
    parameters_file_name = f"default.parameters"

print(f"Getting values from {parameters_file_name}")

parsed_data = parsing.parse_foam_file(os.path.join(path,parameters_file_name))


# Generating the corresponding initial conditions
if args.type == "inletBC":
    temporal_inlet_conditions.generate(parsed_data,path)

elif args.type == "initialField":
    initial_field_conditions.generate(parsed_data,path)

else:
    print("Incorrect type initialization. Choose either inletBC or initialField)
