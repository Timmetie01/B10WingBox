import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt
from constants import const
import area_moments
import wingbox_design



testwingbox = data_import.idealizable_wingboxl(0.2, 0.6, [0.001, 0.01, 0.001, 0.01], 'partially_constant', stringercount=40, stringer_areas=2e-5, stringerspacing='constant_no_endpoints', panels_per_stringer=3, web_panel_count=20)

testwingbox.shear_stress(0)

graphing.shear_stress_plot(testwingbox, 0)