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
ON_FIRST = 3
ON_SECOND = 4
ON_THIRD = 5
GAME_END = 33
BAT_EVENTS = np.array([2, 3, 14, 15, 16, 17, 19, 20, 21, 22, 23])

# TODO add baserunning values for advancing extra bases on different hit types

def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    """returns an array with inning number, batting team, outs, event type, batter and runners on 1st-3rd destinations
    and base occupancy binary."""
    runners_on = str_data[:, [ON_FIRST, ON_SECOND, ON_THIRD, GAME_END]]
    runners_on_int = Utils.runners_on_binary(runners_on)
    sitch_events = int_data[:, [INNING_NUM_INDEX, BTEAM_INDEX, OUTS_INDEX, EVENT_TYPE, BAT_DEST, FIRST_DEST, SECOND_DEST, THIRD_DEST]]
    return np.concatenate((sitch_events, runners_on_int), axis=1, dtype=int)

def get_event_values(sitch_events: np.ndarray, matrix: np.ndarray):
    """Gets value weights for each batting event."""
    event_run_expectancies = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
    # Gets runner state before and after the play
    runners_before = Utils.S_3_list(sitch_events[:, [8, 9, 10]])
    runners_after = runners_before
    runners_after = np.roll(runners_after, -1)

    # Indices where the sides switch or the game ends
    switch_indices = np.where(np.logical_or(sitch_events[:, 1][:-1] != sitch_events[:, 1][1:], sitch_events[:, 0][:-1] != sitch_events[:, 0][1:]))[0]

    # Sets up events for before and after comparison
    after = sitch_events
    after = np.roll(after, -1, axis=0)
    before = Utils.play_score(sitch_events)

    # Gets the run expectancy values from the matrix based on before and after state for each play
    matrix_vals_before = matrix[before[:, 2], runners_before]
    matrix_vals_after = matrix[after[:, 2], runners_after]
    matrix_vals_after[switch_indices] = 0 # Sets after value any time a half inning ends to zero

    # Determines number of runs generated on each play by noting actual runs scored and adding the change in run
    # expectancy following the play
    runs_generated = before[:, 4] + matrix_vals_after - matrix_vals_before

    for i in range(runs_generated.shape[0]):
        # Retrosheet doesn't differentiate between pick-offs that result in an out and those that result in the runner taking
        # the extra base so here we split those into either stolen bases or caught stealing on the runners side.
        # we won't do this when calculating pitcher war as a runner's
        if before[i][3] == 8:
            if before[i][2] != after[i][2]:
                before[i][3] = 6
            else:
                before[i][3] = 4

        # Appends number of runs generated on each play to the index of the corresponding event
        event_run_expectancies[before[i][3]].append(runs_generated[i])
    means = []
    # Iterates through list of events and determines the mean run creation of each event
    for i in range(len(event_run_expectancies)):

        # Ensures an event has occurred at least once in a season
        if len(event_run_expectancies[i]) > 0:
            means.append(statistics.fmean(event_run_expectancies[i]))
        else:
            means.append(0)
    return np.array(means)
