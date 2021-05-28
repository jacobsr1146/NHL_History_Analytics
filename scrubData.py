import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import datetime
import math

def importFiles(file):
    with open(file) as f:
        encode = f.encoding

    df = pd.read_csv(file, sep=',', encoding = encode, low_memory=False) # read in "NHLScoringHistory.csv" file
    data = list(map(list, df.to_numpy()))

    # [	, Season, Player, Age, Tm, Pos, GP, G, GPG, A, PTS, +/-, PIM, EVG, PPG, SHG, GWG, EVA, PPA, SHA, S, S%, TOI,
    #  ATOI, BLK, HIT, FOwin, FOloss, FO%]

    # [Name, Pos, GP, G, A, Pts, +/-, S, S%, GPG, APG, PtsPG]

    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == ' -   ':
                data[i][j] = '0'
            if type(data[i][j]) is float:
                if math.isnan(data[i][j]) is True:
                    data[i][j] = '0'

    players_list = []
    players_stats = []

    for i in data:
        if i[2].replace("*", "") not in players_list:    # new player
            players_list.append(i[2].replace("*", ""))
            players_stats.append([i[2].replace("*", ""), i[5], i[6], int(i[7]), int(i[9]), int(i[10]), int(i[11]), int(i[20])])    # [Name, Pos, GP, G, A, Pts, +/-, S]
        else:   # existing player
            for j in players_stats:
                if j[0] == i[2].replace("*", ""):
                    j[2] += i[6]
                    j[3] += int(i[7])
                    j[4] += int(i[9])
                    j[5] += int(i[10])
                    j[6] += int(i[11])
                    j[7] += int(i[20])

    remove_index = []
    for i in range(len(players_list)):     # remove players that dont meet minimum games requirement
        if players_stats[i][2] < 200:
            remove_index.append(i)
        elif players_stats[i][7] != 0:
            if players_stats[i][3]/players_stats[i][7] > 0.4:
                remove_index.append(i)

    for i in range(len(remove_index)-1, -1, -1):
        index = remove_index[i]
        players_stats.remove(players_stats[index])
        players_list.remove(players_list[index])

    for i in players_stats:     # add extra "per Game" statistics
        if i[7] != 0:
            i.append(i[3]/i[7])
        else:
            i.append(0)
        i.append(i[3]/i[2])
        i.append(i[4]/i[2])
        i.append(i[5]/i[2])
        i.append(i[7]/i[2])
        i[6] = i[6]/i[2]


    # [Name, Pos, GP, G, A, Pts, +/-, S, S%, GPG, APG, PtsPG, SPG]

    return players_list, players_stats

#importFiles("NHLScoringHistory.csv")
