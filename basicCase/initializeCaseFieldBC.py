import os
import pathlib
import sys
import argparse
import openfoamparser as Ofpp



current_path = pathlib.Path().resolve() # Get current path
parent_path = pathlib.Path().resolve().parent # Get parent path
sys.path.append(str(parent_path)) # Add to python path to access scripts folder

# Now import the scripts folder
from scripts import temporal_inlet_conditions, initial_field_conditions
from scripts.common import parsing

# Parse CLI commands
parser = argparse.ArgumentParser(description="Initialization Python script for the planeChannel turbulent transition case")
parser.add_argument("type", type=str, help="Type of initialization: either inletBC or initialField")
parser.add_argument("parameters_file", type=str, help="Parameters file name")
args = parser.parse_args()

# Parse data from a .parameters file
if args.parameters_file:
    parameters_file_name = f"{args.parameters_file}.parameters"
else:
    parameters_file_name = f"default.parameters"

print(f"Getting values from {parameters_file_name}")
parsed_data = parsing.parse_foam_file(os.path.join(current_path,parameters_file_name))

# Extracting current mesh cell centres
cell_centres=Ofpp.parse_internal_field('0/C')


# Generating the corresponding initial conditions
if args.type == "spatial":
    # Generate time varying inlet for spatial changing simulation
    temporal_inlet_conditions.generate(parsed_data,current_path,cell_centres) 

elif args.type == "temporal":
    # Generate spatailly varying field for the time changing simulation
    initial_field_conditions.generate(parsed_data,current_path,cell_centres)

else:
    print("Incorrect type initialization. Choose either inletBC or initialField")
