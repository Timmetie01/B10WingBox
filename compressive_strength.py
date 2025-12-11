import scipy as sp
from constants import const
from worst_cases import worst_case_loading
import numpy as np
import matplotlib.pyplot as plt
from data_import import import_wingbox
from constants import local_chord_at_span
from constants import const

wingbox = import_wingbox('test_cross_section')
y_span = np.linspace(0, const['span']/2, 200)
sigma_tensile = np.zeros_like(y_span)
sigma_compressive = np.zeros_like(y_span)

critical_sigma_z_tensile=const['Yield_stress'] # Pa
critical_sigma_z_compressive=-1 * const['Yield_stress'] # Pa

data = np.loadtxt(r"data\test_cross_section\stringer_properties.txt", skiprows=1)
z_positions = data[:, 1] 

def bending_stress(wingbox, y):
    # Bending stress formula: sigma = M * z / Ixx
    sigma_z = worst_case_loading.M(y, 'abs_min_bending') * z_positions *local_chord_at_span(y)/ wingbox.Ixx(y)
    return sigma_z

for i, y in enumerate(y_span):
    sigma_z = bending_stress(wingbox, y)
    sigma_tensile[i] = np.max(sigma_z) 
    sigma_compressive[i] = np.min(sigma_z) 

def worst_bending_MOS(wingbox, Npoints=200):
    y_span = np.linspace(0, const['span']/2, Npoints)
    sigma_tensile = np.zeros_like(y_span)
    sigma_compressive = np.zeros_like(y_span)

    critical_sigma_z_tensile = const['Yield_stress']
    critical_sigma_z_compressive = -1 * const['Yield_stress']

    for i, y in enumerate(y_span):
        sigma_z = bending_stress(wingbox, y)
        sigma_tensile[i] = np.max(sigma_z) 
        sigma_compressive[i] = np.min(sigma_z) 


#plt.figure(figsize=(8,4))
#plt.plot(y_span, critical_sigma_z_tensile/sigma_tensile, label='Tensile stress safety margin')
#plt.plot(y_span, critical_sigma_z_compressive/sigma_compressive, label='Compressive stress safety margin')
#plt.axhline(0, color='k', linewidth=0.8)
#plt.xlabel('Spanwise location y [m]')
#plt.ylabel('Safety margin [-]')
#plt.title('Spanwise Compressive and Tensile Stress Safety Margins')
#plt.ylim(0, 20) 
#plt.legend()
#plt.grid(True)
#plt.show()