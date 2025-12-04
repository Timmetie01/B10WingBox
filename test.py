import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt
from constants import const
import area_moments
import wingbox_design

iterationwingbox, thickness = wingbox_design.thickness_iteration(0.2, 0.6, stringercount=20, stringer_areas=3e-5, stringerspacing='constant_no_endpoints', panelcount=50)

area_moments.cross_sectional_area(iterationwingbox, 0)

