import matplotlib.pyplot as plt
from constants import const

#Give the wingbox class (and optionally the amount of points you want to plot)
#Plots ixx, iyy and ixy against the half-span
def I_plot(wingbox, npoints=100):
    y_list = []
    Ixx_list = []
    Iyy_list = []
    Ixy_list = []
    for i in range(npoints):
        y = i * const['span'] / ((npoints-1) * 2)
        y_list.append(y)
        Ixx_list.append(wingbox.Ixx(y))
        Iyy_list.append(wingbox.Iyy(y))
        Ixy_list.append(wingbox.Ixy(y))
    plt.plot(y_list, Ixx_list, color='darkblue')
    plt.plot(y_list, Iyy_list, color='firebrick')
    plt.plot(y_list, Ixy_list, color='darkgreen')
    
    plt.legend(['Ixx', 'Iyy', 'Ixy'])
    plt.axis
    plt.xlabel('Span (m)')
    plt.ylabel('I (m^4)')

    plt.grid(axis='y', ls='--')
    plt.show()