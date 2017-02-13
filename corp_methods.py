from nltk import word_tokenize
from nltk.tokenize import *
import nltk
import sqlite3
from nltk import collocations
from nltk import FreqDist
import re

Q_ALL = "select text from scraped limit 10000"
Q_FBONLY = "select text from scraped where scraped.tema"\
            "= 'FB sistemci' OR scraped.tema = 'FB developers' OR scraped.tema = 'FB jobs'"
Q_BUGONLY = "select text,tema from scraped where"\
            " tema <> 'FB sistemci' and tema <> 'FB developers' and tema <> 'FB jobs'"

def theme_posts(num_posts=0):
    """Returns a number of posts per theme"""
    con = sqlite3.connect('baza.db')
    cur = con.cursor()

    cur.execute('select distinct scraped.tema from scraped')
    teme = cur.fetchall()

    lst = []

    for t in teme:
        cur.execute('select count(*), tema from scraped where scraped.tema = ?', t)
        lst.append(cur.fetchone())

    for t in lst:
        if t[0] > num_posts:
            print(t)


def all_posts():
    """Returns a list of strings representing posts from the database"""
    con = sqlite3.connect('baza.db')
    cur = con.cursor()

    cur.execute(Q_FBONLY)
    all = cur.fetchall()
    all = [a[0] for a in all]
    return all


def tweet_tokenize(text):

    tkn = nltk.TweetTokenizer()
    tokens = tkn.tokenize(text)
    return tokens

def avg_tokens(post_tokens):

    tokens = 0
    sum_tokens = 0

    for post in post_tokens:

        tokens = len(post)
        sum_tokens =+ tokens

    return sum_tokens / len(post_tokens)

def query_mysql(database, query, limit=100):

    connection = sqlite3.connect(database)
    cursor = connection.cursor()

    cursor.execute(query)
    return cursor.fetchall()

if __name__ == '__main__':

    data = query_mysql('baza.db', Q_ALL)
    texts = [a[0] for a in data]
    big_string = ' '.join(texts)


    #retard_tokenized = big_string.split(' ')

    tknzr = nltk.TweetTokenizer(preserve_case=False)

    tokens = tknzr.tokenize(big_string)

    tokensNLTK = nltk.Text(tokens)

    #tokens4 = [w for w in tokens if len(w) >= 4]

    #tokens4 = nltk.Text(tokens4)
    #tokens4.collocations(50)

    fil = re.compile('.*[A-Za-z0-9].*')
    url = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    no_punc = [t for t in tokens if fil.match(t)]
    no_links = [t for t in no_punc if not url.match(t)]

    freq = FreqDist(no_punc)

    gg = freq.most_common(200)


    wtf = 'HAHA'
    pass
"""
    tst = 'Nikada ti nisam rekao volim te'
    tst = tst.split(' ')
    tknzr = MWETokenizer([('volim', 'te')])
    g = tknzr.tokenize(tst)
"""


