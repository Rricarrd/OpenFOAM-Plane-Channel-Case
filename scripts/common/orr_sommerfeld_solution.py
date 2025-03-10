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
