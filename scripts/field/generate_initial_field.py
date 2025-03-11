import numpy as np
from scripts.field.velocity_field_functions import space_evolution_field
from scripts.common.files import write_points_file
from scripts.common.utils import clear_directory
import os






def generate(dict, path, cell_centres):

    # --- File ---
    subdirectories = "constant//fieldData"
    folder_path = os.path.join(path, subdirectories)
    
    print("Clearing directory...")
    clear_directory(folder_path)
    
    print("Clearing directory... Done")

    # --- Parameters ---
    N = dict["N"]
    H = dict["H2"]
    W = dict["W"]
    L = dict["L"]
    nx = dict["nx"]
    ny = dict["ny"]
    nz =  dict["nz"]
    yp = np.linspace(0, H, ny - 1)
    zp = np.linspace(0, W, nz - 1)
    xp = np.linspace(0, L, nx - 1)
    t = 0

    # Poiseuille Flow
    Umax = dict["Ucl"]
    para = np.transpose((4.0 * Umax / (H * H)) * yp * (H - yp))
    U_lam = np.reshape(np.tile(para, len(zp)), (len(yp), len(zp)))

    # Unstable K-Type Flow (Orr Sommerfield Solution imposing alpha and beta)
    beta = dict["beta_3D"]  # beta parameter
    A2d = dict["A_2D"]/100*Umax
    A3d = dict["A_3D"]/100*Umax
    R = dict["Reb"]
    alp2d=dict["alpha_2D"]
    alp3d=dict["alpha_3D"]
    n3d = dict["n_3D"]
    n2d = dict["n_2D"]
    Np = dict["Np"]


    # Time evolution
    print("TS Waves inlet calculation...")
    u_space, v_space, w_space, U_space = space_evolution_field(
        N,
        yp,
        zp,
        U_lam,
        alp2d,
        alp3d,
        beta,
        A2d,
        A3d,
        R,
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

    u = u.swapaxes(0, 2).ravel()
    v = v.swapaxes(0, 2).ravel()
    w = w.swapaxes(0, 2).ravel()

    data = np.column_stack((u, v, w))
    file_path_t = os.path.join(folder_path, f"{t:.3f}")
    file_path_u = os.path.join(file_path_t, "U")
    print(file_path_u)
    os.mkdir(file_path_t)
    with open(file_path_u, 'w') as f:
        f.write('(\n')
        for row in data:
            f.write(f"({row[0]} {row[1]} {row[2]})\n")
        f.write(')\n')








