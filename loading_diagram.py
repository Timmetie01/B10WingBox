#We will try to make the loading diagram here, hopefully should be fun!!!!!
import math
import constants
import matplotlib.pyplot as plt

#ISA calculation, can be used for density, temperature, etc.
def ISA(alt):
    g_0 = 9.80665
    R = 287
    T_0 = 288.15
    p_0 = 101325
    a = -0.0065

    alt1 = min(11000, alt)

    t_1 = T_0 + a*(alt1)

    p_1 = p_0*((t_1/T_0)**((-g_0)/(a*R)))

    rho = p_1/(t_1*R)

    if alt <= 11000:
        return t_1, p_1, rho
    
    alt1 = min(20000,alt)

    p_1 = p_1*math.exp((-g_0/(R*t_1))*(alt1-11000))

    rho = p_1/(t_1*R)

    return t_1, p_1, rho

# Constants, pulls from constants.py
LD_OEW = constants.const["eom"]
LD_MTOW = constants.const["mtom"]
LD_W3 = constants.const["eom"] + 1010
S = 35.98385994
v_c = 200.687769

#DO NOT QUESTION THESE VALUES
Clmax_noflaps = 2.0236*0.8
Clmax_flaps_landing = 2.1
Clmax_flaps_takeoff = 2.0236*0.8+0.2

#Function that calculates the stall speed, duh
def stallspeed(W, Clmax):
    v_s = math.sqrt(2*W/(Clmax*S*1.225))
    return v_s

#Maximum speed at which flaps can be deployed
v_f = max(1.6*stallspeed(LD_MTOW, Clmax_flaps_takeoff), 1.8*stallspeed(LD_MTOW, Clmax_flaps_landing))

#Function to calculate the maximum load factor
def n_max(W):
    n_max = max(2.1 + 24000/(W*1/0.454+10000), 2.1)
    if n_max > 3.8:
        return 3.8
    return n_max

#Function to calculate the dive speed, which is basically the maximum speed
def v_d(v_c, alt):

    v_d = v_c*1/0.8
    a = math.sqrt(1.4*287*ISA(alt)[0])

    if (v_d*math.sqrt(1.225/ISA(alt)[2]))/a > 0.75:
        return a*0.75*math.sqrt(ISA(alt)[2]/1.225)
    else:
        return v_d

#Drawing of the diagram, ask the user for what kind of situation the graph is used
print("Type 1 for OEW, type 2 for MTOW, type 3 for OEW + Payload")
choice = input("Enter your choice:")
altitude = int(input("Input the altitude in meters, max 20k:"))

if choice == "1":
    W = LD_MTOW
elif choice == "2":
    W = LD_MTOW
elif choice == "3":
    W = LD_W3
else:
    print("Are you stupid?")
    exit()

v_c = v_c * math.sqrt(ISA(altitude)[2]/1.225)
vtab = []
ntab = []

v_s1 = stallspeed(W, Clmax_noflaps)
n_maximum = n_max(W)
dv = 0.1
dn = 0.001
v = 0
n = 0

#Go up to N_max
while n < n_maximum:
    ntab.append(n)
    vtab.append(v)
    v = v + dv
    n = (v/v_s1)**2
    if n - 2 <= 0.001:
        special_v = v

# Go Down to 0
while v > 0:
    ntab.append(n)
    vtab.append(v)
    v = v - dv
    n = (v/v_s1)**2

#Go Up to N_max with flaps
n = 0
v = 0
v_s0 = stallspeed(W, Clmax_flaps_landing)
while n < 2:
    ntab.append(n)
    vtab.append(v)
    v = v + dv
    n = (v/v_s0)**2

#Go straight until it hits the line or hits a limiting speed
while v < special_v and v < v_f:
    ntab.append(2)
    vtab.append(v)
    v = v + dv

# Go up to N_max
while n < n_maximum:
    ntab.append(n)
    vtab.append(v)
    v = v + dv
    n = (v/v_s1)**2

#Go straight until it gets to dive speed
v_dive = v_d(v_c, altitude)

while v < v_dive:
    ntab.append(n_maximum)
    vtab.append(v)
    v = v + dv

#Go Down
n = n_maximum

while n > 0:
    vtab.append(v)
    ntab.append(n)
    n = n - dn

#Go down linearly to minimum loading factor
slope = -1/(v_dive-v_c)

while v > v_c:
    v = v - dv*0.01
    n = n + slope*dn
    vtab.append(v)
    ntab.append(n)

#Go horizontally back to stall speed
while v > v_s1:
    v = v - dv
    vtab.append(v)
    ntab.append(-1)

#Go back up to 0
while v > 0:
    v = v - dv
    n = -(v/v_s1)**2
    vtab.append(v)
    ntab.append(n)

print("The maximum loading factor is ", n_maximum)

plt.figure()
plt.plot(vtab, ntab)
plt.show()