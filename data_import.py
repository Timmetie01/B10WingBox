import numpy as np


#State a file name (string), it returns a lisnp array (n x 2) t of coordinates. File format:
#Header row
#x1  y1
#x2  y2 etc etc
def importpoints(filename):
    with open(filename) as airfoilpoints:
        lines = np.array(airfoilpoints.readlines())
    
    print('test')
    pointlist = np.zeros((len(lines) - 1,2))

    for i in range(len(lines) - 1):
        
        point = str(lines[i + 1]).strip()
        coordinates = np.array(point.split(), dtype=np.float64)
        pointlist[i] = coordinates

    return pointlist


#Give a list of points (nx2 numpy array of coords). Close the section if necessary. return nx4 array of panel coordinates in x1 y1 x2 y2 format
def makepanels(inputcoordinates):

    #If the pointlist ends with something else, close the section
    if inputcoordinates[0,:] != inputcoordinates[-1,:]:
        inputcoordinates = np.append(inputcoordinates, inputcoordinates[0,:])

    #initiate matrix that will contain the panels
    panelarray = np.zeros((len(inputcoordinates - 1), 4))
    for i in len(inputcoordinates - 1):
            panelarray[i,0:2] = inputcoordinates[i,:]
            panelarray[i,2:4] = inputcoordinates[i+1,:]

    return panelarray



