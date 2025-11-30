import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt

newtestclass = data_import.create_airfoil_like_wingbox(0.2, 0.4, thickness=[0.001, 0.0005, 0.001, 0.0005], thicknesstype='partially_constant', stringercount=10, stringer_areas=0e-5, panelcount=50)

ylist, vlist = deflection_functions.v_trapezoidal(newtestclass)

graphing.deflection_plot(newtestclass, two_wings=False)