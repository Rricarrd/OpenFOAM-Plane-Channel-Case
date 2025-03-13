import openfoamparser as Ofpp
import numpy as np
import sys
C = np.array(Ofpp.parse_internal_field('0/C'))
print(C)
