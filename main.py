import data_import
import classes

testclass = data_import.import_wingbox('test_cross_section')
testscale = classes.ScaledWingbox(testclass, 2)

print(testclass.centroidal_panels)
print(testscale.centroidal_panels)