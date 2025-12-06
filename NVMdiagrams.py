import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math as m
import os

import data_import

from constants import const, ISA
from math import cos, sin, pi
from manoeuvre_envelope import data_from_envelope
from data_from_xflr5 import xcppos_func
from classes import Wingbox


# Constants
cr = const['root_chord']
ct = const['tip_chord']
span = 17.5746
#span = const['span']
g = 9.80665

# Fuel
fuel_weight = 4541.1

# Wing
wing_weight = 711.736

#From xflr5
CL0 =  0.179632
CL10 = 1.004670

# Landing gear
LG_weight = const['main_landing_gear_mass']
LG_y_pos = const['main_landing_gear_y_position']

#Organised aerodynamic coefficients
tablezeroalpha = np.genfromtxt("MainWing_a=0.00HighpanelFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

yspan_0 = tablezeroalpha[:,0]
chordlength_0 = tablezeroalpha[:,1]
Ai_0 = tablezeroalpha[:,2]
Cl_0 = tablezeroalpha[:,3]
PCd_0 = tablezeroalpha[:,4]
ICd_0 = tablezeroalpha[:,5]
cmgeom_0 = tablezeroalpha[:,6]
CmAirfchord4_0 = tablezeroalpha[:,7]
posofcp_0 = tablezeroalpha[:,10]


tabletenalpha = np.genfromtxt("MainWing_a=10.00HighplaneFinal.csv", delimiter=",", skip_header=91, skip_footer=5743)

yspan_10 = tabletenalpha[:,0]
chordlength_10 = tabletenalpha[:,1]
Ai_10 = tabletenalpha[:,2]
Cl_10 = tabletenalpha[:,3]
PCd_10 = tabletenalpha[:,4]
ICd_10 = tabletenalpha[:,5]
cmgeom_10 = tabletenalpha[:,6]
CmAirfchord4_10 = tabletenalpha[:,7]
posofcp_10 = tabletenalpha[:,10]

# Visual Check
# plt.plot(yspan_0,Cl_0)
# plt.plot(yspan_10,Cl_10)
# plt.title("Coefficient of lift for half-span")
# plt.xlabel("Span position [m]")
# plt.ylabel("Coefficient of lift")
# plt.legend(("alpha = 0","alpha=10"))
# plt.tight_layout()
# plt.show()

#Function relating cl,cd,cm4 to y position

function_Cl_0 = sp.interpolate.interp1d(yspan_0,Cl_0,kind="cubic",fill_value="extrapolate")
function_Cl_10 = sp.interpolate.interp1d(yspan_10,Cl_10,kind="cubic",fill_value="extrapolate")

function_Ai_0 = sp.interpolate.interp1d(yspan_0,Ai_0,kind="cubic",fill_value="extrapolate")
function_Ai_10 = sp.interpolate.interp1d(yspan_10,Ai_10,kind="cubic",fill_value="extrapolate")

#Aerodynamic distribution for known CLd (it will give a function dependent on spanwise position)
#Distrinuted lift coefficient which produces total lift CLdes (it will give a function dependent on spanwise position)

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
        Ai_interpolated = Ai_0y + (Ai_10y - Ai_0y)/(CL10 - CL0)*(CLd_specific - CL0) * m.pi/180
        Cl_0y = float(function_Cl_0(y))
        Cl_10y = float(function_Cl_10(y))
        Cl_interpolated = Cl_0y + (Cl_10y - Cl_0y)/(CL10 - CL0)*(CLd_specific - CL0)
        return Ai_interpolated * Cl_interpolated
    return Cd_distr

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

def get_centroid(wingbox):
        scpos = wingbox.centroid_coordinates[0]
        return scpos 

def loading(CL_design: float, q: float, n: float, wingbox: Wingbox, wing_fuel_percentage: float, show_graphs: bool = False):
    CLd = CL_design
    alpha = alphafromCLd(CLd)
    wing_fuel_percentage = wing_fuel_percentage

    #This is going to give Cd_distr(y)
    drag_dist_func = drag_distr(CLd)
    #print(f"This is the drag distr: {drag_dist_func}")

    #Drag per unit span
    def Dub(y):
        return drag_dist_func(y)*q*chord_length(y)

    lift_dist_func = liftdristribution(CLd)
    #Lift per unit span 
    def Lub(y):
        return lift_dist_func(y)*q*chord_length(y)


    #Weight distribution function
    fuel_weight_used = wing_fuel_percentage * fuel_weight

    def shear(y):
            S1, error = sp.integrate.quad(lambda yy: Lub(yy)*m.cos(alpha),y,span/2.0)
            #S2, error = sp.integrate.quad(lambda yy: distributed_weight(yy)*m.cos(alpha),y,span/2.0)
            S3,error = sp.integrate.quad(lambda yy: Dub(yy)*m.sin(alpha), y, span/2.0)

            #V = -S1 + S2 - S3
            V = 0
            V = -S1 - S3

            if y < LG_y_pos:
                V += LG_weight * g

            return  V
    



    ypoints = np.linspace(0.0, span/2.0 ,100)

    # Distributed structural weight
    new_distr_w = np.array([n * wing_weight/const['wing_area']*chord_length(y)*span/2 /100 * g for y in ypoints])
    new_distr_w = new_distr_w[::-1]
    new_distr_w = np.cumsum(new_distr_w)
    new_distr_w = new_distr_w[::-1]

    # Distributed fuel weight
    ypoints_A = np.array([wingbox.area(y) for y in ypoints])
    totalA = np.sum(ypoints_A)
    fuel_distr_w = ypoints_A/totalA * fuel_weight_used/2 * g * n
    #print(np.sum(fuel_distr_w))
    # if show_graphs:
    #     plt.plot(ypoints,fuel_distr_w)
    #     plt.xlabel("Spanwise position [m]")
    #     plt.ylabel("Fuel Weight [N]")
    #     # plt.title("Fuel Weight Distribution")
    #     plt.tight_layout()
    #     plt.show()
    fuel_distr_w = fuel_distr_w[::-1]
    fuel_distr_w = np.cumsum(fuel_distr_w)
    fuel_distr_w = fuel_distr_w[::-1]
    
    
    shearvalues = fuel_distr_w + np.array([shear(y) for y in ypoints]) + new_distr_w

    if show_graphs:
        plt.plot(ypoints,shearvalues)
        plt.grid()
        plt.xlabel("Spanwise position [m]")
        plt.ylabel("Shear Force [N]")
        # plt.title("Internal Shear Force Diagram")
        plt.tight_layout()
        plt.show()

    order = 15
    coefficients = np.polyfit(ypoints,shearvalues,order)
    polynomial = np.poly1d(coefficients)
    shearsmooth = np.polyval(polynomial,ypoints)

    # if show_graphs:
    #     plt.plot(ypoints,shearsmooth)
    #     plt.plot(ypoints,shearvalues,"r+")
    #     # plt.title(f"Polynomial of {order}th order")
    #     plt.show()

    #Moment Function dM/dy = V

    def Moment(y):
        M,_ = sp.integrate.quad(polynomial,y,span/2.0)
        return M

    momentvalues = np.array([Moment(y) for y in ypoints])

    if show_graphs:
        plt.plot(ypoints,momentvalues)
        plt.grid()
        plt.xlabel("Spanwise position [m]")
        plt.ylabel("Moment [Nm]")
        # plt.title("Internal Moment Diagram")
        plt.show()

    #We're going to have xcp as a funciton of (y)
    xcppos_func1 = xcppos_func(CLd)

    #Moment arm for a specific alpha and span position
    def moment_arm(wingbox):
        def distance(y):
            sc = get_centroid(wingbox)
            return (xcppos_func1(y) - sc) * chord_length(y)
        return distance

    MA = moment_arm(wingbox)

    def infinites_torque(y):
        return MA(y) * (Lub(y) * m.cos(alpha) + Dub(y) * m.sin(alpha))

    def Torsion(y):
        T,_ = sp.integrate.quad(lambda yy: infinites_torque(yy), y, span/2.0)

        if y < const['main_landing_gear_y_position']:
            T -= (2.24655-get_centroid(wingbox)*chord_length(const['main_landing_gear_y_position'])) * const['main_landing_gear_mass'] * g * n
            #print(2.24655-get_centroid(wingbox)*chord_length(const['main_landing_gear_y_position']))

        return T

    torsion_values = np.array([Torsion(y) for y in ypoints])

    if show_graphs:
        plt.plot(ypoints,torsion_values)
        plt.xlabel("Spanwise position [m]")
        plt.ylabel("Torsion [Nm]")
        # plt.title("Internal Torsion Diagram")
        plt.tight_layout()
        plt.grid()
        plt.show()

    return shearvalues, momentvalues, torsion_values

    # Torsion (copied from liftarm.py)
    

def generate_loading(case_number: int, wingbox: Wingbox, show_graphs = False):
    # Find loading parameters like density etc. from the loading case
    envelope_data: np.void = data_from_envelope.get_case(case_number)
    altitude = int(envelope_data['Altitude'][2:])* 100 * 0.3048 # [m]
    density = ISA(altitude)[2] # [kg/m^3]
    TAS = float(envelope_data['Indicated_Airspeed'] * m.sqrt(ISA(0)[2]/density)) # [m/s]
    n = float(envelope_data['n']) # [-]
    W = float(envelope_data['Mass']) * g # [N]

    # Calculate relevant parameters    
    q = 1/2 * density * TAS**2
    CL = n*W/(q*const['wing_area'])
    #print(alphafromCLd(CL)*180/m.pi)

    wing_fuel_percentage = 0 if W < 12000 * g else 0.7

    # Actually assumes that the whole lift curve is linear, which is of course nonsensical, maybe we could hardcode some values
    results = loading(CL, q, n, wingbox, wing_fuel_percentage, show_graphs)
    return results[0], results[1], results[2]


def find_worst_loading(first: int, last: int, wingbox, save_folder="worst_cases", show_graphs = False): # Made with ChatGPT
    # Prepare output folder
    os.makedirs(save_folder, exist_ok=True)

    # Worst-case tracking
    abs_max_shear = 0
    abs_max_shear_num = None
    abs_min_shear = 0
    abs_min_shear_num = None

    abs_max_bending = 0
    abs_max_bending_num = None
    abs_min_bending = 0
    abs_min_bending_num = None

    abs_max_torsion = 0
    abs_max_torsion_num = None
    abs_min_torsion = 0
    abs_min_torsion_num = None

    # Store full arrays for saving later
    worst_cases_data = {
        "abs_max_shear":      None,
        "abs_min_shear":      None,
        "abs_max_bending":    None,
        "abs_min_bending":    None,
        "abs_max_torsion":    None,
        "abs_min_torsion":    None,
    }

    for case_number in range(first, last + 1):
        shear, bending, torsion = generate_loading(case_number, wingbox)

        shear_max = shear.max()
        shear_min = shear.min()
        bending_max = bending.max()
        bending_min = bending.min()
        torsion_max = torsion.max()
        torsion_min = torsion.min()

        # --- Update max shear ---
        if abs(shear_max) > abs(abs_max_shear):
            abs_max_shear = shear_max
            abs_max_shear_num = case_number
            worst_cases_data["abs_max_shear"] = (shear, bending, torsion)

        # --- Update min shear ---
        if abs(shear_min) > abs(abs_min_shear):
            abs_min_shear = shear_min
            abs_min_shear_num = case_number
            worst_cases_data["abs_min_shear"] = (shear, bending, torsion)

        # --- Update max bending ---
        if abs(bending_max) > abs(abs_max_bending):
            abs_max_bending = bending_max
            abs_max_bending_num = case_number
            worst_cases_data["abs_max_bending"] = (shear, bending, torsion)

        # --- Update min bending ---
        if abs(bending_min) > abs(abs_min_bending):
            abs_min_bending = bending_min
            abs_min_bending_num = case_number
            worst_cases_data["abs_min_bending"] = (shear, bending, torsion)

        # --- Update max torsion ---
        if abs(torsion_max) > abs(abs_max_torsion):
            abs_max_torsion = torsion_max
            abs_max_torsion_num = case_number
            worst_cases_data["abs_max_torsion"] = (shear, bending, torsion)

        # --- Update min torsion ---
        if abs(torsion_min) > abs(abs_min_torsion):
            abs_min_torsion = torsion_min
            abs_min_torsion_num = case_number
            worst_cases_data["abs_min_torsion"] = (shear, bending, torsion)

        print(f"Checked case {case_number}")

    # -----------------------------------------------------
    # Save the six worst-case files
    # -----------------------------------------------------
    save_map = {
        "abs_max_shear":   abs_max_shear_num,
        "abs_min_shear":   abs_min_shear_num,
        "abs_max_bending": abs_max_bending_num,
        "abs_min_bending": abs_min_bending_num,
        "abs_max_torsion": abs_max_torsion_num,
        "abs_min_torsion": abs_min_torsion_num,
    }

    for key, case_num in save_map.items():
        if case_num is None:
            continue  # skip if not found

        shear, bending, torsion = worst_cases_data[key]

        save_path = os.path.join(save_folder, f"{key}.npz")
        np.savez(
            save_path,
            case_number=case_num,
            shear=shear,
            bending=bending,
            torsion=torsion
        )

        print(f"Saved {key} to {save_path}")

    return save_map



# Put all code under this if statement otherwise the code becomes circular with xflr5
if __name__ == "__main__":
    testclass = data_import.import_wingbox('test_cross_section')
    #find_worst_loading(1, 32, testclass)

    generate_loading(20, testclass, show_graphs=True)