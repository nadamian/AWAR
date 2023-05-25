import numpy as np
import DataParser as parser
# Column indices of data in int data matrix
BTEAM_INDEX = 1
OUTS_INDEX = 2
VIS_SCORE = 3
HOME_SCORE = 4
# Column indices of data in str data matrix
ON_FIRST = 1
ON_SECOND = 2
ON_THIRD = 3


def expectancy(str_data: np.ndarray, int_data):
    runners_on_probs = runners_on_base(str_data)


def runners_on_base(str_data: np.ndarray):
    """Returns an array with the probability that there is a runner on each base"""
    runners_on = str_data[:, [ON_FIRST, ON_SECOND, ON_THIRD]]
    runners_on[runners_on == '""'] = 0
    runners_on[runners_on != '0'] = 1
    runners_on_float = runners_on.astype(float)
    means = np.mean(runners_on_float, axis=0)
    return means


def scores_from_prob(int_data: np.ndarray):
    evt_data = int_data[:, [2, 12, 13, 14]]


def build_run_ex_matrix(outs_scores: np.ndarray):
    """Matrix Structure:
    0 outs | 1 out | 2 outs
    empty, 1B, 2B, 3B, 1B2B, 1B3B, 2B3B, 1B2B3B"""
    base_matrix = np.zeros((3, 8))
    situation_instances = np.zeros(base_matrix.shape)
    innings = np.split(outs_scores, np.where(outs_scores[:, 0][:-1] != outs_scores[:, 0][1:])[0] + 1)
    for inning in innings:
        matrix, instances = run_ex_inning(inning)
        base_matrix = np.add(base_matrix, matrix)
        situation_instances = np.add(situation_instances, instances)
    return np.divide(base_matrix, situation_instances)


def run_ex_inning(inning: np.ndarray):
    base_matrix = np.zeros((3, 8))
    instances = np.zeros(base_matrix.shape)
    last_score = 0
    for event in inning:
        home_away = int(event[0])
        outs = int(event[1])
        values = (int(event[4]), int(event[5]), int(event[6]))
        new_score = event[2 + home_away]
        base_matrix[np.where(instances != 0)] += (new_score - last_score)
        last_score = new_score
        instances[outs, S_3_element(values)] += 1
    return base_matrix, instances


def S_3_element(values):
    """given the positions of runners on the base paths, returns correct row in the matrix."""
    product = pow(2, values[0]) * pow(3, values[1]) * pow(5, values[2])
    S_3 = np.array([1, 2, 3, 5, 6, 10, 15, 30])
    return np.where(S_3 == product)[0]


def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    """returns an array with batting team, outs, visiting score, home score, runners on first, second, third"""
    runners_on = str_data[:, [ON_FIRST, ON_SECOND, ON_THIRD]]
    runners_on[runners_on == '""'] = 0
    runners_on[runners_on != '0'] = 1
    runners_on_float = runners_on.astype(float)
    outs_scores = int_data[:, [BTEAM_INDEX, OUTS_INDEX, VIS_SCORE, HOME_SCORE]]
    return np.concatenate((outs_scores, runners_on_float), axis=1)


if __name__ == '__main__':
    """STRING_PATH = r'C:\Users\natad\PycharmProjects\AWAR\Data\2022\2022ANASTR.csv'
    INT_PATH = r'C:\Users\natad\PycharmProjects\AWAR\Data\2022\2022ANAINT.csv'
    str_data, int_data = parser.read_file(STRING_PATH, INT_PATH)
    outs_scores = stitch_data(str_data, int_data)"""
    pass
