import numpy as np
import classes


#State a wingbox folder (string), it returns a lisnp array (n x 2) t of coordinates. File format:
#Header row
#x1  y1
#x2  y2 etc etc
def import_wingbox_points(foldername):
    with open(foldername + '/wingbox_coords.txt') as airfoilpoints:
        lines = np.array(airfoilpoints.readlines())

    pointlist = np.zeros((len(lines) - 1,2))

    for i in range(len(lines) - 1):
        
        point = str(lines[i + 1]).strip()
        coordinates = np.array(point.split(), dtype=np.float64)
        pointlist[i] = coordinates

    return pointlist

def import_wingbox_thickness(foldername):
    with open(foldername + '/wingbox_thickness.txt') as airfoilpoints:
        lines = np.array(airfoilpoints.readlines())

    thickness_list = np.zeros((len(lines) - 1,1))

    for i in range(len(lines) - 1):
        
        thickness = str(lines[i + 1]).strip()
        thickness_list[i] = np.float64(thickness)

    return thickness_list


def import_stringers(foldername):
    with open(foldername + '/stringer_properties.txt') as airfoilpoints:
        lines = np.array(airfoilpoints.readlines())

    coordinate_list = np.zeros((len(lines) - 1,2))
    area_list = np.zeros((len(lines) - 1, 1))
    

    for i in range(len(lines) - 1):

        linestring = str(lines[i + 1]).strip()
        linearray = np.array(linestring.split(), dtype=np.float64)
        coordinate_list[i,0], coordinate_list[i,1]  = linearray[0], linearray[1]
        area_list[i] = linearray[2]

    return coordinate_list, area_list


#Give a list of points (nx2 numpy array of coords). Closes the cross-section if necessary. return nx4 array of panel coordinates in x1 y1 x2 y2 format
def makepanels(inputcoordinates):

    #If the pointlist ends with something else, close the section
    if inputcoordinates[0,0] != inputcoordinates[-1,0] or inputcoordinates[0,1] != inputcoordinates[-1,1]:
        inputcoordinates = np.vstack((inputcoordinates, inputcoordinates[0,:]))

    #initiate matrix that will contain the panels

    panelarray = np.zeros((len(inputcoordinates) - 1, 4))
    for i in range(len(inputcoordinates) - 1):
            panelarray[i,0:2] = inputcoordinates[i,:]
            panelarray[i,2:4] = inputcoordinates[i+1,:]

    return panelarray




testwingbox = classes.Wingbox(makepanels(import_wingbox_points('data/test_cross_section')), import_wingbox_thickness('data/test_cross_section'), import_stringers('data/test_cross_section')[0], import_stringers('data/test_cross_section')[1])

print(testwingbox.panels)
print(testwingbox.panel_thickness)
print(testwingbox.stringers)
print(testwingbox.stringerarea)