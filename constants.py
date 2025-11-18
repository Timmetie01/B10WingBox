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
    'coefficient_lift_cruise': 0.580201347, # [-]
    'coefficient_lift_to_drag': 13.305, # [-]
    'coefficient_lift_angle_of_attack_slope': 5.537, # [1/rad]
}
def sweep_at_chord_fraction(chord_fraction, leading_edge_sweep = const['leading_edge_sweep'], span = const['span'], taper = const['taper_ratio'], root_chord = const['root_chord']):
    if  chord_fraction < 0 or chord_fraction > 1:
        print(f'Cannot compute sweep. Chord fraction = {chord_fraction}, should be 0 =< chord_fraction =< 1.')
        quit()
    
    # ADSEE formula for sweep at chord fraction
    chord_fraction_sweep = math.atan(math.tan(leading_edge_sweep) - chord_fraction * 2 * root_chord / span * (1-taper)) # [rad]

    return chord_fraction_sweep

def local_chord_at_span(target_span, root_chord = const['root_chord'], taper_ratio = const['taper_ratio'], total_span = const['span']):
    if abs(target_span) > total_span:
        print(f'Target span out of bounds')
        quit()

    # ADSEE formula for trapezoidal planform
    local_chord = root_chord - root_chord * (1-taper_ratio) * abs(target_span) / total_span / 2

    return local_chord