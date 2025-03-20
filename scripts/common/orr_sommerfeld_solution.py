import numpy as np
import matplotlib.pyplot as plt
from Orr_Sommerfeld.OS import Orr_Sommerfeld_Temporal as OSTemporal
from Orr_Sommerfeld.OS import Orr_Sommerfeld_Espacial as OSEspacial


def solve_os_equation(
    N,
    alp2d,
    alp3d,
    beta,
    R,
    n3d,
    n2d,
    Np,
):
    # --- Calculate Orr-Sommerfeld solution ---
    lam3dp, u3dp, v3dp, w3dp = OSTemporal(N, R, alp3d, beta, n3d, Np)
    lam3dm, u3dm, v3dm, w3dm = OSTemporal(N, R, alp3d, -beta, n3d, Np)
    lam2d, u2d, v2d, w2d = OSTemporal(N, R, alp2d, 0, n2d, Np)

    # --- Calculate frequency for the most unstable mode ---
    om2d = -lam2d[np.argmax(np.imag(lam2d))] / 1j 
    om3dp = -lam3dp[np.argmax(np.imag(lam3dp))] / 1j
    om3dm = -lam3dm[np.argmax(np.imag(lam3dm))] / 1j

    # --- Plotting ---
    # Velocity profile for OSrr-Sommerfield solution
    u3dp = u3dp.flatten()
    v3dp = v3dp.flatten()
    w3dp = w3dp.flatten()

    u3dm = u3dm.flatten()
    v3dm = v3dm.flatten()
    w3dm = w3dm.flatten()

    # Velocity profile for Orr-Sommerfield solution
    u2d = u2d.flatten()
    v2d = v2d.flatten()
    w2d = w2d.flatten()

    return u2d, v2d, w2d, u3dp, v3dp, w3dp, u3dm, v3dm, w3dm, om2d, om3dp, om3dm

def parameters(dict):
    # --- Parameters ---
    H = dict["H"]
    W = dict["W"]
    L = dict["L"]
    nx = dict["nx"]
    ny = dict["ny"]
    nz =  dict["nz"]
    yp = np.linspace(0, H, ny)
    zp = np.linspace(0, W, nz)
    xp = np.linspace(0, L, nx)
    t = 0

    # Poiseuille Flow
    Ucl = dict["Ucl"]

    # Reynolds number of the poiseuille flow
    Re_lam = dict["Re_lam"]
    Re_cl = Re_lam * Ucl
    Re_b = 2/3*Re_lam

    # Unstable K-Type Flow (Orr Sommerfield Solution imposing alpha and beta)
    beta = dict["beta_3D"]  # beta parameter
    A2d = dict["A_2D"]/100*Ucl
    A3d = dict["A_3D"]/100*Ucl
    alp2d = dict["alpha_2D"]
    alp3d = dict["alpha_3D"]
    n3d = dict["n_3D"]
    n2d = dict["n_2D"]
    Np = dict["Np"]

    return ny, nx, nz, yp, zp, alp2d, alp3d, beta, A2d, A3d, Re_lam, n3d, n2d, Np, t, xp, Ucl, H
