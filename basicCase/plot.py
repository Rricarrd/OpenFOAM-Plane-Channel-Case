import openfoamparser as Ofpp
import numpy as np
import sys
import os
import matplotlib.pyplot as plt 
import pathlib
import re
import argparse
 

def get_directories(directory):
    # Regex to match valid decimal folder names (e.g., 0.99, 1.12, 3.0, etc.)
    number_pattern = re.compile(r'^\d+(\.\d+)?$')

    # Get folders with valid decimal names and sort them numerically
    folders = [
        f for f in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, f)) and number_pattern.match(f) and f != '0'
    ]

    # Sort by numeric value
    sorted_list = sorted(folders, key=lambda x: float(x))
    sorted_list.pop(0)

    return sorted_list


def plot_ret(parsed_data, current_path):

    # Path
    current_path = str(current_path)
    print(f"Current path: {current_path}")

    # Parameters
    H2 = parsed_data["H"]/2
    nu = 1/parsed_data["Re_lam"]
    ret = []

    directories_list = get_directories(current_path)
    time = [float(i) for i in directories_list]

    for i in directories_list:

        try:
            ut = calculate_ut(current_path, i)
            ret.append(ut*H2/nu)
        except:
            print(f"Error calculating ut for time {i}. Skipping...")


    fig, ax = plt.subplots()
    ax.plot(time,ret)
    ax.set_xlabel(r'Time (s)', fontsize=12)
    ax.set_ylabel(r'$Re_{\tau}$', fontsize=12)
    ax.set_title(r'$Re_{\tau}$ Evolution', fontsize=14)
    ax.grid(True)
    fig.tight_layout()
    fig.savefig('plots/ret.png')
    
    

def plot_uplus_yplus(timestep, parsed_data, current_path,u_type):

    # Path
    current_path = str(current_path)
    print(f"Current path: {current_path}")

    # Parameters
    H = parsed_data["H"]
    H2 = parsed_data["H"]/2
    L = parsed_data["L"]
    W = parsed_data["W"]
    nu = 1/parsed_data["Re_lam"]
    nx = parsed_data["nx"] 
    ny = parsed_data["ny"]
    nz = parsed_data["nz"]

    # Precalculations
    dx = L/nx
    dy = H/ny
    dz = W/nz


    # Get times from the names of the folders
    directories_list = get_directories(current_path)
    
    # Select the time
    time = directories_list[timestep]

    # Get U field
    if u_type == "mean":
        U = Ofpp.parse_internal_field(f'{current_path}/{time}/UMean')
    else:
        U = Ofpp.parse_internal_field(f'{current_path}/{time}/U')

    # Get wall shear stress
    ut = calculate_ut(current_path, time)

    # Initialize arrays
    yplus = np.zeros(ny)
    uplus = np.zeros(ny)

    # Calculate average u
    average_u, average_v, average_w = calculate_slice_average(U, nx, ny, nz, type="vector")

    # Get y values
    ly = get_y_values(ny,nx,current_path, time)
    yplus = ly*ut/nu
    uplus = average_u/ut

    print(f"Some calculated values for time {time}:")
    print(f"ut: {ut}")
    print(f"average_u: {average_u[0:int(ny/2)]}")
    print(f"yplus: {yplus[0:int(ny/2)]}")
    print(f"uplus: {uplus[0:int(ny/2)]}")

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))

    # Average plot
    axs[0].plot(average_u[0:int(ny/2)],ly[0:int(ny/2)],'o-')
    axs[0].set_xlabel(r'u', fontsize=12)
    axs[0].set_ylabel(r'y', fontsize=12)
    axs[0].set_title(r'u vs y', fontsize=14)
    axs[0].grid(True)

    # Uplus plot
    axs[1].plot(yplus[0:int(ny/2)], uplus[0:int(ny/2)],'o-')
    axs[1].set_xlabel(r'$y^{+}$', fontsize=12)
    axs[1].set_ylabel(r'$u^{+}$', fontsize=12)
    axs[1].set_title(r'$u^{+}$ vs $y^{+}$', fontsize=14)
    axs[1].set_xscale('log') 
    axs[1].grid(True)

    fig.tight_layout()
    fig.savefig('plots/uplus_yplus.png')
    
    

def plot_re_stresses(timestep, parsed_data, current_path):

    # Path
    current_path = str(current_path)
    print(f"Current path: {current_path}")

    # Parameters
    H = parsed_data["H"]
    H2 = parsed_data["H"]/2
    L = parsed_data["L"]
    W = parsed_data["W"]
    nu = 1/parsed_data["Re_lam"]
    nx = parsed_data["nx"] 
    ny = parsed_data["ny"]
    nz = parsed_data["nz"]
    
    # Precalculations
    dx = L/nx
    dy = H/ny
    dz = W/nz

    # Get times from the names of the folders
    directories_list = get_directories(current_path)
    
    # Select the time
    time = directories_list[timestep]

    # Get y values
    y = get_y_values(ny,nx,current_path, time)

    print(f"y values: {y}")

    
    # Get U field
    U = Ofpp.parse_internal_field(f'{current_path}/{time}/UPrime2Mean')
    
    # Get friction velocity
    ut = calculate_ut(current_path, time)

    # Calculate average u
    average_uu, average_uv, average_vv, average_ww = calculate_slice_average(U, nx, ny, nz, type="tensor")

    print(f"Some calculated values for time {time}:")
    print(f"average_uu: {average_uu[0:int(ny/2)]}")
    print(f"average_uv: {average_uv[0:int(ny/2)]}")
    print(f"average_vv: {average_vv[0:int(ny/2)]}")
    print(f"average_ww: {average_ww[0:int(ny/2)]}")

    # Calculate re stresses
    re_average_uu = average_uu/ut**2
    re_average_vv = average_vv/ut**2
    re_average_ww = average_ww/ut**2
    re_average_uv = average_uv/ut**2

    # Results plot
    fig, ax = plt.subplots()
    ax.plot(y[0:int(ny/2)], re_average_uu[0:int(ny/2)])
    ax.plot(y[0:int(ny/2)], re_average_uv[0:int(ny/2)])
    ax.plot(y[0:int(ny/2)], re_average_vv[0:int(ny/2)])
    ax.plot(y[0:int(ny/2)], re_average_ww[0:int(ny/2)])

    ax.set_xlabel(r'y', fontsize=12)
    ax.set_ylabel(r'Re stresses', fontsize=12)
    ax.set_title(r'Re stresses vs y', fontsize=14)
    ax.legend([r'$Re_{uu}$', r'$Re_{uv}$', r'$Re_{vv}$', r'$Re_{ww}$'])
    ax.grid(True)

    fig.savefig('plots/re_stresses.png')
    
    
    

def get_y_values(ny,nx,current_path, time):
    C = Ofpp.parse_internal_field(f'{current_path}/constant/C')
    y_values = mesh.get_mesh_y_positions(C,nx,ny)
    return y_values

def calculate_ut(current_path, time):
    w = Ofpp.parse_boundary_field(f'{current_path}/{time}/wallShearStress')
    top_values = w[b"top"][b"value"]
    bot_values = w[b"bottom"][b"value"]
    tau = np.abs(np.average(top_values+bot_values))
    ut = np.sqrt(tau)
    return ut

def calculate_slice_average(U, nx, ny, nz, type="vector"):

    ny2 = int(ny/2)
    if type == "vector":
        # Initialize arrays
        average_u = np.zeros(ny)
        average_v = np.zeros(ny)
        average_w = np.zeros(ny)

        for j in range(ny2):
            xz_slice = np.array([U[i*(nx*ny2) + j*nz + k] for k in range(nz) for i in range(nx)])

            u_xz = xz_slice[:, 0]
            v_xz = xz_slice[:, 1]
            w_xz = xz_slice[:, 2]

            average_u[j] = np.average(u_xz)
            average_v[j] = np.average(v_xz)
            average_w[j] = np.average(w_xz)

        for j in range(ny2,ny):
            xz_slice = np.array([U[i*(nx*ny2) + j*nz + k] for k in range(nz) for i in range(nx)])

            u_xz = xz_slice[:, 0]
            v_xz = xz_slice[:, 1]
            w_xz = xz_slice[:, 2]

            average_u[j] = np.average(u_xz)
            average_v[j] = np.average(v_xz)
            average_w[j] = np.average(w_xz)


        return average_u, average_v, average_w
    
    elif type == "tensor":
        # Initialize arrays
        average_uu = np.zeros(ny)
        average_uv = np.zeros(ny)
        average_vv = np.zeros(ny)
        average_ww = np.zeros(ny)

        for j in range(ny2):
            xz_slice = np.array([U[i*(nx*ny2) + j*nz + k] for k in range(nz) for i in range(nx)])

            uu_xz = xz_slice[:, 0]
            vv_xz = xz_slice[:, 1]
            ww_xz = xz_slice[:, 2]
            uv_xz = xz_slice[:, 3]

            average_uu[j] = np.average(uu_xz)
            average_uv[j] = np.average(uv_xz)
            average_vv[j] = np.average(vv_xz)
            average_ww[j] = np.average(ww_xz)

        for j in range(ny2,ny):
            xz_slice = np.array([U[i*(nx*ny2) + j*nz + k] for k in range(nz) for i in range(nx)])

            uu_xz = xz_slice[:, 0]
            vv_xz = xz_slice[:, 1]
            ww_xz = xz_slice[:, 2]
            uv_xz = xz_slice[:, 3]

            average_uu[j] = np.average(uu_xz)
            average_uv[j] = np.average(uv_xz)
            average_vv[j] = np.average(vv_xz)
            average_ww[j] = np.average(ww_xz)

        return average_uu, average_uv, average_vv, average_ww
    
    else:
        print("Invalid type")
        return None

if __name__ == "__main__":

    # Parsing arguments
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Process some CLI arguments.")

    # Add arguments
    parser.add_argument('--timestep', type=int, help='Desired timestep to plot. Default is t1', default=1)

    # Parse arguments
    args = parser.parse_args()

    # Paths
    parent_path = pathlib.Path().resolve().parent # Get parent path
    sys.path.append(str(parent_path)) # Add to python path to access scripts folder

    # Now import the scripts folder
    from scripts.common import parsing, mesh

    
    current_path = os.path.dirname(os.path.realpath(__file__))
    parsed_data = parsing.parse_foam_file(f"{current_path}/default.parameters")

    print(f"Plotting friction Reynolds over time")
    plot_ret(parsed_data, current_path)

    timestep = args.timestep
    print(f"Plotting boundary layer for timestep {timestep}")
    plot_uplus_yplus(timestep, parsed_data, current_path,u_type="inst")

    print(f"Plotting Reynolds stresses for timestep {timestep}")
    plot_re_stresses(timestep, parsed_data, current_path)

    plt.show()
