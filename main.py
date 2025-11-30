import data_import
from constants import const
import graphing
import deflection_functions
from worst_cases import worst_case_loading
import numpy as np

testclass = data_import.import_wingbox('test_cross_section')

#Testing the I-plot
#graphing.I_plot(testclass)

#Testing the deflection plots, just 
#from data_import import import_wingbox
#testclass = import_wingbox('test_cross_section')
#graphing.deflection_plot(testclass)
#graphing.twist_plot(testclass)


graphing.worst_moment_plot()
graphing.worst_torsion_plot()

deflection = 100
twist = 100
wingboxthickness = 0
while deflection > const['span'] * const['max_deflection_fraction'] or abs(twist) > const['max_twist_degrees']:
    wingboxthickness += 1e-4
    iterationwingbox = data_import.create_airfoil_like_wingbox(0.1, 0.5, thickness=[wingboxthickness, wingboxthickness, wingboxthickness,  wingboxthickness], thicknesstype='partially_constant', stringercount=0, stringer_areas=1e-5, panelcount=50)

    y_list, v_list = deflection_functions.v(iterationwingbox)
    deflection = max(v_list)
    y_list, theta_list = deflection_functions.theta(iterationwingbox)
    theta_list = theta_list * 180 / np.pi
    twist = max(np.abs(theta_list))

    print(wingboxthickness, twist)

print(wingboxthickness)


graphing.airfoil_pointplot(showplot=False)
graphing.wingbox_plot(iterationwingbox)

graphing.deflection_plot(iterationwingbox, two_wings=False)
graphing.twist_plot(iterationwingbox)


