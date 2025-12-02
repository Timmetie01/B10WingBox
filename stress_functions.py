import scipy as sp
from constants import const
from worst_cases import worst_case_loading
import numpy as np
import area_moments

#Using Mx*y/Ixx (but in different coordinate system). i.e. assuming Ixy=0 and only moment around X axis is present.
def max_bending_stress(wingbox, y):
    sigma_z = worst_case_loading.M(y, 'abs_min_bending') * np.array([wingbox.z_max_min(y)[0], wingbox.z_max_min(y)[1]]) / wingbox.Ixx(y)
    return sigma_z[0] if sigma_z[0] > -1 * sigma_z[1] else sigma_z[1]

