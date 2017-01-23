import csv

with open('jutarnji.list_facebook_statuses.csv', 'rt', encoding='utf-8') as f:
    reader = csv.reader(f)
    statuses_j = ([(post[1]) for post in reader])

print(statuses_j)

corp = open('corp.txt', 'w', encoding='utf-8')
for a in statuses_j:
    corp.write(a)
