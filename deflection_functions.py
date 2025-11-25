import scipy as sp
from constants import const
import data_import

testclass = data_import.import_wingbox('test_cross_section')
E = const.get('Shear_Modulus')



def d2v_dy2(y):
    return -M(y)/(E*testclass.Ixx(y))


def dv_dy(y):
    result, error = sp.integrate.quad(d2v_dy2,0,y)
    return -result
def v(y):
    def integrand(gamma):
        return dv_dy(gamma)
    result, error = sp.integrate.quad(integrand, 0, y)
    return result
