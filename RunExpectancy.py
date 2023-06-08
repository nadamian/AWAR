import numpy as np
import os
import Utils

# Column indices of data in int data matrix
INNING_NUM_INDEX = 0
BTEAM_INDEX = 1
OUTS_INDEX = 2
VIS_SCORE = 3
HOME_SCORE = 4
BAT_DEST = 16
FIRST_DEST = 17
SECOND_DEST = 18
THIRD_DEST = 19
# Column indices of data in str data matrix
ON_FIRST = 2
ON_SECOND = 3
ON_THIRD = 4
GAME_END = 32
BASE_DATA_PATH = os.path.join(os.getcwd(), 'Data', 'Output')

"""Run expectancy matrix and helper methods"""
def build_run_ex_matrix(outs_scores: np.ndarray):
    """Matrix Structure:
    0 outs | 1 out | 2 outs
    empty, 1B, 2B, 3B, 1B2B, 1B3B, 2B3B, 1B2B3B"""
    base_matrix = np.zeros((3, 8))
    situation_instances = np.zeros(base_matrix.shape)
    """score_on_play = np.roll(outs_scores[:, 3], -1) - outs_scores[:, 3]
    score_on_play[np.where(score_on_play < 0)] = 0
    outs_scores[:, 3] = score_on_play"""
    outs_scores = Utils.play_score(outs_scores)
    split_indices = np.where(np.logical_or(outs_scores[:, 1][:-1] != outs_scores[:, 1][1:], outs_scores[:, 0][:-1] != outs_scores[:, 0][1:]))[0] + 1
    innings = np.split(outs_scores, split_indices)
    scores = get_game_scores()
    game_index = 0
    for inning in innings:
        if (np.isin(1, inning[:, 11]) or inning[0, 0] >= 9) and (int(inning[0, 1]) == 1): # alt: check_walk_off(games_final, inning, game_index)
            continue
        """if np.isin(1, inning[:, 11]):
            if scores[game_index] != inning[inning.shape[0]-1, 3]:
                game_index += 1
                continue
            game_index +=1"""
        matrix, instances= run_ex_inning(inning)
        base_matrix = np.add(base_matrix, matrix)
        situation_instances = np.add(situation_instances, instances)
        print("inning done")
    return np.divide(base_matrix, situation_instances)


def run_ex_inning(inning: np.ndarray):
    base_matrix = np.zeros((3, 8))
    instances = np.zeros(base_matrix.shape)
    for event in inning:
        outs = int(event[2])
        values = (int(event[8]), int(event[9]), int(event[10]))
        occupied_bases = Utils.S_3_element(values)
        instances[outs, occupied_bases] += 1
        # Event[3] or event[4] depending on scoring style
        base_matrix += event[4] * instances
    return base_matrix, instances


def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    """returns an array with inning, batting team, outs, total score, runners on first, second, third, game end flag
    also returns an indexed array of gameIDs for comparison"""
    runners_on = str_data[:, [ON_FIRST, ON_SECOND, ON_THIRD, GAME_END]]
    runners_on_float = Utils.runners_on_binary(runners_on)
    int_data[:, VIS_SCORE] += int_data[:, HOME_SCORE]
    outs_scores = int_data[:, [INNING_NUM_INDEX, BTEAM_INDEX, OUTS_INDEX, VIS_SCORE, BAT_DEST, FIRST_DEST, SECOND_DEST, THIRD_DEST]]
    return np.concatenate((outs_scores, runners_on_float), axis=1)


def get_game_scores():
    games = np.genfromtxt(os.path.join(BASE_DATA_PATH, '2019GAME.csv'), delimiter=',', dtype=int)
    scores = games[:, 1] + games[:, 2]
    return scores

if __name__ == '__main__':
    pass
