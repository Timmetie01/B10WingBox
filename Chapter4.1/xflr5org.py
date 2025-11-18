import numpy as np

tablezeroalpha = np.genfromtxt("B10WingBox\Chapter4.1\MainWing_a=0.00HighpanelFinal.csv", delimiter=",", skip_header=21, skip_footer=5745)

yspan_0 = tablezeroalpha[:,0]
chordlength_0 = tablezeroalpha[:,1]
Ai_0 = tablezeroalpha[:,2]
Cl_0 = tablezeroalpha[:,3]
PCd_0 = tablezeroalpha[:,4]
ICd_0 = tablezeroalpha[:,5]
cmgeom_0 = tablezeroalpha[:,6]
CmAirfchord4_0 = tablezeroalpha[:,7]
posofcp_0 = tablezeroalpha[:,10]

tabletenalpha = np.genfromtxt("B10WingBox\Chapter4.1\MainWing_a=10.00HighplaneFinal.csv", delimiter=",", skip_header=21, skip_footer=5745)

yspan_10 = tabletenalpha[:,0]
chordlength_10 = tabletenalpha[:,1]
Ai_10 = tabletenalpha[:,2]
Cl_10 = tabletenalpha[:,3]
PCd_10 = tabletenalpha[:,4]
ICd_10 = tabletenalpha[:,5]
cmgeom_10 = tabletenalpha[:,6]
CmAirfchord4_10 = tabletenalpha[:,7]
posofcp_10 = tabletenalpha[:,10]

print(Cl_0)