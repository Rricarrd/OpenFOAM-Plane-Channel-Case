import numpy as np
import matplotlib.pyplot as plt
from scripts.common.orr_sommerfeld_solution import solve_os_equation

########################## TIME EVOLUTION INLET ##########################
def time_evolution_inlet(
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
):
    # --- Calculate Orr-Sommerfeld solution ---
    (
        u2d,
        v2d,
        w2d,
        u3dp,
        v3dp,
        w3dp,
        u3dm,
        v3dm,
        w3dm,
        om2d,
        om3dp,
        om3dm,
    ) = solve_os_equation(
        N,
        alp2d,
        alp3d,
        beta,
        R,
        n3d,
        n2d,
        Np,
    )

    # --- Time evolution ---
    timesteps = int(tEnd / dt)
    u_time = np.zeros((len(yp), len(zp), timesteps))
    v_time = np.zeros((len(yp), len(zp), timesteps))
    w_time = np.zeros((len(yp), len(zp), timesteps))
    U_time = np.zeros((len(yp), len(zp), timesteps))

    for i, t in enumerate(tVals):
        # Calculate time instant
        u_hat, v_hat, w_hat = evaluate_velocity_inlet(
                                A2d,
                                A3d,
                                beta,
                                om2d,
                                om3dp,
                                om3dm,
                                yp,
                                zp,
                                t,
                                speed_factor,
                                u2d,
                                u3dp,
                                u3dm,
                                v2d,
                                v3dp,
                                v3dm,
                                w2d,
                                w3dp,
                                w3dm,
                                )

        # Total velocities
        u_time[:, :, i] = np.reshape(u_hat + U_lam, (len(yp), len(zp)))
        v_time[:, :, i] = np.reshape(v_hat, (len(yp), len(zp)))
        w_time[:, :, i] = np.reshape(w_hat, (len(yp), len(zp)))
        U_time[:, :, i] = np.sqrt(
            u_time[:, :, i] ** 2 + v_time[:, :, i] ** 2 + w_time[:, :, i] ** 2
        )

    return u_time, v_time, w_time, U_time

########################## TIME INSTANT INLET ##########################
def time_instant_inlet(
    N,
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
    t,
    zi,
    plot=False,
):
    # --- Calculate Orr-Sommerfeld solution ---
    (
        u2d,
        v2d,
        w2d,
        u3dp,
        v3dp,
        w3dp,
        u3dm,
        v3dm,
        w3dm,
        om2d,
        om3dp,
        om3dm,
    ) = solve_os_equation(
        N,
        alp2d,
        alp3d,
        beta,
        R,
        n3d,
        n2d,
        Np,
    )
    
    if plot:

        ## 3D
        fig, ax = plt.subplots()
        ax.set_xlabel("u")
        ax.set_ylabel("y")
        ax.set_title("3D Orr-Sommerfeld Velocity Profile")
        ax.grid(True)
        ax.plot(u3dp, yp, label="u")
        ax.plot(v3dp, yp, label="v")
        ax.plot(w3dp, yp, label="w")
        ax.legend()

        ## 2D
        fig, ax = plt.subplots()
        ax.set_xlabel("u")
        ax.set_ylabel("y")
        ax.set_title("2D Orr-Sommerfeld Velocity Profile")
        ax.grid(True)
        ax.plot(u2d, yp, label="u")
        ax.plot(v2d, yp, label="v")
        ax.plot(w2d, yp, label="w")
        ax.legend()

    #####################  PLOTTING  #####################
    u_hat, v_hat, w_hat = evaluate_velocity_inlet(
        A2d,
        A3d,
        beta,
        om2d,
        om3dp,
        om3dm,
        yp,
        zp,
        t,
        speed_factor,
        u2d,
        u3dp,
        u3dm,
        v2d,
        v3dp,
        v3dm,
        w2d,
        w3dp,
        w3dm,
    )

    # Total velocities
    u = U_lam + u_hat
    v = v_hat
    w = w_hat
    U = np.sqrt(u**2 + v**2 + w**2)
    U = np.transpose(np.reshape(U, (len(yp), len(zp))))

    return u, v, w, U


def velocity_inlet(
    A2d,
    A3d,
    hat_u_r2d,
    hat_u_r3d_p,
    hat_u_r3d_m,
    beta,
    om2d,
    om3dp,
    om3dm,
    yp,
    zp,
    t,
):
    real_val = np.zeros((len(yp), len(zp)), dtype=float)

    for j, z in enumerate(zp):
        # 2D
        term_2d = A2d * (hat_u_r2d * np.exp(-1j * om2d * t))

        # 3D positive
        term_3dp = 0.5 * A3d * (hat_u_r3d_p * np.exp(1j * (beta * z - om3dp * t)))

        # 3D negative
        term_3dm = 0.5 * A3d * (hat_u_r3d_m * np.exp(1j * (beta * z - om3dm * t)))

        # Sum up the complex terms
        complex_val = term_2d + term_3dp + term_3dm

        # Take the real part of the vector
        real_val[j] = np.real(complex_val)

    real_val = real_val.flatten()

    return real_val


def evaluate_velocity_inlet(
    A2d,
    A3d,
    beta,
    om2d,
    om3dp,
    om3dm,
    yp,
    zp,
    t,
    speed_factor,
    u2d,
    u3dp,
    u3dm,
    v2d,
    v3dp,
    v3dm,
    w2d,
    w3dp,
    w3dm,
):
    u_hat = velocity_inlet(
        A2d,
        A3d,
        u2d,
        u3dp,
        u3dm,
        beta,
        om2d * speed_factor,
        om3dp * speed_factor,
        om3dm * speed_factor,
        yp,
        zp,
        t,
    )

    v_hat = velocity_inlet(
        A2d,
        A3d,
        v2d,
        v3dp,
        v3dm,
        beta,
        om2d * speed_factor,
        om3dp * speed_factor,
        om3dm * speed_factor,
        yp,
        zp,
        t,
    )

    w_hat = velocity_inlet(
        A2d,
        A3d,
        w2d,
        w3dp,
        w3dm,
        beta,
        om2d * speed_factor,
        om3dp * speed_factor,
        om3dm * speed_factor,
        yp,
        zp,
        t,
    )

    return u_hat, v_hat, w_hat
