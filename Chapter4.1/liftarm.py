from NVMdiagrams import posofcp_0
from NVMdiagrams import posofcp_10
from NVMdiagrams import yspan_0
from NVMdiagrams import yspan_10
import matplotlib.pyplot as plt


#Find avg cp position at AOA 0            
def cp_avg(posofcp_0):
    cp_total = 0
    points = 0

    for i in range(len(posofcp_0)):
        cp_total = cp_total + posofcp_0[i]
        points = points + 1

    return cp_total / points


average = cp_avg(posofcp_0)
print("Avg CP at 0 AOA:",average)


#FInd avg cp position at AOA 10            
            
def cp_avg(posofcp_10):
    cp_total = 0
    points = 0

    for i in range(len(posofcp_10)):
        cp_total = cp_total + posofcp_10[i]
        points = points + 1

    return cp_total / points


average = cp_avg(posofcp_10)
print("Avg CP at 10 AOA:",average)

#function of y which describes the distance of the shear center from the center of pressure
def cp_sc_dist(yspan_0,posofcp_0):
    sc = 0 #shear center pos
    y_values = []
    dist_values = []

    for i in range(len(posofcp_0)):
        distance = sc + posofcp_0[i]
        y = yspan_0[i]
        y_values.append(y)
        dist_values.append(distance)

    return y_values, dist_values

y0, dist0 = cp_sc_dist(yspan_0, posofcp_0)

# plt.plot(y, dist)
# plt.title("AOA 0")
# plt.xlabel("y")
# plt.ylabel("cp - sc distance")
# plt.show()

def cp_sc_dist(yspan_10,posofcp_10):
    sc = 0
    y_values = []
    dist_values = []

    for i in range(len(posofcp_10)):
        distance = sc + posofcp_10[i]
        y = yspan_10[i]
        y_values.append(y)
        dist_values.append(distance)

    return y_values, dist_values

y10, dist10 = cp_sc_dist(yspan_10, posofcp_10)

plt.plot(y0, dist0, y10, dist10)
plt.title("Lift Arm")
plt.xlabel("Spanwise position")
plt.ylabel("CP to SC distance")
plt.legend(("alpha = 0", "alpha = 10"))
plt.show()