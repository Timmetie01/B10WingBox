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
print(.0020421020391436155/.0006572158442155239)

#The final designs after iteration. First the constant thickness one:
test_unscaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0020421020391436155, 0.0034692189338491365, 0.0020421020391436155, 0.0034692189338491365], 'partially_constant', 4, 1.4314458878848655e-05, scaled_thickness=False)
graphing.plot_MOS_graph(test_unscaled_wingbox)

#THe final design after iteration, here the variable thickness one
test_scaled_wingbox = data_import.idealizable_wingbox(0.2, 0.6, [0.0006572158442155239, 0.0011401876353445486, 0.0006572158442155239, 0.0011401876353445486], 'partially_constant', 4, 1.0487964101566806e-05, scaled_thickness=True)
graphing.plot_MOS_graph(test_scaled_wingbox)



