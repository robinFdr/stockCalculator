import json
import csv

with open('./Germany 5 Year Bobl Yield_5years_weekly.json') as f:
    data = json.load(f)
with open("./Germany 5 Year Bobl Yield_5years_weekly.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile, delimiter=";", quoting=csv.QUOTE_ALL)
    writer.writerow(['date', 'x', 'y', 'percentChange', 'change'])
    for row in data:
        writer.writerow([row['date'], row['x'], row['y'], row['percentChange'], row['change']])