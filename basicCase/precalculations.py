import math
import pathlib
import sys
import argparse
import os
import openfoamparser as Ofpp



def get_parameters():
    current_path = pathlib.Path().resolve() # Get current path
    parent_path = pathlib.Path().resolve().parent # Get parent path
    sys.path.append(str(parent_path)) # Add to python path to access scripts folder


    # Now import the scripts folder
    from scripts.common import parsing

    # Parse CLI commands
    parser = argparse.ArgumentParser(description="Initialization Python script for the planeChannel turbulent transition case")
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
    cell_centres=Ofpp.parse_internal_field(f'{str(current_path)}/constant/C')

    return parsed_data, cell_centres


parsed_data, cell_centres = get_parameters()

# Fluid parameters
rho = parsed_data["rho"]
Re_b = parsed_data["Re_b"]

nu = parsed_data["nu"]

# Channel parameters
H = parsed_data["H"]        # Channel total height [m]               
h = H/2                     # Channel height (Characteristic length) [m]
W = parsed_data["W"]           # Channel width [m]
L = parsed_data["L"]          # Channel length [m]

# Cell counts
nx = parsed_data["nx"]
ny = parsed_data["ny"]
nz = parsed_data["nz"]

# Size increase gradient
Rx = 1 + 1e-12
Ry = parsed_data["gradient"]
Rz = 1 + 1e-12

print("######################### MESH CALCULATIONS #######################\n")

# ----------------- DESIRED MESH SIZING -----------------
print("############ Calculations of the desired mesh ############\n")

# y with Ret
print("# Imposing shear Reynolds (Ret)")
Ret = 100
yplus = 1
print(f"Considering Ret is {Ret}")

# 1 - Ut calculation using Ret
Ut = Ret * nu / h

# 2 - y first cell
yRet = nu * yplus / Ut
print(f"Yielding a first cell height of {yRet:.3f} m or {yRet * 1000:.3f} mm\n")

# ----------------- CURRENT MESH CALCULATIONS -----------------
print("############ Calculations of the current mesh ############")
print("# Current plane channel mesh element sizing")

# Geometric progression factors
rx = Rx ** (-1 / (nx - 1))
ry = Ry ** (-1 / (ny - 1))
rz = Rz ** (-1 / (nz - 1))

def final_element_size(L, r, N):
    """
    Calculate the smallest cell size at the wall using the geometric progression formula.
    """
    return L * (r - 1) * (r ** (N - 1)) / (r ** N - 1)

# Smallest cell sizes [m]
mincell_dx = final_element_size(L, rx, nx)
mincell_dy = final_element_size(H, ry, ny)
mincell_dz = final_element_size(W, rz, nz)
print(f"The smallest cells (touching the wall) are dx = {mincell_dx * 1000:.3f} mm, "
      f"dy = {mincell_dy * 1000:.3f} mm and dz = {mincell_dz * 1000:.3f} mm")

# Biggest cell sizes [m]
maxcell_dx = Rx * mincell_dx
maxcell_dy = Ry * mincell_dy
maxcell_dz = Rz * mincell_dz
print(f"The biggest cells (center of channel) are dx = {maxcell_dx * 1000:.3f} mm, "
      f"dy = {maxcell_dy * 1000:.3f} mm and dz = {maxcell_dz * 1000:.3f} mm\n")

print("# Current plane channel mesh element sizing")
mincell_xplus = mincell_dx * Ut / nu
mincell_yplus = mincell_dy * Ut / nu
mincell_zplus = mincell_dz * Ut / nu
print(f"The smallest cells (touching the wall) are xplus = {mincell_xplus:.3f}, "
      f"yplus = {mincell_yplus:.3f} and zplus = {mincell_zplus:.3f}")

print("# Current plane channel mesh element sizing")
maxcell_xplus = maxcell_dx * Ut / nu
maxcell_yplus = maxcell_dy * Ut / nu
maxcell_zplus = maxcell_dz * Ut / nu
print(f"The smallest cells (touching the wall) are xplus = {maxcell_xplus:.3f}, "
      f"yplus = {maxcell_yplus:.3f} and zplus = {maxcell_zplus:.3f}")


