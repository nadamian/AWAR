import numpy as np
import RunExpectancy
import time
import os

# bevent -y 2022 -f 0,26-74 2022ANA.eva > 2022ANA.csv
# string inputs: 0,26-31,35-36,38-39,41-42,44-45,47-50,53,55,57,66-74
# int inputs: 2,3,4,8,9,32-34,37,40,43,46,51-52,54,56,58-65
# bevent -y 2022 -f 0,26-31,35-36,38-39,41-42,44-45,47-50,53,55,57,66-74 2022ANA.eva > 2022ANASTR.csv
# bevent -y 2022 -f 2,3,4,8,9,32-34,37,40,43,46,51-52,54,56,58-65 2022ANA.eva > 2022ANAINT.csv
INT_PATH = r'C:\Users\natad\PycharmProjects\AWAR\Data\2022\2022INT.csv'
STR_PATH = r'C:\Users\natad\PycharmProjects\AWAR\Data\2022\2022STR.csv'


def read_file(path_str: str, path_int: str):
    str_data = np.genfromtxt(path_str, delimiter=',', dtype=str)
    int_data = np.genfromtxt(path_int, delimiter=',', dtype=int)
    return str_data, int_data


if __name__ == '__main__':
    t = time.time()
    str_data, int_data = read_file(STR_PATH, INT_PATH)
    outs_scores = RunExpectancy.stitch_data(str_data, int_data)
    matrix = RunExpectancy.build_run_ex_matrix(outs_scores)
    np.savetxt(os.path.join(os.getcwd(), "RunMatrix.csv"), matrix)
    endtime = time.time()-t
    print("Runtime: " + str(endtime))
