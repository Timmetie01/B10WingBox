import numpy as np
import matplotlib.pyplot as plt

#Arguments to create wingbox class:
#1: n x 2 array of coords from wingbox
#2: n x 1 array of thicknesses of the wingbox panels
#3: n x 2 array of coords of stringers
#4: n x 1 array of stringer areas
class Wingbox:
    def __init__(self, wingboxpoints, panel_thickness, stringercoords, stringer_area):
        import data_import
        import area_moments

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
    
    
#When requiring full-size wingbox instead of unit length airfoil one, the class below can be used
#Enter the unit-length-airfoil class and the scale (i.e. chord length)
class ScaledWingbox:
    def __init__(self, originalclass, scale):
        self.points = originalclass.points * scale
        self.panels = originalclass.panels * scale
        self.panel_thickness = originalclass.panel_thickness * scale
        self.stringers = originalclass.stringers * scale
        self.stringer_area = originalclass.stringer_area * scale ** 2

        self.centroid_coordinates = originalclass.centroid_coordinates * scale
        self.centroidal_points = originalclass.centroidal_points * scale
        self.centroidal_panels = originalclass.centroidal_panels * scale
        self.centroidal_stringers = originalclass.centroidal_stringers * scale



