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
testwingbox = data_import.idealizable_wingboxl(0.2, 0.6, [0.001, 0.003, 0.001, 0.003], 'partially_constant', scaled_thickness=False, stringercount=20, stringer_areas=5e-5, stringerspacing='constant_no_endpoints', panels_per_stringer=5, web_panel_count=30)

testwingbox.shear_stress(0)
#graphing.shear_flow_spanwise_plot(testwingbox)
graphing.shear_flow_plot(testwingbox, 1)
graphing.spar_shear_MOS_plot(testwingbox)


#print(stress_functions.critical_spar_shear(testwingbox, 0))
#print(max(testwingbox.shear_stress(0)), min(testwingbox.shear_stress(0)))
#print(testwingbox.shear_stress(0))

#print(stress_functions.spar_buckling_MOS(testwingbox, 0))
#print(testwingbox.shear_stress(0))






