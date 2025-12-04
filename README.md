Welcome to the Wingbox Calculations done by Group 10B.
In this repository, all Python tools used in the creation of the report for WP4 is located.

A quick overview of how to use of this program (so NOT an description of every file):

The wingbox class:
A large part of this code has been built around the Wingbox class. Entering a list of points and a list of thicknesses for the skin, and a list of points and a list of areas for the stringers, results in the Wingbox class. 
Multiple different (automated) ways of entering these points are present in data_import.py, such as reading from txt or generating by iteration.
When this class has been created, all properties can be called. For example wingbox.Ixx(y) gives the second moment of area at span-wise location y, wingbox.plot() plots the skin and stringers, wingbox.deflection_plot() plots the deflection of the wingbox as a function of span-wise location

Graphing:
Many different graphing functions have been created that instantly create graphs for easy visualization. They typically take the wingbox as an argument, and produce the plot using the wingbox properties set above.
Many graphing functions are also incorporated in the wingbox class and can be called by, for example, wingbox.I_plot()

