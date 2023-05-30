import numpy as np
import RunExpectancy
import time
import os

BASE_DATA_PATH = os.path.join(os.getcwd(), 'Data', 'Output')


def read_raw_data(path_str: str, path_int: str):
    str_data = np.genfromtxt(path_str, delimiter=',', dtype=str)
    int_data = np.genfromtxt(path_int, delimiter=',', dtype=int)
    return str_data, int_data,

def generate_expectancy_matrix(year: str):
    t = time.time()
    str_path = os.path.join(BASE_DATA_PATH, year+'STR.csv')
    int_path = os.path.join(BASE_DATA_PATH, year+'INT.csv')
    str_data, int_data = read_raw_data(str_path, int_path)
    outs_scores = RunExpectancy.stitch_data(str_data, int_data)
    matrix = RunExpectancy.build_run_ex_matrix(outs_scores)
    np.savetxt(os.path.join(BASE_DATA_PATH, year + 'RunMatrix.csv'), matrix.T)
    endtime = time.time()-t
    print('Runtime: ' + str(endtime))

def load_run_matrix(year: str):
    path = os.path.join(BASE_DATA_PATH, year+'RunMatrix.csv')
    matrix = np.genfromtxt(path, delimiter=',', dtype=float)
    return matrix.T

if __name__ == '__main__':
    generate_expectancy_matrix('2019')
