from nltk import word_tokenize
import nltk
import sqlite3

con = sqlite3.connect('baza.db')
cur = con.cursor()

cur.execute('select distinct scraped.tema from scraped')
teme = cur.fetchall()

lst = []

for t in teme:
    cur.execute('select count(*), tema from scraped where scraped.tema = ?', t)
    lst.append(cur.fetchone())

for t in lst:
    if t[0] > 1000:
        print t
