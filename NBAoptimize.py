from ortools.linear_solver import pywraplp

salaryCap = 50000

def getPosNum(name):
    return {
        'Center': 0,
        'Point Guard': 1,
        'Power Forward': 2,
        'Shooting Guard': 3,
        'Small Forward': 4
    }[name]







