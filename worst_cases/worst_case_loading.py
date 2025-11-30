import numpy as np



span = 17.5746 # As given by XFLR panel distribution (pls don't change, it breaks interpolation in data_from_xflr5)
ypoints = np.linspace(0.0, span/2.0 ,100)

# ChatGPT code that improves efficiency
# CACHE DICTIONARY
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


# My code
# def V(y, file_name):
#     data = np.load(f"worst_cases/{file_name}.npz")
#     shear = data["shear"]

#     return np.interp(y, ypoints, shear)

# def M(y, file_name):
#     data = np.load(f"worst_cases/{file_name}.npz")
#     bending = data["bending"]

#     return np.interp(y, ypoints, bending)

# def T(y, file_name):
#     data = np.load(f"worst_cases/{file_name}.npz")
#     torsion = data["torsion"]

#     return np.interp(y, ypoints, torsion)

# print(V(0, 'abs_max_shear'))
# print(M(0, 'abs_max_bending'))
# print(T(0, 'abs_max_torsion'))
# print(V(0, 'abs_min_shear'))
# print(M(0, 'abs_min_bending'))
# print(T(0, 'abs_min_torsion'))