import numpy as np

# Load table
data = np.genfromtxt(r"manoeuvre_envelope\loading_data.csv", delimiter=",", dtype=None, names=True, encoding="utf-8")

def get_case(case_number: int):
    '''Function that returns the specific values for a given case based on table in Overleaf.
    
    Parameters
    ----------
    case_number: int
        desired number from the table

    Returns
    -------
    row: numpy.void
        basically a numpy dictionary with data for following categories: Case, Description, Indicated_Airspeed, Mass, n, Altitude
    
    
    '''
    # Generate the case code (based on Adam's overleaf table)
    case = f"LC-{case_number}"

    # Find the associated index
    idx = np.where(data["Case"] == case)[0]

    # Error proofing
    if len(idx) == 0:
        print(f"{case} not found.")
        return

    # Get the associated data
    row: np.void = data[idx][0]
    
    return row

# Testing:
# num = int(input("Enter case number (1–30): "))
# print(get_case(num))