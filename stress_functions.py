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
        from classes import ScaledWingbox
        import constants
        from worst_cases import worst_case_loading
        import area_moments
        import data_from_xflr5
        xcp = data_from_xflr5.xcppos_func(1.621258898884106)
        #0.2312805658645682
        if not wingbox.idealizable:
            print('This wingbox can not be idealized, so it doenst make sense to calculate shear for it.')
            quit()
        
        #Since axis systems flipped, negative force means upward, but the wingbox is defined positive upward. Thus the force is flipped
        Vy = worst_case_loading.V(y, 'abs_min_shear') * -1
        
        current_wingbox = ScaledWingbox(wingbox, constants.local_chord_at_span(y))

        #Cut in the vertical panel under the leading edge top point, assumed Vx = 0 and Ixy = 0
        shear_b = np.zeros_like(current_wingbox.panel_thickness)
        for i in range(len(shear_b)):
            shear_b[i] = shear_b[i - 1] - Vy / wingbox.Ixx(y) * current_wingbox.idealized_point_areas[i] * current_wingbox.centroidal_points[i,1]

        #Moment around centroid, clockwise positive
        centroidal_moment_qb = 0
        for i in range(len(shear_b)):
            centroidal_moment_qb += shear_b[i] * 2 * area_moments.polygon_area(np.array([[0,0], current_wingbox.centroidal_panels[i,:2], current_wingbox.centroidal_panels[i,2:]]))
        
        #Moment that should be created when loading=internal force
        centroidal_moment_Vy = (wingbox.centroid_coordinates[0] - xcp(y)) * constants.local_chord_at_span(y) * Vy
 
        #Calculating the qs0 such that internal loading and torque equal applied loading and torque
        qs0_contribution = 2 * wingbox.area(y)
        qs0 = (centroidal_moment_Vy - centroidal_moment_qb) / qs0_contribution

        current_wingbox.shear = shear_b + qs0

        #IT WORKS! The internal load sums back to the applied load with less than 0.5% error
        #print(f'Summed shear: {np.sum(current_wingbox.shear * np.transpose([current_wingbox.centroidal_panels[:,3] - current_wingbox.centroidal_panels[:,1]]))}')
        #print(f'Vy: {Vy}')



        return current_wingbox.shear

