import numpy as np
from classes import Wingbox



#State a wingbox folder (string), it returns a np array (n x 2) t of coordinates. File format for input:
#Header row
#x1  y1
#x2  y2 etc etc
def import_wingbox_points(foldername):
    with open(foldername + '/wingbox_coords.txt') as wingboxpoints:
        lines = np.array(wingboxpoints.readlines())

    pointlist = np.zeros((len(lines) - 1,2))

    for i in range(len(lines) - 1):
        
        point = str(lines[i + 1]).strip()
        coordinates = np.array(point.split(), dtype=np.float64)
        pointlist[i] = coordinates

    return pointlist

#State a wingbox folder (string), it returns a np array (n x 1) t of thickness of panels. File format for input:
#Header row
#thickness1
#thickness2 etc etc
def import_wingbox_thickness(foldername):
    with open(foldername + '/wingbox_thickness.txt') as airfoilpoints:
        lines = np.array(airfoilpoints.readlines())

    thickness_list = np.zeros((len(lines) - 1,1))

    for i in range(len(lines) - 1):
        
        thickness = str(lines[i + 1]).strip()
        thickness_list[i] = np.float64(thickness)

    return thickness_list

#State a wingbox folder (string).
#This returns both a nx2 array of coordinates of stringers, and a nx1 array of the areas of those stringers, as specified in the txt file
#Input file format:
#header row
#x1 y1 area1
#x2 y2 thickness2       etc etc
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


def import_wingbox(foldername):
    wingboxclass = Wingbox(import_wingbox_points('data/' + foldername), import_wingbox_thickness('data/' + foldername), import_stringers('data/' + foldername)[0], import_stringers('data/' + foldername)[1])
    return wingboxclass
testwingbox = import_wingbox('test_cross_section')

#testwingbox = Wingbox(import_wingbox_points('data/test_cross_section'), import_wingbox_thickness('data/test_cross_section'), import_stringers('data/test_cross_section')[0], import_stringers('data/test_cross_section')[1])
    

print(testwingbox.points)
print(testwingbox.panels)
print(testwingbox.panel_thickness)
print(testwingbox.stringers)
print(testwingbox.stringerarea)