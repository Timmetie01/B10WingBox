import data_import
from constants import const
import graphing
import deflection_functions
from worst_cases import worst_case_loading
import numpy as np
import wingbox_design
import NVMdiagrams

#Welcome to the wingbox calculations by group 10B. The README contains some information about how to use these tools for designing the wingbox
#Required packages: numpy, scipy, math
#Recommended: Rainbow CSV (XFLR5 Data)

#The following code is used to update the bending and torsion data.
#The torsion depends on the centroidal coordinates of the wingbox, and thus this data must be regenerated before commiting final designs, to avoid minor inaccuracies.
#This can take multiple minutes to run. Therefore only do so at major design steps
#MVMdiagrams.find_worst_loading(1, 32, testclass)

#An example of the Wingbox class being used
#test = data_import.create_airfoil_like_wingbox(xstart, xend, thickness=wingboxthickness, thicknesstype='constant', stringercount=stringercount, stringer_areas=stringer_areas, panelcount=panelcount, stringerspacing=stringerspacing, name=name)
Wingbox_example1 = data_import.create_airfoil_like_wingbox(0.2, 0.6, 0.0015, stringercount=20, thicknesstype='constant', stringer_areas=1.8e-5, stringerspacing='constant_no_endpoints', panelcount=82, name='Wingbox_example1')
#And this wingbox now has many useful properties, such as:
print(f'{Wingbox_example1.name} has the following property\'s at the root:')
print(f'Ixx: {Wingbox_example1.Ixx(0)}')
print(f'J: {Wingbox_example1.J(0)}')

#The previously discussed bending and torsion (and shear) data can also be plotted.
graphing.worst_shear_plot()
graphing.worst_torsion_plot()

#These things together and some numerical integration results in deflection and twist of the total wing!
Wingbox_example1.deflection_plot()
Wingbox_example1.twist_plot()

#Using the extremeties of these graphs, wingboxes can be iterated over to ensure optimal thickness
Wingbox_example2, thickness = wingbox_design.thickness_iteration(0.2, 0.6, stringercount=20, stringer_areas=1.8e-5, thicknesstype='constant', stringerspacing='constant_no_endpoints', panelcount=82, name='Preliminary Design Wingbox 2')
print(f'A more optimal thickness for the previous design would be {round(thickness * 1000, 5)} mm!')

#Some bonus features not yet fully implemented/required:
graphing.bending_stress_plot(Wingbox_example2)
Wingbox_example2.wing_plot()

