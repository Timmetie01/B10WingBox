Welcome to the Wingbox Calculations done by Group 10B.
In this repository, all Python tools used in the creation of the report for WP4 is located.

A quick overview of how to use of this program (so NOT an description of every file):

The wingbox class:
A large part of this code has been built around the Wingbox class. Entering a list of points and a list of thicknesses for the skin, and a list of points and a list of areas for the stringers, results in the Wingbox class. 
Multiple different (automated) ways of entering these points are present in data_import.py, such as reading from txt or generating by iteration.
When this class has been created, all properties can be called. For example wingbox.Ixx(y) gives the second moment of area at span-wise location y, wingbox.plot() plots the skin and stringers, wingbox.deflection_plot() plots the deflection of the wingbox as a function of span-wise location

Final Designs:
The final designs were created by taking all failure modes into account and using scipy.optimize.differential_evolution. In weight_optimizer.py this is done. Since this code can run for op to half an hour, the final designs were saved, rounded and put in final_designs.py. Here, any graphs (Such as MOS) of the final design can quickly be made.

Failure Calculations:
Many files (stress_functions, skinbucklingcorrected, deflection_functions, compressive_strength, area_moments, column_buckling) are used in calculating the different failure modes to design for all of them. These files consist of functions called by the optimizer to ensure all requirements are met. Running final_designs.py plots the margins of safety, and for that it uses all the stress and deflection functions mentioned above. They usually take the wingbox class and a span-wise position as input, see the docstrings and comments for more detail.

Graphing:
Many different graphing functions have been created that instantly create graphs for easy visualization. They typically take the wingbox as an argument, and produce the plot using the wingbox properties set above.
Many graphing functions are also incorporated in the wingbox class and can be called by, for example, wingbox.I_plot()

Manoeuvre envelope:
To generate the manoeuvre envelope to obtain worst-case load scenarios, simply run the file loading_diagram.py. It uses airplane specifications from constants.py, and asks the user about the desired configuration and altitude of the aircraft. 

VMT diagrams:
To determine what the worst-case scenarios are, an iterative code was made that runs through all desired scenarios from a .csv file. To individually look at the diagrams, use the generate_loading(case_num, wingbox) function. This code integrates multiple files since a lot of input is required, such as data_from_xflr5 (interpolating xcp coefficients), data_from_envelope (reading specific loading cases), or the wingbox class.
