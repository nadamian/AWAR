import numpy as np
import os
import Utils

BASE_DATA_PATH = os.path.join(os.getcwd(), 'Data', 'Output')
# Int data indices
EVENT_TYPE_INDEX = 7
INNING_NUM_INDEX = 0
BTEAM_INDEX = 1
# STR data indices
GAME_ID_INDEX = 0
BATTER_ID_INDEX = 2
ON_FIRST = 3
ON_SECOND = 4
ON_THIRD = 5
BAT_EVENTS = np.array([2, 3, 14, 16, 17, 19, 20, 21, 22, 23])
RUN_EVENTS = np.array([4, 6, 8, 9, 10])
def get_batter_stats(str_data: np.ndarray, int_data: np.ndarray, weights: np.ndarray, park_factors: np.ndarray):
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
    team_percentages, teams = team_time(away_home, bteam, hitters_list)
    return np.dstack((hitters_list, player_wraa))[0], team_percentages, teams


def park_adjust(hitters: np.ndarray, player_wraa: np.ndarray, team_percentages: np.ndarray, teams: np.ndarray,
                park_factors: np.ndarray, team_totals: np.ndarray):
    #TODO finish park adjust method
    for i in range(hitters.shape[0]):
        if team_percentages[i][0] is not np.nan:
            teams = np.where(team_percentages[i] != 0)
            factors = park_factors[teams]
            pass


def team_time(away_home:np.ndarray, bteam: np.ndarray, hitter_list: np.ndarray):
    """Determines percentage of a player's plate appearances taken for each team"""
    teams = away_home[:, 0]
    uteams = []
    for team in teams:
        uteams.append(team[:3])
    teamsnp = np.array(uteams)
    uteamsnp = np.unique(teamsnp)
    team_percentages = np.zeros(shape=(hitter_list.shape[0], uteamsnp.shape[0]))
    for i in range(hitter_list.shape[0]):
        player = hitter_list[i]
        home_appearances = np.where(np.logical_and(away_home[:, 1] == player, bteam == 1))
        home_teams = teamsnp[home_appearances]
        h_teams = np.unique(home_teams)
        for team in h_teams:
            x_index = np.where(uteamsnp == team)[0]
            team_percentages[i][x_index] = np.count_nonzero(team == home_teams)
    team_totals = np.sum(team_percentages, axis=1)
    team_percentages /= team_totals[:, None]
    return team_percentages, uteamsnp


def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    ids = str_data[:, [BATTER_ID_INDEX, ON_FIRST, ON_SECOND, ON_THIRD]]
    inning_events = int_data[:, [INNING_NUM_INDEX, EVENT_TYPE_INDEX]]
    away_home = str_data[:, [GAME_ID_INDEX, BATTER_ID_INDEX]]
    bteam = int_data[:, BTEAM_INDEX]
    return ids, inning_events, away_home, bteam
