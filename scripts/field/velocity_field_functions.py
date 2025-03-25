import numpy as np
import matplotlib.pyplot as plt
from scripts.common.orr_sommerfeld_solution import solve_os_equation
from scipy.interpolate import interp1d

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
    Re,
    n3d,
    n2d,
    Np,
    t,
    xp,
    y_cell_centres
):
    # --- Calculate Orr-Sommerfeld solution ---
    (
        yp_orr,
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
        Re,
        n3d,
        n2d,
        Np
    )

    # Adjusting coordinates of orr positions
    yp_orr = yp_orr + 1

    # print("Example of interpolated velocity field:")
    # print(f"u2d before: {u2d}")
    # plt.plot(yp_orr, np.real(u2d), label="Real")
    # plt.plot(yp_orr, np.imag(u2d), label="Imag")

    # --- Interpolate velocity field to the grid ---
    kind = 'linear'
    u2d = interpolate_u(u2d,yp_orr,y_cell_centres, kind)
    v2d = interpolate_u(v2d,yp_orr,y_cell_centres, kind)
    w2d = interpolate_u(w2d,yp_orr,y_cell_centres, kind)

    u3dp = interpolate_u(u3dp,yp_orr,y_cell_centres, kind)
    v3dp = interpolate_u(v3dp,yp_orr,y_cell_centres, kind)
    w3dp = interpolate_u(w3dp,yp_orr,y_cell_centres, kind)

    u3dm = interpolate_u(u3dm,yp_orr,y_cell_centres, kind)
    v3dm = interpolate_u(v3dm,yp_orr,y_cell_centres, kind)
    w3dm = interpolate_u(w3dm,yp_orr,y_cell_centres, kind)

    
    # print(f"With interpolation u2d: {u2d}")
    # plt.plot(y_cell_centres, np.real(u2d), label="Real")
    # plt.plot(y_cell_centres, np.imag(u2d), label="Imag")
    # plt.legend(["Real pre interp", "Imag pre interp", "Real post interp", "Imag post interp"])
    # plt.xlabel("u")
    # plt.ylabel("y")
    # plt.show()

    
    
    
    # --- Space evolution ---
    ny2 = int(len(y_cell_centres)/2)
    u1_space = np.zeros((len(zp), ny2, len(xp)))
    v1_space = np.zeros((len(zp), ny2,  len(xp)))
    w1_space = np.zeros((len(zp), ny2,  len(xp)))
    U1_space = np.zeros((len(zp), ny2,  len(xp)))

    u2_space = np.zeros((len(zp), ny2,  len(xp)))
    v2_space = np.zeros((len(zp), ny2,  len(xp)))
    w2_space = np.zeros((len(zp), ny2,  len(xp)))
    U2_space = np.zeros((len(zp), ny2,  len(xp)))

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
        u1_space[:, :, i] = u_hat[:,0:ny2] + U_lam[:,0:ny2]
        v1_space[:, :, i] = v_hat[:,0:ny2]
        w1_space[:, :, i] = w_hat[:,0:ny2]
        U1_space[:, :, i] = np.sqrt(
            u1_space[:, :, i] ** 2 + v1_space[:, :, i] ** 2 + w1_space[:, :, i] ** 2
        )

        u2_space[:, :, i] = u_hat[:,ny2:ny2*2] + U_lam[:,ny2:ny2*2]
        v2_space[:, :, i] = v_hat[:,ny2:ny2*2]
        w2_space[:, :, i] = w_hat[:,ny2:ny2*2]
        U2_space[:, :, i] = np.sqrt(
            u2_space[:, :, i] ** 2 + v2_space[:, :, i] ** 2 + w2_space[:, :, i] ** 2
        )


    # Total velocities
    u1 = u1_space
    v1 = v1_space
    w1 = w1_space
    u2 = u2_space
    v2 = v2_space
    w2 = w2_space


    return u1, v1, w1, u2, v2, w2

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
    coords = np.zeros((len(yp), len(zp)), dtype=float)

    for j, z in enumerate(zp):
        # 2D
        term_2d = A2d * (hat_u_r2d * np.exp(1j * (alp2d * x - ome2d * t)))

        # 3D positive
        term_3dp = 0.5 * A3d * (hat_u_r3d_p * np.exp(1j * (beta * z + alp3d*x - ome3dp * t)))

        # 3D negative
        term_3dm = 0.5 * A3d * (hat_u_r3d_m * np.exp(1j * (beta * z + alp3d*x - ome3dm * t)))

        # Sum up the complex terms
        complex_val = term_2d + term_3dp + term_3dm

        # Take the real part of the vector
        real_val[j,:] = np.real(complex_val)
 
    # print(real_val)
    # plt.contourf(zp, yp, real_val)
    # plt.show()
    return real_val


def interpolate_u(u,yp,y_cell_centres, kind='cubic'):
    fu_real = interp1d(yp, np.real(u), kind)
    fu_imag = interp1d(yp, np.imag(u), kind) 
    u_interp = fu_real(y_cell_centres) + 1j*fu_imag(y_cell_centres)
    return u_interp
