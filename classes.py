import numpy as np
import matplotlib.pyplot as plt
from constants import const
import scipy as sp

#Arguments to create wingbox class:
#1: n x 2 array of coords from wingbox
#2: n x 1 array of thicknesses of the wingbox panels
#3: n x 2 array of coords of stringers
#4: n x 1 array of stringer areas
#Optional KWArg: name. Used to title some plots, Defaults to None. scaled_thickness: When True, thickness linear with chord, default False. idealizable: True if shear flow can be calculated, default False
class Wingbox:

    def __init__(self, wingboxpoints, panel_thickness, stringercoords, stringer_area, scaled_thickness=False, idealizable=False, name=None):
        '''
        Creates the wingbox class, 
        
        :param wingboxpoints: n x 2 array of coords from wingbox
        :param panel_thickness: n x 1 array of thicknesses of the wingbox panels
        :param stringercoords: n x 2 array of coords of stringers
        :param stringer_area: n x 1 array of stringer areas
        :param scaled_thickness: When True, thickness linearly related with chord, default False
        :param idealizable: True if shear flow can be calculated (i.e. it meets some assumptions used by that function), default False
        :param name: Used to title some plots, Defaults to None.
        '''
        from data_import import makepanels
        import area_moments
        self.name = name

        self.points = wingboxpoints
        self.panels = makepanels(wingboxpoints)
        self.panel_thickness = panel_thickness
        self.stringers = stringercoords
        self.stringer_area = stringer_area
        self.scaled_thickness = scaled_thickness

        self.panel_length = np.sqrt((self.panels[:,2] - self.panels[:,0]) ** 2 + (self.panels[:,3] - self.panels[:,1]) ** 2 )
        self.panel_length = np.transpose(np.array([self.panel_length]))

        self.centroid_coordinates = area_moments.centroidcoords(self.panels, self.panel_thickness, self.stringers, self.stringer_area)
        self.centroidal_points = self.points - self.centroid_coordinates
        self.centroidal_panels = self.panels - np.array([self.centroid_coordinates[0], self.centroid_coordinates[1], self.centroid_coordinates[0], self.centroid_coordinates[1]])
        self.centroidal_stringers = self.stringers - self.centroid_coordinates

        self.idealizable = idealizable
        if idealizable:
            self.idealized_point_areas = np.zeros_like(self.panel_thickness)
            panelarea = self.panel_thickness * self.panel_length 
            self.idealized_point_areas += panelarea / 6 * (2 + np.roll(np.transpose([self.centroidal_points[:,1]]), -1, axis=0) / np.transpose([self.centroidal_points[:,1]]))
            self.idealized_point_areas += np.roll(panelarea, 1, axis=0) / 6 * (2 + np.roll(np.transpose([self.centroidal_points[:,1]]), 1, axis=0) / np.transpose([self.centroidal_points[:,1]]))
            
            
            top_or_bottom_panel_count = (len(self.centroidal_points) - (self.centroidal_points[:,0] >= np.max(self.centroidal_points[:,0]) - 1e-6).sum() * 2 + 4)//2
            #web_point_count = (len(self.centroidal_points) - 2 * top_or_bottom_panel_count)//2
    
            
            stringers_per_side = len(self.stringers) // 2
            panels_per_stringer = (top_or_bottom_panel_count - 1) // (stringers_per_side + 1)

            for i in range(len(self.stringer_area) // 2):
                #top
                self.idealized_point_areas[(i + 1) * (panels_per_stringer)] += self.stringer_area[i]
                
                #bottom
                self.idealized_point_areas[len(self.points)//2 + (i + 1) * (panels_per_stringer)] += self.stringer_area[i + len(self.stringers) //2]
            

    
    #Returns the Ixx at a certain spanwise location. Ixx is around chord-wise axis
    def Ixx(self, y):
        '''
        Calculates and returns Ixx at a certain spanwise position
        
        :param y: Spanwise location
        '''
        import area_moments
        return area_moments.second_area_moment(y, self)[0]
    
    #Returns the Iyy at a certain spanwise location. Iyy is around vertical axis
    def Iyy(self, y):
        '''
        Calculates and returns Iyy at a certain spanwise position
        
        :param y: Spanwise location
        '''
        import area_moments
        return area_moments.second_area_moment(y, self)[1]
    
    #Returns the Ixy at a certain spanwise location. Due to simplifications this can be assumed to be 0.
    def Ixy(self, y):
        '''
        Calculates and returns Ixy at a certain spanwise position
        
        :param y: Spanwise location
        '''
        import area_moments
        return area_moments.second_area_moment(y, self)[2]
    
    #Returns the Torsional constant of the wingbox at a certain spanwise location/
    def J(self, y):
        '''
        Calculates and returns the Torsional Constant J at a certain spanwise position
        
        :param y: Spanwise location
        '''
        import area_moments
        import constants
        scale = constants.local_chord_at_span(y)
        current_wingbox = ScaledWingbox(self, scale)
        return area_moments.Torsional_constant(current_wingbox.centroidal_points, current_wingbox.panel_thickness)

    #Shows the point highest and lowest compared to the neutral axis. Required for normal stress due to bending.
    def z_max_min(self, y):
        '''
        Returns the points highest and lowest compared to centroidal chordwise axis. Used for max bending stress
        
        :param y: Spanwise location
        '''
        import area_moments
        return area_moments.z_max_min(y, self)

    #Plots the wingbox: Panels and Stringers
    def plot(self, showplot=True):
        '''
        Plots the wingbox skin, stringers and spar.
        
        :param showplot: Shows plot if True. If not true, the wingbox will be drawn but the plot can be expanded upon before showing
        '''
        import graphing
        graphing.wingbox_plot(self, showplot)

    #Plots a 3D representation of the wing under worst-case loading
    def wing_plot(self, Npoints=50, twowings=False):
        '''
        Plots a 3d surface of the wing under worst case bending and twist
        
        :param Npoints: The amount of spanwise points at which the surface is plotted
        :param twowings: Plots both left and right wing when True, default False
        '''
        import graphing
        graphing.wing_plot(self, Npoints, twowings)

    #Plots the deflection of the wing as a function of spanwise position. Show_wing plots the top and bottom surface of the wing too (Looks a lot better)
    def deflection_plot(self, show_wing=True, two_wings=False):
        '''
        Plots the deflection of the wing along its span

        :param show_wing: Plots upper and lower surface too, looks better. Default True
        :param two_wings: Plots both left and right wing when True, default False
        '''
        import graphing
        graphing.deflection_plot(self, show_wing, two_wings)

    #Plots the twist distribution along the span of the wing
    def twist_plot(self):
        '''
        Plots the twist distribution along the span of the wing
        '''
        import graphing
        graphing.twist_plot(self)

    #Plots the Ixx, Iyy, Ixy and J at each spanwise position of the wing.
    def I_plot(self,npoints=100):
        '''
        Graphs the distribution of Ixx, Iyy, Ixy and J along the span of the wing

        :param npoints: The amount of spanwise points at which the variables are calculated
        '''
        import graphing
        graphing.I_plot(self, npoints)
    
    #Returns the highest bending stress present along the entire wing, by iterating along its span and checking for the highest value
    def max_bending_stress(self, Npoints=250):
        '''
        Returns the highest bending stress present along the entire wing, by iterating along its span and checking for the highest value
        
        :param Npoints: The amount of points along the span at which the stresses are calculated
        '''
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
        '''
        Returns the area inside the wingbox at a certain spanwise points (used for fuel volume)

        :param y: Spanwise location
        '''
        import area_moments
        import constants
        current_wingbox = ScaledWingbox(self, constants.local_chord_at_span(y))
        return area_moments.polygon_area(current_wingbox.points)
    
    #Returns (and optionally prints) the weight of the entire wingbox.
    def weight(self, print_value=True):
        '''
        Returns the total weight of the wingbox. (Takes both left and right wing into account)
        
        :param print_value: When True, also prints the weight of the wingbox. Default True
        '''
        import area_moments
        y_tab = np.linspace(0, const['span']/2, 1000)
        area_tab = []
        for i in y_tab:
            area_tab.append(area_moments.cross_sectional_area(self, i))

        volume = 2 * sp.integrate.cumulative_trapezoid(area_tab, y_tab, initial=0)[-1]
        mass = volume * const['Density']
        if print_value:
            print(f'The total wingbox weighs {round(mass, 3)} kg.')
        return mass
    
    def shear_flow(self, y):
        '''
        Calculates and returns the shear flow on each panel of the wing box. 
        
        :param y: Spanwise location
        '''
        from stress_functions import shear_stress
        return shear_stress(self, y)
    
    def shear_stress(self, y):
        '''
        Calculates and returns the shear stress on each panel of the wing box. 
        
        :param y: Spanwise location
        '''
        shear_flow = self.shear_flow(y)
        return shear_flow / self.panel_thickness
    
    def shear_flow_plot(self, y):
        '''
        Plots the shear flow in the skin of the wingbox at a certain spanwise location
        
        :param y: Spanwise location
        '''
        import graphing
        graphing.shear_flow_plot(self, y)

    def shear_flow_spanwise_plot(self, showplot=True):
        '''
        Plots the distribution of the highest shear flow at each cross-section along the span

        :param showplot: Spanwise location
        '''
        import graphing
        graphing.shear_flow_spanwise_plot(self, showplot)

    def worst_spar_shear_MOS(self, Npoints = 50):
        '''
        Returns the lowest Margin of Safety to the critical/buckling shear load found in the entire wing
        
        :param Npoints: The amount of spanwise points at which the properties are calculated
        '''
        import stress_functions
        y_tab = np.linspace(0, const['span']/2, Npoints, endpoint=False)
        MOS_tab = []
        for i in y_tab:
            MOS_tab.append(stress_functions.spar_buckling_MOS(self, i))
            print(f'Calculating worst case shear MOS, {round(i * 100 / max(y_tab),1)}%', end='\r', flush=True)
        print('')
        return min(MOS_tab)



        
    
#When requiring full-size wingbox instead of unit length airfoil one, the class below can be used
#Enter the unit-length-airfoil class and the scale (i.e. chord length)
class ScaledWingbox:
    def __init__(self, originalclass, scale):
        '''
        To easily work with local cross-sections, this class was created. Simply enter the original wingbox, and the scale (often constants.local_chord_at_span(y)) and all properties are scaled as required
        
        :param originalclass: The original unit length wingbox class
        :param scale: The scale with which the coordinates of the original class must be multiplied, such as the chord length
        '''
        self.name = originalclass.name
        self.points = originalclass.points * scale
        self.panels = originalclass.panels * scale
        self.panel_thickness = originalclass.panel_thickness * (scale if originalclass.scaled_thickness else 1) #Unsure if scaling is required for the designs, will be considered during WP5
        self.stringers = originalclass.stringers * scale
        self.stringer_area = originalclass.stringer_area  #Stringer area is kept constant throughout all designs, and thus this line must be kept commented!

        self.panel_length = np.sqrt((self.panels[:,2] - self.panels[:,0]) ** 2 + (self.panels[:,3] - self.panels[:,1]) ** 2 )
        self.panel_length = np.transpose(np.array([self.panel_length]))

        self.centroid_coordinates = originalclass.centroid_coordinates * scale
        self.centroidal_points = originalclass.centroidal_points * scale
        self.centroidal_panels = originalclass.centroidal_panels * scale
        self.centroidal_stringers = originalclass.centroidal_stringers * scale

        self.idealizable = originalclass.idealizable
        if self.idealizable:
            self.idealized_point_areas = np.zeros_like(self.panel_thickness)
            panelarea = self.panel_thickness * self.panel_length 
            self.idealized_point_areas += panelarea / 6 * (2 + np.roll(np.transpose([self.centroidal_points[:,1]]), -1, axis=0) / np.transpose([self.centroidal_points[:,1]]))
            self.idealized_point_areas += np.roll(panelarea, 1, axis=0) / 6 * (2 + np.roll(np.transpose([self.centroidal_points[:,1]]), 1, axis=0) / np.transpose([self.centroidal_points[:,1]]))
            


