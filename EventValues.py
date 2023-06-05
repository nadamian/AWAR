import numpy as np
import os
import Utils
import statistics

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
EVENT_TYPE = 7
# Column indices of data in str data matrix
ON_FIRST = 1
ON_SECOND = 2
ON_THIRD = 3
GAME_END = 31

def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    runners_on = str_data[:, [ON_FIRST, ON_SECOND, ON_THIRD, GAME_END]]
    runners_on_int = Utils.runners_on_binary(runners_on)
    sitch_events = int_data[:, [INNING_NUM_INDEX, BTEAM_INDEX, OUTS_INDEX, EVENT_TYPE, BAT_DEST, FIRST_DEST, SECOND_DEST, THIRD_DEST]]
    return np.concatenate((sitch_events, runners_on_int), axis=1, dtype=int)

def get_event_values(sitch_events: np.ndarray, matrix: np.ndarray):
    event_run_expectancies = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    runners_before = Utils.S_3_list(sitch_events[:, [8, 9, 10]])
    runners_after = runners_before
    runners_after = np.roll(runners_after, -1)
    switch_indices = np.where(np.logical_or(sitch_events[:, 1][:-1] != sitch_events[:, 1][1:], sitch_events[:, 0][:-1] != sitch_events[:, 0][1:]))[0]
    after = sitch_events
    after = np.roll(after, -1, axis=0)
    before = Utils.play_score(sitch_events)
    matrix_vals_before = matrix[before[:, 2], runners_before]
    matrix_vals_after = matrix[after[:, 2], runners_after]
    matrix_vals_after[switch_indices] = 0
    runs_generated = before[:, 4] + matrix_vals_after - matrix_vals_before
    # not filling event_run_expectancies properly
    for i in range(runs_generated.shape[0]):
        if before[i][3] == 8:
            if before[i][2] != after[i][2]:
                before[i][3] = 6
            else:
                before[i][3] = 4
        event_run_expectancies[before[i][3]].append(runs_generated[i])
    means = []
    for i in range(len(event_run_expectancies)):
        if len(event_run_expectancies[i]) > 0:
            means.append(statistics.fmean(event_run_expectancies[i]))
        else:
            means.append(0)
    return np.array(means)
