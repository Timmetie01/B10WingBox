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
def deflection_plot(wingbox, show_wing=True, two_wings=False):
    y_list, v_list = deflection_functions.v(wingbox)

    if show_wing:
        top_wing_list = []
        bottom_wing_list = []
        for i in range(len(y_list)):
            wingthickness = const['thickness_to_chord'] * constants.local_chord_at_span(y_list[i])
            top_wing_list.append(v_list[i] + 0.5 * wingthickness)
            bottom_wing_list.append(v_list[i] - 0.5 * wingthickness)

    

    plt.plot(y_list, v_list, color='darkblue')
    if show_wing:
        plt.plot(y_list, top_wing_list, color='black')
        plt.plot(y_list, bottom_wing_list, color='black')

    if two_wings:
        plt.plot(y_list * -1, v_list, color='darkblue')
        if show_wing:
            plt.plot(y_list * -1, top_wing_list, color='black')
            plt.plot(y_list * -1, bottom_wing_list, color='black')

        plt.plot([const['span']/-2 + 1, const['span']/-2 - 0.3], [const['span'] * const['max_deflection_fraction'], const['span'] * const['max_deflection_fraction']], color='red')
    

    plt.plot([const['span']/2 - 1, const['span']/2 + 0.3], [const['span'] * const['max_deflection_fraction'], const['span'] * const['max_deflection_fraction']], color='red')
    
    plt.gca().set_aspect('equal')
    plt.title('Wing Deflection')
    plt.xlabel('Spanwise position (m)')
    plt.ylabel('Deflection (m)')
    plt.show()

#Enter the wingbox class, shows graph of resulting twist at certain span locations
def twist_plot(wingbox):
    y_list, theta_list = deflection_functions.theta(wingbox)
    theta_list = theta_list * 180 / np.pi

    plt.plot(y_list, theta_list)
    plt.title('Wing twist at different spanwise positions')
    plt.xlabel('Spanwise position (m)')
    plt.ylabel('Twist (deg)')
    plt.show()

#Shows airfoil plot by default, but if required to plot another layer on top of this one, the function can be called using showplot=False
#When using showplot=False, no styling will be done and plt.show won't be called.
def airfoil_pointplot(showplot=True):
    import data_import
    inputcoordinates = data_import.import_airfoil_points()
    plt.plot(inputcoordinates[:, 0], inputcoordinates[:, 1], 'k-')

    if showplot:
        plt.gca().set_aspect('equal')
        xmin, xmax = inputcoordinates[:, 0].min(), inputcoordinates[:, 0].max()
        ymin, ymax = inputcoordinates[:, 1].min(), inputcoordinates[:, 1].max()
        plt.xlim(xmin - 0.1, xmax + 0.1)
        plt.ylim(ymin - 0.1, ymax + 0.1)

        plt.show()


#When using showplot=False, no styling will be done and plt.show won't be called.
def wingbox_plot(wingbox, showplot=True):
    wingbox_points = wingbox.points

    if wingbox_points[0,0] != wingbox_points[-1,0] or wingbox_points[0,1] != wingbox_points[-1,1]:
        wingbox_points = np.vstack((wingbox_points, wingbox_points[0,:]))

    wingbox_xcoords, wingbox_ycoords = wingbox_points[:,0], wingbox_points[:,1]

    plt.plot(wingbox_xcoords, wingbox_ycoords, color='darkblue')
    plt.scatter(wingbox.stringers[:,0], wingbox.stringers[:,1], s=wingbox.stringer_area * 1e6, c='green', marker='o')

    if showplot:
        plt.gca().set_aspect('equal')
        plt.show()

#Plots the worst case moment
def worst_moment_plot():
    from worst_cases import worst_case_loading
    
    ytab = np.linspace(0, const['span']/2, 1000)
    Mtabmax = []
    Mtabmin = []
    for i in ytab:
        Mtabmax.append(worst_case_loading.M(i, 'abs_max_bending'))
        Mtabmin.append(worst_case_loading.M(i, 'abs_min_bending'))

    plt.plot(ytab, Mtabmax)
    plt.plot(ytab, Mtabmin)
    plt.title('Bending moment over the wing span')
    plt.xlabel('y (m)')
    plt.ylabel('Bending moment (Nm)')

    plt.show()

#Plots the worst case Torsion
def worst_torsion_plot():
    from worst_cases import worst_case_loading
    
    ytab = np.linspace(0, const['span']/2, 1000)
    thetatabmax = []
    thetatabmin = []
    for i in ytab:
        thetatabmax.append(worst_case_loading.T(i, 'abs_max_torsion'))
        thetatabmin.append(worst_case_loading.T(i, 'abs_min_torsion'))

    plt.plot(ytab, thetatabmax)
    plt.plot(ytab, thetatabmin)
    plt.title('Torsion over the wing span')
    plt.xlabel('y (m)')
    plt.ylabel('Torsion (Nm)')

    plt.show()

#Plots the currently designed wingbox under worst possible conditions (worst bending and worst torsion.)
def wing_plot(wingbox, Npoints=20):
    import deflection_functions
    import data_import
    y_list, v_list = deflection_functions.v(wingbox, N=Npoints)
    y_list, theta_list = deflection_functions.theta(wingbox, N=Npoints)
    Y = np.transpose(np.array([y_list] * len(y_list)))
    X = np.ones_like(Y, dtype=float)
    Ztop = np.ones_like(Y, dtype=float)
    Zbottom = np.ones_like(Y, dtype=float) 
    for i in range(len(y_list)):
        chord = constants.local_chord_at_span(Y[i,0])
        X[i] = np.linspace( Y[i,0] * np.tan(const['leading_edge_sweep']), Y[i,0] * np.tan(const['leading_edge_sweep']) + chord, Npoints)

        #Airfoil + deflection + twist (Assuming twist angle small)
        Ztop[i] = data_import.airfoil_interpolation(np.linspace(0, 1, Npoints), side='top') * chord + v_list[i]
        Ztop[i] += np.linspace(-1 * chord /4 * np.sin(theta_list[i]), 3 * chord / 4 * np.sin(theta_list[i]), Npoints)
        
        #Airfoil + deflection + twist (Assuming twist angle small)
        Zbottom[i] = data_import.airfoil_interpolation(np.linspace(0, 1, Npoints), side='bottom') * chord + v_list[i]
        Zbottom[i] += np.linspace(-1 * chord /4 * np.sin(theta_list[i]), 3 * chord / 4 * np.sin(theta_list[i]), Npoints)
        
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    surface1 = ax.plot_surface(X, Y, Ztop, antialiased=False)
    surface2 = ax.plot_surface(X, Y, Zbottom, antialiased=False)
    plt.xlabel('x (m)')
    plt.ylabel('Span (m)')
    plt.gca().set_aspect('equal')
    
    plt.show()



