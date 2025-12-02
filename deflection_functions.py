import scipy as sp
from constants import const
import data_import
from worst_cases import worst_case_loading
import numpy as np


testclass = data_import.import_wingbox('test_cross_section')

E = const.get('Modulus_of_Elasticity')
b = const.get('span')
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

#ouputs the twist distribution as a function of the spanwise position of the wing by integrating the function above
#wingbox: input a wingbox class variable
#def theta(wingbox, y=b/2): 
#    result, error = sp.integrate.quad(dtheta_dy,0,y, args=(wingbox,))
#    return result

def theta(wingbox, y_end=None, N=2000):
    if y_end is None:
        y_end = const['span'] / 2

    y = np.linspace(0, y_end, N)
    
    f = dtheta_dy(y, wingbox)

    dtheta_dy_values = sp.integrate.cumulative_trapezoid(f, y, initial=0)
    theta_values = sp.integrate.cumulative_trapezoid(dtheta_dy_values, y, initial=0)

    return y, theta_values

#outputs the second derivative of the deflection wrt the spanwise position, using the bending distribution and Ixx
#wingbox: input a wingbox class variable
#def d2v_dy2(y, wingbox):
#    return worst_case_loading.M(y, 'abs_max_bending') / (E * wingbox.Ixx(y))

#outputs the derivative of the deflection wrt the spanwise position, using the bending distribution and Ixx
#wingbox: input a wingbox class variable
#def dv_dy(y, wingbox):
#    result, error = sp.integrate.quad(d2v_dy2, 0, y, args=(wingbox,))
#    return result

#ouputs the deflection distribution as a function of the spanwise position of the wing by integrating the function(s) above
#wingbox: input a wingbox class variable
#def v(wingbox, y=b/2):
#    result, error = sp.integrate.quad(dv_dy, 0, y, args=(wingbox,))
#    return result
    
def d2v_dy2(y, wingbox):
    y = np.asarray(y)
    M = worst_case_loading.M(y, 'abs_min_bending')
    Ixx_list = np.zeros_like(y, dtype=float)
    for i in range(len(y)):
        Ixx_list[i] = wingbox.Ixx(y[i])
    return - M / (E * Ixx_list)

#Returns two evenly spaced arrays. First an array of y-values, second an array of v-values corresponding to the y values in the first array.
#To find the deflection at a specific y-value, either search the array or input y_end and take the [-1] indexed value of the array.
def v(wingbox, y_end=None, N=2000):
    if y_end is None:
        y_end = const['span'] / 2

    y = np.linspace(0, y_end, N)
    
    f = d2v_dy2(y, wingbox)

    dv_dy_values = sp.integrate.cumulative_trapezoid(f, y, initial=0)
    v_values = sp.integrate.cumulative_trapezoid(dv_dy_values, y, initial=0)

    return y, v_values
