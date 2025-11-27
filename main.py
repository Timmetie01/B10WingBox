import data_import
from constants import const
import graphing
import deflection_functions

testclass = data_import.import_wingbox('test_cross_section')

#Testing the I-plot
#graphing.I_plot(testclass)

#Testing the deflection plots, just 
#from data_import import import_wingbox
#testclass = import_wingbox('test_cross_section')
#graphing.deflection_plot(testclass)
#graphing.twist_plot(testclass)

graphing.airfoil_pointplot(showplot=False)

#newtestclass = data_import.create_airfoil_like_wingbox(0.1, 0.6, thickness=[0.003, 0.001, 0.003, 0.001], thicknesstype='full_array', stringercount=12, stringer_areas=2e-5, panelcount=4)
#graphing.wingbox_plot(newtestclass)
#graphing.deflection_plot(newtestclass, two_wings=False)

deflection = 100
wingboxthickness = 0
while deflection > const['span'] * const['max_deflection_fraction']:
    wingboxthickness += 1e-5
    iterationwingbox = data_import.create_airfoil_like_wingbox(0.1, 0.6, thickness=[wingboxthickness, 0.005, wingboxthickness, 0.005], thicknesstype='partially_constant', stringercount=40, stringer_areas=3e-5, panelcount=50)

    deflection = deflection_functions.v(iterationwingbox)

print(wingboxthickness)
graphing.wingbox_plot(iterationwingbox)
graphing.deflection_plot(iterationwingbox, two_wings=False)


