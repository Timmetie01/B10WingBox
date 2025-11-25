import data_import
import classes
import area_moments
import constants
import graphing

testclass = data_import.import_wingbox('test_cross_section')

print(testclass.J(0))


#print(testclass.centroidal_panels)
#print(testscale.centroidal_panels)

#The Ixx, Iyy and Ixy functions must be checked to confirm if they work. 
#print(testclass.Ixx(0))
#print(testclass.Ixx(2))
#print(testclass.Ixx(4))
#print(testclass.Ixx(6))
#print(testclass.Ixx(8))

graphing.I_plot(testclass)

