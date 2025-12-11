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

    K = 4
    E = const['Modulus_of_Elasticity']
    I = 1e-9
    #Assuming worst case
    A = np.min(local_wingbox.stringer_area)
    L = const['span'] / 2

    critical_buckling_stress = K * math.pi**2 * E * I / (A * L ** 2)

    if printvalue:
        print(critical_buckling_stress / (10 ** 6), "MPa")

    return critical_buckling_stress

def stringer_buckling_MOS(wingbox, y):
    import stress_functions
    critical_buckling_stress = min_stringer_buckling_stress(wingbox, y)
    max_normal_Stress = stress_functions.max_bending_stress(wingbox, y)

    return critical_buckling_stress / max_normal_Stress

def lowest_strigner_buckling_MOS(wingbox, Npoints = 200):
    import stress_functions
    y_tab = np.linspace(0, const['span']/2, Npoints)
    MOS_tab = []
    for i in y_tab:
        MOS_tab.append(stringer_buckling_MOS(wingbox, i))

    return np.min(MOS_tab)