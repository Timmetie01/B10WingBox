import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt
from constants import const
import area_moments
import wingbox_design
import stress_functions


testwingbox = data_import.idealizable_wingboxl(0.2, 0.6, [0.0005, 0.005, 0.0005, 0.01], 'partially_constant', stringercount=40, stringer_areas=5e-5, stringerspacing='constant_no_endpoints', panels_per_stringer=20, web_panel_count=50)

#testwingbox.shear_stress(0)
graphing.shear_flow_plot(testwingbox, 0)

print(stress_functions.critical_spar_shear(testwingbox, 0))
#print(max(testwingbox.shear_stress(0)), min(testwingbox.shear_stress(0)))
#print(testwingbox.shear_stress(0))

print(stress_functions.spar_buckling_MOS(testwingbox, 0))

