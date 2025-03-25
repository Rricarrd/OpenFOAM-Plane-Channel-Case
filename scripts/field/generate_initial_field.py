import numpy as np
from scripts.field.velocity_field_functions import space_evolution_field
from scripts.common.files import write_points_file
from scripts.common.utils import clear_directory
from scripts.common.orr_sommerfeld_solution import parameters
from scripts.common.mesh import get_mesh_y_positions
import os
import matplotlib.pyplot as plt




def generate(dict, path, cell_centres):

    # --- File ---
    subdirectories = "constant//fieldData"
    folder_path = os.path.join(path, subdirectories)

    # Other
    only_perturbations = False
    
    print("Clearing directory...")
    clear_directory(folder_path)
    print("Clearing directory... Done")

    print("Generating parameter values from .parameters file...")
    ny, nx, nz, yp, zp, alp2d, alp3d, beta, A2d, A3d, Re_lam, n3d, n2d, Np, t, xp, Ucl, H = parameters(dict)


    # Get y position of the cell centres from the mesh
    y_cell_centres = get_mesh_y_positions(cell_centres, nx, ny)

    # Calculating U laminar for the grid
    if only_perturbations:
        para = y_cell_centres*0
    else:
        para = ((4.0 * Ucl / (H * H)) * y_cell_centres * (H - y_cell_centres))

    U_lam_slice = np.reshape(np.tile(para, len(zp)), (len(yp), len(zp)))

    # Time evolution
    print("TS Waves inlet calculation...")
    u1_space, v1_space, w1_space, u2_space, v2_space, w2_space = space_evolution_field(
        ny+1,
        yp,
        zp,
        U_lam_slice,
        alp2d,
        alp3d,
        beta,
        A2d,
        A3d,
        Re_lam,
        n3d,
        n2d,
        Np,
        t,
        xp,
        y_cell_centres
    )


    print("TS Waves inlet calculation... Done")
    print("Writing velocity files...")

    write_field_velocity_file(u1_space, v1_space, w1_space, t, folder_path, type="start")
    write_field_velocity_file(u2_space, v2_space, w2_space, t, folder_path, type="finish")

def write_field_velocity_file(u, v, w, t, folder_path,type):

    # Then the data is ravelled (or flattened in a 1D array) following
    # the order of the arrays
    u = u.ravel()
    v = v.ravel()
    w = w.ravel()

    data = np.column_stack((u, v, w))

    file_path_t = os.path.join(folder_path, f"{t:.3f}")
    file_path_u = os.path.join(file_path_t, "U")

    

    if type =="start":
        os.mkdir(file_path_t)
        with open(file_path_u, 'w') as f:
            f.write(f'internalField nonuniform List<vector>\n(\n')
            for row in data:
                f.write(f"({row[0]} {row[1]} {row[2]})\n")

    if type =="finish":
        with open(file_path_u, 'a') as f:
            for row in data:
                f.write(f"({row[0]} {row[1]} {row[2]})\n")
            f.write(');\n')








