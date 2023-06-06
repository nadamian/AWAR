import numpy as np
import os
import Utils

BASE_DATA_PATH = os.path.join(os.getcwd(), 'Data', 'Output')
BATTER_ID_INDEX = 1
EVENT_TYPE_INDEX = 7
INNING_NUM_INDEX = 0
ON_FIRST = 1
ON_SECOND = 2
ON_THIRD = 3
BAT_EVENTS = [2, 3, 14, 16, 17, 19, 20, 21, 22, 23]
RUN_EVENTS = [4, 6, 8, 9, 10]
def get_league_stats(str_data: np.ndarray, int_data: np.ndarray, weights: np.ndarray):
    """
    we need to determine the batter for each plate appearence and split when that batter changes, charging them with each
    PA ending event except IBB, simultaneously count up all events league wide then both for players and league divide total
    run contribution by number of plate appearences
    vars needed: player id, inning (to see if player appearing twice in a row is b/c of SB or smth or b/c of new game, event
    ID
    """



def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    ids = str_data[:, [BATTER_ID_INDEX, ON_FIRST, ON_SECOND, ON_THIRD]]
    inning_events = int_data[:, [INNING_NUM_INDEX, EVENT_TYPE_INDEX]]
    return ids, inning_events

