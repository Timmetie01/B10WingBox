import data_import
from constants import const
import graphing
import deflection_functions
from worst_cases import worst_case_loading
import numpy as np
import wingbox_design


#Iteration 1:
iterationwingbox, thickness = wingbox_design.thickness_iteration(0.1, 0.5, stringercount=0, stringer_areas=1e-5, stringerspacing='constant_no_endpoints', panelcount=50)


#graphing.airfoil_pointplot(showplot=False)
#iterationwingbox.plot()

iterationwingbox.wing_plot(Npoints=50)

iterationwingbox.deflection_plot()
#iterationwingbox.twist_plot()

#graphing.worst_moment_plot()
#graphing.I_plot(iterationwingbox)

#print(iterationwingbox.max_bending_stress())

#graphing.bending_stress_plot(iterationwingbox)

