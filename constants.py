import math


const = {
    # General Specs
    'maximum_take_off_mass': 12314.28, # [kg]
    'empty_operating_mass': 6763.18, # [kg]
    'thrust_to_weight_ratio': 0.4779, # [-]

    # Planform Specs
    'span': 17.59150919, # [-]
    'aspect_ratio': 8.6, # [-]
    'wing_area': 35.98385994, # [m^2]
    'leading_edge_sweep': 26.8227774 * math.pi / 180, # [rad]
    'root_chord': 3.108170068, # [m]
    'tip_chord': 0.98287858, # [m]
    'taper_ratio': 0.316224196, # [-]
    'mean_aerodynamic_chord': 2.229538428, # [m]
    'lift_coefficient_cruise': 0.580201347, # [-]
    'lift_to_drag': 13.305, # [-]
    'lift_coefficient_slope': 5.537, # [1/rad]
    'flap_start_position': 1.050, # [m]
    'flap_end_position': 4.423, # [m]
    'thickness_to_chord': 0.12, # [-]

    #Fuselage specs
    'fuselage_length': 15.85, # [m]
    'nose_length': 3, # [m]
    'tailcone_length': 6.234, # [m]
    'fuselage_diameter': 2.078,# [m]

    #Landing Gear specs
    'ground_to_fuselage_height': 0.9795, # [m]
    'main_landing_gear_wheel_diameter': 0.5588, # [m]
    'main_landing_gear_width': 0.17145, # [m]
    'nose_landing_gear_diameter': 0.5588, # [m]
    'nose_landing_gear_width': 0.17145, # [m]
    'main_landing_gear_mass': 317.833/2, # [kg] (one side)
    'main_landing_gear_y_position': 1.9808, # [m] (from axis of symmetry to main landing gear cg)

    #Material specs
    #https://asm.matweb.com/search/SpecificMaterial.asp?bassnum=MA2024T81
    'Density': 2780, #[kg/m^3]
    'Modulus_of_Elasticity': 72.4e9, # [Pa] (assumed same modulus for tension & compression - only 2% variation in aluminium alloys)
    'Shear_Modulus': 28e9, # [Pa]
    'Yield_stress': 4.5e8, # [Pa]
    'Ultimate_tensile_stress': 4.85e8, # [Pa]
    'Fatigue_stress': 1.25e8, # [Pa]
    'Poisson\'s Ratio': 0.33, # [-]

    #Design constraints
    'max_deflection_fraction': 0.15,
    'max_twist_degrees': 10
    
}

#Returns the sweep angle (always in radians!!) at a certain chord fraction
def sweep_at_chord_fraction(chord_fraction, leading_edge_sweep = const['leading_edge_sweep'], span = const['span'], taper = const['taper_ratio'], root_chord = const['root_chord']):
    if  chord_fraction < 0 or chord_fraction > 1:
        print(f'Cannot compute sweep. Chord fraction = {chord_fraction}, should be 0 =< chord_fraction =< 1.')
        quit()
    
    # ADSEE formula for sweep at chord fraction
    chord_fraction_sweep = math.atan(math.tan(leading_edge_sweep) - chord_fraction * 2 * root_chord / span * (1-taper)) # [rad]

    return chord_fraction_sweep

#Returns the chord length at a certain span location of the wing
def local_chord_at_span(target_span, root_chord = const['root_chord'], taper_ratio = const['taper_ratio'], total_span = const['span']):
    if abs(target_span - 1e-6) > total_span / 2:
        print(f'Target span out of bounds')
        quit()

    # ADSEE formula for trapezoidal planform
    local_chord = root_chord - root_chord * (1-taper_ratio) * abs(target_span) / (total_span / 2)

    return local_chord

# ISA values calculator to an altitude of 20000m by Adam
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
