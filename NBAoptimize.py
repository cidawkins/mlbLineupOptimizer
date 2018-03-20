# NBA Optimizer
#
# by Dave Hensley
#
# Picks an ideal fantasy NBA team using a modified knapsack algorithm
#
# Usage: python nba-optimizer.py players.csv

import csv, sys
from ortools.linear_solver import pywraplp

salaryCap = 50000


def getPositionNumber(name):
    return {
        'C': 0,
        'PG': 1,
        'PG/SG': 2,
        'PF': 3,
        'PF/C': 4,
        'SG': 5,
        'SG/SF': 6,
        'SF': 7,
        'SF/PF': 8,
        'PG/SF': 9
    }[name]


def getTeamNum(team):
    return {
        'ATL': 0,
        'BKN': 1,
        'BOS': 2,
        'CHA': 3,
        'CHI': 4,
        'CLE': 5,
        'DAL': 6,
        'DEN': 7,
        'DET': 8,
        'GSW': 9,
        'HOU': 10,
        'IND': 11,
        'LAC': 12,
        'LAL': 13,
        'MEM': 14,
        'MIA': 15,
        'MIL': 16,
        'MIN': 17,
        'NOP': 18,
        'NYK': 19,
        'OKC': 20,
        'ORL': 21,
        'PHO': 22,
        'PHX': 23,
        'POR': 24,
        'SAC': 25,
        'SAS': 26,
        'TOR': 27,
        'UTA': 28,
        'WAS': 29
    }[team]


def lineupBuilder(players, salaryCap, lineups):
    solver = pywraplp.Solver('CoinsGridCLP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    rangeC = range(len(players[0]))
    rangePG = range(len(players[1]))
    rangePGSG = range(len(players[2]))
    rangePF = range(len(players[3]))
    rangePFC = range(len(players[4]))
    rangeSG = range(len(players[5]))
    rangeSGSF = range(len(players[6]))
    rangeSF = range(len(players[7]))
    rangeSFPF = range(len(players[8]))
    rangePGSF = range(len(players[9]))

    takeC = [solver.IntVar(0, 1, 'takeC[%i]' % j) for j in rangeC]
    takePG = [solver.IntVar(0, 1, 'takePG[%i]' % j) for j in rangePG]
    takePGSG = [solver.IntVar(0, 1, 'takePGSG[%i]' % j) for j in rangePGSG]
    takePF = [solver.IntVar(0, 1, 'takePF[%i]' % j) for j in rangePF]
    takePFC = [solver.IntVar(0, 1, 'takePFC[%i]' % j) for j in rangePFC]
    takeSG = [solver.IntVar(0, 1, 'takeSG[%i]' % j) for j in rangeSG]
    takeSGSF = [solver.IntVar(0, 1, 'takeSGSF[%i]' % j) for j in rangeSGSF]
    takeSF = [solver.IntVar(0, 1, 'takeSF[%i]' % j) for j in rangeSF]
    takeSFPF = [solver.IntVar(0, 1, 'takeSFPF[%i]' % j) for j in rangeSFPF]
    takePGSF = [solver.IntVar(0, 1, 'takePGSF[%i]' % j) for j in rangePGSF]

    teamsC = []
    teamsPG = []
    teamsPGSG = []
    teamsPF = []
    teamsPFC = []
    teamsSG = []
    teamsSGSF = []
    teamsSF = []
    teamsSFPF = []
    teamsPGSF = []

    for teamNumber in range(0, 29):
        teamsC.insert(teamNumber, solver.Sum([(players[0][i][3] == teamNumber + 1) * takeC[i] for i in rangeC]))
        teamsPG.insert(teamNumber, solver.Sum([(players[1][i][3] == teamNumber + 1) * takePG[i] for i in rangePG]))
        teamsPGSG.insert(teamNumber, solver.Sum([(players[2][i][3] == teamNumber + 1) * takePGSG[i] for i in rangePGSG]))
        teamsPF.insert(teamNumber, solver.Sum([(players[3][i][3] == teamNumber + 1) * takePF[i] for i in rangePF]))
        teamsPFC.insert(teamNumber, solver.Sum([(players[4][i][3] == teamNumber + 1) * takePFC[i] for i in rangePFC]))
        teamsSG.insert(teamNumber, solver.Sum([(players[5][i][3] == teamNumber + 1) * takeSG[i] for i in rangeSG]))
        teamsSGSF.insert(teamNumber, solver.Sum([(players[6][i][3] == teamNumber + 1) * takeSGSF[i] for i in rangeSGSF]))
        teamsSF.insert(teamNumber, solver.Sum([(players[7][i][3] == teamNumber + 1) * takeSF[i] for i in rangeSF]))
        teamsSFPF.insert(teamNumber, solver.Sum([(players[8][i][3] == teamNumber + 1) * takeSFPF[i] for i in rangeSFPF]))
        teamsPGSF.insert(teamNumber,
                         solver.Sum([(players[9][i][3] == teamNumber + 1) * takePGSF[i] for i in rangePGSF]))

    lCrossC = []
    lCrossPG = []
    lCrossPGSG = []
    lCrossPF = []
    lCrossPFC = []
    lCrossSG = []
    lCrossSGSF = []
    lCrossSF = []
    lCrossSFPF = []
    lCrossPGSF = []

    for j in range(0, len(lineups)):
        lCrossC.insert(j, solver.Sum(
            [((players[0][i][0] == lineups[j][0]) or (players[0][i][0] == lineups[j][1]) or
              (players[0][i][0] == lineups[j][2]) or (players[0][i][0] == lineups[j][3]) or
              (players[0][i][0] == lineups[j][4]) or (players[0][i][0] == lineups[j][5]) or
              (players[0][i][0] == lineups[j][6]) or (players[0][i][0] == lineups[j][7])) * takeC[i] for i in rangeC]))
        lCrossPG.insert(j, solver.Sum(
            [((players[1][i][0] == lineups[j][0]) or (players[1][i][0] == lineups[j][1]) or
              (players[1][i][0] == lineups[j][2]) or (players[1][i][0] == lineups[j][3]) or
              (players[1][i][0] == lineups[j][4]) or (players[1][i][0] == lineups[j][5]) or
              (players[1][i][0] == lineups[j][6]) or (players[1][i][0] == lineups[j][7])) * takePG[i] for i in rangePG]))
        lCrossPGSG.insert(j, solver.Sum(
            [((players[2][i][0] == lineups[j][0]) or (players[2][i][0] == lineups[j][1]) or
              (players[2][i][0] == lineups[j][2]) or (players[2][i][0] == lineups[j][3]) or
              (players[2][i][0] == lineups[j][4]) or (players[2][i][0] == lineups[j][5]) or
              (players[2][i][0] == lineups[j][6]) or (players[2][i][0] == lineups[j][7])) * takePGSG[i] for i in
             rangePGSG]))
        lCrossPF.insert(j, solver.Sum(
            [((players[3][i][0] == lineups[j][0]) or (players[3][i][0] == lineups[j][1]) or
              (players[3][i][0] == lineups[j][2]) or (players[3][i][0] == lineups[j][3]) or
              (players[3][i][0] == lineups[j][4]) or (players[3][i][0] == lineups[j][5]) or
              (players[3][i][0] == lineups[j][6]) or (players[3][i][0] == lineups[j][7])) * takePF[i] for i in rangePF]))
        lCrossPFC.insert(j, solver.Sum(
            [((players[4][i][0] == lineups[j][0]) or (players[4][i][0] == lineups[j][1]) or
              (players[4][i][0] == lineups[j][2]) or (players[4][i][0] == lineups[j][3]) or
              (players[4][i][0] == lineups[j][4]) or (players[4][i][0] == lineups[j][5]) or
              (players[4][i][0] == lineups[j][6]) or (players[4][i][0] == lineups[j][7])) * takePFC[i] for i in
             rangePFC]))
        lCrossSG.insert(j, solver.Sum(
            [((players[5][i][0] == lineups[j][0]) or (players[5][i][0] == lineups[j][1]) or
              (players[5][i][0] == lineups[j][2]) or (players[5][i][0] == lineups[j][3]) or
              (players[5][i][0] == lineups[j][4]) or (players[5][i][0] == lineups[j][5]) or
              (players[5][i][0] == lineups[j][6]) or (players[5][i][0] == lineups[j][7])) * takeSG[i] for i in
             rangeSG]))
        lCrossSGSF.insert(j, solver.Sum(
            [((players[6][i][0] == lineups[j][0]) or (players[6][i][0] == lineups[j][1]) or
              (players[6][i][0] == lineups[j][2]) or (players[6][i][0] == lineups[j][3]) or
              (players[6][i][0] == lineups[j][4]) or (players[6][i][0] == lineups[j][5]) or
              (players[6][i][0] == lineups[j][6]) or (players[6][i][0] == lineups[j][7])) * takeSGSF[i] for i in
             rangeSGSF]))
        lCrossSF.insert(j, solver.Sum(
            [((players[7][i][0] == lineups[j][0]) or (players[7][i][0] == lineups[j][1]) or
              (players[7][i][0] == lineups[j][2]) or (players[7][i][0] == lineups[j][3]) or
              (players[7][i][0] == lineups[j][4]) or (players[7][i][0] == lineups[j][5]) or
              (players[7][i][0] == lineups[j][6]) or (players[7][i][0] == lineups[j][7])) * takeSF[i] for i in rangeSF]))
        lCrossSFPF.insert(j, solver.Sum(
            [((players[8][i][0] == lineups[j][0]) or (players[8][i][0] == lineups[j][1]) or
              (players[8][i][0] == lineups[j][2]) or (players[8][i][0] == lineups[j][3]) or
              (players[8][i][0] == lineups[j][4]) or (players[8][i][0] == lineups[j][5]) or
              (players[8][i][0] == lineups[j][6]) or (players[8][i][0] == lineups[j][7])) * takeSFPF[i] for i in rangeSFPF]))
        lCrossPGSF.insert(j, solver.Sum(
            [((players[9][i][0] == lineups[j][0]) or (players[9][i][0] == lineups[j][1]) or
              (players[9][i][0] == lineups[j][2]) or (players[9][i][0] == lineups[j][3]) or
              (players[9][i][0] == lineups[j][4]) or (players[9][i][0] == lineups[j][5]) or
              (players[9][i][0] == lineups[j][6]) or (players[9][i][0] == lineups[j][7])) * takePGSF[i] for i in
             rangePGSF]))

    valueC = solver.Sum([players[0][i][1] * takeC[i] for i in rangeC])
    valuePG = solver.Sum([players[1][i][1] * takePG[i] for i in rangePG])
    valuePGSG = solver.Sum([players[2][i][1] * takePGSG[i] for i in rangePGSG])
    valuePF = solver.Sum([players[3][i][1] * takePF[i] for i in rangePF])
    valuePFC = solver.Sum([players[4][i][1] * takePFC[i] for i in rangePFC])
    valueSG = solver.Sum([players[5][i][1] * takeSG[i] for i in rangeSG])
    valueSGSF = solver.Sum([players[6][i][1] * takeSGSF[i] for i in rangeSGSF])
    valueSF = solver.Sum([players[7][i][1] * takeSF[i] for i in rangeSF])
    valueSFPF = solver.Sum([players[8][i][1] * takeSFPF[i] for i in rangeSFPF])
    valuePGSF = solver.Sum([players[9][i][1] * takePGSF[i] for i in rangePGSF])

    salaryC = solver.Sum([players[0][i][2] * takeC[i] for i in rangeC])
    salaryPG = solver.Sum([players[1][i][2] * takePG[i] for i in rangePG])
    salaryPGSG = solver.Sum([players[2][i][2] * takePGSG[i] for i in rangePGSG])
    salaryPF = solver.Sum([players[3][i][2] * takePF[i] for i in rangePF])
    salaryPFC = solver.Sum([players[4][i][2] * takePFC[i] for i in rangePFC])
    salarySG = solver.Sum([players[5][i][2] * takeSG[i] for i in rangeSG])
    salarySGSF = solver.Sum([players[6][i][2] * takeSGSF[i] for i in rangeSGSF])
    salarySF = solver.Sum([players[7][i][2] * takeSF[i] for i in rangeSF])
    salarySFPF = solver.Sum([players[8][i][2] * takeSFPF[i] for i in rangeSFPF])
    salaryPGSF = solver.Sum([players[9][i][2] * takePGSF[i] for i in rangePGSF])

    solver.Add(salaryC + salaryPG + salaryPGSG + salaryPF + salaryPFC + salarySG + salarySGSF +
               salarySF + salarySFPF + salaryPGSF <= salaryCap)

    # Constraints setting number of players per position
    pgCount = solver.Sum(takePG[i] for i in rangePG)
    pgsgCount = solver.Sum(takePGSG[i] for i in rangePGSG)
    sgCount = solver.Sum(takeSG[i] for i in rangeSG)
    sgsfCount = solver.Sum(takeSGSF[i] for i in rangeSGSF)
    sfCount = solver.Sum(takeSF[i] for i in rangeSF)
    sfpfCount = solver.Sum(takeSFPF[i] for i in rangeSFPF)
    pfCount = solver.Sum(takePF[i] for i in rangePF)
    pfcCount = solver.Sum(takePFC[i] for i in rangePFC)
    cCount = solver.Sum(takeC[i] for i in rangeC)
    pgsfCount = solver.Sum(takePGSF[i] for i in rangePGSF)

    solver.Add((pgCount + pgsgCount + sgCount + sgsfCount + pfCount + pfcCount + sfCount + cCount + sfpfCount
               + pgsfCount) == 8)

    solver.Add(1 <= (pgCount + pgsgCount + pgsfCount) <= 6)
    solver.Add(1 <= (sgCount + sgsfCount + pgsgCount) <= 6)
    solver.Add(1 <= (sfCount + sgsfCount + sfpfCount + pgsfCount) <= 7)
    solver.Add(1 <= (pfCount + pfcCount + sfpfCount) <= 5)
    solver.Add(1 <= (cCount + pfcCount) <= 4)
    solver.Add(pgCount == 1)
    solver.Add(sgCount == 1)
    solver.Add(sfCount == 1)
    solver.Add(pfCount == 1)
    solver.Add(cCount == 1)
    solver.Add(pgsgCount <= 4)
    solver.Add(sgsfCount <= 5)
    solver.Add(sfpfCount <= 4)
    solver.Add(pfcCount <= 4)
    solver.Add(pgsfCount <= 5)

    # Constraint for picking at least 3 guards and forwards
    solver.Add((pgCount + pgsgCount + sgCount + sgsfCount + pgsfCount) >= 3)
    solver.Add((sfCount + pfCount + pfcCount + sfpfCount + sgsfCount + pgsfCount) >= 3)
    """
    # Stack at least three hitters from the same team.  THis seems like a very sloppy way of doing it, but it does work
    solver.Add((teamsPG[0] + teamsPGSG[0] + teamsSG[0] + teamsSGSF[0] + teamsSF[0] + teamsSFPF[0] + teamsPF[0] +
                teamsPFC[0] + teamsC[0] + teamsPGSF[0] >= 2) or
               (teamsPG[1] + teamsPGSG[1] + teamsSG[1] + teamsSGSF[1] + teamsSF[1] + teamsSFPF[1] + teamsPF[1] +
                teamsPFC[1] + teamsC[1] + teamsPGSF[1]>= 2) or
               (teamsPG[2] + teamsPGSG[2] + teamsSG[2] + teamsSGSF[2] + teamsSF[2] + teamsSFPF[2] + teamsPF[2] +
                teamsPFC[2] + teamsC[2] + teamsPGSF[2] >= 2) or
               (teamsPG[3] + teamsPGSG[3] + teamsSG[3] + teamsSGSF[3] + teamsSF[3] + teamsSFPF[3] + teamsPF[3] +
                teamsPFC[3] + teamsC[3] + teamsPGSF[3] >= 2) or
               (teamsPG[4] + teamsPGSG[4] + teamsSG[4] + teamsSGSF[4] + teamsSF[4] + teamsSFPF[4] + teamsPF[4] +
                teamsPFC[4] + teamsC[4] + teamsPGSF[4] >= 2) or
               (teamsPG[5] + teamsPGSG[5] + teamsSG[5] + teamsSGSF[5] + teamsSF[5] + teamsSFPF[5] + teamsPF[5] +
                teamsPFC[5] + teamsC[5] + teamsPGSF[5] >= 2) or
               (teamsPG[6] + teamsPGSG[6] + teamsSG[6] + teamsSGSF[6] + teamsSF[6] + teamsSFPF[6] + teamsPF[6] +
                teamsPFC[6] + teamsC[6] + teamsPGSF[6] >= 2) or
               (teamsPG[7] + teamsPGSG[7] + teamsSG[7] + teamsSGSF[7] + teamsSF[7] + teamsSFPF[7] + teamsPF[7] +
                teamsPFC[7] + teamsC[7] + teamsPGSF[7] >= 2) or
               (teamsPG[8] + teamsPGSG[8] + teamsSG[8] + teamsSGSF[8] + teamsSF[8] + teamsSFPF[8] + teamsPF[8] +
                teamsPFC[8] + teamsC[8] + teamsPGSF[8] >= 2) or
               (teamsPG[9] + teamsPGSG[9] + teamsSG[9] + teamsSGSF[9] + teamsSF[9] + teamsSFPF[9] + teamsPF[9] +
                teamsPFC[9] + teamsC[9] + teamsPGSF[9] >= 2) or
               (teamsPG[10] + teamsPGSG[10] + teamsSG[10] + teamsSGSF[10] + teamsSF[10] + teamsSFPF[10] + teamsPF[10] +
                teamsPFC[10] + teamsC[10] + teamsPGSF[10] >= 2) or
               (teamsPG[11] + teamsPGSG[11] + teamsSG[11] + teamsSGSF[11] + teamsSF[11] + teamsSFPF[11] + teamsPF[11] +
                teamsPFC[11] + teamsC[11] + teamsPGSF[11] >= 2) or
               (teamsPG[12] + teamsPGSG[12] + teamsSG[12] + teamsSGSF[12] + teamsSF[12] + teamsSFPF[12] + teamsPF[12] +
                teamsPFC[12] + teamsC[12] + teamsPGSF[12] >= 2) or
               (teamsPG[13] + teamsPGSG[13] + teamsSG[13] + teamsSGSF[13] + teamsSF[13] + teamsSFPF[13] + teamsPF[13] +
                teamsPFC[13] + teamsC[13] + teamsPGSF[13] >= 2) or
               (teamsPG[14] + teamsPGSG[14] + teamsSG[14] + teamsSGSF[14] + teamsSF[14] + teamsSFPF[14] + teamsPF[14] +
                teamsPFC[14] + teamsC[14] + teamsPGSF[14] >= 2) or
               (teamsPG[15] + teamsPGSG[15] + teamsSG[15] + teamsSGSF[15] + teamsSF[15] + teamsSFPF[15] + teamsPF[15] +
                teamsPFC[15] + teamsC[15] + teamsPGSF[15] >= 2) or
               (teamsPG[16] + teamsPGSG[16] + teamsSG[16] + teamsSGSF[16] + teamsSF[16] + teamsSFPF[16] + teamsPF[16] +
                teamsPFC[16] + teamsC[16] + teamsPGSF[16] >= 2) or
               (teamsPG[17] + teamsPGSG[17] + teamsSG[17] + teamsSGSF[17] + teamsSF[17] + teamsSFPF[17] + teamsPF[17] +
                teamsPFC[17] + teamsC[17] + teamsPGSF[17] >= 2) or
               (teamsPG[18] + teamsPGSG[18] + teamsSG[18] + teamsSGSF[18] + teamsSF[18] + teamsSFPF[18] + teamsPF[18] +
                teamsPFC[18] + teamsC[18] + teamsPGSF[18] >= 2) or
               (teamsPG[19] + teamsPGSG[19] + teamsSG[19] + teamsSGSF[19] + teamsSF[19] + teamsSFPF[19] + teamsPF[19] +
                teamsPFC[19] + teamsC[19] + teamsPGSF[19] >= 2) or
               (teamsPG[20] + teamsPGSG[20] + teamsSG[20] + teamsSGSF[20] + teamsSF[20] + teamsSFPF[20] + teamsPF[20] +
                teamsPFC[20] + teamsC[20] + teamsPGSF[20] >= 2) or
               (teamsPG[21] + teamsPGSG[21] + teamsSG[21] + teamsSGSF[21] + teamsSF[21] + teamsSFPF[21] + teamsPF[21] +
                teamsPFC[21] + teamsC[21] + teamsPGSF[21] >= 2) or
               (teamsPG[22] + teamsPGSG[22] + teamsSG[22] + teamsSGSF[22] + teamsSF[22] + teamsSFPF[22] + teamsPF[22] +
                teamsPFC[22] + teamsC[22] + teamsPGSF[22] >= 2) or
               (teamsPG[23] + teamsPGSG[23] + teamsSG[23] + teamsSGSF[23] + teamsSF[23] + teamsSFPF[23] + teamsPF[23] +
                teamsPFC[23] + teamsC[23] + teamsPGSF[23] >= 2) or
               (teamsPG[24] + teamsPGSG[24] + teamsSG[24] + teamsSGSF[24] + teamsSF[24] + teamsSFPF[24] + teamsPF[24] +
                teamsPFC[24] + teamsC[24] + teamsPGSF[24] >= 2) or
               (teamsPG[25] + teamsPGSG[25] + teamsSG[25] + teamsSGSF[25] + teamsSF[25] + teamsSFPF[25] + teamsPF[25] +
                teamsPFC[25] + teamsC[25] + teamsPGSF[25] >= 2) or
               (teamsPG[26] + teamsPGSG[26] + teamsSG[26] + teamsSGSF[26] + teamsSF[26] + teamsSFPF[26] + teamsPF[26] +
                teamsPFC[26] + teamsC[26] + teamsPGSF[26] >= 2) or
               (teamsPG[27] + teamsPGSG[27] + teamsSG[27] + teamsSGSF[27] + teamsSF[27] + teamsSFPF[27] + teamsPF[27] +
                teamsPFC[27] + teamsC[27] + teamsPGSF[27] >= 2) or
               (teamsPG[28] + teamsPGSG[28] + teamsSG[28] + teamsSGSF[28] + teamsSF[28] + teamsSFPF[28] + teamsPF[28] +
                teamsPFC[28] + teamsC[28] + teamsPGSF[28] >= 2) or
               (teamsPG[29] + teamsPGSG[29] + teamsSG[29] + teamsSGSF[29] + teamsSF[29] + teamsSFPF[29] + teamsPF[29] +
                teamsPFC[29] + teamsC[29] + teamsPGSF[29] >= 2))
    """
    # Add constraint to adjust for lineup overlap
    for i in range(0, len(lineups)):
        solver.Add(lCrossC[i] + lCrossSG[i] + lCrossSGSF[i] + lCrossSF[i] + lCrossSFPF[i] + lCrossPF[i] +
                   lCrossPFC[i] + lCrossPG[i] + lCrossPGSG[i] + lCrossPGSF[i] <= 5)

    # Max 4 players per team
    for i in range(0, 29):
        solver.Add(teamsPG[i] + teamsPGSG[i] + teamsC[i] + teamsPF[i] + teamsPFC[i] + teamsSG[i] + teamsSGSF[i] +
                   teamsSF[i] + teamsSFPF[i] + teamsPGSF[i] <= 5)

    solver.Maximize(valueC + valuePG + valuePGSG + valuePF + valuePFC + valueSG + valueSGSF + valueSF + valueSFPF + valuePGSF)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print('Solved in', solver.wall_time(), 'milliseconds!', "\n")

    salary = 0
    projection = 0
    tempLineup = [[], [], [], [], [], [], [], [], [], []]
    for i in rangeC:
        if (takeC[i].SolutionValue()):
            salary += players[0][i][2]
            projection += players[0][i][1]
            tempLineup[0].append(players[0][i][0])

    for i in rangePG:
        if (takePG[i].SolutionValue()):
            salary += players[1][i][2]
            projection += players[1][i][1]
            tempLineup[1].append(players[1][i][0])

    for i in rangePGSG:
        if (takePGSG[i].SolutionValue()):
            salary += players[2][i][2]
            projection += players[2][i][1]
            tempLineup[2].append(players[2][i][0])

    for i in rangePF:
        if (takePF[i].SolutionValue()):
            salary += players[3][i][2]
            projection += players[3][i][1]
            tempLineup[3].append(players[3][i][0])

    for i in rangePFC:
        if (takePFC[i].SolutionValue()):
            salary += players[4][i][2]
            projection += players[4][i][1]
            tempLineup[4].append(players[4][i][0])

    for i in rangeSG:
        if (takeSG[i].SolutionValue()):
            salary += players[5][i][2]
            projection += players[5][i][1]
            tempLineup[5].append(players[5][i][0])

    for i in rangeSGSF:
        if (takeSGSF[i].SolutionValue()):
            salary += players[6][i][2]
            projection += players[6][i][1]
            tempLineup[6].append(players[6][i][0])

    for i in rangeSF:
        if (takeSF[i].SolutionValue()):
            salary += players[7][i][2]
            projection += players[7][i][1]
            tempLineup[7].append(players[7][i][0])

    for i in rangeSFPF:
        if takeSFPF[i].SolutionValue():
            salary += players[8][i][2]
            projection += players[8][i][1]
            tempLineup[8].append(players[8][i][0])

    for i in rangePGSF:
        if takePGSF[i].SolutionValue():
            salary += players[9][i][2]
            projection += players[9][i][1]
            tempLineup[9].append(players[9][i][0])

    if len(tempLineup) == 9:
        tempLineup.append([])

    currLineup = [[], [], [], [], [], [], [], []]

    for i in range(0, len(currLineup)):
        while not currLineup[i]:
            if i == 0:
                if tempLineup[1]:
                    currLineup[i] = [tempLineup[1][0]]
                    del tempLineup[1][0]
                elif tempLineup[2]:
                    currLineup[i] = [tempLineup[2][0]]
                    del tempLineup[2][0]
                elif tempLineup[9]:
                    currLineup[i] = [tempLineup[2][0]]
                    del tempLineup[9][0]
            elif i == 1:
                if tempLineup[5]:
                    currLineup[i] = [tempLineup[5][0]]
                    del tempLineup[5][0]
                elif tempLineup[2]:
                    currLineup[i] = [tempLineup[2][0]]
                    del tempLineup[2][0]
                elif tempLineup[6]:
                    currLineup[i] = [tempLineup[6][0]]
                    del tempLineup[6][0]
            elif i == 2:
                if tempLineup[7]:
                    currLineup[i] = [tempLineup[7][0]]
                    del tempLineup[7][0]
                elif tempLineup[8]:
                    currLineup[i] = [tempLineup[8][0]]
                    del tempLineup[8][0]
                elif tempLineup[9]:
                    currLineup[i] = [tempLineup[9][0]]
                    del tempLineup[9][0]
                elif tempLineup[6]:
                    currLineup[i] = [tempLineup[6][0]]
                    del tempLineup[6][0]
            elif i == 3:
                if tempLineup[3]:
                    currLineup[i] = [tempLineup[3][0]]
                    del tempLineup[3][0]
                elif tempLineup[4]:
                    currLineup[i] = [tempLineup[4][0]]
                    del tempLineup[4][0]
                elif tempLineup[8]:
                    currLineup[i] = [tempLineup[8][0]]
                    del tempLineup[8][0]
            elif i == 4:
                if tempLineup[0]:
                    currLineup[i] = [tempLineup[0][0]]
                    del tempLineup[0][0]
                elif tempLineup[4]:
                    currLineup[i] = [tempLineup[4][0]]
                    del tempLineup[4][0]
            elif i == 5:
                if tempLineup[1]:
                    currLineup[i] = [tempLineup[1][0]]
                    del tempLineup[1][0]
                elif tempLineup[2]:
                    currLineup[i] = [tempLineup[2][0]]
                    del tempLineup[2][0]
                elif tempLineup[5]:
                    currLineup[i] = [tempLineup[5][0]]
                    del tempLineup[5][0]
                elif tempLineup[6]:
                    currLineup[i] = [tempLineup[6][0]]
                    del tempLineup[6][0]
                elif tempLineup[9]:
                    currLineup[i] = [tempLineup[9][0]]
                    del tempLineup[9][0]
            elif i == 6:
                if tempLineup[3]:
                    currLineup[i] = [tempLineup[3][0]]
                    del tempLineup[3][0]
                elif tempLineup[4]:
                    currLineup[i] = [tempLineup[4][0]]
                    del tempLineup[4][0]
                elif tempLineup[6]:
                    currLineup[i] = [tempLineup[6][0]]
                    del tempLineup[6][0]
                elif tempLineup[7]:
                    currLineup[i] = [tempLineup[7][0]]
                    del tempLineup[7][0]
                elif tempLineup[8]:
                    currLineup[i] = [tempLineup[8][0]]
                    del tempLineup[8][0]
                elif tempLineup[9]:
                    currLineup[i] = [tempLineup[9][0]]
                    del tempLineup[9][0]
            elif i == 7:
                if tempLineup[0]:
                    currLineup[i] = [tempLineup[0][0]]
                    del tempLineup[0][0]
                elif tempLineup[1]:
                    currLineup[i] = [tempLineup[1][0]]
                    del tempLineup[1][0]
                elif tempLineup[2]:
                    currLineup[i] = [tempLineup[2][0]]
                    del tempLineup[2][0]
                elif tempLineup[3]:
                    currLineup[i] = [tempLineup[3][0]]
                    del tempLineup[3][0]
                elif tempLineup[4]:
                    currLineup[i] = [tempLineup[4][0]]
                    del tempLineup[4][0]
                elif tempLineup[5]:
                    currLineup[i] = [tempLineup[5][0]]
                    del tempLineup[5][0]
                elif tempLineup[6]:
                    currLineup[i] = [tempLineup[6][0]]
                    del tempLineup[6][0]
                elif tempLineup[7]:
                    currLineup[i] = [tempLineup[7][0]]
                    del tempLineup[7][0]
                elif tempLineup[8]:
                    currLineup[i] = [tempLineup[8][0]]
                    del tempLineup[8][0]
                elif tempLineup[9]:
                    currLineup[i] = [tempLineup[9][0]]
                    del tempLineup[9][0]

    line = [0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(0, len(currLineup)):
        line[i] = currLineup[i][0]


    """
    sortedLineup = sorted(tempLineup, key=len, reverse=True)
    lKey = []
    currLineup = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in range(0, len(sortedLineup)):
        if sortedLineup[i]:
            if sortedLineup[i][0] in tempLineup[0]:
                lKey.append('C')
            elif sortedLineup[i][0] in tempLineup[1]:
                lKey.append('PG')
            elif sortedLineup[i][0] in tempLineup[2]:
                lKey.append('PGSG')
            elif sortedLineup[i][0] in tempLineup[3]:
                lKey.append('PF')
            elif sortedLineup[i][0] in tempLineup[4]:
                lKey.append('PFC')
            elif sortedLineup[i][0] in tempLineup[5]:
                lKey.append('SG')
            elif sortedLineup[i][0] in tempLineup[6]:
                lKey.append('SGSF')
            elif sortedLineup[i][0] in tempLineup[7]:
                lKey.append('SF')
            elif sortedLineup[i][0] in tempLineup[8]:
                lKey.append('SFPF')
            elif sortedLineup[i][0] in tempLineup[9]:
                lKey.append('PGSF')

    for i in range(0, len(lKey)):
        while sortedLineup[i]:
            if lKey[i] == 'C':
                if currLineup[4] == 0:
                    currLineup[4] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'PG':
                if currLineup[0] == 0:
                    currLineup[0] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[5] == 0:
                    currLineup[5] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'PGSG':
                if currLineup[0] == 0:
                    currLineup[0] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[1] == 0:
                    currLineup[1] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[5] == 0:
                    currLineup[5] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'PF':
                if currLineup[3] == 0:
                    currLineup[3] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[6] == 0:
                    currLineup[6] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'PFC':
                if currLineup[3] == 0:
                    currLineup[3] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[4] == 0:
                    currLineup[4] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[6] == 0:
                    currLineup[6] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'SG':
                if currLineup[1] == 0:
                    currLineup[1] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[5] == 0:
                    currLineup[5] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'SGSF':
                if currLineup[1] == 0:
                    currLineup[1] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[2] == 0:
                    currLineup[2] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[5] == 0:
                    currLineup[5] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[6] == 0:
                    currLineup[6] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'SF':
                if currLineup[2] == 0:
                    currLineup[2] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[6] == 0:
                    currLineup[6] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'SFPF':
                if currLineup[2] == 0:
                    currLineup[2] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[3] == 0:
                    currLineup[3] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[6] == 0:
                    currLineup[6] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
            elif lKey[i] == 'PGSF':
                if currLineup[0] == 0:
                    currLineup[0] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[2] == 0:
                    currLineup[2] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[5] == 0:
                    currLineup[5] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[6] == 0:
                    currLineup[6] = sortedLineup[i][0]
                    del sortedLineup[i][0]
                elif currLineup[7] == 0:
                    currLineup[7] = sortedLineup[i][0]
                    del sortedLineup[i][0]
    """

    """
    for i in rC:
        if currLineup[4] == 0:
            currLineup[4] = tempLineup[0][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[0][i]

    for i in rPG:
        if currLineup[0] == 0:
            currLineup[0] = tempLineup[1][i]
        elif currLineup[5] == 0:
            currLineup[5] = tempLineup[1][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[1][i]

    for i in rPGSG:
        if currLineup[0] == 0:
            currLineup[0] = tempLineup[2][i]
        elif currLineup[1] == 0:
            currLineup[1] = tempLineup[2][i]
        elif currLineup[5] == 0:
            currLineup[5] = tempLineup[2][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[2][i]

    for i in rPF:
        if currLineup[3] == 0:
            currLineup[3] = tempLineup[3][i]
        elif currLineup[6] == 0:
            currLineup[6] = tempLineup[3][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[3][i]

    for i in rPFC:
        if currLineup[3] == 0:
            currLineup[3] = tempLineup[4][i]
        elif currLineup[4] == 0:
            currLineup[4] = tempLineup[4][i]
        elif currLineup[6] == 0:
            currLineup[6] = tempLineup[4][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[4][i]

    for i in rSG:
        if currLineup[1] == 0:
            currLineup[1] = tempLineup[5][i]
        elif currLineup[5] == 0:
            currLineup[5] = tempLineup[5][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[5][i]

    for i in rSGSF:
        if currLineup[1] == 0:
            currLineup[1] = tempLineup[6][i]
        elif currLineup[2] == 0:
            currLineup[2] = tempLineup[6][i]
        elif currLineup[5] == 0:
            currLineup[5] = tempLineup[6][i]
        elif currLineup[6] == 0:
            currLineup[6] = tempLineup[6][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[6][i]

    for i in rSF:
        if currLineup[2] == 0:
            currLineup[2] = tempLineup[7][i]
        elif currLineup[6] == 0:
            currLineup[6] = tempLineup[7][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[7][i]

    for i in rSFPF:
        if currLineup[2] == 0:
            currLineup[2] = tempLineup[8][i]
        elif currLineup[3] == 0:
            currLineup[3] = tempLineup[8][i]
        elif currLineup[6] == 0:
            currLineup[6] = tempLineup[8][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[8][i]

    for i in rPGSF:
        if currLineup[0] == 0:
            currLineup[0] = tempLineup[9][i]
        elif currLineup[2] == 0:
            currLineup[2] = tempLineup[9][i]
        elif currLineup[5] == 0:
            currLineup[5] = tempLineup[9][i]
        elif currLineup[6] == 0:
            currLineup[6] = tempLineup[9][i]
        elif currLineup[7] == 0:
            currLineup[7] = tempLineup[9][i]
    """
    return [line, salary, projection]


players = [[], [], [], [], [], [], [], [], [], []]

with open('rgplayers.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)

    for row in spamreader:
        players[getPositionNumber(row['Subposition'])].append(
            [row['Name'], float(row['Value']), int(row['Salary']), getTeamNum(row['Team'])])


def lineups(numLineups):
    lineupList = []
    resultList = []
    lineupList.append(['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'])

    for i in range(0, numLineups):
        results = lineupBuilder(players, salaryCap, lineupList)
        lineupList.append(results[0])
        resultList.append(results)

    lineupsOnly = [['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'UTIL']]

    for i in range(0, numLineups):
        lineupsOnly.append(resultList[i][0])

    # Create csv file of lineups
    myFile = open('lineups.csv', 'w')
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(lineupsOnly)

    print("Writing complete")

    # Create csv file of lineups with additional results
    mF2 = open('lineupsWithResults.csv', 'w')
    with mF2:
        writer = csv.writer(mF2)
        writer.writerows(resultList)

    print("Writing complete")

    return resultList


print(lineups(37))
