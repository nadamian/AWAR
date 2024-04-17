import os
import pytest
import numpy as np
import DataParser as parser
import RunExpectancy
import time

BASE_DATA_PATH = os.path.join(os.path.dirname(os.getcwd()), 'Data', 'Output')
STRING_PATH = os.path.join(BASE_DATA_PATH, '2019STR.csv')
INT_PATH = os.path.join(BASE_DATA_PATH, '2019INT.csv')
str_data, int_data = parser.read_raw_data('2019')
outs_scores = RunExpectancy.stitch_data(str_data, int_data)
test_matrix = np.genfromtxt(BASE_DATA_PATH, '2019RunMatrixTest.csv')


def test_run_matrix():
    matrix = RunExpectancy.build_run_ex_matrix(outs_scores)
    assert np.array_equal(matrix, test_matrix)
