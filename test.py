import os
import pathlib
import sys
import argparse

current_path = pathlib.Path().resolve() # Get current path
parent_path = pathlib.Path().resolve().parent # Get parent path
sys.path.append(str(parent_path)) # Add to python path to access scripts folder
type = "temporal"

# Now import the scripts folder
from scripts import temporal_inlet_conditions, initial_field_conditions
from scripts.common import parsing

parameters_file_name = f"default.parameters"

print(f"Getting values from {parameters_file_name}")
parsed_data = parsing.parse_foam_file(os.path.join(current_path,parameters_file_name))


# Generating the corresponding initial conditions
if type == "spatial":
    # Generate time varying inlet for spatial changing simulation
    temporal_inlet_conditions.generate(parsed_data,current_path) 

elif type == "temporal":
    # Generate spatailly varying field for the time changing simulation
    initial_field_conditions.generate(parsed_data,current_path)

else:
    print("Incorrect type initialization. Choose either inletBC or initialField")
