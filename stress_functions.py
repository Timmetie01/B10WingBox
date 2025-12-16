import scipy as sp
from constants import const
from worst_cases import worst_case_loading
import numpy as np
import area_moments



#Using Mx*y/Ixx (but in different coordinate system). i.e. assuming Ixy=0 and only moment around X axis is present.
def max_bending_stress(wingbox, y):
    '''
    Returns the worst normal stress at a certain cross-section using Mx*y/Ixx (but in different coordinate system). i.e. assuming Ixy=0 and only moment around X axis is present.
    
    :param wingbox: The input wingbox-class
    :param y: The spanwise location
    '''
    sigma_z = worst_case_loading.M(y, 'abs_min_bending') * np.array([wingbox.z_max_min(y)[0], wingbox.z_max_min(y)[1]]) / wingbox.Ixx(y)
    return sigma_z[0] if sigma_z[0] > -1 * sigma_z[1] else sigma_z[1]



def shear_stress(wingbox, y):
        '''
        A function that calculates shear stress in each \'panel\' of the wingbox, using boom method and moment equivalence 
        
        :param wingbox: The wingbox to calculate shear flow on
        :param y: span-wise position
        :return q: a matrix with the shear flow following each panel, as in wingbox.panels
        '''
        from classes import ScaledWingbox
        import constants
        from worst_cases import worst_case_loading
        import area_moments
        import data_from_xflr5
        xcp = data_from_xflr5.xcppos_func(1.621258898884106)
        #0.2312805658645682
        if not wingbox.idealizable:
            print('This wingbox can not be idealized, so it doenst make sense to calculate shear for it.')
            quit()
        
        #Since axis systems flipped, negative force means upward, but the wingbox is defined positive upward. Thus the force is flipped
        Vy = worst_case_loading.V(y, 'abs_min_shear') * -1
        
        current_wingbox = ScaledWingbox(wingbox, constants.local_chord_at_span(y))

        #Cut in the vertical panel under the leading edge top point, assumed Vx = 0 and Ixy = 0
        shear_b = np.zeros_like(current_wingbox.panel_thickness)
        for i in range(len(shear_b)):
            shear_b[i] = shear_b[i - 1] - Vy / wingbox.Ixx(y) * current_wingbox.idealized_point_areas[i] * current_wingbox.centroidal_points[i,1]

        #Moment around centroid, clockwise positive
        centroidal_moment_qb = 0
        for i in range(len(shear_b)):
            #centroidal_moment_qb += shear_b[i] * 2 * area_moments.polygon_area(np.array([[0,0], current_wingbox.centroidal_panels[i,:2], current_wingbox.centroidal_panels[i,2:]]))
            #More efficent way of triangle area with one vertex 0,0 below:
            centroidal_moment_qb += shear_b[i] * 2 * 0.5 * abs(current_wingbox.centroidal_panels[i,0] * current_wingbox.centroidal_panels[i,3] - current_wingbox.centroidal_panels[i,2] * current_wingbox.centroidal_panels[i,1])
            
        #Moment that should be created when loading=internal force
        #centroidal_moment_Vy = (wingbox.centroid_coordinates[0] - xcp(y)) * constants.local_chord_at_span(y) * Vy
        centroidal_moment_Vy = worst_case_loading.T(y, 'abs_max_torsion')
 
        #Calculating the qs0 such that internal loading and torque equal applied loading and torque
        qs0_contribution = 2 * wingbox.area(y)
        qs0 = (centroidal_moment_Vy - centroidal_moment_qb) / qs0_contribution

        current_wingbox.shear = shear_b + qs0

        #It works! The internal load sums back to the applied load with less than 0.5% error. To check, uncomment the following lines
        #print(f'Summed shear: {np.sum(current_wingbox.shear * np.transpose([current_wingbox.centroidal_panels[:,3] - current_wingbox.centroidal_panels[:,1]]))}')
        #print(f'Vy: {Vy}')

        return current_wingbox.shear

def critical_spar_shear(wingbox, y):
    """
    Returns the critical shear stress for the front and rear spar
    
    :param wingbox: Wingbox Input
    :param y: The spanwise location
    :return tau_cr_front: The critical shear stress for the front spar
    :return tau_cr_rear: The critical shear stress for the rear spar
    """

    import classes
    import constants
    current_wingbox = classes.ScaledWingbox(wingbox, constants.local_chord_at_span(y))

    ks = 6/11 + 9 #Page 41 of reader. aspect ratio >5 (wing long compared to height), and clamped edges

    #Reverse engineering how many points are contained in the skin vs the spars
    #CODE BELOW CAN BE VECTORIZED FOR OPTIMIZATION (if required)
    xmin, xmax = np.min(current_wingbox.centroidal_points[:,0]), np.max(current_wingbox.centroidal_points[:,0])
    rear_spar_max, rear_spar_min = 0, 0
    front_spar_max, front_spar_min = 0, 0
    for i in current_wingbox.centroidal_points:
        if i[0] <= xmin + 1e-7 and i[1] > front_spar_max:
             front_spar_max = i[1]
        elif i[0] <= xmin + 1e-7 and i[1] < front_spar_min:
             front_spar_min = i[1]
        elif i[0] >= xmax - 1e-7 and i[1] > rear_spar_max:
             rear_spar_max = i[1]
        elif i[0] >= xmax - 1e-7 and i[1] < rear_spar_min:
             rear_spar_min = i[1]

    rear_spar_height, front_spar_height = rear_spar_max - rear_spar_min, front_spar_max - front_spar_min
    rear_spar_thickness, front_spar_thickness = current_wingbox.panel_thickness[len(current_wingbox.panel_thickness)//2 - 1], current_wingbox.panel_thickness[-1]

    tau_cr_rear = np.pi ** 2 * ks * const['Modulus_of_Elasticity'] / (12 * (1 - const['Poisson\'s Ratio'] ** 2)) * (rear_spar_thickness / rear_spar_height) ** 2 
    tau_cr_front = np.pi ** 2 * ks * const['Modulus_of_Elasticity'] / (12 * (1 - const['Poisson\'s Ratio'] ** 2)) * (front_spar_thickness / front_spar_height) ** 2 

    return tau_cr_front, tau_cr_rear

def spar_buckling_MOS(wingbox, y, return_info=False):
    """
    Checks if the spar shear-buckles OR exceeds maximum shear stress.
     
    :param wingbox: The wingbox to be analyzed
    :param y: Span-wise positon
    :param return_info: Will return a string you can print that describes what failed.
    :return MOS: Margin of safety under current loading
    """
    from classes import ScaledWingbox
    import constants
    current_wingbox = ScaledWingbox(wingbox, constants.local_chord_at_span(y))

    tau_cr_front, tau_cr_rear = critical_spar_shear(wingbox, y)
    
    returnstring = 'The things that failed are: '
    
    #Assuming that the spar is created from top left corner and goes around clockwise, as all wingbox-creating functions do.
    rear_spar_thickness, front_spar_thickness = current_wingbox.panel_thickness[len(current_wingbox.panel_thickness)//2 - 1], current_wingbox.panel_thickness[-1]
    
    #Shear stress = q/t
    #Since the highest moments are positive as determined in wp4, the max is on the left and the min on the right.
    front_spar_max = max(wingbox.shear_flow(y)) / front_spar_thickness
    rear_spar_max = abs(min(wingbox.shear_flow(y))) / rear_spar_thickness

    #Calculating MOS for all cases
    if tau_cr_front/front_spar_max < 1:
        returnstring += 'Shear buckling in front stringer, '
    if tau_cr_rear/rear_spar_max < 1:
        returnstring += 'Shear buckling in rear stringer, '
    if (const['Yield_stress']/2) / front_spar_max < 1:
        returnstring += 'Yield shear stress in front stringer, '
    if (const['Yield_stress']/2) / rear_spar_max < 1:
        returnstring += 'Yield shear stress in rear stringer, '

    #print(front_spar_max, rear_spar_max)
    #print(tau_cr_front/front_spar_max, tau_cr_rear/rear_spar_max, (const['Ultimate_tensile_stress']/2) / front_spar_max, (const['Ultimate_tensile_stress']/2) / rear_spar_max)
    margin_of_safety = (tau_cr_front/front_spar_max, tau_cr_rear/rear_spar_max, (const['Ultimate_tensile_stress']/2) / front_spar_max, (const['Ultimate_tensile_stress']/2) / rear_spar_max)
    return (margin_of_safety, returnstring) if return_info else min(margin_of_safety)
         
    


     
     
    

