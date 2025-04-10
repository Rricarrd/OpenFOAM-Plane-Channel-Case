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
    directories_list = get_directories(current_path)
    time = [float(i) for i in directories_list]

    ret = []

    for i in directories_list:

        ut = calculate_ut(current_path, i)
        ret.append(ut*(parsed_data["H"]/2)/parsed_data["nu"])



    fig, ax = plt.subplots()
    ax.plot(time,ret, label="case")
    ax.set_xlabel(r'Time (s)', fontsize=12)
    ax.set_ylabel(r'$Re_{\tau}$', fontsize=12)
    ax.set_title(r'$Re_{\tau}$ Evolution', fontsize=14)
    ax.grid(True)

    # Reference data DNS
    times_dns = [9.79765708200213, 25.559105431309906, 42.17252396166134, 57.082002129925456, 69.43556975505858, 82.64110756123536, 95.42066027689032, 107.77422790202344, 117.14589989350374, 126.0915867944622, 132.48136315228967, 138.0191693290735, 142.2790202342918, 145.26091586794462, 147.3908413205538, 150.3727369542066, 152.50266240681577, 155.05857294994675, 158.0404685835996, 160.17039403620873, 162.72630457933974, 165.28221512247072, 167.83812566560172, 170.3940362087327, 172.09797657082004, 175.07987220447285, 178.06176783812566, 180.19169329073483, 183.17358892438764, 188.71139510117146, 193.82321618743345, 197.2310969116081, 201.0649627263046, 201.49094781682643, 207.02875399361022, 210.86261980830673, 217.2523961661342, 223.21618743343984, 227.47603833865816, 233.86581469648564, 237.69968051118212, 241.10756123535677, 247.07135250266242, 256.8690095846645, 261.98083067092654, 266.6666666666667, 272.2044728434505, 276.038338658147, 282.8541001064963, 289.66986155484557, 294.7816826411076, 299.89350372736953, 309.26517571884983, 316.93290734824285, 330.1384451544196, 335.67625133120345, 341.21405750798726, 345.8998935037274, 351.86368477103304, 361.66134185303514, 374.0149094781683, 380.8306709265176, 382.96059637912674, 386.7944621938232, 390.6283280085197, 397.44408945686905]
    ret_dns = [101.14503816793894, 101.6030534351145, 101.6030534351145, 101.37404580152672, 101.37404580152672, 101.14503816793894, 101.37404580152672, 102.29007633587786, 104.12213740458016, 107.32824427480917, 112.13740458015268, 117.17557251908397, 121.98473282442748, 128.62595419847327, 133.89312977099237, 140.53435114503816, 149.9236641221374, 160.2290076335878, 179.92366412213738, 194.35114503816794, 205.34351145038167, 219.08396946564886, 227.09923664122135, 236.2595419847328, 242.90076335877862, 244.50381679389312, 242.67175572519085, 238.54961832061068, 233.2824427480916, 223.66412213740458, 221.83206106870227, 218.62595419847327, 213.3587786259542, 209.6946564885496, 209.46564885496184, 208.0916030534351, 203.51145038167937, 201.6793893129771, 201.22137404580153, 202.59541984732823, 204.42748091603053, 204.8854961832061, 204.19847328244276, 206.4885496183206, 205.34351145038167, 204.19847328244276, 204.6564885496183, 207.17557251908397, 207.63358778625954, 207.17557251908397, 206.71755725190837, 207.40458015267177, 209.23664122137404, 210.61068702290078, 210.83969465648855, 211.5267175572519, 213.81679389312978, 211.5267175572519, 210.61068702290078, 207.63358778625954, 207.8625954198473, 208.0916030534351, 209.00763358778624, 210.61068702290078, 211.29770992366412, 212.44274809160305]

    ax.scatter(times_dns, ret_dns, label="DNS")

    fig.legend()
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
    nu = parsed_data["nu"]
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
    nu = parsed_data["nu"]
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

    mags_top = np.linalg.norm(w[b"top"][b"value"],axis=1)
    mags_bot = np.linalg.norm(w[b"bottom"][b"value"],axis=1)
    
    top_value = np.average(mags_top)
    bot_value = np.average(mags_bot)
    
    print(f"Top value {top_value}")
    print(f"Bot value {bot_value}")
    
    tau = np.abs((top_value+bot_value)/2)
    print(f"tau average is: {tau}")
    ut = np.sqrt(tau)
    print(f"ut value is: {ut}")
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
    sys.path.append(str(parent_path.parent)) # Add to python path to access scripts folder
    
    # Now import the scripts folder
    from scripts.common import parsing, mesh

    
    current_path = os.path.dirname(os.path.realpath(__file__))
    parsed_data = parsing.parse_foam_file(f"{current_path}/default.parameters")

    print(f"Plotting friction Reynolds over time")
    plot_ret(parsed_data, current_path)

    timestep = args.timestep
    print(f"Plotting boundary layer for timestep {timestep}")
    plot_uplus_yplus(timestep, parsed_data, current_path,u_type="inst")

    try:
        print(f"Plotting Reynolds stresses for timestep {timestep}")
        plot_re_stresses(timestep, parsed_data, current_path)
    except:
        pass
    
    plt.show()
