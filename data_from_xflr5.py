import numpy as np
import math as m

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

# AOA = 11deg
table11alpha = np.genfromtxt(r"xflr5data\MainWing_a=11.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_11 = table11alpha[:,10]

# AOA = 12deg
table12alpha = np.genfromtxt(r"xflr5data\MainWing_a=12.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_12 = table12alpha[:,10]

# AOA = 13deg
table13alpha = np.genfromtxt(r"xflr5data\MainWing_a=13.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_13 = table13alpha[:,10]

# AOA = 14deg
table14alpha = np.genfromtxt(r"xflr5data\MainWing_a=14.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_14 = table14alpha[:,10]

# AOA = 15deg
table15alpha = np.genfromtxt(r"xflr5data\MainWing_a=15.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_15 = table15alpha[:,10]

# AOA = 16deg
table16alpha = np.genfromtxt(r"xflr5data\MainWing_a=16.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_16 = table16alpha[:,10]

# AOA = 17deg
table17alpha = np.genfromtxt(r"xflr5data\MainWing_a=17.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_17 = table17alpha[:,10]

# AOA = 18deg
table18alpha = np.genfromtxt(r"xflr5data\MainWing_a=18.00_v=10.00ms.csv", delimiter=",", skip_header=21)
posofcp_18 = table18alpha[:,10]

posofcplist = [posofcp_0, posofcp_1, posofcp_2, posofcp_3, posofcp_4, posofcp_5, posofcp_6, posofcp_7, posofcp_8, posofcp_9, 
               posofcp_10, posofcp_11, posofcp_12, posofcp_13, posofcp_14, posofcp_15, posofcp_16, posofcp_17, posofcp_18]


def xcppos_func(CLd_specific):
    from NVMdiagrams import alphafromCLd

    def xcp_officialpos(y):
        alpha: float = abs(m.degrees(alphafromCLd(CLd_specific)))

        # Make sure the alpha is in the correct range
        if alpha > 18:
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
    return xcp_officialpos
