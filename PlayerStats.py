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
    """Returns each batter's season wRAA"""
    ids, events, away_home, bteam = stitch_data(str_data, int_data)

    # Takes only weights for bat events
    bat_weights = weights[BAT_EVENTS]

    # Gets a unique list of every batter in the league. Pitcher hitting should be filtered out before this step
    hitters_list = np.unique(ids[:, 0])
    player_stats = np.zeros(shape=(hitters_list.shape[0], BAT_EVENTS.shape[0]))

    # Classifies each event and assigns it to a batter
    for i in range(ids.shape[0]):
        # Checks that the event is the batters doing and not, for example, a stolen base or an intentional walk
        if np.isin(events[i][1], BAT_EVENTS):
            player_id = ids[i][0]
            player_stats[np.where(hitters_list == player_id)[0], np.where(BAT_EVENTS == events[i][1])] += 1

    # Gets the total number of batter events for the season
    league_events = np.sum(player_stats)

    # Gets the sum of
    league_stats = np.sum(player_stats, axis=0)

    # dot product of event weights vector with batter events matrix to get batter total run contribution
    league_runs = np.dot(league_stats, bat_weights)
    league_pprc = league_runs / league_events  # PPRC = per plate appearance run creation

    # Plate appearances and run creation for individual players
    player_pa = np.sum(player_stats, axis=1)
    player_rc = np.dot(player_stats, bat_weights)

    # Computes wRAA for individual player
    player_wraa = player_rc - league_pprc * player_pa

    team_percentages, teams, team_time_totals = team_time(away_home, bteam, hitters_list)
    batting_runs = park_adjust(hitters_list, player_wraa, team_percentages, park_factors, team_time_totals, league_pprc)
    return np.dstack((hitters_list, batting_runs))[0]


def park_adjust(hitters: np.ndarray, player_wraa: np.ndarray, team_percentages: np.ndarray,
                park_factors: np.ndarray, team_time_totals: np.ndarray, league_pprc: float):
    """Park adjusts batter runs"""
    batting_runs = np.ndarray(player_wraa.shape)
    for i in range(hitters.shape[0]):
        if team_percentages[i][0] is not np.nan:
            # Setup all variables
            teams = np.where(team_percentages[i] != 0)  # Gets teams the player hit for in home games
            factors = park_factors[teams] / 100  # Gets the park factors for those home parks
            percentages = team_percentages[i][teams]  # Percentage of player's PA taken for each team
            totals_home_pa = np.sum(team_time_totals[i][teams])
            wraa = player_wraa[i]
            percentage_factors = np.dot(factors, percentages)

            # Computes batting runs, not including league adjustment b/c I plan to compute these separately by league
            # down the line
            adjustment = (league_pprc - percentage_factors * league_pprc) * totals_home_pa
            batting_runs[i] = wraa + adjustment
    return batting_runs


def team_time(away_home:np.ndarray, bteam: np.ndarray, hitter_list: np.ndarray):
    """Determines percentage of a player's plate appearances taken for each team, additionally returns
    unique list of each team for the season and each player's total number of plate appearances taken for each team"""
    # Makes a list of active teams in given season
    teams = away_home[:, 0]
    uteams = []
    for team in teams:
        uteams.append(team[:3])
    teamsnp = np.array(uteams)
    uteamsnp = np.unique(teamsnp)

    # For each player determines number of plate appearances taken in home games for each team
    team_percentages = np.zeros(shape=(hitter_list.shape[0], uteamsnp.shape[0]))
    for i in range(hitter_list.shape[0]):
        player = hitter_list[i]
        home_appearances = np.where(np.logical_and(away_home[:, 1] == player, bteam == 1))
        home_teams = teamsnp[home_appearances]
        h_teams = np.unique(home_teams)
        for team in h_teams:
            x_index = np.where(uteamsnp == team)[0]
            team_percentages[i][x_index] = np.count_nonzero(team == home_teams)
    team_percentages[np.where(np.isnan(team_percentages))] = 0
    team_totals = np.sum(team_percentages, axis=1)
    team_time_totals = team_percentages
    team_totals[np.where(team_totals == 0)] = 1
    team_percentages /= team_totals[:, None]
    team_percentages[np.where(np.isnan(team_percentages))] = 0
    w = np.where(np.isnan(team_percentages))
    return team_percentages, uteamsnp, team_time_totals


def stitch_data(str_data: np.ndarray, int_data: np.ndarray):
    """Returns four arrays, ids of batter and runners, bat events and inning number, game ids and batter ids, and
    binary away/home batting team"""
    ids = str_data[:, [BATTER_ID_INDEX, ON_FIRST, ON_SECOND, ON_THIRD]]
    inning_events = int_data[:, [INNING_NUM_INDEX, EVENT_TYPE_INDEX]]
    away_home = str_data[:, [GAME_ID_INDEX, BATTER_ID_INDEX]]
    bteam = int_data[:, BTEAM_INDEX]
    return ids, inning_events, away_home, bteam
