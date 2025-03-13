import numpy as np
from scripts.field.velocity_field_functions import space_evolution_field
from scripts.common.files import write_points_file
from scripts.common.utils import clear_directory
from scripts.common.orr_sommerfeld_solution import parameters
import os




def generate(dict, path, cell_centres):

    # --- File ---
    subdirectories = "constant//fieldData"
    folder_path = os.path.join(path, subdirectories)
    
    print("Clearing directory...")
    clear_directory(folder_path)
    print("Clearing directory... Done")

    print("Generating parameter values from .parameters file...")
    ny, yp, zp, U_lam, alp2d, alp3d, beta, A2d, A3d, Re_b, n3d, n2d, Np, t, xp = parameters(dict)


    # Time evolution
    print("TS Waves inlet calculation...")
    u_space, v_space, w_space, U_space = space_evolution_field(
        ny,
        yp,
        zp,
        U_lam,
        alp2d,
        alp3d,
        beta,
        A2d,
        A3d,
        Re_b,
        n3d,
        n2d,
        Np,
        t,
        xp
    )
    
    print("TS Waves inlet calculation... Done")
    print("Writing velocity files...")

    write_field_velocity_file(u_space, v_space, w_space, t, folder_path)


def write_field_velocity_file(u, v, w, t, folder_path):

    # Then the data is ravelled (or flattened in a 1D array) following
    # the order of the arrays
    u = u.ravel()
    v = v.ravel()
    w = w.ravel()

    data = np.column_stack((u, v, w))

    file_path_t = os.path.join(folder_path, f"{t:.3f}")
    file_path_u = os.path.join(file_path_t, "U")
    print(file_path_u)
    os.mkdir(file_path_t)
    with open(file_path_u, 'w') as f:
        f.write(f'internalField nonuniform List<vector>\n(\n')
        for row in data:
            f.write(f"({row[0]} {row[1]} {row[2]})\n")
        f.write(');\n')








