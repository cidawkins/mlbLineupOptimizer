# NBA Optimizer
#
# by Dave Hensley
#
# Picks an ideal fantasy NBA team using a modified knapsack algorithm
#
# Usage: python nba-optimizer.py players.csv

import csv, sys
from ortools.linear_solver import pywraplp

salaryCap = 60000


def getPositionNumber(name):
    return {
        'Center': 0,
        'Point Guard': 1,
        'Power Forward': 2,
        'Shooting Guard': 3,
        'Small Forward': 4
    }[name]


def lineupBuilder(players, salaryCap, lineups):
    solver = pywraplp.Solver('CoinsGridCLP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    rangeC = range(len(players[0]))
    rangePG = range(len(players[1]))
    rangePF = range(len(players[2]))
    rangeSG = range(len(players[3]))
    rangeSF = range(len(players[4]))

    takeC = [solver.IntVar(0, 1, 'takeC[%i]' % j) for j in rangeC]
    takePG = [solver.IntVar(0, 1, 'takePG[%i]' % j) for j in rangePG]
    takePF = [solver.IntVar(0, 1, 'takePF[%i]' % j) for j in rangePF]
    takeSG = [solver.IntVar(0, 1, 'takeSG[%i]' % j) for j in rangeSG]
    takeSF = [solver.IntVar(0, 1, 'takeSF[%i]' % j) for j in rangeSF]

    teamsC = []
    teamsPG = []
    teamsPF = []
    teamsSG = []
    teamsSF = []

    for teamNumber in range(0, 29):
        teamsC.insert(teamNumber, solver.Sum([(players[0][i][3] == teamNumber + 1) * takeC[i] for i in rangeC]))
        teamsPG.insert(teamNumber, solver.Sum([(players[1][i][3] == teamNumber + 1) * takePG[i] for i in rangePG]))
        teamsPF.insert(teamNumber, solver.Sum([(players[2][i][3] == teamNumber + 1) * takePF[i] for i in rangePF]))
        teamsSG.insert(teamNumber, solver.Sum([(players[3][i][3] == teamNumber + 1) * takeSG[i] for i in rangeSG]))
        teamsSF.insert(teamNumber, solver.Sum([(players[4][i][3] == teamNumber + 1) * takeSF[i] for i in rangeSF]))

    lCrossPG = []
    lCrossC = []
    lCrossSG = []
    lCrossSF = []
    lCrossPF = []

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
        lCrossPF.insert(j, solver.Sum(
            [((players[2][i][0] == lineups[j][0]) or (players[2][i][0] == lineups[j][1]) or
              (players[2][i][0] == lineups[j][2]) or (players[2][i][0] == lineups[j][3]) or
              (players[2][i][0] == lineups[j][4]) or (players[2][i][0] == lineups[j][5]) or
              (players[2][i][0] == lineups[j][6]) or (players[2][i][0] == lineups[j][7])) * takePF[i] for i in rangePF]))
        lCrossSF.insert(j, solver.Sum(
            [((players[4][i][0] == lineups[j][0]) or (players[4][i][0] == lineups[j][1]) or
              (players[4][i][0] == lineups[j][2]) or (players[4][i][0] == lineups[j][3]) or
              (players[4][i][0] == lineups[j][4]) or (players[4][i][0] == lineups[j][5]) or
              (players[4][i][0] == lineups[j][6]) or (players[4][i][0] == lineups[j][7])) * takeSF[i] for i in rangeSF]))
        lCrossSG.insert(j, solver.Sum(
            [((players[3][i][0] == lineups[j][0]) or (players[3][i][0] == lineups[j][1]) or
              (players[3][i][0] == lineups[j][2]) or (players[3][i][0] == lineups[j][3]) or
              (players[3][i][0] == lineups[j][4]) or (players[3][i][0] == lineups[j][5]) or
              (players[3][i][0] == lineups[j][6]) or (players[3][i][0] == lineups[j][7])) * takeSG[i] for i in rangeSG]))

    valueC = solver.Sum([players[0][i][1] * takeC[i] for i in rangeC])
    valuePG = solver.Sum([players[1][i][1] * takePG[i] for i in rangePG])
    valuePF = solver.Sum([players[2][i][1] * takePF[i] for i in rangePF])
    valueSG = solver.Sum([players[3][i][1] * takeSG[i] for i in rangeSG])
    valueSF = solver.Sum([players[4][i][1] * takeSF[i] for i in rangeSF])

    salaryC = solver.Sum([players[0][i][2] * takeC[i] for i in rangeC])
    salaryPG = solver.Sum([players[1][i][2] * takePG[i] for i in rangePG])
    salaryPF = solver.Sum([players[2][i][2] * takePF[i] for i in rangePF])
    salarySG = solver.Sum([players[3][i][2] * takeSG[i] for i in rangeSG])
    salarySF = solver.Sum([players[4][i][2] * takeSF[i] for i in rangeSF])

    solver.Add(salaryC + salaryPG + salaryPF + salarySG + salarySF <= salaryCap)

    # Constraint mandating team has 8 players
    solver.Add(((solver.Sum(takePG[i] for i in rangePG)) + (solver.Sum(takeSG[i] for i in rangeSG)) + (
        solver.Sum(takeSF[i] for i in rangeSF)) + (solver.Sum(takePF[i] for i in rangePF)) + (
                    solver.Sum(takeC[i] for i in rangeC))) == 8)

    # Constraints setting number of players per position
    # NOTE: This is causing a problem.  Currently, this is sometimes resulting in only havin 1 PG and 1 SG and does not
    # allow for the third G position to be filled.  The same is true for the third F position. Possibly creating a
    # separate array of all guards would fix this?

    # This helps, as it mandates that there at least 3 PG and 3 SG. It could be manually fixed by changing PG/SF or
    # SG/PF minimum to 2

    solver.Add(((solver.Sum(takePG[i] for i in rangePG)) + (solver.Sum(takeSG[i] for i in rangeSG)) >= 3))
    solver.Add(((solver.Sum(takeSF[i] for i in rangeSF)) + (solver.Sum(takePF[i] for i in rangePF)) >= 3))

    solver.Add((solver.Sum(takePG[i] for i in rangePG) >= 1) and (solver.Sum(takePG[i] for i in rangePG) <= 3))
    solver.Add((solver.Sum(takeSG[i] for i in rangeSG) >= 1) and (solver.Sum(takeSG[i] for i in rangeSG) <= 3))
    solver.Add((solver.Sum(takeSF[i] for i in rangeSF) >= 1) and (solver.Sum(takeSF[i] for i in rangeSF) <= 3))
    solver.Add((solver.Sum(takePF[i] for i in rangePF) >= 1) and (solver.Sum(takePF[i] for i in rangePF) <= 3))
    solver.Add((solver.Sum(takeC[i] for i in rangeC) >= 1) and (solver.Sum(takeC[i] for i in rangeC) <= 2))

    # Stack at least three hitters from the same team.  THis seems like a very sloppy way of doing it, but it does work
    solver.Add((teamsPG[0] + teamsSG[0] + teamsSF[0] + teamsPF[0] + teamsC[0] >= 3) or
               (teamsPG[1] + teamsSG[1] + teamsSF[1] + teamsPF[1] + teamsC[1] >= 3) or
               (teamsPG[2] + teamsSG[2] + teamsSF[2] + teamsPF[2] + teamsC[2] >= 3) or
               (teamsPG[3] + teamsSG[3] + teamsSF[3] + teamsPF[3] + teamsC[3] >= 3) or
               (teamsPG[4] + teamsSG[4] + teamsSF[4] + teamsPF[4] + teamsC[4] >= 3) or
               (teamsPG[5] + teamsSG[5] + teamsSF[5] + teamsPF[5] + teamsC[5] >= 3) or
               (teamsPG[6] + teamsSG[6] + teamsSF[6] + teamsPF[6] + teamsC[6] >= 3) or
               (teamsPG[7] + teamsSG[7] + teamsSF[7] + teamsPF[7] + teamsC[7] >= 3) or
               (teamsPG[8] + teamsSG[8] + teamsSF[8] + teamsPF[8] + teamsC[8] >= 3) or
               (teamsPG[9] + teamsSG[9] + teamsSF[9] + teamsPF[9] + teamsC[9] >= 3) or
               (teamsPG[10] + teamsSG[10] + teamsSF[10] + teamsPF[10] + teamsC[10] >= 3) or
               (teamsPG[11] + teamsSG[11] + teamsSF[11] + teamsPF[11] + teamsC[11] >= 3) or
               (teamsPG[12] + teamsSG[12] + teamsSF[12] + teamsPF[12] + teamsC[12] >= 3) or
               (teamsPG[13] + teamsSG[13] + teamsSF[13] + teamsPF[13] + teamsC[13] >= 3) or
               (teamsPG[14] + teamsSG[14] + teamsSF[14] + teamsPF[14] + teamsC[14] >= 3) or
               (teamsPG[15] + teamsSG[15] + teamsSF[15] + teamsPF[15] + teamsC[15] >= 3) or
               (teamsPG[16] + teamsSG[16] + teamsSF[16] + teamsPF[16] + teamsC[16] >= 3) or
               (teamsPG[17] + teamsSG[17] + teamsSF[17] + teamsPF[17] + teamsC[17] >= 3) or
               (teamsPG[18] + teamsSG[18] + teamsSF[18] + teamsPF[18] + teamsC[18] >= 3) or
               (teamsPG[19] + teamsSG[19] + teamsSF[19] + teamsPF[19] + teamsC[19] >= 3) or
               (teamsPG[20] + teamsSG[20] + teamsSF[20] + teamsPF[20] + teamsC[20] >= 3) or
               (teamsPG[21] + teamsSG[21] + teamsSF[21] + teamsPF[21] + teamsC[21] >= 3) or
               (teamsPG[22] + teamsSG[22] + teamsSF[22] + teamsPF[22] + teamsC[22] >= 3) or
               (teamsPG[23] + teamsSG[23] + teamsSF[23] + teamsPF[23] + teamsC[23] >= 3) or
               (teamsPG[24] + teamsSG[24] + teamsSF[24] + teamsPF[24] + teamsC[24] >= 3) or
               (teamsPG[25] + teamsSG[25] + teamsSF[25] + teamsPF[25] + teamsC[25] >= 3) or
               (teamsPG[26] + teamsSG[26] + teamsSF[26] + teamsPF[26] + teamsC[26] >= 3) or
               (teamsPG[27] + teamsSG[27] + teamsSF[27] + teamsPF[27] + teamsC[27] >= 3) or
               (teamsPG[28] + teamsSG[28] + teamsSF[28] + teamsPF[28] + teamsC[28] >= 3) or
               (teamsPG[29] + teamsSG[29] + teamsSF[29] + teamsPF[29] + teamsC[29] >= 3))

    # Add constraint to adjust for lineup overlap
    for i in range(0, len(lineups)):
        solver.Add(lCrossC[i] + lCrossSG[i] + lCrossSF[i] + lCrossPF[i] + lCrossPG[i] <= 3)

    # Max 4 players per team
    for i in range(0, 29):
        solver.Add(teamsPG[i] + teamsC[i] + teamsPF[i] + teamsSG[i] + teamsSF[i] <= 4)

    solver.Maximize(valueC + valuePG + valuePF + valueSG + valueSF)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print('Solved in', solver.wall_time(), 'milliseconds!', "\n")

    salary = 0
    projection = 0
    tempLineup = [[], [], [], [], []]
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

    for i in rangePF:
        if (takePF[i].SolutionValue()):
            salary += players[2][i][2]
            projection += players[2][i][1]
            tempLineup[2].append(players[2][i][0])

    for i in rangeSG:
        if (takeSG[i].SolutionValue()):
            salary += players[3][i][2]
            projection += players[3][i][1]
            tempLineup[3].append(players[3][i][0])

    for i in rangeSF:
        if (takeSF[i].SolutionValue()):
            salary += players[4][i][2]
            projection += players[4][i][1]
            tempLineup[4].append(players[4][i][0])

    rC = range(0, len(tempLineup[0]))
    rPG = range(0, len(tempLineup[1]))
    rPF = range(0, len(tempLineup[2]))
    rSG = range(0, len(tempLineup[3]))
    rSF = range(0, len(tempLineup[4]))

    currLineup = [0, 0, 0, 0, 0, 0, 0, 0]

    countC = 0
    countPG = 0
    countPF = 0
    countSG = 0
    countSF = 0

    for i in rC:
        if countC == 0:
            currLineup[4] = tempLineup[0][i]
            countC = countC + 1
        elif countC == 1:
            currLineup[7] = tempLineup[0][i]
            countC = countC + 1

    for i in rPG:
        if countPG == 0:
            currLineup[0] = tempLineup[1][i]
            countPG = countPG + 1
        elif countPG == 1:
            currLineup[5] = tempLineup[1][i]
            countPG = countPG + 1
        elif countPG == 2:
            currLineup[7] = tempLineup[1][i]
            countPG = countPG + 1

    for i in rPF:
        if countPF == 0:
            currLineup[3] = tempLineup[2][i]
            countPF = countPF + 1
        elif countPF == 1:
            currLineup[6] = tempLineup[2][i]
            countPF = countPF + 1
        elif countPF == 2:
            currLineup[7] = tempLineup[2][i]
            countPF = countPF + 1

    for i in rSG:
        if countSG == 0:
            currLineup[1] = tempLineup[3][i]
            countSG = countSG + 1
        elif countSG == 1:
            currLineup[5] = tempLineup[3][i]
            countSG = countSG + 1
        elif countSG == 2:
            currLineup[7] = tempLineup[3][i]
            countSG = countSG + 1

    for i in rSF:
        if countSF == 0:
            currLineup[2] = tempLineup[4][i]
            countSF = countSF + 1
        elif countSF == 1:
            currLineup[6] = tempLineup[4][i]
            countSF = countSF + 1
        elif countSF == 2:
            currLineup[7] = tempLineup[4][i]
            countSF = countSF + 1

    return [currLineup, salary, projection]


players = [[], [], [], [], []]

with open('playersNBA.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)

    for row in spamreader:
        players[getPositionNumber(row['Subposition'])].append(
            [row['Name'], float(row['Value']), int(row['Salary']), int(row['Team'])]
        )


def lineups(numLineups):
    lineupList = []
    resultList = []
    lineupList.append(['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'])

    for i in range(0, numLineups):
        results = lineupBuilder(players, salaryCap, lineupList)
        lineupList.append(results[0])
        resultList.append(results)

    lineupsOnly = [['PG', 'SG', 'SF', 'PF', 'C', 'G', 'F', 'UTIL']]

    for i in range(1, numLineups):
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


print(lineups(20))
