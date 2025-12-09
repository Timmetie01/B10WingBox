from math import pi
from classes import Wingbox
from constants import const
from classes import Wingbox
from wingbox_design import design3_wingbox, thickness3 
import matplotlib.pyplot as plt

# Variables 
k_c = 7.1
E = 72.4*10**9
t = 0. #skin thickness
b = 0. #short side of the skin plate
v_poisson = 0.33 
a = const['span']

# SKIN BUCKLING FRO INDIVIDUAL PLATES

#1. Access the appropriate thickness and length 

def get_panel_t(wingbox):
    t = wingbox.panel_thickness
    return t 

def get_panel_length(wingbox):
    b = wingbox.panel_length
    return b 

toverb_list = []

#change wingbox argument to specific wingbox
for i in range(len(design3_wingbox.panels)):
    toverbratio = get_panel_t(design3_wingbox)[i][0]/get_panel_length(design3_wingbox)[i][0]
    toverb_list.append(toverbratio)

panel_critical_stress_lst = []

for i in range(len(design3_wingbox.panels)):
    critical_stress = pi**2*k_c*E/(12*(1-v_poisson**2)) * toverb_list[i]**2
    panel_critical_stress_lst.append(critical_stress)

total_critical_stress = sum(panel_critical_stress_lst)

#print(total_critical_stress)
#print(get_panel_length(design3_wingbox))
print(panel_critical_stress_lst)

#2. Generate approximated graph to calculate k_c out of a/b
#In the end we assume that given that a is extremely large compared to panel length, it tends to infinity, in the graph it is around 7.1

