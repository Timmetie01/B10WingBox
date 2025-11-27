import data_import
import classes
import area_moments
import constants
import graphing

testclass = data_import.import_wingbox('test_cross_section')

#Testing the I-plot
#graphing.I_plot(testclass)

#Testing the deflection plots, just 
#from data_import import import_wingbox
#testclass = import_wingbox('test_cross_section')
#graphing.deflection_plot(testclass)
#graphing.twist_plot(testclass)

graphing.airfoil_pointplot(showplot=False)

newtestclass = data_import.create_airfoil_like_wingbox(0.1, 0.6, thickness=[0.003, 0.001, 0.003, 0.001], thicknesstype='full_array', stringercount=12, stringer_areas=2e-5, panelcount=4)

graphing.wingbox_plot(newtestclass)
graphing.deflection_plot(newtestclass, two_wings=False)

