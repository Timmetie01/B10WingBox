import numpy as np
import scipy as sp
from constants import const
from area_moments import Torsional_constant
import data_import
import classes

testclass = data_import.import_wingbox('test_cross_section')


def T(y):
    b = const['span']
    return 5000*(1-y)/(b/2)

def dtheta_dz(y):
    G = const['Shear_Modulus']
    return T(y)/(G*testclass.J(y))
def theta(y):
    result, error = sp.integrate.quad(dtheta_dz,0,y)
    return result








