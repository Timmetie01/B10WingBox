import data_import
import classes
import area_moments
import constants

testclass = data_import.import_wingbox('test_cross_section')
testscale = classes.ScaledWingbox(testclass, 2)

#print(testclass.centroidal_panels)
#print(testscale.centroidal_panels)

#The Ixx, Iyy and Ixy functions must be checked to confirm if they work. 
print(testclass.Ixx(0))
print(testclass.Ixx(4))
print(testclass.Ixx(8))

