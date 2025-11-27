from NVMdiagrams import chord_length
from NVMdiagrams import alpha
from NVMdiagrams import Lub
from NVMdiagrams import Dub
import math as m
import data_import 
import scipy as sp
import numpy as np
from NVMdiagrams import span
import matplotlib.pyplot as plt
from data_from_xflr5 import xcppos_func
from NVMdiagrams import CLd


testclass = data_import.import_wingbox('test_cross_section')

def get_centroid(wingbox):
    scpos = wingbox.centroid_coordinates[0]
    return scpos 

print(f"This is the x coord for testclass {get_centroid(testclass)}")

'''
#Find avg cp position at AOA 0            
def cp_avg(posofcp_0):
    cp_total = 0
    points = 0

    for i in range(len(posofcp_0)):
        cp_total = cp_total + posofcp_0[i]
        points = points + 1

    return cp_total / points


average = cp_avg(posofcp_0)
print("Avg CP at 0 AOA:",average)


#FInd avg cp position at AOA 10            
            
def cp_avg(posofcp_10):
    cp_total = 0
    points = 0

    for i in range(len(posofcp_10)):
        cp_total = cp_total + posofcp_10[i]
        points = points + 1

    return cp_total / points


average = cp_avg(posofcp_10)
print("Avg CP at 10 AOA:",average)
'''
# Position of xcp as a funciton of alpha and the span position

#We're going to have xcp as a funciton of (y)
xcppos_func1 = xcppos_func(CLd)

#Moment arm for a specific alpha and span position
def moment_arm(wingbox):
    def distance(y):
        sc = get_centroid(wingbox)
        return (xcppos_func1(y) - sc) * chord_length(y)
    return distance

MA = moment_arm(testclass)

def infinites_torque(y):
    return MA(y) * (Lub(y) * m.cos(alpha) + Dub(y) * m.sin(alpha))

def Torsion(y):
    T,_ = sp.integrate.quad(lambda yy: infinites_torque(yy), y, span/2.0)
    return T

ypoints = np.linspace(0.0, span/2.0 ,200)
torsion_values = np.array([Torsion(y) for y in ypoints])

plt.plot(ypoints,torsion_values)
plt.xlabel("Spanwise position [m]")
plt.ylabel("Torsion [Nm]")
plt.title("Internal Torsion Diagram")
plt.tight_layout()
plt.show()

