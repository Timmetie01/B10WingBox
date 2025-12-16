from math import pi,sqrt
from constants import const
from classes import ScaledWingbox
#from wingbox_design import design3_wingbox
#from wingbox_design import design1_wingbox
import matplotlib.pyplot as plt
import constants
import numpy as np
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
    nmb_of_panels = len(wingbox.stringers) - 1

    for i in range(nmb_of_panels):
        b = sqrt((stringer_pos_spanwise(wingbox,y)[i+1][0]-stringer_pos_spanwise(wingbox,y)[i][0])**2 + (stringer_pos_spanwise(wingbox,y)[i+1][1]-stringer_pos_spanwise(wingbox,y)[i][1])**2)
        length_panel_lst.append(b)

    #Find y coordinates of stringer that confomr criticl b

    del length_panel_lst[len(length_panel_lst)//2]

    index_maxb = length_panel_lst.index(max(length_panel_lst))
    if index_maxb < (len(length_panel_lst)+2)//2:
        index_maxb = index_maxb
    if index_maxb > (len(length_panel_lst)+2)//2:
        index_maxb = index_maxb + 1
    
    zpos_for_stress = (stringer_pos_spanwise(wingbox,y)[index_maxb][1] + stringer_pos_spanwise(wingbox,y)[index_maxb +1][1])/2

    return max(length_panel_lst),zpos_for_stress

#1. Find the minimum critical stress (biggest b)
#2. Define b as a function of y 
#3. Define thickness as a function of y

def thickness(wingbox,y):
    local_thickness = ScaledWingbox(wingbox,constants.local_chord_at_span(y))
    return local_thickness.panel_thickness[0]

#Find most critical k_c --> the lower k_c, the lower critical value; k_c is lower when a/b is higher -->  a bigger and b smaller
#1. Find b of the most critical value at the tip 

def k_c_det(wingbox):
    aoverb_ratio = a/get_max_panel_len(wingbox,a)[0]
    if aoverb_ratio >= 5:
        return 7.1
    else:
        print(f"See graph for a precise k_c with a/b ration {aoverb_ratio}")
        return 7.1


def crit_sigma_buckling(wingbox,y):
    return pi**2*k_c_det(wingbox)*E/(12*(1-v_poisson**2))*(thickness(wingbox,y)/get_max_panel_len(wingbox,y)[0])**2*10**(-6)

#Plotting (select wingbox)
#ypoints = np.linspace(0.0, const['span']/2.0 ,100)
#sigma_crit_points = np.array([crit_sigma_buckling(design3_wingbox,y) for y in ypoints])

'''
plt.plot(ypoints,sigma_crit_points)
plt.xlabel("Span [m]")
plt.ylabel("Buckling Stress [MPa]")
plt.show()
'''

'''
def bending_sress_func(wingbox,y):
    return (worst_case_loading.M(y, 'abs_min_bending') + 1e-5)*get_max_panel_len(wingbox,y)[1]/ wingbox.Ixx(y)
'''
 
def margin_of_safety_skinbuckling(wingbox,y):
    import stress_functions
    return abs(crit_sigma_buckling(wingbox,y)*10**6/stress_functions.max_bending_stress(wingbox,y))

'''
marginofsafety_points = np.array([margin_of_safety_skinbuckling(design3_wingbox,y) for y in ypoints])

plt.plot(ypoints,marginofsafety_points)
plt.xlabel("Span position [m]")
plt.ylabel("Margin of Safety [-]")
plt.show()
'''








'''
def get_max_panel_len2(wingbox):
    def max_b(y):
        length_panel_lst = []
        nmb_of_panels = len(wingbox.stringers)

        for i in range(nmb_of_panels-1):
            b = sqrt((stringer_pos_spanwise(wingbox,y)[i+1][0]-stringer_pos_spanwise(wingbox,y)[i][0])**2 + (stringer_pos_spanwise(wingbox,y)[i+1][1]-stringer_pos_spanwise(wingbox,y)[i][1])**2)
            length_panel_lst.append(b)

        del length_panel_lst[(len(length_panel_lst)+1)/2]
        return max(length_panel_lst)
    return max_b
'''
