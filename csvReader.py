import csv

class stats:

    def __init__(self, fname):
        self.players = []
        self.projections = []

        with open(fname) as csvDataFile:
            csvReader = csv.reader(csvDataFile)
            for row in csvReader:
                self.players.append(row[0])
                self.projections.append(row[1])