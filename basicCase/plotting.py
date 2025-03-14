import openfoamparser as Ofpp
import numpy as np
import sys
import matplotlib.pyplot as plt

h = 1
nu = 3e-4
ret = list()

for i in range(1, 149):
    w = Ofpp.parse_boundary_field(f'{i}/wallShearStress')
    top_values = w[b"top"][b"value"]
    bot_values = w[b"bottom"][b"value"]

    tau = np.abs(np.average(top_values+bot_values))

    ut = np.sqrt(tau)

    ret.append(ut*h/nu)

plt.plot(ret)
plt.show()
