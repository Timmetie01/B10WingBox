import data_import
from constants import const
import deflection_functions
import stress_functions
import numpy as np
from scipy.optimize import minimize, differential_evolution

#WARNING: Running this file can take ~20 minutes. When using a laptop, letting it charge meanwhile and enabling any sort of 'performance mode' significantly reduces running time

#Due to limitations regarding the ways to enable multi-threaded processing in scipy.optimizide.differential_evolution,
#The inputs for the final design must be manually entered. The performance increase is more than worth it.
xstart = 0.2 
xend = 0.6
margin_of_safety = 1
scaled_thickness = True
web_panel_count = 20
skin_panel_count = 200
name=None

#x = sparthickness, skinthickness, stringercount, stringerarea
x = [0.0001, 0.0002, 20., 5e-5]

#Upper and lower bounds taken into account by the differential evolution
bounds = [
    (0.0001, 0.05),
    (0.0001, 0.01),
    (4,50),
    (3e-5, 2e-4)
]

#Initial guess, doesnt really matter
x0 = [0.0001, 0.0002, 20, 3e-5]

def force_even_stringercount(x):
    '''
    Since differential Evolution doesnt use integers, the stringer count must manually be forced to an integer
    
    :param x: Vector of unknowns
    '''
    x[2] = int(x[2] // 2 * 2)
    return x

def wingbox_simplified(x):
    '''
    Creates a wingbox while taking the iterables vector as an input
    
    :param x: The unknowns vector for the optimization
    '''
    x = force_even_stringercount(x)
    return data_import.idealizable_wingbox(xstart, xend, [x[1], x[0], x[1], x[0]], 'partially_constant', x[2], x[3], stringerspacing='constant_no_endpoints', panels_per_stringer=160//x[2], web_panel_count=web_panel_count, scaled_thickness=scaled_thickness, name=name)

def deflection_MOS(x):
    wingbox = wingbox_simplified(x)
    return (const['max_deflection_fraction'] * const['span'] / (max(deflection_functions.v(wingbox)[1]))) - margin_of_safety

def twist_MOS(x):
    wingbox = wingbox_simplified(x)
    return const['max_twist_degrees'] * np.pi / 180 / (max(abs(deflection_functions.theta(wingbox)[1]))) - margin_of_safety

def shear_MOS(x):
    wingbox = wingbox_simplified(x)
    return wingbox.worst_spar_shear_MOS() - margin_of_safety

def compressive_tensile_MOS(x):
    wingbox = wingbox_simplified(x)
    y_span = np.linspace(0, const['span']/2, 100)
    sigma_tensile = np.zeros_like(y_span)
    sigma_compressive = np.zeros_like(y_span)

    critical_sigma_z_tensile = const['Yield_stress']
    critical_sigma_z_compressive = -1 * const['Yield_stress']

    for i, y in enumerate(y_span):
        sigma_z = stress_functions.max_bending_stress(wingbox, y)
        sigma_tensile[i] = np.max(sigma_z) 
        sigma_compressive[i] = np.min(sigma_z) 

    return abs(min(critical_sigma_z_tensile / max(sigma_tensile), critical_sigma_z_compressive / max(sigma_compressive))) - margin_of_safety
    
def stringer_column_MOS(x):
    import column_buckling
    wingbox = wingbox_simplified(x)
    return column_buckling.lowest_stringer_buckling_MOS(wingbox) - margin_of_safety

def skin_buckling_MOS(x):
    import skinbucklingcorrected
    wingbox = wingbox_simplified(x)
    y_tab = np.linspace(0, const['span']/2, 100)
    MOS_tab = []
    for i in y_tab:
        MOS_tab.append(abs(skinbucklingcorrected.margin_of_safety_skinbuckling(wingbox, i)))

    return min(MOS_tab) - margin_of_safety


'''
def objective(x):
    wingbox = wingbox_simplified(x)
    print(x)
    return wingbox.weight(print_value=False)

constraints = [
    {"type": "ineq", "fun": deflection_MOS},
    {"type": "ineq", "fun": twist_MOS},
    {"type": "ineq", "fun": shear_MOS},
    {"type": "ineq", "fun": compressive_tensile_MOS},
    {"type": "ineq", "fun": stringer_column_MOS},
    {"type": "ineq", "fun": skin_buckling_MOS},        
]
'''

def constrained_objective(x):
    x = x.copy()
    wingbox = wingbox_simplified(x)

    if deflection_MOS(x) < 0:           return 1e6
    if twist_MOS(x) < 0:                return 1e6
    if shear_MOS(x) < 0:                return 1e6
    if compressive_tensile_MOS(x) < 0:  return 1e6
    if stringer_column_MOS(x) < 0:      return 1e6
    if skin_buckling_MOS(x) < 0:        return 1e6

    return wingbox.weight(print_value=False) 

'''
 result = minimize(
    objective,
    x0,
    method='SLSQP',
    bounds=bounds,
    constraints=constraints,
    options={'disp': True, 'maxiter': 200}
)'
'''

#Has to be formatted as below to use all available cores
if __name__ == "__main__":
    result = differential_evolution(
        constrained_objective,
        bounds=bounds,
        maxiter=100,
        popsize=15,
        workers=-1
    )

    x_opt = force_even_stringercount(result.x)
    designwingbox = wingbox_simplified(x_opt)

    print(f"Optimal design:")
    print(f"spar thickness: ", x_opt[0])
    print(f"skin thickness: ", x_opt[1])
    print(f"stringer area: ", x_opt[3])
    print(f"number of stringers: ", x_opt[2])
    print(f"Final weight: {round(designwingbox.weight(print_value=False), 4)} kg")
    print(f"That is with xstart={xstart}, xend={xend}, Scaledthickness={scaled_thickness}, margin of safety of at least {margin_of_safety}.")

    print(result)
    #print(deflection_MOS(x_opt) + margin_of_safety, twist_MOS(x_opt) + margin_of_safety, shear_MOS(x_opt) + margin_of_safety, abs(compressive_tensile_MOS(x_opt)) + margin_of_safety, stringer_column_MOS(x_opt) + margin_of_safety, constrained_objective(x_opt) + margin_of_safety)

    import graphing
    graphing.plot_MOS_graph(designwingbox)

    
    
