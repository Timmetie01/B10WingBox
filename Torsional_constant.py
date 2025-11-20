import numpy as np
def Area(coords):
    x = coords[:,0]
    y = coords[:,1]
    return 0.5 * np.abs(
        np.dot(x, np.roll(y, 1)) -
        np.dot(y, np.roll(x, 1)))


def contour_int(coords,t):
    d = np.roll(coords, -1, axis=0) - coords
    ds = np.linalg.norm(d, axis=1)
    integral = np.sum(ds / t)
    return integral

def Torsional_constant(coords,t):
    A = Area(coords)
    integral = contour_int(coords,t)
    return 4*A/integral

coords = np.array([[0,0],[1,1],[0,1]])
t = np.array([1,1,1])
print(contour_int(coords, t))

