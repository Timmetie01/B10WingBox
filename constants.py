import math as m

const = {
    #General specs
    'mtom': 12314.28,
    'MTOM': 12314.28,
    'eom': 6763.18,
    'EOM': 6763.18,
    'TW': 0.4779,

    #Planform specs
    'span': 17.59150919,
    'AR': 8.6,
    'Sw': 35.98385994,
    'wing_area': 35.98385994,
    'le_sweep': 26.8227774 * m.pi / 180,
    'cr': 3.108170068,
    'root_chord': 3.108170068,
    'ct': 0.98287858,
    'tip_chord': 0.98287858,
    'taper': 0.316224196,
    'taper_ratio': 0.316224196,
    'MAC': 2.229538428,
    'mean_aerodynamic_chord': 2.229538428,
    'Cl_cruise': 0.580201347,
    'Cl_Cd_cruise': 13.305,
    'Cl_alpha': 5.537,
    'flap_start_pos': 1.050,
    'flap_end_pos': 4.423,

    #Fuselage specs
    'fus_length': 15.85,
    'nose_length': 3,
    'tailcone_length': 6.234,
    'fus_diameter': 2.078,

    #Landing Gear specs
    'ground_to_fuselage_height':0.9795,
    'main_lg_wheel_diameter': 0.5588,
    'main_lg_width': 0.17145,
    'nose_lg_diameter': 0.5588,
    'nose_lg_width': 0.17145, 


}


#sweep angle (IN RADIANS) at fraction of chord. 0.25 => quarter chord
#input x = fraction of chord
#output is integer of sweep (in radians!!)
def sweep(x, le_sweep=const['le_sweep'], span=const['span'], taper=const['taper'], cr=const['cr']):
    if x < 0 or x > 1:
        print(f'Can not compute sweep. x={x}, it should be 0 =< x =< 1.')
        quit()
    
    #Formula obtained from ADSEE project
    return m.atan(m.tan(le_sweep) - x * 2 * cr / span * (1-taper))

#calculate the chord length at a certain span location y
def chord(y, cr=const['cr'], taper=const['taper'], span=const['span']):
    if abs(y) > span:
        print(f'entering a location of y={y}, but its absolute value can only be as large as the span of b={span}.')
        quit()

    #Just the standard formula for a trapezedoidal wing
    return cr - cr * (1-taper) * abs(y) / (span / 2)