import numpy as np
import RunExpectancy
import time
from argparse import ArgumentParser


# bevent -y 2022 -f 0,26-74 2022ANA.eva > 2022ANA.csv
# string inputs: 0,26-31,35-36,38-39,41-42,44-45,47-50,53,55,57,66-74
# int inputs: 2,3,4,8,9,32-34,37,40,43,46,51-52,54,56,58-65
# bevent -y 2022 -f 0,26-31,35-36,38-39,41-42,44-45,47-50,53,55,57,66-74 2022ANA.eva > 2022ANASTR.csv
# bevent -y 2022 -f 2,3,4,8,9,32-34,37,40,43,46,51-52,54,56,58-65 2022ANA.eva > 2022ANAINT.csv


def read_file(path_str: str, path_int: str):
    str_data = np.genfromtxt(path_str, delimiter=',', dtype=str)
    int_data = np.genfromtxt(path_int, delimiter=',', dtype=int)
    return str_data, int_data


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument('--strcsv', help='path to string data csv', type=str, nargs=1, dest='str_csv_path')
    argparser.add_argument('--intcsv', help='path to int data csv', type=str, nargs=1, dest='int_csv_path')
    args = argparser.parse_args()
    if (args.str_csv_path is None or args.str_csv_path == "") or (args.int_csv_path is None or args.int_csv_path == ""):
        raise ValueError("Must provide paths to both string and int data")
    t = time.time()
    args = argparser.parse_args()
    str_data, int_data = read_file(args.str_csv_path[0], args.int_csv_path[0])
    RunExpectancy.stitch_data(str_data, int_data)
    endtime = time.time()-t
    print("Runtime: " + str(endtime))
