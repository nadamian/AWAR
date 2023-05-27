import numpy as np
import DataParser as parser
# Column indices of data in int data matrix
INNING_NUM_INDEX = 0
BTEAM_INDEX = 1
OUTS_INDEX = 2
VIS_SCORE = 3
HOME_SCORE = 4
RBI_INDEX = 10
# Column indices of data in str data matrix
ON_FIRST = 1
ON_SECOND = 2
ON_THIRD = 3
GAME_END = 31

# TODO need final scores from BGAME : (
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


def build_run_ex_matrix(outs_scores: np.ndarray, games_final: np.ndarray, ids):
    """Matrix Structure:
    0 outs | 1 out | 2 outs
    empty, 1B, 2B, 3B, 1B2B, 1B3B, 2B3B, 1B2B3B"""
    base_matrix = np.zeros((3, 8))
    situation_instances = np.zeros(base_matrix.shape)
    split_indices = np.where(np.logical_or(outs_scores[:, 1][:-1] != outs_scores[:, 1][1:], outs_scores[:, 0][:-1] != outs_scores[:, 0][1:]))[0] + 1
    innings = np.split(outs_scores, split_indices)
    index = 0
    for inning in innings:
        matrix, instances, new_ind = run_ex_inning(inning, games_final, ids, index)
        base_matrix = np.add(base_matrix, matrix)
        situation_instances = np.add(situation_instances, instances)
        index = new_ind
        print("inning done")
    return np.divide(base_matrix, situation_instances)


def run_ex_inning(inning: np.ndarray, games_final: np.ndarray, ids: np.ndarray, index: int):
    base_matrix = np.zeros((3, 8))
    instances = np.zeros(base_matrix.shape)
    last_score = 0
    for event in inning:
        home_away = int(event[1])
        outs = int(event[2])
        values = (int(event[5]), int(event[6]), int(event[7]))
        new_score = event[3 + home_away]
        base_matrix += (new_score - last_score) * instances
        occupied_bases = S_3_element(values)
        instances[outs, occupied_bases] += 1
        last_score = new_score
        if event[8] == 1:
            if event[3] == event[4]:
                print('penis')
            game_id = ids[index]
            final_index = np.where(games_final[:, 0] == game_id)[0][0]
            final_score = int(games_final[final_index, 1 + home_away])
            base_matrix += (final_score - last_score) * instances
        index += 1
    return base_matrix, instances, index


def S_3_element(values):
    """given the positions of runners on the base paths, returns correct row in the matrix."""
    product = pow(2, values[0]) * pow(3, values[1]) * pow(5, values[2])
    S_3 = np.array([1, 2, 3, 5, 6, 10, 15, 30])
    return np.where(S_3 == product)[0]


def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    """returns an array with inning, batting team, outs, visiting score, home score, runners on first, second, third, game end flag
    also returns an indexed array of gameIDs for comparison"""
    runners_on = str_data[:, [ON_FIRST, ON_SECOND, ON_THIRD, GAME_END]]
    runners_on[np.logical_or(runners_on == '', runners_on == 'F')] = 0
    runners_on[runners_on != '0'] = 1
    runners_on_float = runners_on.astype(float)
    outs_scores = int_data[:, [INNING_NUM_INDEX, BTEAM_INDEX, OUTS_INDEX, VIS_SCORE, HOME_SCORE]]
    return np.concatenate((outs_scores, runners_on_float), axis=1), str_data[:, 0]

if __name__ == '__main__':
    pass
