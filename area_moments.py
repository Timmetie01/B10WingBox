import numpy as np
import data_import

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

def centroidcoords(panelcoords, panelthickness):
    panelaveragecoords = np.zeros((len(panelcoords), 2))

    #The center coordinates of the panel
    panelaveragecoords[:,0] = (panelcoords[:,0] + panelcoords[:,2]) / 2
    panelaveragecoords[:,1] = (panelcoords[:,1] + panelcoords[:,3]) / 2

    panellength = np.sqrt((panelcoords[:,2] - panelcoords[:,0]) * (panelcoords[:,2] - panelcoords[:,0]) + (panelcoords[:,3] - panelcoords[:,1]) * (panelcoords[:,3] - panelcoords[:,1]))


    return True



