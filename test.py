import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt
from constants import const
import area_moments
import wingbox_design
import stress_functions
import data_import

#XCP is not smooth
#testwingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.001, 0.003, 0.001, 0.003], 'partially_constant', scaled_thickness=False, stringercount=20, stringer_areas=5e-5, stringerspacing='constant_no_endpoints', panels_per_stringer=5, web_panel_count=30)

#graphing.shear_flow_spanwise_plot(testwingbox)
#graphing.shear_flow_plot(testwingbox, 1)
#graphing.compressive_strength_MOS_graph(testwingbox, showplot=False)
#graphing.stringer_column_bucklin_MOS_graph(testwingbox, showplot=False)
#graphing.spar_shear_MOS_plot(testwingbox)


#print(testwingbox.worst_spar_shear_MOS())

#print(stress_functions.critical_spar_shear(testwingbox, 0))
#print(max(testwingbox.shear_stress(0)), min(testwingbox.shear_stress(0)))
#print(testwingbox.shear_stress(0))

#print(stress_functions.spar_buckling_MOS(testwingbox, 0))
#print(testwingbox.shear_stress(0))

test_scaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0006572158442155239, 0.0011401876353445486, 0.0006572158442155239, 0.0011401876353445486], 'partially_constant', 4, 1.0487964101566806e-05, scaled_thickness=True)

graphing.compressive_strength_MOS_graph(test_scaled_wingbox, showplot=False)
graphing.stringer_column_bucklin_MOS_graph(test_scaled_wingbox, showplot=False)
graphing.compressive_strength_MOS_graph(test_scaled_wingbox, showplot=False)
graphing.skin_buckling_MOS_plot(test_scaled_wingbox, showplot=False)
graphing.spar_shear_MOS_plot(test_scaled_wingbox)

test_unscaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0020421020391436155,0.0034692189338491365,0.0020421020391436155,0.0034692189338491365], 'partially_constant', 4, 1.4314458878848655e-05, scaled_thickness=False)
graphing.compressive_strength_MOS_graph(test_unscaled_wingbox, showplot=False)
graphing.stringer_column_bucklin_MOS_graph(test_unscaled_wingbox, showplot=False)
graphing.compressive_strength_MOS_graph(test_unscaled_wingbox, showplot=False)
graphing.skin_buckling_MOS_plot(test_unscaled_wingbox, showplot=False)
graphing.spar_shear_MOS_plot(test_unscaled_wingbox)

