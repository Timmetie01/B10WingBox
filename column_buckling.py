import math
from constants import const
from classes import Wingbox

K = 1/4
E = const['Modulus_of_Elasticity']
I = 1 #for now
A = Wingbox.stringer_area[0]
L = const['span'] / 2

critical_buckling_stress = K * math.pi**2 * E * I / (A * L ** 2)
print(critical_buckling_stress / (10 ** 6), "MPa")