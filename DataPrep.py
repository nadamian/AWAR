import subprocess
import pandas as pd
import os.path

TEAMSAL = ['ANA', 'BAL', 'BOS', 'CHA', 'CLE','DET', 'HOU', 'KCA', 'MIN', 'NYA', 'OAK', 'SEA', 'TBA', 'TEX', 'TOR']
TEAMSNL = ['ARI', 'ATL', 'CHN', 'CIN', 'COL', 'LAN', 'MIA', 'MIL', 'NYN', 'PHI', 'PIT', 'SDN', 'SFN', 'SLN', 'WAS']
PATH = r"C:\Users\natad\PycharmProjects\AWAR\Data\2022"
INT_INDICES = "2,3,4,8,9,32-34,37,40,43,46,51-52,54,56,58-65"
STR_INDICES = "0,26-31,35-36,38-39,41-42,44-45,47-50,53,55,57,66-74,79"
GAME_INDICES = "0,34-35"


def event_process(year: str):
    for team in TEAMSAL:
        subprocess.run(["bevent", "-y", year, "-f", INT_INDICES, year + team + ".EVA", ">", year + team + "INT.csv"],
                       shell=True, cwd=PATH)
        subprocess.run(["bevent", "-y", year, "-f", STR_INDICES, year + team + ".EVA", ">", year + team + "STR.csv"],
                       shell=True, cwd=PATH)
    for team in TEAMSNL:
        subprocess.run(["bevent", "-y", year, "-f", INT_INDICES, year + team + ".EVN", ">", year + team + "INT.csv"],
                       shell=True, cwd=PATH)
        subprocess.run(["bevent", "-y", year, "-f", STR_INDICES, year + team + ".EVN", ">", year + team + "STR.csv"],
                       shell=True, cwd=PATH)


def game_process(year: str):
    for team in TEAMSAL:
        subprocess.run(["bgame", "-y", year, "-f", GAME_INDICES, year + team + ".EVA", ">", year + team + "GAME.csv"],
                       shell=True, cwd=PATH)
    for team in TEAMSNL:
        subprocess.run(["bgame", "-y", year, "-f", GAME_INDICES, year + team + ".EVN", ">", year + team + "GAME.csv"],
                       shell=True, cwd=PATH)

def merge_files(year: str):
    df_csv_append_int = pd.DataFrame()
    df_csv_append_str = pd.DataFrame()
    for team in TEAMSAL:
        df = pd.read_csv(os.path.join(PATH, year + team + "INT.csv"), header=None)
        df_csv_append_int = df_csv_append_int.append(df, ignore_index=True)
        df = pd.read_csv(os.path.join(PATH, year + team + "STR.csv"), header=None)
        df_csv_append_str = df_csv_append_str.append(df, ignore_index=True)
    for team in TEAMSNL:
        df = pd.read_csv(os.path.join(PATH, year + team + "INT.csv"), header=None)
        df_csv_append_int = df_csv_append_int.append(df, ignore_index=True)
        df = pd.read_csv(os.path.join(PATH, year + team + "STR.csv"), header=None)
        df_csv_append_str = df_csv_append_str.append(df, ignore_index=True)
    df_csv_append_int.to_csv(os.path.join(PATH, year + "INT.csv"), header=False, index=False)
    df_csv_append_str.to_csv(os.path.join(PATH, year + "STR.csv"), header=False, index=False)

def merge_games(year: str):
    df_csv_append_game = pd.DataFrame()
    for team in TEAMSAL:
        df = pd.read_csv(os.path.join(PATH, year + team + "GAME.csv"), header=None)
        df_csv_append_game = df_csv_append_game.append(df, ignore_index=True)
    for team in TEAMSNL:
        df = pd.read_csv(os.path.join(PATH, year + team + "GAME.csv"), header=None)
        df_csv_append_game = df_csv_append_game.append(df, ignore_index=True)
    df_csv_append_game.to_csv(os.path.join(PATH, year + "GAME.csv"), header=False, index=False)

if __name__ == '__main__':
    game_process("2022")
    merge_games("2022")
