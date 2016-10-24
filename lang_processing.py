import csv
import nltk


with open('jutarnji_facebook_comments.csv', 'rb') as f:
    reader = csv.reader(f)
    comments = ([(comment[3]) for comment in reader])



splited = [c.split(' ') for c in comments]

i = 0
sum = 0
for c in splited:
    sum += len(c)
    i += 1

print sum / i