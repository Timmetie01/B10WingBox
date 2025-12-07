import numpy as np
import matplotlib.pyplot as plt
from constants import const
import scipy as sp

#Arguments to create wingbox class:
#1: n x 2 array of coords from wingbox
#2: n x 1 array of thicknesses of the wingbox panels
#3: n x 2 array of coords of stringers
#4: n x 1 array of stringer areas
#Optional KWArg: name. Used to title some plots. Defaults to None
class Wingbox:
    def __init__(self, wingboxpoints, panel_thickness, stringercoords, stringer_area, scaled_thickness=False, name=None):
        import data_import
        import area_moments
        self.name = name

        self.points = wingboxpoints
        self.panels = data_import.makepanels(wingboxpoints)
        self.panel_thickness = panel_thickness
        self.stringers = stringercoords
        self.stringer_area = stringer_area
        self.scaled_thickness = scaled_thickness

        self.centroid_coordinates = area_moments.centroidcoords(self.panels, self.panel_thickness, self.stringers, self.stringer_area)
        self.centroidal_points = self.points - self.centroid_coordinates
        self.centroidal_panels = self.panels - np.array([self.centroid_coordinates[0], self.centroid_coordinates[1], self.centroid_coordinates[0], self.centroid_coordinates[1]])
        self.centroidal_stringers = self.stringers - self.centroid_coordinates
    
    #Returns the Ixx at a certain spanwise location. Ixx is around chord-wise axis
    def Ixx(self, y):
        import area_moments
        return area_moments.second_area_moment(y, self)[0]
    
    #Returns the Iyy at a certain spanwise location. Iyy is around vertical axis
    def Iyy(self, y):
        import area_moments
        return area_moments.second_area_moment(y, self)[1]
    
    #Returns the Ixy at a certain spanwise location. Due to simplifications this can be assumed to be 0.
    def Ixy(self, y):
        import area_moments
        return area_moments.second_area_moment(y, self)[2]
    
    #Returns the Torsional constant of the wingbox at a certain spanwise location/
    def J(self, y):
        import area_moments
        import constants
        scale = constants.local_chord_at_span(y)
        current_wingbox = ScaledWingbox(self, scale)
        return area_moments.Torsional_constant(current_wingbox.centroidal_points, current_wingbox.panel_thickness)
    
    #Shows the point highest and lowest compared to the neutral axis. Required for normal stress due to bending.
    def z_max_min(self, y):
        import area_moments
        return area_moments.z_max_min(y, self)

    #Plots the wingbox: Panels and Stringers
    def plot(self, showplot=True):
        import graphing
        graphing.wingbox_plot(self, showplot)

    #Plots a 3D representation of the wing under worst-case loading
    def wing_plot(self, Npoints=50, twowings=False):
        import graphing
        graphing.wing_plot(self, Npoints, twowings)

    #Plots the deflection of the wing as a function of spanwise position. Show_wing plots the top and bottom surface of the wing too (Looks a lot better)
    def deflection_plot(self, show_wing=True, two_wings=False):
        import graphing
        graphing.deflection_plot(self, show_wing, two_wings)

    #Plots the twist distribution along the span of the wing
    def twist_plot(self):
        import graphing
        graphing.twist_plot(self)

    #Plots the Ixx, Iyy, Ixy and J at each spanwise position of the wing.
    def I_plot(self,npoints=100):
        import graphing
        graphing.I_plot(self, npoints)
    
    #Prints the highest bending stress present along the entire wing, by iterating along its span and checking for the highest value
    def max_bending_stress(self, Npoints=250):
        import stress_functions
        import constants
        import stress_functions
        y_tab = np.linspace(0, constants.const['span']/2, Npoints)
        stress_tab = []

        max_stress = 0
        y_max_stress = 0
        for i in y_tab:
            current_stress = stress_functions.max_bending_stress(self, i)
            stress_tab.append(current_stress)
            if current_stress > max_stress:
                max_stress = current_stress
                y_max_stress = i
        
        
        return max(stress_tab), y_max_stress
    
    #Returns the area inside the panels of the wingbox (used for fuel volume calculations)
    def area(self, y):
        import area_moments
        import constants
        current_wingbox = ScaledWingbox(self, constants.local_chord_at_span(y))
        return area_moments.polygon_area(current_wingbox.points)
    
    #Returns (and optionally prints) the weight of the entire wingbox.
    def weight(self, print_value=True):
        import area_moments
        y_tab = np.linspace(0, const['span']/2, 1000)
        area_tab = []
        for i in y_tab:
            area_tab.append(area_moments.cross_sectional_area(self, i))

        volume = 2 * sp.integrate.cumulative_trapezoid(area_tab, y_tab, initial=0)[-1]
        mass = volume * const['Density']
        if print_value:
            print(f'The total wingbox weights {round(mass, 3)} kg.')
        return mass
        
    
#When requiring full-size wingbox instead of unit length airfoil one, the class below can be used
#Enter the unit-length-airfoil class and the scale (i.e. chord length)
class ScaledWingbox:
    def __init__(self, originalclass, scale):
        self.name = originalclass.name
        self.points = originalclass.points * scale
        self.panels = originalclass.panels * scale
        self.panel_thickness = originalclass.panel_thickness * (scale if originalclass.scaled_thickness else 1) #Unsure if scaling is required for the designs, will be considered during WP5
        self.stringers = originalclass.stringers * scale
        self.stringer_area = originalclass.stringer_area  #Stringer area is kept constant throughout all designs, and thus this line must be kept commented!

        self.centroid_coordinates = originalclass.centroid_coordinates * scale
        self.centroidal_points = originalclass.centroidal_points * scale
        self.centroidal_panels = originalclass.centroidal_panels * scale
        self.centroidal_stringers = originalclass.centroidal_stringers * scale

