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

def T(y):
    return 5000*(1-y)/(b/2)

def dtheta_dz(y):
    return T(y)/(G*testclass.J(y))
def theta(y):
    result, error = sp.integrate.quad(dtheta_dz,0,y)
    return result




def M(y):
    return 5000 - 1000*y/(b/2)

def d2v_dy2(y):
    return -M(y) / (E * testclass.Ixx(y))


def dv_dy(y):
    result, error = sp.integrate.quad(d2v_dy2, 0, y)
    return result


def v(y):
    result, error = sp.integrate.quad(dv_dy, 0, y)
    return result

