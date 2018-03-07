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

    # Stack at least three hitters from the same team (This is saying that there has to be at least "0" or more players
    # per team.  This is not what needs to be done for stacking, and needs to be fixed!


    # Add constraint to adjust for lineup overlap
    for i in range(0, len(lineups)):
        solver.Add(lCrossC[i] + lCross1B[i] + lCross2B[i] + lCross3B[i] + lCrossSS[i] + lCrossOF[i] <= 3)

    # Add constraint to add pitcher to stack



    solver.Maximize(valueP + valueC + value1B + value2B + value3B + valueSS + valueOF)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print('Solved in', solver.wall_time(), 'milliseconds!', "\n")

    salary = 0

    for i in rangeP:
        if (takeP[i].SolutionValue()):
            salary += players[0][i][2]
            currLineup.append(players[0][i][0])

    for i in rangeC:
        if (takeC[i].SolutionValue()):
            salary += players[1][i][2]
            currLineup.append(players[1][i][0])

    for i in range1B:
        if (take1B[i].SolutionValue()):
            salary += players[2][i][2]
            currLineup.append(players[2][i][0])

    for i in range2B:
        if (take2B[i].SolutionValue()):
            salary += players[3][i][2]
            currLineup.append(players[3][i][0])

    for i in range3B:
        if (take3B[i].SolutionValue()):
            salary += players[4][i][2]
            currLineup.append(players[4][i][0])

    for i in rangeSS:
        if (takeSS[i].SolutionValue()):
            salary += players[5][i][2]
            currLineup.append(players[5][i][0])

    for i in rangeOF:
        if (takeOF[i].SolutionValue()):
            salary += players[6][i][2]
            currLineup.append(players[6][i][0])


    return currLineup

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
    lineupList.append(['x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x', 'x'])

    for i in range(0, numLineups):
        lineupList.append(lineupBuilder(players, salaryCap, lineupList))

    return lineupList

print(lineups(2))



