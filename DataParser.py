import numpy as np
import RunExpectancy
import EventValues
import PlayerStats
import time
import os

BASE_DATA_PATH = os.path.join(os.getcwd(), 'Data', 'Output')


def read_raw_data(year: str):
    str_path = os.path.join(BASE_DATA_PATH, year + 'STR.csv')
    int_path = os.path.join(BASE_DATA_PATH, year + 'INT.csv')
    str_data = np.genfromtxt(str_path, delimiter=',', dtype=str)
    int_data = np.genfromtxt(int_path, delimiter=',', dtype=int)
    return str_data, int_data


def generate_expectancy_matrix(year: str):
    t = time.time()
    str_data, int_data = read_raw_data(year)
    outs_scores = RunExpectancy.stitch_data(str_data, int_data)
    matrix = RunExpectancy.build_run_ex_matrix(outs_scores)
    np.savetxt(os.path.join(BASE_DATA_PATH, year + 'RunMatrix.csv'), matrix.T, delimiter=',')
    endtime = time.time()-t
    print('Runtime: ' + str(endtime))


def generate_event_values(year: str):
    t = time.time()
    str_data, int_data = read_raw_data(year)
    situation_events = EventValues.stitch_data(str_data, int_data)
    matrix = load_run_matrix(year)
    values = EventValues.get_event_values(situation_events, matrix)
    np.savetxt(os.path.join(BASE_DATA_PATH, year + 'EventValues.csv'), values, delimiter=',')
    endtime = time.time() - t
    print('Runtime: ' + str(endtime))


def get_player_batting_runs(year: str):
    t = time.time()
    park_factors = load_park_factors(year)
    str_data, int_data = read_raw_data(year)
    weights = load_linear_weights(year)
    batting_runs = PlayerStats.get_batter_stats(str_data, int_data, weights, park_factors)
    np.savetxt(os.path.join(BASE_DATA_PATH, year + 'BattingRuns.csv'), batting_runs, delimiter=',', fmt='%s')
    endtime = time.time() - t
    print('Runtime: ' + str(endtime))


def load_run_matrix(year: str):
    path = os.path.join(BASE_DATA_PATH, year+'RunMatrix.csv')
    matrix = np.genfromtxt(path, delimiter=',', dtype=float)
    return matrix.T


def load_linear_weights(year: str):
    path = os.path.join(BASE_DATA_PATH, year+'EventValues.csv')
    weights = np.genfromtxt(path, delimiter=',', dtype=float)
    return weights


def load_park_factors(year: str):
    path = os.path.join(BASE_DATA_PATH, year + 'ParkFactors.csv')
    park_factors = np.genfromtxt(path, delimiter=',', dtype=float)
    return park_factors


def load_league_stats(year: str):
    path = os.path.join(BASE_DATA_PATH, year + 'LeagueStats.csv')
    stats = np.genfromtxt(path, delimiter=',', dtype=float)
    return stats


def load_data(year: str, info: str, dtype=float):
    path = os.path.join(BASE_DATA_PATH, year + info + '.csv')
    return np.genfromtxt(path, delimiter=',', dtype=dtype)


if __name__ == '__main__':
    #generate_expectancy_matrix('2019')
    generate_event_values('2019')
    get_player_batting_runs('2019')
