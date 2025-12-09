import numpy as np
from classes import Wingbox
import scipy as sp

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

#Give a list of points (nx2 numpy array of coords). Closes the cross-section if necessary. return nx4 array of panel coordinates in x_start y_start x_end y_end format. 
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

#When a folder with fully correct syntax provides wingbox data, just input the folder name (as a string) into this function and it will return a completely defined wingbox class! 
#Only really useful in testing of functions.
def import_wingbox(foldername):
    wingboxclass = Wingbox(import_wingbox_points('data/' + foldername), import_wingbox_thickness('data/' + foldername), import_stringers('data/' + foldername)[0], import_stringers('data/' + foldername)[1])
    return wingboxclass
testwingbox = import_wingbox('test_cross_section')

#Returns the coordinates of the airfoil we used for the wing. Call once and save array instead of calling multiple times to improve performance!
def import_airfoil_points():
    with open('data/Airfoils/Project_Airfoil_Coords.txt') as airfoilpoints:
        lines = np.array(airfoilpoints.readlines())
    
    pointlist = np.zeros((len(lines) - 1,2))

    for i in range(len(lines) - 1):
        point = str(lines[i + 1]).strip()
        coordinates = np.array(point.split(), dtype=np.float64)
        pointlist[i] = coordinates

    return pointlist

#Choose either the 'top' or 'bottom' side, and give x value (or array of values) to find interpolated y value (or array of values) of the unit airfoil
def airfoil_interpolation(x, side='top'):
    airfoil_points = import_airfoil_points()
    if side != 'top' and side != 'bottom':
        print('Airfoil side must be either \'top\' or \'bottom\'.')
        quit()
    
    if side == 'top':
        airfoil_points = airfoil_points[:(len(airfoil_points) // 2)+1,:]
        airfoil_points = np.flip(airfoil_points, 0)
    else:
        airfoil_points = airfoil_points[(len(airfoil_points) // 2):,:]

    return np.interp(np.asarray(x), airfoil_points[:,0], airfoil_points[:,1], period=None)


#The following function makes a wingbox that follows the contours of the airfoil between two x values
#xstart and xend are the front and rear spar x/c location
#Thickness: constant number when thicknesstype = 'constant', [top, right, bottom, left] array when  thicknesstype = 'partially_constant', or full array in order of panels when thicknesstype = 'full_array'
#stringercount: amount of stringers
#stringerspacing:'constant_endpoints' gives constant spacing including corners of wingbox, 'constant_no_endpoints' gives constant spacing excluding the corners of the wingbox
#stringerareas: float for constant and array for variable areas
#Panelcount: the amount of panels the wingbox will consist of, defaults to 50
def create_airfoil_like_wingbox(xstart, xend, thickness, thicknesstype, stringercount, stringer_areas, stringerspacing='constant_endpoints', panelcount=50, scaled_thickness=False, name=None):
    import classes
    import numbers
    panelcount = (panelcount//2) * 2
    stringercount = (stringercount//2) * 2

    wingbox_points = np.zeros((panelcount, 2))
    wingbox_xcoords = np.linspace(xstart, xend, panelcount//2)

    wingbox_points[:panelcount//2, 0], wingbox_points[:panelcount//2, 1] = wingbox_xcoords, airfoil_interpolation(wingbox_xcoords, 'top')
    wingbox_points[panelcount//2:, 0], wingbox_points[panelcount//2:, 1] = np.flip(wingbox_xcoords), airfoil_interpolation(np.flip(wingbox_xcoords), 'bottom')


    #Different types of stringer placements
    #stringerspacing:'constant_endpoints' gives constant spacing including corners of wingbox
    #'constant_no_endpoints' gives constant spacing excluding the corners of the wingbox
    if stringerspacing == 'constant_endpoints':
        stringer_points = np.zeros((stringercount, 2))
        stringer_xcoords = np.linspace(xstart, xend, stringercount//2)

        stringer_points[:stringercount//2, 0], stringer_points[:stringercount//2, 1] = stringer_xcoords, airfoil_interpolation(stringer_xcoords, 'top')
        stringer_points[stringercount//2:, 0], stringer_points[stringercount//2:, 1] = np.flip(stringer_xcoords), airfoil_interpolation(np.flip(stringer_xcoords), 'bottom')
    elif stringerspacing == 'constant_no_endpoints':
        stringer_points = np.zeros((stringercount, 2))
        stringer_xcoords = np.linspace(xstart, xend, stringercount//2 + 1, endpoint=False)[1:]

        stringer_points[:stringercount//2, 0], stringer_points[:stringercount//2, 1] = stringer_xcoords, airfoil_interpolation(stringer_xcoords, 'top')
        stringer_points[stringercount//2:, 0], stringer_points[stringercount//2:, 1] = np.flip(stringer_xcoords), airfoil_interpolation(np.flip(stringer_xcoords), 'bottom')
    else:
        print('Choose available method of stringer spacing please!! (from data_import.create_airfoil_like_wingbox)')
        quit()

    #Either make array when input is a number or keep array when array is given and check if it has the right length
    if isinstance(stringer_areas, numbers.Number):
        stringer_areas = np.transpose(np.array([[stringer_areas] * stringercount]))
    elif len(stringer_areas) != stringercount:
        print('Stringer thickness should either be a single number, or an array with the length of the amount of stringers.')
        quit() 

    #The different ways of entering thickness:
    #Thickness: constant number when thicknesstype = 'constant', 
    #[top, right, bottom, left] array when  thicknesstype = 'partially_constant'
    #Or full array in order of panel when thicknesstype = 'full_array'
    if thicknesstype == 'constant':
        thickness = np.transpose(np.array([[thickness] * panelcount]))
    elif thicknesstype == 'partially_constant':
        if len(thickness) != 4:
            print('When using partially constant panel thicknesses, an array of length 4 must be provided!')
            quit()
        thickness_top = np.ones((panelcount//2-1,1)) * thickness[0]
        thickness_right = np.ones((1,1)) * thickness[1]
        thickness_bottom = np.ones((panelcount//2-1,1)) * thickness[2]
        thickness_left = np.ones((1,1)) * thickness[3]
        thickness = np.vstack((thickness_top, thickness_right, thickness_bottom, thickness_left))    
    elif thicknesstype == 'full_array':
        thickness = np.transpose([thickness])
        if len(thickness) != panelcount:
            print('Make sure to give the thickness array with equal length as the amount of panels')
            quit()
    else:
        print('Choose any of the available ways of entering thickness! (or define your own :D )')
        quit()

    return classes.Wingbox(wingbox_points, thickness, stringer_points, stringer_areas, scaled_thickness=scaled_thickness, name=name)


def idealizable_wingboxl(xstart, xend, thickness, thicknesstype, stringercount, stringer_areas, stringerspacing='constant_no_endpoints', panels_per_stringer=5, web_panel_count=20, scaled_thickness=False, name=None):
    """
    Creates an airfoil which can be idealized by using the panel boom method
    
    :param xstart: The x/c location of the front spar
    :param xend: The x/c location of the rear spar
    :param thickness: Either constant thickness or [top, right, bottom left] array 
    :param thicknesstype: \'constant\' when inputting constant thickness,  \'partially_constant\' when inputting [top, right, bottom left]
    :param stringercount: The amount of stringers.  Will be rounded down to multiple of 2
    :param stringer_areas: Either a single number or an array with thicknesses of each stringer
    :param stringerspacing: \'constant_endpoints\':constant spacing including corners of wingbox (CURRENTLY NOT IMPLEMENTED), \'constant_no_endpoints\' gives constant spacing excluding the corners of the wingbox
    :param panels_per_stringer: Amount of panels generated per stringer, recommended to keep below 10
    :param web_panel_count: Amount of panels generated throughout the web
    :param scaled_thickness: If True, thickness will be multiplied by chord length. If false, it will be constant along span
    :param name: The name of the wingbox, can be used to title plots
    :return wingbox: A wingbos-class that can use idealization!
    """

    import classes
    import numbers
    #Amount of panels in each spar, to accurately model shear
    web_panel_count -= 1
    stringercount = (stringercount//2) * 2
    #Amount of panels between spars at the top or bottom
    if stringerspacing == 'constant_endpoints':
        flange_panel_count = (stringercount//2 - 1) * panels_per_stringer + 1
    elif stringerspacing == 'constant_no_endpoints':
        flange_panel_count = (stringercount//2 + 1) * panels_per_stringer + 1
    else:
        print('Choose available method of stringer spacing please!! (from data_import.create_airfoil_like_wingbox)')
        quit()
    
    

    wingbox_points = np.zeros((2 * web_panel_count + 2 * flange_panel_count, 2))
    wingbox_xcoords = np.linspace(xstart, xend, flange_panel_count)

    wingbox_points[0:flange_panel_count, 0], wingbox_points[:flange_panel_count, 1] = wingbox_xcoords, airfoil_interpolation(wingbox_xcoords, 'top')
    wingbox_points[flange_panel_count:flange_panel_count + web_panel_count, 0], wingbox_points[flange_panel_count:flange_panel_count + web_panel_count, 1] = xend, np.linspace(airfoil_interpolation(xend, 'top'), airfoil_interpolation(xend, 'bottom'), web_panel_count + 2)[1:-1]
    wingbox_points[flange_panel_count + web_panel_count:2 * flange_panel_count + web_panel_count, 0], wingbox_points[flange_panel_count + web_panel_count:2 * flange_panel_count + web_panel_count, 1] = np.flip(wingbox_xcoords), airfoil_interpolation(np.flip(wingbox_xcoords), 'bottom')
    wingbox_points[2 * flange_panel_count + web_panel_count:, 0], wingbox_points[2 * flange_panel_count + web_panel_count:, 1] = xstart, np.linspace(airfoil_interpolation(xstart, 'bottom'), airfoil_interpolation(xstart, 'top'), web_panel_count + 2)[1:-1]

    #Different types of stringer placements
    #stringerspacing:'constant_endpoints' gives constant spacing including corners of wingbox
    #'constant_no_endpoints' gives constant spacing excluding the corners of the wingbox
    #if stringerspacing == 'constant_endpoints':
    #    stringer_points = np.zeros((stringercount, 2))
    #    stringer_xcoords = np.linspace(xstart, xend, stringercount//2)

    #    stringer_points[:stringercount//2, 0], stringer_points[:stringercount//2, 1] = stringer_xcoords, airfoil_interpolation(stringer_xcoords, 'top')
    #    stringer_points[stringercount//2:, 0], stringer_points[stringercount//2:, 1] = np.flip(stringer_xcoords), airfoil_interpolation(np.flip(stringer_xcoords), 'bottom')
    if stringerspacing == 'constant_no_endpoints':
        stringer_points = np.zeros((stringercount, 2))
        stringer_xcoords = np.linspace(xstart, xend, stringercount//2 + 1, endpoint=False)[1:]

        stringer_points[:stringercount//2, 0], stringer_points[:stringercount//2, 1] = stringer_xcoords, airfoil_interpolation(stringer_xcoords, 'top')
        stringer_points[stringercount//2:, 0], stringer_points[stringercount//2:, 1] = np.flip(stringer_xcoords), airfoil_interpolation(np.flip(stringer_xcoords), 'bottom')
    else:
        print('Currently only \'constant no endpoints\' is the supported stringer spacing!')
        quit()
       

    #For easy idealization, all stringer points should also be points in the wingbox skin. If not, throw an error.
    for i in range(len(stringer_points)):
        if np.round(stringer_points[i,:], 7) not in np.round(wingbox_points, 7):
            print('Something went wrong in creating an idealizable airfoil.')
            print(stringer_points[i,:])
            quit()

    #Either make array when input is a number or keep array when array is given and check if it has the right length
    if isinstance(stringer_areas, numbers.Number):
        stringer_areas = np.transpose(np.array([[stringer_areas] * stringercount]))
    elif len(stringer_areas) != stringercount:
        print('Stringer thickness should either be a single number, or an array with the length of the amount of stringers.')
        quit() 

    #The different ways of entering thickness:
    #Thickness: constant number when thicknesstype = 'constant', 
    #[top, right, bottom, left] array when  thicknesstype = 'partially_constant'
    if thicknesstype == 'constant':
        thickness = np.transpose(np.array([[thickness] * len(wingbox_points)]))
    elif thicknesstype == 'partially_constant':
        if len(thickness) != 4:
            print('When using partially constant panel thicknesses, an array of length 4 must be provided!')
            quit()
        thickness_top = np.ones((len(wingbox_xcoords) - 1,1)) * thickness[0]
        thickness_right = np.ones((web_panel_count + 1,1)) * thickness[1]
        thickness_bottom = np.ones((len(wingbox_xcoords) - 1,1)) * thickness[2]
        thickness_left = np.ones((web_panel_count + 1,1)) * thickness[3]
        thickness = np.vstack((thickness_top, thickness_right, thickness_bottom, thickness_left))    
    else:
        print('Choose any of the available ways of entering thickness! (or define your own :D )')
        quit()

    return classes.Wingbox(wingbox_points, thickness, stringer_points, stringer_areas, scaled_thickness=scaled_thickness, idealizable=True, name=name)



testwingbox = idealizable_wingboxl(0.2, 0.6, 0.001, 'constant', stringercount=20, stringer_areas=2e-5, stringerspacing='constant_no_endpoints', panels_per_stringer=10, web_panel_count=20)

print(testwingbox.shear_stress(1))