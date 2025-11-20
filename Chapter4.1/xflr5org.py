import numpy as np
import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
from math import cos, sin, pi

#Constants
cr = 3.108170068
ct = 0.98287858
taper = 0.316224196
span = 17.59150919
rho = 0.28711101
vinfinity = 200.5593111
q = 0.5*rho*vinfinity**2
CLcruise = 0.58020
wing_fuel_percentage = 0.7
fuel_weight = 4541.1
wing_weight = 711.736
alpha = float(float(input("Input an alpha value n degrees"))*pi/180)

#From xflr5
CL0 =  0.179632
CL10 = 1.004670


#Organised aerodynamic coefficients
tablezeroalpha = np.genfromtxt("B10WingBox\Chapter4.1\MainWing_a=0.00HighpanelFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

yspan_0 = tablezeroalpha[:,0]
chordlength_0 = tablezeroalpha[:,1]
Ai_0 = tablezeroalpha[:,2]
Cl_0 = tablezeroalpha[:,3]
PCd_0 = tablezeroalpha[:,4]
ICd_0 = tablezeroalpha[:,5]
cmgeom_0 = tablezeroalpha[:,6]
CmAirfchord4_0 = tablezeroalpha[:,7]
posofcp_0 = tablezeroalpha[:,10]


tabletenalpha = np.genfromtxt("B10WingBox\Chapter4.1\MainWing_a=10.00HighplaneFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

yspan_10 = tabletenalpha[:,0]
chordlength_10 = tabletenalpha[:,1]
Ai_10 = tabletenalpha[:,2]
Cl_10 = tabletenalpha[:,3]
PCd_10 = tabletenalpha[:,4]
ICd_10 = tabletenalpha[:,5]
cmgeom_10 = tabletenalpha[:,6]
CmAirfchord4_10 = tabletenalpha[:,7]
posofcp_10 = tabletenalpha[:,10]

plt.plot(yspan_0,Cl_0)
plt.plot(yspan_10,Cl_10)
plt.title("Coefficient of lift for half-span")
plt.xlabel("Span position [m]")
plt.ylabel("Coefficient of lift")
plt.legend(("alpha = 0", "alpha = 10"))
plt.show()

#Function relating cl,cd,cm4 to y position

function_Cl_0 = sp.interpolate.interp1d(yspan_0,Cl_0,kind="cubic",fill_value="extrapolate")
print(function_Cl_0(0.296))

function_Cl_10 = sp.interpolate.interp1d(yspan_10,Cl_10,kind="cubic",fill_value="extrapolate")

function_Cd_0 = sp.interpolate.interp1d(yspan_0,ICd_0,kind="cubic",fill_value="extrapolate")
function_Cd_10 = sp.interpolate.interp1d(yspan_10,ICd_10,kind="cubic",fill_value="extrapolate")

function_cm4_0 = sp.interpolate.interp1d(yspan_0,CmAirfchord4_0,kind="cubic",fill_value="extrapolate")
function_cm4_0 = sp.interpolate.interp1d(yspan_10,CmAirfchord4_10,kind="cubic",fill_value="extrapolate")

def chord_length(ypos):
    chordlength = cr + (ct-cr)*2/span*ypos
    return chordlength

def chordlength2(cr,taper,span,ypos):
    chordlength2 = cr -cr*(1-taper)*ypos/(span/2)
    return chordlength2

#Distrinuted lift coefficient which produces total lift CLdes (it will give a function dependent on spanwise position)

def liftdristribution(CLd):
    def Cldistr(y):
        Cl_0y = function_Cl_0(y)
        Cl_10y = function_Cl_10(y)
        return Cl_0y + (Cl_10y - Cl_0y)/(CL10 - CL0)*(CLd - CL0)
    return Cldistr

#Lift per unit span 
def Lub(y):
    return liftdristribution(CLcruise)(y)*q*chord_length(y)


#Another way
#plt.title("Noisy data")
#plt.plot(yspan_0,Cl_0,"r+")
#plt.show()


#order = 20

#coefficients = np.polyfit(yspan_0,Cl_0,order)
#polynomial = np.poly1d(coefficients)
#ysmooth = np.polyval(polynomial,yspan_0)

#plt.plot(yspan_0,ysmooth)
#plt.plot(yspan_0,Cl_0,"r+")
#plt.title(f"polynomial {order} order")
#plt.show()

   # print(polynomial)


#Weight distribution function

fuel_weight = wing_fuel_percentage*fuel_weight
total_wing_weight = wing_weight + fuel_weight

halfspan_chord_summation, error = sp.integrate.quad(chord_length,0,span/2)

print(halfspan_chord_summation)

def distributed_weight(y):
    return chord_length(y)/halfspan_chord_summation * total_wing_weight/2


def shear(y):
    if alpha == 0:
        S, error = sp.integrate.quad(Lub,y,span/2)
        S2, error = sp.integrate.quad(distributed_weight,y,span/2)
        return -1*S1 + S2
    else:
        S1, error = sp.integrate.quad(Lub*cos(alpha),y,span/2)
        S2, error = sp.integrate.quad(distributed_weight*cos(alpha),y,span/2)
        return -1*S1 + S2


ypoints = np.linspace(0, span/2,200)
shearvalues = np.array([shear(y) for y in ypoints])

plt.plot(ypoints,shearvalues)
plt.xlabel("Spanwise position [m]")
plt.ylabel("Shear Force[N]")
plt.show()

