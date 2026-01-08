import matplotlib.pyplot as plt
from constants import const
import deflection_functions
import constants
import numpy as np

#Give the wingbox class (and optionally the amount of points you want to plot)
#Plots ixx, iyzz and ixz against the half-span
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

    plt.legend(['Ixx', 'Izz', 'Ixz', 'J'])
    plt.axis
    plt.xlabel('Span (m)')
    plt.ylabel('I (m^4)')

    plt.grid(axis='y', ls='--')
    plt.grid(axis='x', ls='--')
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

    plt.plot([const['span']/2 - 1, const['span']/2 + 0.3], [const['span'] * const['max_deflection_fraction'], const['span'] * const['max_deflection_fraction']], color='red')
    

    plt.plot(y_list, v_list, color='darkblue')
    plt.legend('Wing Centerline')
    if show_wing:
        plt.plot(y_list, top_wing_list, color='black')
        plt.plot(y_list, bottom_wing_list, color='black')
        plt.legend(('Allowed Deflection Limit (Centerline)', 'Wing Centerline', 'Wing surface'))
        

    if two_wings:
        plt.plot(y_list * -1, v_list, color='darkblue')
        if show_wing:
            plt.plot(y_list * -1, top_wing_list, color='black')
            plt.plot(y_list * -1, bottom_wing_list, color='black')

        plt.plot([const['span']/-2 + 1, const['span']/-2 - 0.3], [const['span'] * const['max_deflection_fraction'], const['span'] * const['max_deflection_fraction']], color='red')
    

    plt.gca().set_aspect('equal')
    plt.title('Wing Deflection')
    plt.xlabel('Spanwise position (m)')
    plt.ylabel('Deflection (m)')
    plt.grid(axis='y', ls='--')
    plt.grid(axis='x', ls='--')
    plt.show()

#Enter the wingbox class, shows graph of resulting twist at certain span locations
def twist_plot(wingbox):
    y_list, theta_list = deflection_functions.theta(wingbox)
    theta_list = theta_list * 180 / np.pi

    plt.plot(y_list, theta_list)
    plt.title('Wing twist at different spanwise positions')
    plt.xlabel('Spanwise position (m)')
    plt.ylabel('Twist (deg)')
    plt.grid(axis='y', ls='--')
    plt.grid(axis='x', ls='--')
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
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')

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
        plt.xlabel('x / chord')
        plt.ylabel('y / chord')
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')
        #plt.title(wingbox.name)
        if len(wingbox.stringers) > 0:
            plt.legend(('Airfoil', 'Wingbox Skin', 'Stringers'))
        else: 
            plt.legend(('Airfoil', 'Wingbox Skin'))
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
    plt.grid(axis='y', ls='--')
    plt.grid(axis='x', ls='--')

    plt.show()

#Plots the worst case Torsion
def worst_torsion_plot():
    from worst_cases import worst_case_loading
    
    ytab = np.linspace(0, const['span']/2, 1000)
    Ttabmax = []
    Ttabmin = []
    for i in ytab:
        Ttabmax.append(worst_case_loading.T(i, 'abs_max_torsion'))
        Ttabmin.append(worst_case_loading.T(i, 'abs_min_torsion'))

    plt.plot(ytab, Ttabmax)
    plt.plot(ytab, Ttabmin)
    plt.title('Torsion over the wing span')
    plt.xlabel('y (m)')
    plt.ylabel('Torsion (Nm)')
    plt.grid(axis='y', ls='--')
    plt.grid(axis='x', ls='--')
    plt.show()

def worst_shear_plot():
    from worst_cases import worst_case_loading
    
    ytab = np.linspace(0, const['span']/2, 1000)
    Vtabmax = []
    Vtabmin = []
    for i in ytab:
        Vtabmax.append(worst_case_loading.V(i, 'abs_max_shear'))
        Vtabmin.append(worst_case_loading.V(i, 'abs_min_shear'))

    plt.plot(ytab, Vtabmax)
    plt.plot(ytab, Vtabmin)
    plt.title('Shear over the wing span')
    plt.xlabel('y (m)')
    plt.ylabel('Shear (N)')
    plt.grid(axis='y', ls='--')
    plt.grid(axis='x', ls='--')

    plt.show()

#Plots the entered designed wingbox under current worst possible conditions (worst bending and worst torsion.)
def wing_plot(wingbox, Npoints=50, twowings=False):
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

        #Airfoil + deflection + twist (Assuming twist angle small, only vertically using twist displacement (cos(theta)=1))
        Ztop[i] = data_import.airfoil_interpolation(np.linspace(0, 1, Npoints), side='top') * chord + v_list[i]
        Ztop[i] += np.linspace(1 * chord /4 * np.sin(theta_list[i]), -3 * chord / 4 * np.sin(theta_list[i]), Npoints)
        
        #Airfoil + deflection + twist (Assuming twist angle small, only vertically using twist displacement (cos(theta)=1))
        Zbottom[i] = data_import.airfoil_interpolation(np.linspace(0, 1, Npoints), side='bottom') * chord + v_list[i]
        Zbottom[i] += np.linspace(1 * chord /4 * np.sin(theta_list[i]), -3 * chord / 4 * np.sin(theta_list[i]), Npoints)
         
    #X, Y, Ztop, Zbottom = np.transpose(X), np.transpose(Y), np.transpose(Ztop), np.transpose(Zbottom),

    X = np.vstack((np.flip(X), X))
    Y = np.vstack((np.flip(Y), Y))
    Z = np.vstack((np.flip(Ztop), Zbottom))
    fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
    ax.plot_surface(X, Y, Z, antialiased=True, color='grey')
    if twowings:
        ax.plot_surface(X, -1*Y, Z, antialiased=True, color='grey')
    ax.set_proj_type('persp')
    plt.xlabel('x (m)')
    plt.ylabel('Span (m)')
    plt.gca().set_aspect('equal')
    plt.title('3D Surface of the wing under maximum deflection and maximum twist')
    
    
    plt.show()

#Plots the highest normal stress due to bending found in each cross section over y
def bending_stress_plot(wingbox, Npoints = 250, showplot=True):
    import stress_functions
    y_tab = np.linspace(0, const['span']/2, Npoints)
    stress_tab = []
    for i in y_tab:
        stress_tab.append(stress_functions.max_bending_stress(wingbox, i))

    plt.plot(y_tab, stress_tab)
    if showplot:
        plt.xlabel('Spanwise position (m)')
        plt.ylabel('Highest cross-sectional stress')
        plt.title('Highest normal stresses at cross sections.')
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')
        plt.show()

#Plots the shear flow along the wingbox at a certain span-wise position
def shear_flow_plot(wingbox, y=0):
    X = wingbox.panels[:,0]/2 + wingbox.panels[:,2]/2
    Y = wingbox.panels[:,1]/2 + wingbox.panels[:,3]/2
    U_V = (wingbox.panels[:,2:] - wingbox.panels[:,:2]) @ np.array([[0,1],[-1,0]]) / wingbox.panel_length
    U_V = U_V * np.abs(wingbox.shear_flow(y))
    wingbox_plot(wingbox, showplot=False)
    plt.xlim((min(wingbox.points[:,0] - 0.1), max(wingbox.points[:,0] + 0.1)))
    plt.ylim((min(wingbox.points[:,1] - 0.2), max(wingbox.points[:,1] + 0.2)))
    plt.quiver( X,     # x
                Y,     # y
                U_V[:, 0],     # u
                U_V[:, 1],     # v 
                width=0.002)
    
    plt.xlabel('Span')

    plt.show()

#Plots the highest shear flow found at each point in the cross seactino
def shear_flow_spanwise_plot(wingbox, showplot=True, Npoints=500):
    
    y_tab = np.linspace(0, const['span']/2, Npoints, endpoint=False)
    MOS_tab = []
    
    for i in y_tab:
        MOS_tab.append(max(wingbox.shear_flow(i)))
        print(f'Plotting shear flow distribution... {round(i * 100 / max(y_tab),1)}%', end='\r', flush=True)
    print('Plotting shear flow distribution... 100%!  ', end='\n', flush=True)
        

    plt.plot(y_tab, MOS_tab)

    if showplot:
        plt.xlabel('Spanwise position (m)')
        plt.ylabel('Shear Flow (N/m)')
        plt.title('Highest shear flow at certain cross-sections')
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')
        plt.show()

#Plots the Margin of Safety of shear along the span
def spar_shear_MOS_plot(wingbox, Npoints=100, showplot=True):
    """
    Plots the Margins Of Safety in the spar due to shear
    
    :param wingbox: The wingbox input
    :param Npoints: The amount of points taken into account along the span
    :param showplot: Either shows the plot when True, or does not show the plot and returns its entries for the legend
    """


    import stress_functions
    y_tab = np.linspace(0, const['span']/2, Npoints, endpoint=False)
    MOS_buckle_tab = []
    MOS_maxshear_tab = []
    for i in y_tab:
        MOS_buckle_tab.append(min(stress_functions.spar_buckling_MOS(wingbox, i, return_info=True)[0][:2]))
        MOS_maxshear_tab.append(min(stress_functions.spar_buckling_MOS(wingbox, i, return_info=True)[0][2:]))
        print(f'Plotting shear flow distribution... {round(i * 100 / max(y_tab),1)}%', end='\r', flush=True)
    print('Plotting shear flow distribution... 100%!  ', end='\n', flush=True)
    

    if showplot:
        plt.plot(y_tab, MOS_buckle_tab, color='darkblue', label='Spar Shear Buckling')
        plt.plot(y_tab, MOS_maxshear_tab, color='darkgreen', label='Spar Max Shear Stress')
        plt.plot([0, const['span']/2], [1,1], color='black', label='Lower Limit')
        plt.legend(fontsize=15)
        plt.xlabel('Spanwise position (m)', fontsize=20)
        plt.ylabel('Margin of Safety [-]', fontsize=20)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        plt.ylim((-2, 20))
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')
        plt.show()
    else:
        plt.plot(y_tab, MOS_buckle_tab, label='Spar Shear Buckling')
        plt.plot(y_tab, MOS_maxshear_tab, label='Spar Max Shear Stress')

#Plots the Margin of Safety of deflection and twist alongthe span
def deflection_twist_MOS_plot(wingbox, Npoints=1000, showplot=True):
    y_list, v_list = deflection_functions.v(wingbox)
    y_list, theta_list = deflection_functions.theta(wingbox)
    #Add tiny increment to v list to avoid dividing by zero. Only for graphing purposes, so inaccuracy barely matters
    MOS_v_list, MOS_theta_list = const['max_deflection_fraction'] * const['span'] / (v_list + 1e-20), const['max_twist_degrees'] * np.pi / 180 / (theta_list + 1e-20)

    if showplot:
        plt.plot(y_list, MOS_v_list, color='darkblue', label='Deflection')
        plt.plot(y_list, MOS_theta_list, color='darkgreen', label='Twist')

        plt.plot([0, const['span']/2], [1,1], color='firebrick')
        plt.legend()
        plt.xlabel('Spanwise position (m)')
        plt.ylabel('Margin of Safety [-]')
        plt.title('MOS from Deflection and Twist')
        plt.ylim((-2, 20))
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')
        plt.show()
    else:
        plt.plot(y_list, MOS_v_list, label='Deflection Margin Of Safety')
        plt.plot(y_list, MOS_theta_list, label='Twist Margin Of Safety')

#Plots the Margin of Safety of compressive and tensile strength alongthe span
def compressive_strength_MOS_graph(wingbox, showplot=True, Npoints=500):
    from compressive_strength import bending_stress

    y_span = np.linspace(0, const['span']/2, Npoints)
    sigma_tensile = np.zeros_like(y_span)
    sigma_compressive = np.zeros_like(y_span)

    critical_sigma_z_tensile = const['Yield_stress']
    critical_sigma_z_compressive = -1 * const['Yield_stress']

    for i, y in enumerate(y_span):
        sigma_z = bending_stress(wingbox, y)
        sigma_tensile[i] = np.max(sigma_z) 
        sigma_compressive[i] = np.min(sigma_z) 

    if showplot:
        plt.plot(y_span, critical_sigma_z_tensile/(sigma_tensile + 1e-15), label='Tensile stress')
        plt.plot(y_span, critical_sigma_z_compressive/(sigma_compressive + 1e-15), label='Compressive stress')
        plt.axhline(0, color='k', linewidth=0.8)
        plt.xlabel('Spanwise location y [m]')
        plt.ylabel('Margin of Safety [-]')
        plt.title('Spanwise Compressive and Tensile Stress')
        plt.ylim(-2, 20) 
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')
        plt.legend()
        plt.show()
    else:
        plt.plot(y_span, np.abs(critical_sigma_z_tensile/(sigma_tensile + 1e-5)), label='Tensile stress')
        plt.plot(y_span, np.abs(critical_sigma_z_compressive/(sigma_compressive + 1e-5)), label='Compressive stress')
     
#Plots the Margin of Safety of column buckling alongthe span
def stringer_column_bucklin_MOS_graph(wingbox, showplot=True, Npoints=500):
    import column_buckling

    y_tab = np.linspace(0, const['span']/2, Npoints)
    MOS_tab = []
    for i in y_tab:
        MOS_tab.append(column_buckling.stringer_buckling_MOS(wingbox, i))

    if showplot:
        plt.plot(y_tab, MOS_tab, color='darkblue', label='Stringer Column Buckling')
        plt.plot([0, const['span']/2], [1,1], color='firebrick')
        plt.legend()
        plt.xlabel('Spanwise position (m)')
        plt.ylabel('Margin of Safety [-]')
        plt.ylim((-2, 20))
        plt.grid(axis='y', ls='--')
        plt.grid(axis='x', ls='--')
        plt.show()
    else:
        plt.plot(y_tab, MOS_tab, label='Stringer Column Buckling')

#Plots the Margin of Safety of skin buckling alongthe span
def skin_buckling_MOS_plot(wingbox, discrete_graph=False, showplot=True, Npoints=500):
    import skinbucklingcorrected
    
    if not discrete_graph:
        y_tab = np.linspace(0, const['span']/2, Npoints)

        MOS_tab = []
        for i in y_tab:
            MOS_tab.append(skinbucklingcorrected.margin_of_safety_skinbuckling(wingbox, i))
        MOS_tab = np.abs(MOS_tab)

        if showplot:
            plt.plot(y_tab, MOS_tab, color='darkblue', label='Skin Buckling')
            plt.plot([0, const['span']/2], [1,1], color='firebrick')
            plt.legend()
            plt.xlabel('Spanwise position (m)')
            plt.ylabel('Margin of Safety [-]')
            plt.ylim((-2, 20))
            plt.grid(axis='y', ls='--')
            plt.grid(axis='x', ls='--')
            plt.show()
        else:
            plt.plot(y_tab, MOS_tab, label='Skin Buckling')

    elif discrete_graph:
        rib_count = const['total_rib_count']    
        if rib_count % 2 == 1:
            y_tab_start = np.linspace(0, const['span']/2, (rib_count + 1) //2)
        else:
            y_tab_start = np.linspace(-1 * const['span']/2, const['span']/2, rib_count)
            y_tab_start = np.insert(y_tab_start[(len(y_tab_start))//2:], 0, 0)

        y_tab = []
        MOS_tab = []
        for i in range(len(y_tab_start) - 1):
            y_tab.append(y_tab_start[i])
            y_tab.append(y_tab_start[i+1])
            MOS_tab.append(skinbucklingcorrected.margin_of_safety_skinbuckling(wingbox, y_tab_start[i]))
            MOS_tab.append(skinbucklingcorrected.margin_of_safety_skinbuckling(wingbox, y_tab_start[i]))

        if showplot:
            plt.plot(y_tab, MOS_tab, color='darkblue', label='Skin Buckling')
            plt.plot([0, const['span']/2], [1,1], color='firebrick')
            plt.legend()
            plt.xlabel('Spanwise position (m)')
            plt.ylabel('Margin of Safety [-]')
            plt.ylim((-2, 20))
            plt.grid(axis='y', ls='--')
            plt.grid(axis='x', ls='--')
            plt.show()
        else:
            plt.plot(y_tab, MOS_tab, label='Skin Buckling')
    
def MOS_rib_location_plot(showplot=True):
    rib_count = const['total_rib_count']    
    if rib_count % 2 == 1:
        y_tab = np.linspace(0, const['span']/2, (rib_count + 1) //2)
    else:
        y_tab = np.linspace(-1 * const['span']/2, const['span']/2, rib_count)
        y_tab = np.insert(y_tab[(len(y_tab))//2:], 0, 0)

    rib_locations = np.zeros((len(y_tab), 2))
    rib_locations[:,0] = y_tab

    plt.plot(rib_locations[1:,0], rib_locations[1:,1], '|', label='Rib Locations', ms=20, color='black')

    if showplot:
            plt.plot([0, const['span']/2], [1,1], color='firebrick')
            plt.legend()
            plt.xlabel('Spanwise position (m)')
            plt.ylabel('Margin of Safety [-]')
            plt.ylim((-2, 20))
            plt.grid(axis='y', ls='--')
            plt.grid(axis='x', ls='--')
            plt.show()

#Plots all MOS's along the span
def plot_MOS_graph(wingbox):
    compressive_strength_MOS_graph(wingbox, showplot=False)
    stringer_column_bucklin_MOS_graph(wingbox, showplot=False)
    skin_buckling_MOS_plot(wingbox, showplot=False)
    deflection_twist_MOS_plot(wingbox, showplot=False)
    MOS_rib_location_plot(showplot=False)
    spar_shear_MOS_plot(wingbox, Npoints=135, showplot=False)

    ax = plt.gca()
    for line in ax.lines:
        line.set_ydata(line.get_ydata() / 1.5)
    ax.relim()
    ax.autoscale_view()

    plt.plot([0, const['span']/2], [1,1], color='black', label='Lower Limit')
    plt.legend(fontsize=25)
    plt.xlabel('Spanwise position (m)', fontsize=40)
    plt.ylabel('Margin of Safety [-]', fontsize=40)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.ylim((-2, 15))
    plt.grid(axis='y', ls='--')
    plt.grid(axis='x', ls='--')
    plt.show()
