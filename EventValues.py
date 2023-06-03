import numpy as np
import os
import Utils

# Column indices of data in int data matrix
OUTS_INDEX = 2
VIS_SCORE = 3
HOME_SCORE = 4
BAT_DEST = 16
FIRST_DEST = 17
SECOND_DEST = 18
THIRD_DEST = 19
EVENT_TYPE = 7
# Column indices of data in str data matrix
ON_FIRST = 1
ON_SECOND = 2
ON_THIRD = 3
GAME_END = 31

def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    runners_on = str_data[:, [ON_FIRST, ON_SECOND, ON_THIRD, GAME_END]]
    runners_on_int = Utils.runners_on_binary(runners_on)
    sitch_events = int_data[:, [OUTS_INDEX, VIS_SCORE, HOME_SCORE, EVENT_TYPE, BAT_DEST, FIRST_DEST, SECOND_DEST, THIRD_DEST]]
    return np.concatenate((sitch_events, runners_on_int), axis=1, dtype=int)

def get_event_values(sitch_events: np.ndarray, matrix: np.ndarray):
    event_run_expectancies = np.ndarray((sitch_events.shape[0], 23))
    runners_before = Utils.S_3_list(sitch_events[:, [8, 9, 10]])
    runners_after = runners_before
    runners_after = np.roll(runners_after, -1)
    after = sitch_events
    after = np.roll(after, -1, axis=0)
    before = Utils.play_score(sitch_events)
    runs_generated = before[:, 4] + matrix[after[:, 0], runners_after] - matrix[before[:, 0], runners_before]
    runs_generated[-1] = np.nan
    # not filling event_run_expectancies properly 
    event_run_expectancies = np.append(event_run_expectancies[:, before[3]-1], runs_generated[:])
    means = np.mean(event_run_expectancies, axis=1)
    return np.mean(event_run_expectancies, axis=1)
