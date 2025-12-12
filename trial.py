from math import pi,sqrt
from classes import Wingbox
from constants import const
from classes import ScaledWingbox
from wingbox_design import design3_wingbox, thickness3 
import matplotlib.pyplot as plt
import constants
import numpy as np
from stress_functions import max_bending_stress
from worst_cases import worst_case_loading

# Constants
E = const['Modulus_of_Elasticity']
v_poisson = const['Poisson\'s Ratio']
a = const['span']/2.0

# MAXIMUM LENGTH OF SKIN PANEL

#Stringer pos wrt span (to find panel length)
def stringer_pos_spanwise(wingbox,y):
    local_wingbox = ScaledWingbox(wingbox,constants.local_chord_at_span(y))
    return local_wingbox.stringers

#Use design3_wingbox for wingbox
#Find maximum panel length spanwise
def get_max_panel_len(wingbox,y):
    length_panel_lst = []
    nmb_of_panels = len(wingbox.stringers) -1 

    for i in range(nmb_of_panels):
        b = sqrt((stringer_pos_spanwise(wingbox,y)[i+1][0]-stringer_pos_spanwise(wingbox,y)[i][0])**2 + (stringer_pos_spanwise(wingbox,y)[i+1][1]-stringer_pos_spanwise(wingbox,y)[i][1])**2)
        length_panel_lst.append(b)

    #Find y coordinates of stringer that confomr criticl b

    del length_panel_lst[len(length_panel_lst)//2]
    
    return max(length_panel_lst)

print(get_max_panel_len(design3_wingbox,a))
#1. Find the minimum critical stress (biggest b)
#2. Define b as a function of y 
#3. Define thickness as a function of y

def thickness(wingbox,y):
    local_thickness = ScaledWingbox(wingbox,constants.local_chord_at_span(y))
    return local_thickness.panel_thickness[0]

#Find most critical k_c --> the lower k_c, the lower critical value; k_c is lower when a/b is higher -->  a bigger and b smaller
#1. Find b of the most critical value at the tip 

def k_c_det(wingbox):
    aoverb_ratio = a/get_max_panel_len(wingbox,a)
    if aoverb_ratio >= 5:
        return 7.1
    else:
        print(f"See graph for a precise k_c with a/b ration {aoverb_ratio}")
        return 7.1


def crit_sigma_buckling(wingbox,y):
    return pi**2*k_c_det(wingbox)*E/(12*(1-v_poisson**2))*(thickness(wingbox,y)/get_max_panel_len(wingbox,y))**2*10**(-6)

#Plotting (select wingbox)
ypoints = np.linspace(0.0, a ,100)
sigma_crit_points = np.array([crit_sigma_buckling(design3_wingbox,y) for y in ypoints])

plt.plot(ypoints,sigma_crit_points)
plt.xlabel("Span position [m]")
plt.ylabel("Critical buckling stress [MPa]")
plt.show()

