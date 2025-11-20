import numpy as np
import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt
import math as m

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

#From xflr5
CL0 =  0.179632
CL10 = 1.004670


#Organised aerodynamic coefficients
tablezeroalpha = np.genfromtxt("Chapter4.1\\MainWing_a=0.00HighpanelFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

yspan_0 = tablezeroalpha[:,0]
chordlength_0 = tablezeroalpha[:,1]
Ai_0 = tablezeroalpha[:,2]
Cl_0 = tablezeroalpha[:,3]
PCd_0 = tablezeroalpha[:,4]
ICd_0 = tablezeroalpha[:,5]
cmgeom_0 = tablezeroalpha[:,6]
CmAirfchord4_0 = tablezeroalpha[:,7]
posofcp_0 = tablezeroalpha[:,10]


tabletenalpha = np.genfromtxt("Chapter4.1\\MainWing_a=10.00HighplaneFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

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

def chordlength(ypos, cr, ct, span):
    chordlength = cr + (ct-cr)*2/span*ypos
    return chordlength

def chordlength2(cr,taper,span,ypos):
    chordlength2 = cr -cr*(1-taper)*ypos/(span/2)
    return chordlength2

def weightdistribution(y: float, alpha: float, step: float = span/2 / 200, LG_weight: float = 317.833/2, LG_y_pos: float = 1.9808):
    """A function that represents the weight distribution of the landing gear
    
    Parameters
    ----------
    y: float
        y position for which the weight should be given
    alpha: float
        angle of attack
    step:
        the step size of the integration to create a range in which the point mass acts
        Default is span/400
    LG_weight: float
        mass of one side of main LG in [kg]
        Default is 317.833/2
    LG_y_pos: float
        y position of the main landing gear CG
        Default is 1.9808
    
    Returns
    -------
    weight_at_y: float
        weight at y position in [N]
    """
    
    weight_at_y = 0 #add weight at chord, fuel at chord...
    
    if y - step/2 < LG_y_pos and LG_y_pos > y + step/2:
        weight_at_y += LG_weight * g

    return weight_at_y * m.cos(alpha)

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

    alpha = m.pi/18 * (CLd - CL0)/(CL10-CL0)
    return alpha


#Aerodynamic distribution for known CLd (it will give a function dependent on spanwise position)

def liftdristribution(CLd):
    def Cldistr(y):
        Cl_0y = function_Cl_0(y)
        Cl_10y = function_Cl_10(y)
        return Cl_0y + (Cl_10y - Cl_0y)/(CL10 - CL0)*(CLd - CL0)
    return Cldistr

def Lub(y):
    return liftdristribution(CLcruise)(y)*q*chordlength(y,cr,ct,span)

def shear(y, alpha):
    S, error = sp.integrate.quad(Lub,y,span/2)
    W, error2 = sp.integrate.quad(weightdistribution, y, span/2, args = (alpha)) # add the weight distribution
    return -1*(S-W)



ypoints = np.linspace(0, span/2,200)
shearvalues = np.array([shear(y, 10*m.pi/180) for y in ypoints])

print(shearvalues.min())


plt.plot(ypoints,shearvalues)
plt.xlabel("Spanwise position [m]")
plt.ylabel("Shear Force[N]")
plt.show()

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

