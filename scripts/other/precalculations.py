import math

# ----------------- CURRENT PARAMETERS -----------------
# Fluid parameters
rho = 1
nu = 2.54e-3

# Channel parameters
H = 1         # Channel height (Characteristic length) [m]
H2 = 2 * H    # Channel total height [m]
W = math.pi   # Channel width [m]
L = 60        # Channel length [m]

# Cell counts
nx = 300
ny = 16
nz = 35

# Size increase gradient
Rx = 1 + 1e-12
Ry = 10.7028
Rz = 1 + 1e-12

print("######################### MESH CALCULATIONS #######################\n")

# ----------------- DESIRED MESH SIZING -----------------
print("############ Calculations of the desired mesh ############\n")

# y with Re and y+
print("# Imposing Re and U")
yplus = 1
U = 17.55
print(f"Considering yplus is {yplus} and U is {U:.3f} m/s")

# 1 - Reynolds number
Reb = U * H / nu
print(f"The bulk Reynolds number (Re) is {Reb:.3f}")

# 2 - Friction coefficient
Cf = 0.058 * (Reb ** (-0.2))

# 3 - Shear stress
tauw = 0.5 * Cf * rho * (U ** 2)

# 4 - Shear speed
Ut = math.sqrt(tauw / rho)

# 5 - y first cell
yReb = nu * yplus / Ut
print(f"Yielding a first cell height of {yReb:.3f} m or {yReb * 1000:.3f} mm\n")

# y with Ret
print("# Imposing shear Reynolds (Ret)")
Ret = 395
print(f"Considering Ret is {Ret}")

# 1 - Ut calculation using Ret
Ut = Ret * nu / H

# 2 - y first cell
yRet = nu * yplus / Ut
print(f"Yielding a first cell height of {yRet:.3f} m or {yRet * 1000:.3f} mm\n")

# ----------------- CURRENT MESH CALCULATIONS -----------------
print("############ Calculations of the current mesh ############")
print("# Current plane channel mesh element sizing")

# Geometric progression factors
rx = Rx ** (-1 / (nx - 1))
ry = Ry ** (-1 / (ny - 1))
rz = Rz ** (-1 / (nz - 1))

def final_element_size(L, r, N):
    """
    Calculate the smallest cell size at the wall using the geometric progression formula.
    """
    return L * (r - 1) * (r ** (N - 1)) / (r ** N - 1)

# Smallest cell sizes [m]
mincell_dx = final_element_size(L, rx, nx)
mincell_dy = final_element_size(H, ry, ny)
mincell_dz = final_element_size(W, rz, nz)
print(f"The smallest cells (touching the wall) are dx = {mincell_dx * 1000:.3f} mm, "
      f"dy = {mincell_dy * 1000:.3f} mm and dz = {mincell_dz * 1000:.3f} mm")

# Biggest cell sizes [m]
maxcell_dx = Rx * mincell_dx
maxcell_dy = Ry * mincell_dy
maxcell_dz = Rz * mincell_dz
print(f"The biggest cells (center of channel) are dx = {maxcell_dx * 1000:.3f} mm, "
      f"dy = {maxcell_dy * 1000:.3f} mm and dz = {maxcell_dz * 1000:.3f} mm\n")

print("# Current plane channel mesh element sizing")
mincell_xplus = mincell_dx * Ut / nu
mincell_yplus = mincell_dy * Ut / nu
mincell_zplus = mincell_dz * Ut / nu
print(f"The smallest cells (touching the wall) are xplus = {mincell_xplus:.3f}, "
      f"yplus = {mincell_yplus:.3f} and zplus = {mincell_zplus:.3f}")

# ----------------- TURBULENCE MODEL -----------------
print("############ Calculations of the turbulence models ############")
print("# For a transitional K - omega SST model gamma - Re-theta")

I = 0.01      # Turbulent intensity (Low: 0.01, Medium: 0.05, High: 0.1)
Cmu = 0.09    # Model constant
print(f"And considering a turbulent intensity of {I:.3f}")

# Bulk turbulence kinetic energy (kb)
kb = 1.5 * (I * U) ** 2
print(f"kb: The bulk initial turbulent kinetic energy (kb) is {kb:.3f}")

# Bulk turbulent dissipation rate (wb)
wb = math.sqrt(kb) / (Cmu ** 0.25 * H)
print(f"wb: The bulk initial turbulent dissipation rate (wb) is {wb:.3f}")

# Bulk turbulent viscosity (nutb)
nutb = 0
print(f"nutb: The bulk initial turbulent viscosity (nutb) is {nutb:.3f}")

# Bulk intermittency (gammab)
gammab = 1
print(f"gammab: The bulk intermittency (gammab) is {gammab:.3f}")

# Bulk transition momentum thickness Reynolds number (retheta)
Tu = 100 * math.sqrt(2 / (3 * kb)) / U
if Tu <= 1.3:
    Rethetab = 1173.51 - 589.428 * Tu + 0.2196 / (Tu ** 2)
else:
    Rethetab = 333.51 / ((Tu - 0.5658) ** 0.671)
print(f"The bulk transition momentum thickness Reynolds number (retheta) is {Rethetab:.3f}\n")

# ----------------- BOUNDARY CONDITIONS -----------------
# k walls = 0
# k inlet = kb
#
# w walls = zeroGradient
# w inlet = wb
# w outlet = zeroGradient
#
# nut walls = zeroGradient
# nut inlet/outlet = calculated
#
# gammaint inlet = 1
# gammaint walls = zeroGradient
#
# retheta inlet = Reb
# retheta walls = zeroGradient

# ----------------- MESH REFINEMENT CALCULATIONS -----------------
print("############ Calculations of the mesh refinement ############")
# (Further mesh refinement calculations would go here...)
