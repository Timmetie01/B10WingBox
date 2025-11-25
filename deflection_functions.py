import scipy as sp
from constants import const
import data_import
from loading_diagram import M

testclass = data_import.import_wingbox('test_cross_section')
E = const.get('Modulus_of_Elasticity')
b = const.get('span')
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

