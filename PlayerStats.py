import numpy as np
import os
import Utils

BASE_DATA_PATH = os.path.join(os.getcwd(), 'Data', 'Output')
# Int data indices
EVENT_TYPE_INDEX = 7
INNING_NUM_INDEX = 0
BTEAM_INDEX = 1
# STR data indices
VISIT_TEAM_INDEX = 1
HOME_TEAM_INDEX = 2
BATTER_ID_INDEX = 3
ON_FIRST = 4
ON_SECOND = 5
ON_THIRD = 6
BAT_EVENTS = np.array([2, 3, 14, 16, 17, 19, 20, 21, 22, 23])
RUN_EVENTS = np.array([4, 6, 8, 9, 10])
def get_batter_stats(str_data: np.ndarray, int_data: np.ndarray, weights: np.ndarray):
    """
    we need to determine the batter for each plate appearence and split when that batter changes, charging them with each
    PA ending event except IBB, simultaneously count up all events league wide then both for players and league divide total
    run contribution by number of plate appearences
    vars needed: player id, inning (to see if player appearing twice in a row is b/c of SB or smth or b/c of new game, event
    ID
    """
    ids, events, away_home, bteam = stitch_data(str_data, int_data)
    hitters_list = np.unique(ids[:, 0])
    player_stats = np.zeros(shape=(hitters_list.shape[0], 25))
    for i in range(ids.shape[0]):
        player_id = ids[i][0]
        player_stats[np.where(hitters_list == player_id)[0], events[i][1]] += 1
    league_events = np.sum(player_stats)
    league_stats = np.sum(player_stats, axis=0)
    league_runs = np.dot(league_stats, weights)
    league_pprc = league_runs / league_events #  PPRC = per plate appearance run creation
    player_pa = np.sum(player_stats, axis=1)
    player_rc = np.dot(player_stats, weights)
    player_wraa = player_rc - league_pprc * player_pa
    return np.dstack((hitters_list, player_wraa))[0]


def team_time(away_home, bteam, hitter_list: np.ndarray):
    """Determines how many games a player played for each team they played for during the season"""
    for id in hitter_list:
        pass

def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    ids = str_data[:, [BATTER_ID_INDEX, ON_FIRST, ON_SECOND, ON_THIRD]]
    inning_events = int_data[:, [INNING_NUM_INDEX, EVENT_TYPE_INDEX]]
    away_home = str_data[:, [VISIT_TEAM_INDEX, HOME_TEAM_INDEX, BATTER_ID_INDEX]]
    bteam = int_data[:, BTEAM_INDEX]
    return ids, inning_events, away_home, bteam
