import math
from constants import const
from classes import Wingbox
import numpy as np
import constants



#K = 1/4
#E = const['Modulus_of_Elasticity']
#I = 1 #for now
#A = Wingbox.stringer_area[0]
#L = const['span'] / 2






def min_stringer_buckling_stress(wingbox, y, printvalue=False):
    import classes
    local_wingbox = classes.ScaledWingbox(wingbox, constants.local_chord_at_span(y))
    K = 1/4
    E = const['Modulus_of_Elasticity']
    I = wingbox.Ixx(y)
    #Assuming worst case
    A = np.min(local_wingbox.stringer_area)
    L = const['span'] / 2

    critical_buckling_stress = K * math.pi**2 * E * I / (A * L ** 2)

    if printvalue:
        print(critical_buckling_stress / (10 ** 6), "MPa")

    return critical_buckling_stress

def 