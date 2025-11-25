import numpy as np
import scipy as sp
from constants import const
from area_moments import Torsional_constant
import data_import
import classes
from loading_diagram import M

testclass = data_import.import_wingbox('test_cross_section')

E = const.get('Modulus_of_Elasticity')
b = const.get('span')
G = const['Shear_Modulus']

def T(y): #random linear function used to test output, to be replaced by 4.1s torsion distribution 
    return 50000*(1-y)/(b/2)

def dtheta_dy(y, wingbox): #outputs the derivative of the twist wrt the spanwose position, using the torsion distribution and torsional constant
    return T(y)/(G*wingbox.J(y))

def theta(wingbox, y=b/2): #ouputs the twist distribution as a function of the spanwise position of the wing by integrating the function above
    result, error = sp.integrate.quad(dtheta_dy,0,y, args=(wingbox,))
    return result


def M(y):
    return -1.5e6*(1-y/(b/2))

def d2v_dy2(y, wingbox):
    return -M(y) / (E * wingbox.Ixx(y))

def dv_dy(y, wingbox):
    result, error = sp.integrate.quad(d2v_dy2, 0, y, args=(wingbox,))
    return result

def v(wingbox, y=b/2):
    result, error = sp.integrate.quad(dv_dy, 0, y, args=(wingbox,))
    return result

