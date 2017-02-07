import csv
import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()

with open('developers_fb.csv', 'rt', encoding='utf-8') as f:
    reader = csv.reader(f)
    for c in reader:
        fb_post = [(None, c[1], None, c[6], 'Dev_hr')]
        cur.executemany('INSERT INTO mydata VALUES (?,?,?,?,?)', fb_post)
    con.commit()
