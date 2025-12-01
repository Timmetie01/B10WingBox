import data_import
from constants import const
import graphing
import deflection_functions
from worst_cases import worst_case_loading
import numpy as np

deflection = 100
twist = 100
wingboxthickness = 0
while deflection > const['span'] * const['max_deflection_fraction'] or abs(twist) > const['max_twist_degrees']:
    wingboxthickness += 5e-5
    iterationwingbox = data_import.create_airfoil_like_wingbox(0.1, 0.5, thickness=[wingboxthickness, wingboxthickness, wingboxthickness,  wingboxthickness], thicknesstype='partially_constant', stringercount=20, stringer_areas=1e-5, panelcount=50, stringerspacing='constant_no_endpoints')

    y_list, v_list = deflection_functions.v(iterationwingbox)
    deflection = max(v_list)
    y_list, theta_list = deflection_functions.theta(iterationwingbox)
    theta_list = theta_list * 180 / np.pi
    twist = max(np.abs(theta_list))

    print(f'Thickness: {round(const['root_chord'] * wingboxthickness * 1000, 5)} mm  \ttwist: {round(twist, 4)} deg  \tdeflection: {round(deflection, 4)} m.')

print(f'The final wingbox thickness is {round(const['root_chord'] * wingboxthickness * 1000, 5)} mm at the chord, and {round(const['tip_chord'] * wingboxthickness * 1000, 5)} mm at the tip!')


#graphing.airfoil_pointplot(showplot=False)
#graphing.wingbox_plot(iterationwingbox)

graphing.wing_plot(iterationwingbox)
#graphing.deflection_plot(iterationwingbox, two_wings=False)
#graphing.twist_plot(iterationwingbox)

#graphing.I_plot(iterationwingbox)


