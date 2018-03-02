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

def main(players, salaryCap):
    solver = pywraplp.Solver('CoinsGridCLP', pywraplp.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

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

    valueP = solver.Sum([players[0][i][1] * takeP[i] for i in rangeP])
    valueC = solver.Sum([players[1][i][1] * takeC[i] for i in rangeC])
    value1B = solver.Sum([players[2][i][1] * take1B[i] for i in range1B])
    value2B = solver.Sum([players[3][i][1] * take2B[i] for i in range2B])
    value3B = solver.Sum([players[4][i][1] * take3B[i] for i in range3B])
    valueSS = solver.Sum([players[5][i][1] * takeSS[i] for i in rangeSS])
    valueOF = solver.Sum([players[6][i][1] * takeOF[i] for i in rangeOF])

    salaryP = solver.Sum([players[0][i][1] * takeP[i] for i in rangeP])
    salaryC = solver.Sum([players[1][i][1] * takeC[i] for i in rangeC])
    salary1B = solver.Sum([players[2][i][1] * take1B[i] for i in range1B])
    salary2B = solver.Sum([players[3][i][1] * take2B[i] for i in range2B])
    salary3B = solver.Sum([players[4][i][1] * take3B[i] for i in range3B])
    salarySS = solver.Sum([players[5][i][1] * takeSS[i] for i in rangeSS])
    salaryOF = solver.Sum([players[6][i][1] * takeOF[i] for i in rangeOF])

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

    solver.Maximize(valueP + valueC + value1B + value2B + value3B + valueSS + valueOF)
    solver.Solve()
    assert solver.VerifySolution(1e-7, True)
    print('Solved in', solver.wall_time(), 'milliseconds!', "\n")

    salary = 0

    for i in rangeP:
        if (takeP[i].SolutionValue()):
            salary += players[0][i][2]
            print(players[0][i][0], '(P): ${:,d}'.format(players[0][i][2]), '(' + str(players[0][i][1]) + ')')

    for i in rangeC:
        if (takeC[i].SolutionValue()):
            salary += players[1][i][2]
            print(players[1][i][0], '(C): ${:,d}'.format(players[1][i][2]), '(' + str(players[1][i][1]) + ')')

    for i in range1B:
        if (take1B[i].SolutionValue()):
            salary += players[2][i][2]
            print(players[2][i][0], '(1B): ${:,d}'.format(players[2][i][2]), '(' + str(players[2][i][1]) + ')')

    for i in range2B:
        if (take2B[i].SolutionValue()):
            salary += players[3][i][2]
            print(players[3][i][0], '(2B): ${:,d}'.format(players[3][i][2]), '(' + str(players[3][i][1]) + ')')

    for i in range3B:
        if (take3B[i].SolutionValue()):
            salary += players[4][i][2]
            print(players[4][i][0], '(3B): ${:,d}'.format(players[4][i][2]), '(' + str(players[4][i][1]) + ')')

    for i in rangeSS:
        if (takeSS[i].SolutionValue()):
            salary += players[5][i][2]
            print(players[5][i][0], '(SS): ${:,d}'.format(players[5][i][2]), '(' + str(players[5][i][1]) + ')')

    for i in rangeOF:
        if (takeOF[i].SolutionValue()):
            salary += players[6][i][2]
            print(players[6][i][0], '(OF): ${:,d}'.format(players[6][i][2]), '(' + str(players[6][i][1]) + ')')

    print("\n", 'Total: ${:,d}'.format(salary), '(' + str(solver.Objective().Value()) + ')')

    if (len(sys.argv) < 2):
        print('Usage:', sys.executable, sys.argv[0], 'players.csv')
        sys.exit(1)

players = [[], [], [], [], [], [], []]

with open('players.csv', 'r') as csvfile:
    spamreader = csv.DictReader(csvfile)

    for row in spamreader:
        players[getPosNum(row['Subposition'])].append(
            [row['Name'], float(row['Value']), int(row['Salary']), int(row['Team'])]
        )

main(players, salaryCap)



