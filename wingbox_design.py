from constants import const
import constants
import numpy as np
import scipy as sp
import data_import
import deflection_functions
import graphing
import NVMdiagrams

#Assuming constant thickness, iterate until the thickness is enough to overcome deflection and twist requirements
def thickness_iteration(xstart, xend, stringercount, stringer_areas, thicknesstype='constant', spar_thickness = 0.005, stringerspacing='constant_endpoints', panelcount=50, scaled_thickness=False, name=None):
    deflection = 100
    twist = 100
    iteration_thickness = 0
    wingboxthickness=0

    print('Iterating over thickness', end='')

    while deflection > const['span'] * const['max_deflection_fraction'] or abs(twist) > const['max_twist_degrees']:
        iteration_thickness += 2e-5
        if thicknesstype == 'partially_constant':
            wingboxthickness = [iteration_thickness, spar_thickness, iteration_thickness, spar_thickness]
        elif thicknesstype == 'constant':
            wingboxthickness = iteration_thickness
        else:
            print('Choose available thickness defining type to iterate over it!')
            quit()

        iterationwingbox = data_import.create_airfoil_like_wingbox(xstart, xend, thickness=wingboxthickness, thicknesstype='constant', stringercount=stringercount, stringer_areas=stringer_areas, panelcount=panelcount, stringerspacing=stringerspacing, scaled_thickness=scaled_thickness, name=name)

        deflection, twist = deflection_functions.max_deflection_and_twist(iterationwingbox)
        twist = twist * 180 / np.pi #Formula outputs radians

        print('.', end='', flush=True)

    print('\tDone!')

    return iterationwingbox, iteration_thickness


#Uncomment lines as necessary to verify part of the design
#Design 1:
#thickness constant
#design1_wingbox, thickness1 = thickness_iteration(0.2, 0.6, stringercount=0, stringer_areas=3e-5, stringerspacing='constant_no_endpoints', panelcount=4, name='Preliminary Design Wingbox 1')
#print(thickness1)

#print(design1_wingbox.panels)
#print(design1_wingbox.panel_thickness)
#graphing.airfoil_pointplot(showplot=False)
#design1_wingbox.plot()
#design1_wingbox.deflection_plot()
#design1_wingbox.twist_plot()
#design1_wingbox.I_plot()
#design1_wingbox.weight()
#graphing.bending_stress_plot(design1_wingbox)

# print(design1_wingbox.panels)
# print(design1_wingbox.panel_thickness)
# graphing.airfoil_pointplot(showplot=False)
# design1_wingbox.plot()
# design1_wingbox.deflection_plot()
# design1_wingbox.twist_plot()
# design1_wingbox.I_plot()
# design1_wingbox.weight()
# graphing.bending_stress_plot(design1_wingbox)

#Design 2
#Thickness constant, stringer area constant
#design2_wingbox, thickness2 = thickness_iteration(0.2, 0.6, stringercount=20, stringer_areas=1.8e-5, stringerspacing='constant_no_endpoints', panelcount=82, name='Preliminary Design Wingbox 2')
#print(thickness2)

#print(design2_wingbox.panels)
#print(design2_wingbox.panel_thickness)
#print(design2_wingbox.stringers)
#print(design2_wingbox.stringer_area)
#graphing.airfoil_pointplot(showplot=False)
#design2_wingbox.plot()
#design2_wingbox.deflection_plot()
#design2_wingbox.twist_plot()
#design2_wingbox.weight()
#design2_wingbox.I_plot()
#graphing.bending_stress_plot(design2_wingbox)


#Design 3
#Thickness Variable, stringer area constant
#design3_wingbox, thickness3 = thickness_iteration(0.2, 0.6, stringercount=20, stringer_areas=1.8e-5, stringerspacing='constant_no_endpoints', panelcount=82, scaled_thickness=True, name='Preliminary Design Wingbox 3')
#print(thickness3)

# print(design3_wingbox.panels)
# print(design3_wingbox.panel_thickness)
# print(design3_wingbox.stringers)
# print(design3_wingbox.stringer_area)
# graphing.airfoil_pointplot(showplot=False)
# design3_wingbox.plot()
# design3_wingbox.deflection_plot()
# design3_wingbox.twist_plot()
# design3_wingbox.weight()
# design3_wingbox.I_plot()
# graphing.bending_stress_plot(design3_wingbox)

# print(data_import.list_to_string(design3_wingbox.points))
# print(data_import.list_to_string(design3_wingbox.panel_thickness))
# print(data_import.list_to_string(design3_wingbox.stringers))