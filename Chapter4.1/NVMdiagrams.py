import numpy as np
import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
import math as m
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
g = 9.80665
wing_fuel_percentage = 0.7
fuel_weight = 4541.1
wing_weight = 711.736

#From xflr5
CL0 =  0.179632
CL10 = 1.004670

# Landing gear
LG_weight = 317.833/2
LG_y_pos = 1.9808

def chord_length(ypos):

    return cr + (ct-cr)*2/span*ypos

def alphafromCLd(CLd):
    """A function that gives the alpha for a given CLd. Assumes that the lift coefficient is linear between 0 and 10 degrees.
    
    Parameters
    ----------
    CLd: float
        the desired lift coefficient
    
    Returns
    -------
    alpha: float
        angle of attack [rad]

    """

    alpha_deg = (CLd - CL0)/(CL10-CL0)*10.0
    return m.radians(alpha_deg)

CLd = float(input("Input a CLd = "))
alpha = alphafromCLd(CLd)

print(f"Calculations for alpha = {alpha} rad ({m.degrees(alpha)} deg) for CLd={CLd}")

#Organised aerodynamic coefficients
tablezeroalpha = np.genfromtxt("Chapter4.1\MainWing_a=0.00HighpanelFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

yspan_0 = tablezeroalpha[:,0]
chordlength_0 = tablezeroalpha[:,1]
Ai_0 = tablezeroalpha[:,2]
Cl_0 = tablezeroalpha[:,3]
PCd_0 = tablezeroalpha[:,4]
ICd_0 = tablezeroalpha[:,5]
cmgeom_0 = tablezeroalpha[:,6]
CmAirfchord4_0 = tablezeroalpha[:,7]
posofcp_0 = tablezeroalpha[:,10]


tabletenalpha = np.genfromtxt("Chapter4.1\MainWing_a=10.00HighplaneFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

yspan_10 = tabletenalpha[:,0]
chordlength_10 = tabletenalpha[:,1]
Ai_10 = tabletenalpha[:,2]
Cl_10 = tabletenalpha[:,3]
PCd_10 = tabletenalpha[:,4]
ICd_10 = tabletenalpha[:,5]
cmgeom_10 = tabletenalpha[:,6]
CmAirfchord4_10 = tabletenalpha[:,7]
posofcp_10 = tabletenalpha[:,10]

#Visual Check

plt.plot(yspan_0,Cl_0)
plt.plot(yspan_10,Cl_10)
plt.title("Coefficient of lift for half-span")
plt.xlabel("Span position [m]")
plt.ylabel("Coefficient of lift")
plt.legend(("alpha = 0","alpha=10"))
plt.show()

#Function relating cl,cd,cm4 to y position

function_Cl_0 = sp.interpolate.interp1d(yspan_0,Cl_0,kind="cubic",fill_value="extrapolate")
#print(function_Cl_0(0.296))

function_Cl_10 = sp.interpolate.interp1d(yspan_10,Cl_10,kind="cubic",fill_value="extrapolate")

function_Cd_0 = sp.interpolate.interp1d(yspan_0,ICd_0,kind="cubic",fill_value="extrapolate")
function_Cd_10 = sp.interpolate.interp1d(yspan_10,ICd_10,kind="cubic",fill_value="extrapolate")

function_cm4_0 = sp.interpolate.interp1d(yspan_0,CmAirfchord4_0,kind="cubic",fill_value="extrapolate")
function_cm4_10 = sp.interpolate.interp1d(yspan_10,CmAirfchord4_10,kind="cubic",fill_value="extrapolate")

function_Ai_0 = sp.interpolate.interp1d(yspan_0,Ai_0,kind="cubic",fill_value="extrapolate")
function_Ai_10 = sp.interpolate.interp1d(yspan_10,Ai_10,kind="cubic",fill_value="extrapolate")


#Aerodynamic distribution for known CLd (it will give a function dependent on spanwise position)
#Distrinuted lift coefficient which produces total lift CLdes (it will give a function dependent on spanwise position)

'''
def induced_angle(CLd_specific):
    def Ai_distr(y):
        Ai_0y = float(function_Ai_0(y))
        Ai_10y = float(function_Ai_10(y))
        return Ai_0y + (Ai_10y - Ai_0y)/(CL10 - CL0)*(CLd_specific - CL0)
    return Ai_distr
'''

def liftdristribution(CLd_specific):
    def Cldistr(y):
        Cl_0y = float(function_Cl_0(y))
        Cl_10y = float(function_Cl_10(y))
        return Cl_0y + (Cl_10y - Cl_0y)/(CL10 - CL0)*(CLd_specific - CL0)
    return Cldistr

def drag_distr(CLd_specific):
    def Cd_distr(y):
        Ai_0y = float(function_Ai_0(y))
        Ai_10y = float(function_Ai_10(y))
        Cl_0y = float(function_Cl_0(y))
        Cl_10y = float(function_Cl_10(y))
        return (Ai_0y + (Ai_10y - Ai_0y)/(CL10 - CL0)*(CLd_specific - CL0))*(Cl_0y + (Cl_10y - Cl_0y)/(CL10 - CL0)*(CLd_specific - CL0))
    return Cd_distr
'''
def drag_distr(CLd_specific):
    def Cd_distr(y):
        Ai_for_cd = induced_angle(CLd_specific)
        Cl_for_cd = liftdristribution(CLd_specific)
        return Ai_for_cd * Cl_for_cd
    return Cd_distr
'''

#This is going to gove Cd_distr(y)
drag_dist_func = drag_distr(CLd)
print(f"This is the drag distr: {drag_dist_func}")

#Drag per unit span
def Dub(y):
    return drag_dist_func(y)*q*chord_length(y)

lift_dist_func = liftdristribution(CLd)
#Lift per unit span 
def Lub(y):
    return lift_dist_func(y)*q*chord_length(y)

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

fuel_weight_used = wing_fuel_percentage * fuel_weight
total_wing_weight = wing_weight + fuel_weight_used

halfspan_chord_summation, error = sp.integrate.quad(chord_length,0.0,span/2.0)
print(f"Half-span chord integral = {halfspan_chord_summation}")

def distributed_weight(y):
    return chord_length(y)/halfspan_chord_summation * total_wing_weight/2.0 * g

def shear(y):
        S1, error = sp.integrate.quad(lambda yy: Lub(yy)*m.cos(alpha),y,span/2.0)
        S2, error = sp.integrate.quad(lambda yy: distributed_weight(yy)*m.cos(alpha),y,span/2.0)
        S3,error = sp.integrate.quad(lambda yy: Dub(yy)*m.sin(alpha), y, span/2.0)

        #V = -S1 + S2 - S3
        V = 0

        if y < LG_y_pos:
            V += LG_weight * g

        return  V


ypoints = np.linspace(0.0, span/2.0 ,200)
shearvalues = np.array([shear(y) for y in ypoints])

plt.plot(ypoints,shearvalues)
plt.xlabel("Spanwise position [m]")
plt.ylabel("Shear Force[N]")
plt.show()

order = 15
coefficients = np.polyfit(ypoints,shearvalues,order)
polynomial = np.poly1d(coefficients)
shearsmooth = np.polyval(polynomial,ypoints)

plt.plot(ypoints,shearsmooth)
plt.plot(ypoints,shearvalues,"r+")
plt.title(f"Polynomial of {order}th order")
plt.show()

#Moment Function dM/dy = V

def Moment(y):
    M,_ = sp.integrate.quad(polynomial,y,span/2.0)
    return M

momentvalues = np.array([Moment(y) for y in ypoints])

plt.plot(ypoints,momentvalues)
plt.xlabel("Spanwise position [m]")
plt.ylabel("Moment Force[N*m]")
plt.show()

#Torsion = momentarm * Lift *cos(alpha) + momentarm * Drag*sin(alpha)

#   momentarm (y) * Lub(y) 
# momentarm (y) * Dub(y)

# Torsion = integration accounting for angles and then return sum 