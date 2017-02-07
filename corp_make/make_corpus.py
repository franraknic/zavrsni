import csv
import re
from nltk.corpus.reader import plaintext
from nltk.probability import FreqDist
from nltk.tokenize import *
import nltk
from nltk.util import ngrams


def csv_corpus(filename, data_index, size = 0):

    with open(filename, 'rt', encoding='utf-8') as file:
        reader = csv.reader(file)
        data = [(p[data_index]) for p in reader]

    print('Lines in CSV: %d \n' % len(data))

    corp = open((filename[:-4] + '_corp.txt'), 'w', encoding='utf-8')
    for a in data:
        corp.write(a)

    print('Written to file: %s' % (filename[:-4] + '_corp.txt'))


def clean_html(html):

    # First we remove inline JavaScript/CSS:
    cleaned = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", html.strip())
    # Then we remove html comments. This has to be done before removing regular
    # tags since comments can contain '>' characters.
    cleaned = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", cleaned)
    # Next we can remove the remaining tags:
    cleaned = re.sub(r"(?s)<.*?>", " ", cleaned)
    # Finally, we deal with whitespace
    cleaned = re.sub(r"&nbsp;", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    cleaned = re.sub(r"  ", " ", cleaned)
    return cleaned.strip()

if __name__ == '__main__':

    #csv_corpus('jobs.csv', 1)
    reader = plaintext.PlaintextCorpusReader('F:\zavrsni\corp_make', 'jobs_corp.txt', encoding='utf-8')

    print('Number of words in corpus %d' % len(reader.words()))

    s = reader.words()
    long_words = [w for w in s if len(w) > 3]
    long_words = [w.lower() for w in long_words]
    print(long_words)

    fdist = FreqDist(long_words)
    print(fdist.most_common(20))

    s = nltk.Text(s)
    print(s.concordance('php'))

    #s.dispersion_plot(['php', 'python', 'javascript', 'c++', 'c'])

    #fdist.plot(5, cumulative=False)

    print(list(ngrams(s, 4)))