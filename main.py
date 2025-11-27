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

#graphing.wingbox_plot(testclass, showplot=False)
graphing.airfoil_pointplot(showplot=False)
#print(data_import.airfoil_interpolation([0.1, 0.2, 0.3], side='top'))

newtestclass = data_import.create_airfoil_like_wingbox(0.1, 0.5, thickness=[0.005, 0.002, 0.005, 0.002], thicknesstype='partially_constant', stringercount=10, stringer_areas=2e-5)
print(newtestclass.points)

graphing.wingbox_plot(newtestclass)
graphing.deflection_plot(newtestclass)

newtestclass = data_import.create_airfoil_like_wingbox(0.1, 0.5, thickness=[0.005, 0.002, 0.005, 0.002], thicknesstype='partially_constant', stringercount=10, stringer_areas=2e-5, panelcount=4)
graphing.wingbox_plot(newtestclass)
