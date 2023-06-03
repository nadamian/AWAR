import numpy as np

def runners_on_binary(runners_on: np.ndarray):
    runners_on[np.logical_or(runners_on == '', runners_on == 'F')] = 0
    runners_on[runners_on != '0'] = 1
    return runners_on.astype(int)

def S_3_element(values):
    """given the positions of runners on the base paths, returns correct row in the matrix."""
    product = pow(2, values[0]) * pow(3, values[1]) * pow(5, values[2])
    S_3 = np.array([1, 2, 3, 5, 6, 10, 15, 30])
    return np.where(S_3 == product)[0]

def S_3_list(values: np.ndarray):
    products = pow(2, values[:, 0]) * pow(3, values[:, 1]) * pow(5, values[:, 2])
    S_3 = np.array([1, 2, 3, 5, 6, 10, 15, 30])
    inds = []
    for product in products:
        inds.append(np.where(S_3 == product)[0][0])
    return np.array(inds)

def play_score(outs_scores: np.ndarray):
    runner_dests = outs_scores[:, [4, 5, 6 ,7]]
    runner_dests[runner_dests <= 3] = 0
    runner_dests[runner_dests > 3] = 1
    outs_scores[:, 4] = np.sum(runner_dests, axis=1)
    return outs_scores

