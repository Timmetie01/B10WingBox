#We will try to make the loading diagram here, hopefully should be fun!!!!!
import math
import constants
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

LD_OEW = constants.const["eom"]
LD_MTOW = constants.const["mtow"]
LD_W3 = constants.const["eom"] + 1010
