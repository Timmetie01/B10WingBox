import numpy as np

'''Code that takes accesses the data for worst case loadings'''


span = 17.5746 # As given by XFLR panel distribution (pls don't change, it breaks interpolation in data_from_xflr5)
ypoints = np.linspace(0.0, span/2.0 ,100)

# made with ChatGPT to improve efficiency (saves the data in a temporary memory so that it doesn;t have to load the file every time the functino is called)
_cache = {}

def load_case(file_name):
    if file_name not in _cache:
        _cache[file_name] = np.load(f"worst_cases/{file_name}.npz")
    return _cache[file_name]

def V(y, file_name):
    data = load_case(file_name)
    shear = data["shear"]
    return np.interp(y, ypoints, shear)

def M(y, file_name):
    data = load_case(file_name)
    bending = data["bending"]
    return np.interp(y, ypoints, bending)


def T(y, file_name):
    data = load_case(file_name)
    torsion = data["torsion"]
    return np.interp(y, ypoints, torsion)


# print(V(0, 'abs_max_shear'))
# print(M(0, 'abs_max_bending'))
#print(T(0, 'abs_max_torsion'))
# print(V(0, 'abs_min_shear'))
# print(M(0, 'abs_min_bending'))
# print(T(0, 'abs_min_torsion'))

# Code for printing worst case scenario loading case:
if __name__ == '__main__': # runs only if this file is run as main
    for filename in ['abs_max_shear', 'abs_max_bending', 'abs_max_torsion', 'abs_min_shear', 'abs_min_bending', 'abs_min_torsion']:
        data = np.load(f"worst_cases/{filename}.npz")
        print(f'For {filename}, the worst case scenario is LC-{data["case_number"]}.')