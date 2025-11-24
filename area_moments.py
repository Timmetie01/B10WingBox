import numpy as np
import data_import
import constants
from constants import const
import classes

#Outputs the area of a polygon when input is a numpy nx2 array (coordinates of the wingbox)
def Area(coords):
    x = coords[:,0]
    y = coords[:,1]
    return 0.5 * np.abs(
        np.dot(x, np.roll(y, 1)) -
        np.dot(y, np.roll(x, 1)))

#Outputs the contour integral needed for the torsional constant: int(ds/t) when inputs are 1) a numpy nx2 array for the coordinates (of the winbox)
#2) the thicknesses of each panel in a nx1 array
def contour_int(coords,t):
    d = np.roll(coords, -1, axis=0) - coords
    ds = np.linalg.norm(d, axis=1)
    integral = np.sum(ds / t)
    return integral


#Outputs the torsional constant of a shape (the wingbox) when inputs are 1) a numpy nx2 array for the coordinates (of the winbox)
#2) the thicknesses of each panel in a nx1 array
def Torsional_constant(coords,t):
    A = Area(coords)
    integral = contour_int(coords,t)
    return 4*A**2/integral

#Returns the centroid coordinates, is called inside the Wingbox class
def centroidcoords(panelcoords, panelthickness, stringercoords, stringer_area):
    panelaveragecoords = np.zeros((len(panelcoords), 2))

    #The center coordinates of the panel
    panelaveragecoords[:,0] = (panelcoords[:,0] + panelcoords[:,2]) / 2
    panelaveragecoords[:,1] = (panelcoords[:,1] + panelcoords[:,3]) / 2

    panellength = np.sqrt((panelcoords[:,2] - panelcoords[:,0]) * (panelcoords[:,2] - panelcoords[:,0]) + (panelcoords[:,3] - panelcoords[:,1]) * (panelcoords[:,3] - panelcoords[:,1]))
    panellength = np.transpose(np.array([panellength]))

    totalarea = np.sum(panellength * panelthickness) + np.sum(stringer_area)

    wingboxcontribution = np.array([np.sum(np.transpose(np.array([panelaveragecoords[:,0]])) * panellength * panelthickness), np.sum(np.transpose(np.array([panelaveragecoords[:,1]])) * panellength * panelthickness)])
    
    stringercontribution = np.array([np.sum(np.transpose(np.array([panelaveragecoords[:,0]])) * stringer_area),  np.sum(np.transpose(np.array([panelaveragecoords[:,1]])) * stringer_area)])
    
    return (stringercontribution + wingboxcontribution) / totalarea

#Used in calculating Ixx, Iyy and Ixy in the wingbox class. Also equires the spanwise position of the section, and automatically scales the wingbox to the chord length at that position.
def second_area_moment(y, wingbox):
    chord = constants.local_chord_at_span(y)
    local_wingbox = classes.ScaledWingbox(wingbox, chord)
    panelcoords = local_wingbox.centroidal_panels

    #The center coordinates of the panel
    panelaveragecoords = np.zeros((len(panelcoords), 2)) 
    panelaveragecoords[:,0] = np.transpose((panelcoords[:,0] + panelcoords[:,2]) / 2)
    panelaveragecoords[:,1] = np.transpose((panelcoords[:,1] + panelcoords[:,3]) / 2)

    panellength = np.sqrt((panelcoords[:,2] - panelcoords[:,0]) ** 2 + (panelcoords[:,3] - panelcoords[:,1]) ** 2 )
    panellength = np.transpose(np.array([panellength]))

    panelangle = np.transpose([np.arctan2(panelcoords[:,3] - panelcoords[:,1], panelcoords[:,2] - panelcoords[:,0])])

    Ixx = np.sum(local_wingbox.stringer_area * np.transpose([local_wingbox.centroidal_stringers[:,1]]) ** 2) + np.sum(local_wingbox.panel_thickness * panellength ** 3 * np.sin(panelangle) ** 2) / 12 + np.sum(local_wingbox.panel_thickness * panellength * np.transpose([panelaveragecoords[:,1]]) ** 2)
    Iyy = np.sum(local_wingbox.stringer_area * np.transpose([local_wingbox.centroidal_stringers[:,0]]) ** 2) + np.sum(local_wingbox.panel_thickness * panellength ** 3 * np.cos(panelangle) ** 2) / 12 + np.sum(local_wingbox.panel_thickness * panellength * np.transpose([panelaveragecoords[:,0]]) ** 2)
    Ixy = np.sum(local_wingbox.stringer_area * np.transpose([local_wingbox.centroidal_stringers[:,0]]) * local_wingbox.centroidal_stringers[:,1]) + np.sum(local_wingbox.panel_thickness * panellength ** 3 * np.sin(panelangle) * np.cos(panelangle)) / 12 + np.sum(local_wingbox.panel_thickness * panellength * np.transpose([panelaveragecoords[:,1]]) * np.transpose([panelaveragecoords[:,0]]))
    
    return Ixx, Iyy, Ixy

    

