import scipy as sp
from constants import const
import data_import
from worst_cases import worst_case_loading
import numpy as np

testclass = data_import.import_wingbox('test_cross_section')

E = const['Modulus_of_Elasticity']
b = const['span']
G = const['Shear_Modulus']

#outputs the derivative of the twist wrt the spanwise position, using the torsion distribution and torsional constant
#wingbox: input a wingbox class variable
def dtheta_dy(y, wingbox): 
    np.asarray(y)
    T = worst_case_loading.T(y, 'abs_max_torsion')
    J_list = np.zeros_like(y, dtype=float)
    for i in range(len(y)):
        J_list[i] = wingbox.J(y[i])
    return T/(G* J_list)

#Returns two evenly spaced arrays. First an array of y-values, second an array of theta-values corresponding to the y values in the first array.
#To find the twist at a specific y-value, either search the array or input y_end and take the [-1] indexed value of the array.
#Theta is in RADIANS!
def theta(wingbox, y_end=None, N=2000):
    if y_end is None:
        y_end = b / 2

    y = np.linspace(0, y_end, N)
    
    f = dtheta_dy(y, wingbox)

    theta_values = sp.integrate.cumulative_trapezoid(f, y, initial=0)

    return y, theta_values


#outputs the second derivative of the deflection wrt the spanwise position, using the bending distribution and Ixx
#wingbox: input a wingbox class variable
def d2v_dy2(y, wingbox):
    y = np.asarray(y)
    M = worst_case_loading.M(y, 'abs_min_bending')
    Ixx_list = np.zeros_like(y, dtype=float)
    for i in range(len(y)):
        Ixx_list[i] = wingbox.Ixx(y[i])
    return - M / (E * Ixx_list)

#Returns two evenly spaced arrays. First an array of y-values (0-half span), second an array of v-values corresponding to the y values in the first array.
#To find the deflection at a specific y-value, either search the array or input y_end and take the [-1] indexed value of the array.
def v(wingbox, y_end=None, N=2000):
    if y_end is None:
        y_end = b / 2

    y = np.linspace(0, y_end, N)
    
    f = d2v_dy2(y, wingbox)

    dv_dy_values = sp.integrate.cumulative_trapezoid(f, y, initial=0)
    v_values = sp.integrate.cumulative_trapezoid(dv_dy_values, y, initial=0)

    return y, v_values

#Returns the maximum deflection and absolute maximum twist found along the wing. Twist is IN RADIANS!
def max_deflection_and_twist(wingbox):
    import deflection_functions
    y_list, v_list = deflection_functions.v(wingbox)
    deflection = max(v_list)
    y_list, theta_list = deflection_functions.theta(wingbox)
    twist = max(np.abs(theta_list))

    return deflection, twist

def worst_V_twist_MOS(wingbox):
    y_list, v_list = v(wingbox)
    y_list, theta_list = theta(wingbox)
    MOS_v_list, MOS_theta_list = const['max_deflection_fraction'] * const['span'] / v_list, const['max_twist_degrees'] * np.pi / 180 / theta_list

    return min(MOS_v_list), min(MOS_theta_list)