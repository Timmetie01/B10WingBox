import scipy as sp
from constants import const
from worst_cases import worst_case_loading
import numpy as np
import area_moments


#Using Mx*y/Ixx (but in different coordinate system). i.e. assuming Ixy=0 and only moment around X axis is present.
def max_bending_stress(wingbox, y):
    sigma_z = worst_case_loading.M(y, 'abs_min_bending') * np.array([wingbox.z_max_min(y)[0], wingbox.z_max_min(y)[1]]) / wingbox.Ixx(y)
    return sigma_z[0] if sigma_z[0] > -1 * sigma_z[1] else sigma_z[1]

def shear_stress(wingbox, y):
        import classes
        import constants
        from worst_cases import worst_case_loading
        if not wingbox.idealizable:
            print('This wingbox can not be idealized, so it doenst make sense to calculate shear for it.')
            quit()
        
        #Since axis systems flipped, negative force means upward, but the wingbox is defined positive upward. Thus the force is flipped
        Vy = worst_case_loading.V(y, 'abs_max_shear') * -1
        current_wingbox = classes.ScaledWingbox(wingbox, constants.local_chord_at_span(y))

        #Cut in the vertical panel under the leading edge top point, assumed Vx = 0 and Ixy = 0
        wingbox.shear_b = np.zeros_like(wingbox.panel_thickness)
        for i in range(len(wingbox.shear_b)):
            wingbox.shear_b[i] = wingbox.shear_b[i - 1] - Vy / wingbox.Ixx(y) * wingbox.idealized_point_areas[i] * wingbox.centroidal_points[i,1]

        print(np.sum(wingbox.shear_b * (wingbox.centroidal_panels[:,3] - wingbox.centroidal_panels[:,1]) / wingbox.panel_thickness))

        return wingbox.shear_b

