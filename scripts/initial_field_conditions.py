import numpy as np
from scripts.velocity_field import space_evolution_field
from scripts.common.files import write_points_file, write_field_velocity_file
from scripts.common.utils import clear_directory
import os






def generate(dict, path, cell_centres):

    print(len(cell_centres))
    print(len(cell_centres[:,1]))

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


    for i in range(len(xp)):
        write_field_velocity_file(u_space[:,:,i].flatten(), v_space[:,:,i].flatten(), w_space[:,:,i].flatten(), t, folder_path)











