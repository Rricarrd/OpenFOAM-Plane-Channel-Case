import numpy as np
import matplotlib.pyplot as plt
from scripts.common.orr_sommerfeld_solution import solve_os_equation

########################## MAIN FUNCTIONS: TIME INSTANT FIELD ##########################
def space_evolution_field(
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
    
    # --- Space evolution ---
    u_space = np.zeros((len(yp), len(zp), len(xp)))
    v_space = np.zeros((len(yp), len(zp), len(xp)))
    w_space = np.zeros((len(yp), len(zp), len(xp)))
    U_space = np.zeros((len(yp), len(zp), len(xp)))

    for i, x in enumerate(xp):
        u_hat, v_hat, w_hat = evaluate_velocity_field_slice(
            A2d,
            A3d,
            beta,
            om2d,
            om3dp,
            om3dm,
            alp2d,
            alp3d,
            yp,
            zp,
            x,
            u2d,
            u3dp,
            u3dm,
            v2d,
            v3dp,
            v3dm,
            w2d,
            w3dp,
            w3dm,
            t
        )

        # Total velocities
        u_space[:, :, i] = u_hat #+ U_lam
        v_space[:, :, i] = v_hat
        w_space[:, :, i] = w_hat
        U_space[:, :, i] = np.sqrt(
            u_space[:, :, i] ** 2 + v_space[:, :, i] ** 2 + w_space[:, :, i] ** 2
        )

        # fig, ax = plt.subplots()
        # ax.set_xlabel("yp")
        # ax.set_ylabel("zp")
        # ax.set_title("3D Orr-Sommerfeld Velocity Profile")
        # ax.grid(True)
        # ax.contourf(zp, yp, np.transpose(u_space[:, :, i]), label="u")
        # ax.legend()
        # fig.show()

    # Total velocities
    u = u_hat
    v = v_hat
    w = w_hat
    U = np.sqrt(u**2 + v**2 + w**2)
    # U = np.transpose(np.reshape(U, (len(yp), len(zp))))
    return u, v, w, U

###################################

def evaluate_velocity_field_slice(
    A2d,
    A3d,
    beta,
    om2d,
    om3dp,
    om3dm,
    alp2d,
    alp3d,
    yp,
    zp,
    x,
    u2d,
    u3dp,
    u3dm,
    v2d,
    v3dp,
    v3dm,
    w2d,
    w3dp,
    w3dm,
    t,
):
    
    """
    Calculate all velocity components (u,v,w) a rectangular section of the velocity field at
    a given x position and for a given
    t time
    """
    u_hat = velocity_section(
        A2d,
        A3d,
        u2d,
        u3dp,
        u3dm,
        beta,
        alp2d,
        alp3d,
        om2d,
        om3dp,
        om3dm,
        t,
        yp,
        zp,
        x
    )

    v_hat = velocity_section(
        A2d,
        A3d,
        v2d,
        v3dp,
        v3dm,
        beta,
        alp2d,
        alp3d,
        om2d,
        om3dp,
        om3dm,
        t,
        yp,
        zp,
        x,
    )

    w_hat = velocity_section(
        A2d,
        A3d,
        w2d,
        w3dp,
        w3dm,
        beta,
        alp2d,
        alp3d,
        om2d,
        om3dp,
        om3dm,
        t,
        yp,
        zp,
        x,
    )

    return u_hat, v_hat, w_hat

###################################

def velocity_section(
    A2d,
    A3d,
    hat_u_r2d,
    hat_u_r3d_p,
    hat_u_r3d_m,
    beta,
    alp2d,
    alp3d,
    ome2d,
    ome3dp,
    ome3dm,
    t,
    yp,
    zp,
    x,
):
    """
    Calculate a velocity component rectangular section of the velocity field at 
    a given x position and for a given t time.
    """

    real_val = np.zeros((len(yp), len(zp)), dtype=float)

    for j, y in enumerate(yp):
        # 2D
        term_2d = A2d * (hat_u_r2d * np.exp(1j * (alp2d * x - ome2d * t)))

        # 3D positive
        term_3dp = 0.5 * A3d * (hat_u_r3d_p * np.exp(1j * (beta * y + alp3d*x - ome3dp * t)))

        # 3D negative
        term_3dm = 0.5 * A3d * (hat_u_r3d_m * np.exp(1j * (beta * y + alp3d*x - ome3dm * t)))

        # Sum up the complex terms
        complex_val = term_2d + term_3dp + term_3dm

        # Take the real part of the vector
        real_val[j,:] = np.real(complex_val)


    return real_val



    # if plot:

    #     ## 3D
    #     fig, ax = plt.subplots()
    #     ax.set_xlabel("u")
    #     ax.set_ylabel("y")
    #     ax.set_title("3D Orr-Sommerfeld Velocity Profile")
    #     ax.grid(True)
    #     ax.plot(u3dp, yp, label="u")
    #     ax.plot(v3dp, yp, label="v")
    #     ax.plot(w3dp, yp, label="w")
    #     ax.legend()

    #     ## 2D
    #     fig, ax = plt.subplots()
    #     ax.set_xlabel("u")
    #     ax.set_ylabel("y")
    #     ax.set_title("2D Orr-Sommerfeld Velocity Profile")
    #     ax.grid(True)
    #     ax.plot(u2d, yp, label="u")
    #     ax.plot(v2d, yp, label="v")
    #     ax.plot(w2d, yp, label="w")
    #     ax.legend()