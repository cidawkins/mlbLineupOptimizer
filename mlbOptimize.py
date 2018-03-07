import csv, sys
from ortools.linear_solver import pywraplp

salaryCap = 50000

def getPosNum(name):
    return {
        'SP': 0,
        'RP': 0,
        'P': 0,
        'SP, RP': 0,
        'C': 1,
        '1B': 2,
        '2B': 3,
        '3B': 4,
        'SS': 5,
        'OF': 6
    }[name]

def getTeamNum(team):
    return {
        'BOS': 0,
        'NYY': 1,
        'TB': 2,
        'TOR': 3,
        'BAL': 4,
        'CHW': 5,
        'MIN': 6,
        'KC': 7,
        'DET': 8,
        'CLE': 9,
        'OAK': 10,
        'LAA': 11,
        'HOU': 12,
        'TEX': 13,
        'SEA': 14,
        'ATL': 15,
        'PHI': 16,
        'NYM': 17,
        'WAS': 18,
        'MIA': 19,
        'CHC': 20,
        'PIT': 21,
        'CIN': 22,
        'MIL': 23,
        'STL': 24,
        'LAD': 25,
        'SF': 26,
        'SD': 27,
        'COL': 28,
        'ARI': 29
    }[team]

def lineupBuilder(players, salaryCap, lineups):
    solver = pywraplp.Solver('CoinsGridCLP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    currLineup = []

    rangeP = range(len(players[0]))
    rangeC = range(len(players[1]))
    range1B = range(len(players[2]))
    range2B = range(len(players[3]))
    range3B = range(len(players[4]))
    rangeSS = range(len(players[5]))
    rangeOF = range(len(players[6]))

    takeP = [solver.IntVar(0, 1, 'takeP[%i]' % j) for j in rangeP]
    takeC = [solver.IntVar(0, 1, 'takeC[%i]' % j) for j in rangeC]
    take1B = [solver.IntVar(0, 1, 'take1B[%i]' % j) for j in range1B]
    take2B = [solver.IntVar(0, 1, 'take2B[%i]' % j) for j in range2B]
    take3B = [solver.IntVar(0, 1, 'take3B[%i]' % j) for j in range3B]
    takeSS = [solver.IntVar(0, 1, 'takeSS[%i]' % j) for j in rangeSS]
    takeOF = [solver.IntVar(0, 1, 'takeOF[%i]' % j) for j in rangeOF]

    teamsP = []
    teamsC = []
    teams1B = []
    teams2B = []
    teams3B = []
    teamsSS = []
    teamsOF = []

    for teamNumber in range(0, 29):
        teamsP.insert(teamNumber, solver.Sum([(players[0][i][3] == teamNumber + 1) * takeP[i] for i in rangeP]))
        teamsC.insert(teamNumber, solver.Sum([(players[1][i][3] == teamNumber + 1) * takeC[i] for i in rangeC]))
        teams1B.insert(teamNumber, solver.Sum([(players[2][i][3] == teamNumber + 1) * take1B[i] for i in range1B]))
        teams2B.insert(teamNumber, solver.Sum([(players[3][i][3] == teamNumber + 1) * take2B[i] for i in range2B]))
        teams3B.insert(teamNumber, solver.Sum([(players[4][i][3] == teamNumber + 1) * take3B[i] for i in range3B]))
        teamsSS.insert(teamNumber, solver.Sum([(players[5][i][3] == teamNumber + 1) * takeSS[i] for i in rangeSS]))
        teamsOF.insert(teamNumber, solver.Sum([(players[6][i][3] == teamNumber + 1) * takeOF[i] for i in rangeOF]))

    lCrossP = []
    lCrossC = []
    lCross1B = []
    lCross2B = []
    lCross3B = []
    lCrossSS = []
    lCrossOF = []

    for j in range(0, len(lineups)):
        lCrossP.insert(j, solver.Sum([((players[0][i][0] == lineups[j][0]) or (players[0][i][0] == lineups[j][1])) * takeP[i] for i in rangeP]))
        lCrossC.insert(j, solver.Sum([(players[1][i][0] == lineups[j][2]) * takeC[i] for i in rangeC]))
        lCross1B.insert(j, solver.Sum([(players[2][i][0] == lineups[j][3]) * take1B[i] for i in range1B]))
        lCross2B.insert(j, solver.Sum([(players[3][i][0] == lineups[j][4]) * take2B[i] for i in range2B]))
        lCross3B.insert(j, solver.Sum([(players[4][i][0] == lineups[j][5]) * take3B[i] for i in range3B]))
        lCrossSS.insert(j, solver.Sum([(players[5][i][0] == lineups[j][6]) * takeSS[i] for i in rangeSS]))
        lCrossOF.insert(j, solver.Sum([((players[6][i][0] == lineups[j][7]) or (players[6][i][0] == lineups[j][8]) or (players[6][i][0] == lineups[j][9])) * takeOF[i] for i in rangeOF]))

    valueP = solver.Sum([players[0][i][1] * takeP[i] for i in rangeP])
    valueC = solver.Sum([players[1][i][1] * takeC[i] for i in rangeC])
    value1B = solver.Sum([players[2][i][1] * take1B[i] for i in range1B])
    value2B = solver.Sum([players[3][i][1] * take2B[i] for i in range2B])
    value3B = solver.Sum([players[4][i][1] * take3B[i] for i in range3B])
    valueSS = solver.Sum([players[5][i][1] * takeSS[i] for i in rangeSS])
    valueOF = solver.Sum([players[6][i][1] * takeOF[i] for i in rangeOF])

    salaryP = solver.Sum([players[0][i][2] * takeP[i] for i in rangeP])
    salaryC = solver.Sum([players[1][i][2] * takeC[i] for i in rangeC])
    salary1B = solver.Sum([players[2][i][2] * take1B[i] for i in range1B])
    salary2B = solver.Sum([players[3][i][2] * take2B[i] for i in range2B])
    salary3B = solver.Sum([players[4][i][2] * take3B[i] for i in range3B])
    salarySS = solver.Sum([players[5][i][2] * takeSS[i] for i in rangeSS])
    salaryOF = solver.Sum([players[6][i][2] * takeOF[i] for i in rangeOF])

    solver.Add(salaryP + salaryC + salary1B + salary2B + salary3B + salarySS + salaryOF <= salaryCap)

    # Sets number of player to pick per position.  Can this be adjusted for a utility slot?
    solver.Add(solver.Sum(takeP[i] for i in rangeP) == 2)
    solver.Add(solver.Sum(takeC[i] for i in rangeC) == 1)
    solver.Add(solver.Sum(take1B[i] for i in range1B) == 1)
    solver.Add(solver.Sum(take2B[i] for i in range2B) == 1)
    solver.Add(solver.Sum(take3B[i] for i in range3B) == 1)
    solver.Add(solver.Sum(takeSS[i] for i in rangeSS) == 1)
    solver.Add(solver.Sum(takeOF[i] for i in rangeOF) == 3)

    # Max 5 hitters per team
    for i in range(0, 29):
        solver.Add(teamsC[i] + teams1B[i] + teams2B[i] + teams3B[i] + teamsSS[i] + teamsOF[i] <= 5)

    # Stack at least three hitters from the same team.  THis seems like a very sloppy way of doing it, but it does work
    solver.Add((teamsC[0] + teams1B[0] + teams2B[0] + teams3B[0] + teamsSS[0] + teamsOF[0] >= 3) or
               (teamsC[1] + teams1B[1] + teams2B[1] + teams3B[1] + teamsSS[1] + teamsOF[1] >= 3) or
               (teamsC[2] + teams1B[2] + teams2B[2] + teams3B[2] + teamsSS[2] + teamsOF[2] >= 3) or
               (teamsC[3] + teams1B[3] + teams2B[3] + teams3B[3] + teamsSS[3] + teamsOF[3] >= 3) or
               (teamsC[4] + teams1B[4] + teams2B[4] + teams3B[4] + teamsSS[4] + teamsOF[4] >= 3) or
               (teamsC[5] + teams1B[5] + teams2B[5] + teams3B[5] + teamsSS[5] + teamsOF[5] >= 3) or
               (teamsC[6] + teams1B[6] + teams2B[6] + teams3B[6] + teamsSS[6] + teamsOF[6] >= 3) or
               (teamsC[7] + teams1B[7] + teams2B[7] + teams3B[7] + teamsSS[7] + teamsOF[7] >= 3) or
               (teamsC[8] + teams1B[8] + teams2B[8] + teams3B[8] + teamsSS[8] + teamsOF[8] >= 3) or
               (teamsC[9] + teams1B[9] + teams2B[9] + teams3B[9] + teamsSS[9] + teamsOF[9] >= 3) or
               (teamsC[10] + teams1B[10] + teams2B[10] + teams3B[10] + teamsSS[10] + teamsOF[10] >= 3) or
               (teamsC[11] + teams1B[11] + teams2B[11] + teams3B[11] + teamsSS[11] + teamsOF[11] >= 3) or
               (teamsC[12] + teams1B[12] + teams2B[12] + teams3B[12] + teamsSS[12] + teamsOF[12] >= 3) or
               (teamsC[13] + teams1B[13] + teams2B[13] + teams3B[13] + teamsSS[13] + teamsOF[13] >= 3) or
               (teamsC[14] + teams1B[14] + teams2B[14] + teams3B[14] + teamsSS[14] + teamsOF[14] >= 3) or
               (teamsC[15] + teams1B[15] + teams2B[15] + teams3B[15] + teamsSS[15] + teamsOF[15] >= 3) or
               (teamsC[16] + teams1B[16] + teams2B[16] + teams3B[16] + teamsSS[16] + teamsOF[16] >= 3) or
               (teamsC[17] + teams1B[17] + teams2B[17] + teams3B[17] + teamsSS[17] + teamsOF[17] >= 3) or
               (teamsC[18] + teams1B[18] + teams2B[18] + teams3B[18] + teamsSS[18] + teamsOF[18] >= 3) or
               (teamsC[19] + teams1B[19] + teams2B[19] + teams3B[19] + teamsSS[19] + teamsOF[19] >= 3) or
               (teamsC[20] + teams1B[20] + teams2B[20] + teams3B[20] + teamsSS[20] + teamsOF[20] >= 3) or
               (teamsC[21] + teams1B[21] + teams2B[21] + teams3B[21] + teamsSS[21] + teamsOF[21] >= 3) or
               (teamsC[22] + teams1B[22] + teams2B[22] + teams3B[22] + teamsSS[22] + teamsOF[22] >= 3) or
               (teamsC[23] + teams1B[23] + teams2B[23] + teams3B[23] + teamsSS[23] + teamsOF[23] >= 3) or
               (teamsC[24] + teams1B[24] + teams2B[24] + teams3B[24] + teamsSS[24] + teamsOF[24] >= 3) or
               (teamsC[25] + teams1B[25] + teams2B[25] + teams3B[25] + teamsSS[25] + teamsOF[25] >= 3) or
               (teamsC[26] + teams1B[26] + teams2B[26] + teams3B[26] + teamsSS[26] + teamsOF[26] >= 3) or
               (teamsC[27] + teams1B[27] + teams2B[27] + teams3B[27] + teamsSS[27] + teamsOF[27] >= 3) or
               (teamsC[28] + teams1B[28] + teams2B[28] + teams3B[28] + teamsSS[28] + teamsOF[28] >= 3) or
               (teamsC[29] + teams1B[29] + teams2B[29] + teams3B[29] + teamsSS[29] + teamsOF[29] >= 3))

    # Add constraint to adjust for lineup overlap
    for i in range(0, len(lineups)):
        solver.Add(lCrossC[i] + lCross1B[i] + lCross2B[i] + lCross3B[i] + lCrossSS[i] + lCrossOF[i] <= 3)

    # Add constraint to add pitcher to stack



    solver.Maximize(valueP + valueC + value1B + value2B + value3B + valueSS + valueOF)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print('Solved in', solver.wall_time(), 'milliseconds!', "\n")

    salary = 0
    projection = 0

    for i in rangeP:
        if (takeP[i].SolutionValue()):
            salary += players[0][i][2]
            projection += players[0][i][1]
            currLineup.append(players[0][i][0])

    for i in rangeC:
        if (takeC[i].SolutionValue()):
            salary += players[1][i][2]
            projection += players[1][i][1]
            currLineup.append(players[1][i][0])

    for i in range1B:
        if (take1B[i].SolutionValue()):
            salary += players[2][i][2]
            projection += players[2][i][1]
            currLineup.append(players[2][i][0])

    for i in range2B:
        if (take2B[i].SolutionValue()):
            salary += players[3][i][2]
            projection += players[3][i][1]
            currLineup.append(players[3][i][0])

    for i in range3B:
        if (take3B[i].SolutionValue()):
            salary += players[4][i][2]
            projection += players[4][i][1]
            currLineup.append(players[4][i][0])

    for i in rangeSS:
        if (takeSS[i].SolutionValue()):
            salary += players[5][i][2]
            projection += players[5][i][1]
            currLineup.append(players[5][i][0])

    for i in rangeOF:
        if (takeOF[i].SolutionValue()):
            salary += players[6][i][2]
            projection += players[6][i][1]
            currLineup.append(players[6][i][0])


    return [currLineup, salary, projection]

players = [[], [], [], [], [], [], []]

with open('players.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)

    for row in spamreader:
        players[getPosNum(row['Subposition'])].append(
            [row['Name'], float(row['Value']), int(row['Salary']), int(row['Team'])]
        )


# Make multiple lineups

def lineups(numLineups):

    lineupList = []
    resultList = []
    lineupList.append(['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'])

    for i in range(0, numLineups):
        results = lineupBuilder(players, salaryCap, lineupList)
        lineupList.append(results[0])
        resultList.append(results)

    return resultList

print(lineups(10))



