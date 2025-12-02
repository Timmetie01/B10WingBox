import data_import
import numpy as np
import graphing
import deflection_functions
import matplotlib.pyplot as plt
from constants import const

from data_import import import_wingbox
testwingbox = import_wingbox('test_cross_section')

print(testwingbox.z_max_min(0))