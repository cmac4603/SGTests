import csv

with open('CSV Test Sheet.csv', newline='') as test:
    testreader = csv.reader(test, delimiter=',', quotechar='|')
    for row in testreader:
        print(' '.join(row))
