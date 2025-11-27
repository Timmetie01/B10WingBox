import numpy as np
import math as m
from NVMdiagrams import alphafromCLd

# AOA = 0deg
tablezeroalpha = np.genfromtxt(r"xflr5data\MainWing_a=0.00_v=10.00ms.csv", delimiter=",", skip_header=21)

yspan_0 = tablezeroalpha[:,0]
posofcp_0 = tablezeroalpha[:,10]

# AOA = 1deg
table1alpha = np.genfromtxt(r"xflr5data\MainWing_a=1.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_1 = table1alpha[:,10]

# AOA = 2deg
table2alpha = np.genfromtxt(r"xflr5data\MainWing_a=2.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_2 = table2alpha[:,10]

# AOA = 3deg
table3alpha = np.genfromtxt(r"xflr5data\MainWing_a=3.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_3 = table3alpha[:,10]

# AOA = 4deg
table4alpha = np.genfromtxt(r"xflr5data\MainWing_a=4.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_4 = table4alpha[:,10]

# AOA = 5deg
table5alpha = np.genfromtxt(r"xflr5data\MainWing_a=5.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_5 = table5alpha[:,10]

# AOA = 6deg
table6alpha = np.genfromtxt(r"xflr5data\MainWing_a=6.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_6 = table6alpha[:,10]

# AOA = 7deg
table7alpha = np.genfromtxt(r"xflr5data\MainWing_a=7.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_7 = table7alpha[:,10]

# AOA = 8deg
table8alpha = np.genfromtxt(r"xflr5data\MainWing_a=8.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_8 = table8alpha[:,10]

# AOA = 9deg
table9alpha = np.genfromtxt(r"xflr5data\MainWing_a=9.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_9 = table9alpha[:,10]

# AOA = 10deg
table10alpha = np.genfromtxt(r"xflr5data\MainWing_a=10.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_10 = table10alpha[:,10]

posofcplist = [posofcp_0, posofcp_1, posofcp_2, posofcp_3, posofcp_4, posofcp_5, posofcp_6, posofcp_7, posofcp_8, posofcp_9, posofcp_10]


def xcppos_func(CLd_specific, y):
    alpha: float = abs(m.degrees(alphafromCLd(CLd_specific)))

    # Make sure the alpha is in the correct range
    if alpha > 10:
        raise Exception("CLd out of range. Only values for angle of attack from -10 to 10 work")
    
    # One y index
    idx_1 = abs(yspan_0 - y).argmin()

    # Find out if it is the lower or higher value
    y_1 = yspan_0[idx_1]
    if y_1 < y: # It is the lower bound
        idx_2 = idx_1 + 1
    else: # It is the higher bound
        idx_2 = idx_1 - 1  
    y_2 = yspan_0[idx_2]

    # Finding weight for the alpha
    diff = y - y_1
    weight1 = diff / abs(y_2-y_1)
    weight2 = 1 - weight1

    # Find the lower alpha
    alpha_lower: int = int(alpha)
    alpha_higher: int = alpha_lower + 1


    # Find a middle value for lower angle
    alpha1 = posofcplist[alpha_lower][idx_1]
    alpha2 = posofcplist[alpha_lower][idx_2]

    # Weight the values to get average for 
    avg1 = weight1 * alpha1 + weight2 * alpha2

    # Find a middle value for hogher angle
    alpha1 = posofcplist[alpha_higher][idx_1]
    alpha2 = posofcplist[alpha_higher][idx_2]

    # Weight the values to get average for 
    avg2 = weight1 * alpha1 + weight2 * alpha2

    # Find weight for interpolating across alpha
    weight1 = (alpha - alpha_lower)
    weight2 = 1 - weight1

    return avg1 * weight1 + avg2 * weight2