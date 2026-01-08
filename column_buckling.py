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

def local_stringer_length(y, rib_places=const['half_wing_rib_locations']):
    #The code breaks when y==0, so changed it slightly
    if y < 0.01:
        y = 0.01
    y = abs(y)
    if y > const['span']/2:
        print('Stringer length outside wing range!')
        quit()
    relative_coords = np.array(rib_places) - y
    return np.min(np.where(relative_coords > 0, relative_coords, np.inf)) - np.max(np.where(relative_coords < 0, relative_coords, -np.inf))




def min_stringer_buckling_stress(wingbox, y, rib_places=const['half_wing_rib_locations'], printvalue=False):
    import classes
    local_wingbox = classes.ScaledWingbox(wingbox, constants.local_chord_at_span(y))

    K = 4
    E = const['Modulus_of_Elasticity']
    #Assuming worst case
    A = np.min(local_wingbox.stringer_area)
    #Assuming 2:1 height to width L stringer, and 1:10 t:L ratio
    I = 120/81 * A ** 2
    
    
    #L = const['span'] / const['total_rib_count']
    L = local_stringer_length(y, rib_places)

    critical_buckling_stress = K * math.pi**2 * E * I / (A * L ** 2)

    if printvalue:
        print(critical_buckling_stress / (10 ** 6), "MPa")

    return critical_buckling_stress

def stringer_buckling_MOS(wingbox, y, rib_places=const['half_wing_rib_locations']):
    import stress_functions
    critical_buckling_stress = min_stringer_buckling_stress(wingbox, y, rib_places)
    max_normal_Stress = stress_functions.max_bending_stress(wingbox, y)

    return critical_buckling_stress / (max_normal_Stress + 1e-5)

def lowest_stringer_buckling_MOS(wingbox, Npoints = 200):
    y_tab = np.linspace(0, const['span']/2, Npoints)
    MOS_tab = []
    for i in y_tab:
        MOS_tab.append(stringer_buckling_MOS(wingbox, i))

    return np.min(MOS_tab)

def generate_rib_spacing(wingbox, printvalues=False):
    rib_list = [0]

    for y in list(np.linspace(0.1, const['span']/2 - 0.001, 10000)):
        #print(stringer_buckling_MOS(wingbox, rib_list[-2], np.insert(rib_list, -1, y)))
        if stringer_buckling_MOS(wingbox, rib_list[-1] + 0.00001, np.append(rib_list, y)) < 1.51:
            rib_list = np.append(rib_list, y)

    rib_list = np.append(rib_list, const['span']/2)
    if printvalues:
        print(f'Optimal rib spacing is: \n{rib_list}')
    return rib_list
