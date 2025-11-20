import numpy as np



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
        self.stringerarea = stringer_area

        self.centroid_coordinates = area_moments.centroidcoords(self.panels, self.panel_thickness, self.stringers, self.stringerarea)
        self.centroidal_points = self.points - self.centroid_coordinates
        self.centroidal_panels = self.points - np.array(self.centroid_coordinates + self.centroid_coordinates)
        self.centroidal_stringers = self.stringers - self.centroid_coordinates


