import matplotlib.pyplot as plt
from constants import const
import deflection_functions
import constants
import numpy as np

#Give the wingbox class (and optionally the amount of points you want to plot)
#Plots ixx, iyy and ixy against the half-span
def I_plot(wingbox, npoints=100):
    y_list = []
    Ixx_list = []
    Iyy_list = []
    Ixy_list = []
    J_list = []
    for i in range(npoints):
        y = i * const['span'] / ((npoints-1) * 2)
        y_list.append(y)
        Ixx_list.append(wingbox.Ixx(y))
        Iyy_list.append(wingbox.Iyy(y))
        Ixy_list.append(wingbox.Ixy(y))
        J_list.append(wingbox.J(y))
    plt.plot(y_list, Ixx_list, color='darkblue')
    plt.plot(y_list, Iyy_list, color='firebrick')
    plt.plot(y_list, Ixy_list, color='darkgreen')
    plt.plot(y_list, J_list, color='darkmagenta')

    plt.legend(['Ixx', 'Iyy', 'Ixy', 'J'])
    plt.axis
    plt.xlabel('Span (m)')
    plt.ylabel('I (m^4)')

    plt.grid(axis='y', ls='--')
    plt.show()

#Enter the wingbox class. When show_wing is true, it plots the upper and lower sides of the wing surface using the thickness-to-chord and chord functions
def deflection_plot(wingbox, show_wing=True):
    y_list = np.linspace(0, const['span']/2, 100)
    v_list = []
    if show_wing:
        top_wing_list = []
        bottom_wing_list = []

    for i in y_list:
        current_v = deflection_functions.v(wingbox, i)
        v_list.append(current_v)
        if show_wing:
            wingthickness = const['thickness_to_chord'] * constants.local_chord_at_span(i)
            top_wing_list.append(current_v + 0.5 * wingthickness)
            bottom_wing_list.append(current_v - 0.5 * wingthickness)

    plt.plot(y_list, v_list, color='darkblue')
    if show_wing:
        plt.plot(y_list, top_wing_list, color='black')
        plt.plot(y_list, bottom_wing_list, color='black')
    plt.gca().set_aspect('equal')
    plt.title('Wing Deflection')
    plt.xlabel('Spanwise position (m)')
    plt.ylabel('Deflection (m)')
    plt.show()

#Enter the wingbox class, shows graph of resulting twist at certain span locations
def twist_plot(wingbox):
    y_list = np.linspace(0, const['span']/2, 100)
    theta_list = []
    for i in y_list:
        theta_list.append(deflection_functions.theta(wingbox, i) * 180 / np.pi)

    plt.plot(y_list, theta_list)
    plt.title('Wing twist at different spanwise positions')
    plt.xlabel('Spanwise position (m)')
    plt.ylabel('Twist (deg)')
    plt.show()






