import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt
from constants import const
import area_moments
import wingbox_design
import stress_functions

#XCP is not smooth
testwingbox = data_import.idealizable_wingboxl(0.2, 0.6, [0.001, 0.003, 0.001, 0.003], 'partially_constant', scaled_thickness=False, stringercount=20, stringer_areas=5e-5, stringerspacing='constant_no_endpoints', panels_per_stringer=3, web_panel_count=10)

testwingbox.shear_stress(0)
#graphing.shear_flow_spanwise_plot(testwingbox)
graphing.shear_flow_plot(testwingbox, 1)
graphing.spar_shear_MOS_plot(testwingbox)


#print(stress_functions.critical_spar_shear(testwingbox, 0))
#print(max(testwingbox.shear_stress(0)), min(testwingbox.shear_stress(0)))
#print(testwingbox.shear_stress(0))

print(stress_functions.spar_buckling_MOS(testwingbox, 0))
print(testwingbox.shear_stress(0))

#import worst_cases
#print(worst_cases.worst_case_loading.V(0, 'abs_min_shear'))
#print(worst_cases.worst_case_loading.T(1, 'abs_max_torsion'))



