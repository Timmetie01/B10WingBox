import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt
from constants import const

t = 3.26358 / const['root_chord']

iterationwingbox = data_import.create_airfoil_like_wingbox(0.1, 0.5, thickness=[t, t, t,  t], thicknesstype='partially_constant', stringercount=20, stringer_areas=1e-5, panelcount=50, stringerspacing='constant_no_endpoints')


graphing.wing_plot(iterationwingbox)