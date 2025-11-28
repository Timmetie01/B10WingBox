import scipy as sp
from constants import const
from area_moments import Torsional_constant
import data_import

testclass = data_import.import_wingbox('test_cross_section')

E = const.get('Modulus_of_Elasticity')
b = const.get('span')
G = const['Shear_Modulus']

#random linear function used to test output, to be replaced by 4.1s torsion distribution 
def T(y): 
    return 50000*(1-y)/(b/2)

#outputs the derivative of the twist wrt the spanwise position, using the torsion distribution and torsional constant
#wingbox: input a wingbox class variable
def dtheta_dy(y, wingbox): 
    return T(y)/(G*wingbox.J(y))

#ouputs the twist distribution as a function of the spanwise position of the wing by integrating the function above
#wingbox: input a wingbox class variable
def theta(wingbox, y=b/2): 
    result, error = sp.integrate.quad(dtheta_dy,0,y, args=(wingbox,))
    return result


#random linear function used to test output, to be replaced by 4.1s bending distribution
def M(y):
    return -1.4e6*(1-y/(b/2))

#outputs the second derivative of the deflection wrt the spanwise position, using the bending distribution and Ixx
#wingbox: input a wingbox class variable
def d2v_dy2(y, wingbox):
    return -M(y) / (E * wingbox.Ixx(y))

#outputs the derivative of the deflection wrt the spanwise position, using the bending distribution and Ixx
#wingbox: input a wingbox class variable
def dv_dy(y, wingbox):
    result, error = sp.integrate.quad(d2v_dy2, 0, y, args=(wingbox,))
    return result

#ouputs the deflection distribution as a function of the spanwise position of the wing by integrating the function(s) above
#wingbox: input a wingbox class variable
def v(wingbox, y=b/2):
    result, error = sp.integrate.quad(dv_dy, 0, y, args=(wingbox,))
    return result

