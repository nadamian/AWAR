import numpy as np

def runners_on_binary(runners_on: np.ndarray):
    runners_on[np.logical_or(runners_on == '', runners_on == 'F')] = 0
    runners_on[runners_on != '0'] = 1
    return runners_on.astype(float)
