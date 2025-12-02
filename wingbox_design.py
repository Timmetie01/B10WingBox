from constants import const
import constants
import numpy as np
import scipy as sp
import data_import
import deflection_functions

#Assuming constant thickness, iterate until the thickness is enough
def thickness_iteration(xstart, xend, stringercount, stringer_areas, stringerspacing='constant_endpoints', panelcount=50):
    deflection = 100
    twist = 100
    wingboxthickness = 0

    print('Iterating over thickness', end='')
    while deflection > const['span'] * const['max_deflection_fraction'] or abs(twist) > const['max_twist_degrees']:
        wingboxthickness += 5e-5
        iterationwingbox = data_import.create_airfoil_like_wingbox(xstart, xend, thickness=wingboxthickness, thicknesstype='constant', stringercount=stringercount, stringer_areas=stringer_areas, panelcount=panelcount, stringerspacing=stringerspacing)

        deflection, twist = deflection_functions.max_deflection_and_twist(iterationwingbox)
        twist = twist * 180 / np.pi #Formula outputs radians

        print('.', end='', flush=True)

    print('\tDone!')

    return wingboxthickness, iterationwingbox

        



