import numpy as np
from scripts.inlet.velocity_inlet_functions import time_evolution_inlet
from scripts.common.files import write_points_file
from scripts.common.utils import clear_directory
import os






def generate(dict, path, cell_centres):
    # --- File ---
    subdirectories = "constant//boundaryData//inlet"
    folder_path = os.path.join(path, subdirectories)
    
    print("Clearing directory...")
    clear_directory(folder_path)
    
    print("Clearing directory... Done")
    
    # --- Time parameters ---
    tStart = dict["tStart"]
    tEnd = dict["tEnd"]
    dt = dict["dt"]
    tVals = np.arange(tStart, tEnd, dt)
    speed_factor = 1

    # --- Parameters ---
    H = dict["H"]
    L = dict["L"]
    W = dict["W"]
    yp = np.linspace(0, H, N - 1)
    zp = np.linspace(0, W, N - 1)

    # Poiseuille Flow
    Umax = dict["Ucl"]
    para = np.transpose((4.0 * Umax / (H * H)) * yp * (H - yp))
    U_lam = np.tile(para, len(zp))

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


    # Get points at the inlet
    write_points_file(yp,zp,folder_path)


    # Time evolution
    print("TS Waves inlet calculation...")
    u_time, v_time, w_time, U_time = time_evolution_inlet(
        N,
        tEnd,
        dt,
        speed_factor,
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
        tVals,
    )
    print("TS Waves inlet calculation... Done")
    print("Writing velocity files...")
    for i, t in enumerate(tVals):
        write_inlet_velocity_file(u_time[:,:,i].flatten(), v_time[:,:,i].flatten(), w_time[:,:,i].flatten(), t, folder_path)
    print("Writing velocity files... Done")



def write_inlet_velocity_file(u, v, w, t, folder_path):
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







