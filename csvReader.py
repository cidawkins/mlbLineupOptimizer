import csv

players = []
projections = []

with open('players.csv') as csvDataFile:
    csvReader = csv.reader(csvDataFile)
    for row in csvReader:
        players.append(row[0])
        projections.append(row[1])

print(players)
print(projections)