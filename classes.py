import numpy as np
import matplotlib.pyplot as plt
from constants import const
import scipy as sp

#Arguments to create wingbox class:
#1: n x 2 array of coords from wingbox
#2: n x 1 array of thicknesses of the wingbox panels
#3: n x 2 array of coords of stringers
#4: n x 1 array of stringer areas
class Wingbox:
    def __init__(self, wingboxpoints, panel_thickness, stringercoords, stringer_area, name=None):
        import data_import
        import area_moments
        self.name = name

        self.points = wingboxpoints
        self.panels = data_import.makepanels(wingboxpoints)
        self.panel_thickness = panel_thickness
        self.stringers = stringercoords
        self.stringer_area = stringer_area

        self.centroid_coordinates = area_moments.centroidcoords(self.panels, self.panel_thickness, self.stringers, self.stringer_area)
        self.centroidal_points = self.points - self.centroid_coordinates
        self.centroidal_panels = self.panels - np.array([self.centroid_coordinates[0], self.centroid_coordinates[1], self.centroid_coordinates[0], self.centroid_coordinates[1]])
        self.centroidal_stringers = self.stringers - self.centroid_coordinates
    
    def Ixx(self, y):
        import area_moments
        return area_moments.second_area_moment(y, self)[0]
    
    def Iyy(self, y):
        import area_moments
        return area_moments.second_area_moment(y, self)[1]
    
    def Ixy(self, y):
        import area_moments
        return area_moments.second_area_moment(y, self)[2]
    
    def J(self, y):
        import area_moments
        import constants
        scale = constants.local_chord_at_span(y)
        current_wingbox = ScaledWingbox(self, scale)
        return area_moments.Torsional_constant(current_wingbox.centroidal_points, current_wingbox.panel_thickness)
    
    def z_max_min(self, y):
        import area_moments
        return area_moments.z_max_min(y, self)

    def plot(self, showplot=True):
        import graphing
        graphing.wingbox_plot(self, showplot)

    def wing_plot(self, Npoints=50, twowings=False):
        import graphing
        graphing.wing_plot(self, Npoints, twowings)

    def deflection_plot(self, show_wing=True, two_wings=False):
        import graphing
        graphing.deflection_plot(self, show_wing, two_wings)

    def twist_plot(self):
        import graphing
        graphing.twist_plot(self)

    def I_plot(self,npoints=100):
        import graphing
        graphing.I_plot(self, npoints)
    
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
    
    def area(self, y):
        import area_moments
        import constants
        current_wingbox = ScaledWingbox(self, constants.local_chord_at_span(y))
        return area_moments.polygon_area(current_wingbox.points)
    
    def weight(self):
        import area_moments
        y_tab = np.linspace(0, const['span']/2, 1000)
        area_tab = []
        for i in y_tab:
            area_tab.append(area_moments.cross_sectional_area(self, i))

        volume = 2 * sp.integrate.cumulative_trapezoid(area_tab, y_tab, initial=0)[-1]
        mass = volume * const['Density']
        print(f'The total wingbox weights {round(mass, 3)} kg.')
        return mass
        

    
#When requiring full-size wingbox instead of unit length airfoil one, the class below can be used
#Enter the unit-length-airfoil class and the scale (i.e. chord length)
#root chord = const['root_chord']
class ScaledWingbox:
    def __init__(self, originalclass, scale):
        self.name = originalclass.name
        self.points = originalclass.points * scale
        self.panels = originalclass.panels * scale
        self.panel_thickness = originalclass.panel_thickness * scale   #Unsure if scaling is required for the designs, will be considered during WP5
        self.stringers = originalclass.stringers * scale
        self.stringer_area = originalclass.stringer_area # scale ** 2  #Stringer area is kept constant throughout all designs

        self.centroid_coordinates = originalclass.centroid_coordinates * scale
        self.centroidal_points = originalclass.centroidal_points * scale
        self.centroidal_panels = originalclass.centroidal_panels * scale
        self.centroidal_stringers = originalclass.centroidal_stringers * scale



