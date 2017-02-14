import nltk
import sqlite3
from nltk import TweetTokenizer
import re
from nltk import FreqDist
import random

#hardware - Ostale hardverske teme, Benchmark, Tvrdi i optički diskovi, Mrežni hardver, Grafičke kartice, Overclocking
#software - FB developers, Razvoj web-stranica, Programiranje, Ostale softverske teme, Sigurnosni softver
#igre - Komentari Games Master vijesti, PC igre, Web igre, Igraće konzole, Igre - općenito,
#non-it - Filmovi, TV serije, glazba..., Sport, Ostalo, Automobili, motori, bicikli...


Q_HARDWARE = "select text from scraped where scraped.tema = 'Ostale hardverske teme' or scraped.tema = 'Benchmark' or scraped.tema = 'Tvrdi i optički diskovi' or scraped.tema = 'Mrežni hardver' or scraped.tema = 'Grafičke kartice' or scraped.tema = 'Overclocking'"
Q_SOFTWARE = "select text from scraped where scraped.tema = 'FB developers' or scraped.tema = 'Razvoj web-stranica' or scraped.tema = 'Programiranje' or scraped.tema = 'Ostale softverske teme' or scraped.tema = 'Sigurnosni softver'"
Q_IGRE = "select text from scraped where scraped.tema = 'Komentari Games Master vijesti' or scraped.tema = 'PC igre' or scraped.tema = 'Web igre' or scraped.tema = 'Igraće konzole' or scraped.tema = 'Igre - općenito'"
Q_NONIT = "select text from scraped where scraped.tema = 'Filmovi, TV serije, glazba...' or scraped.tema = 'Sport' or scraped.tema = 'Ostalo' or scraped.tema = 'Automobili, motori, bicikli...'"


def get_posts_labeled(query, label):

    try:

        print("Fetching posts with label: %s" % label)
        connection = sqlite3.connect('baza.db')
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    except sqlite3.Error:
        print(sqlite3.Error)

    data = [a[0] for a in data]

    labeled = ([(post, label) for post in data])

    return labeled


def get_features(post):

    features = {}

    tknz = TweetTokenizer(preserve_case=False)
    tokens = tknz.tokenize(post)

    fil = re.compile('.*[A-Za-z0-9].*')
    urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    tokens = [w for w in tokens if fil.match(w)]
    tokens = [w for w in tokens if not urls.match(w)]

    features['number_tokens'] = len(tokens)
    features['first_token'] = tokens[0]

    tokens = [w for w in tokens if len(w) > 4]

    hardware_tokens = cat_tokens(Q_HARDWARE)
    software_tokens = cat_tokens(Q_SOFTWARE)
    igre_tokens = cat_tokens(Q_IGRE)
    ostalo_tokens = cat_tokens(Q_NONIT)

    """
    all_t = [hardware_tokens, software_tokens, igre_tokens, ostalo_tokens]
    for cat in all_t:
        counter = 0
        for t in cat:
            counter += tokens.count(t)
    """
    counter = 0
    for t in hardware_tokens:
        counter += tokens.count(t)
    features['hardware_tokens'] = counter

    counter = 0
    for t in software_tokens:
        counter += tokens.count(t)
    features['software_tokens'] = counter

    counter = 0
    for t in igre_tokens:
        counter += tokens.count(t)
    features['igre_tokens'] = counter

    counter = 0
    for t in ostalo_tokens:
        counter += tokens.count(t)
    features['ostalo_tokens'] = counter


    return features

def cat_tokens(query):

    connection = sqlite3.connect('baza.db')
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        data = cursor.fetchall()

        print("Fetching data query: %s \n" % query[:10])

        data = [a[0] for a in data]
        data = " ".join(data)
    except sqlite3.Error:
        print(sqlite3.Error)

    tknz = TweetTokenizer(preserve_case=False)

    try:
        print("Tokenizing category text...")
        tokens = tknz.tokenize(data)
        print("Got %d tokens!\n" % len(tokens))
    except:
        print("Error tokenizing text!")


    fil = re.compile('.*[A-Za-z0-9].*')
    urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    tokens = [w for w in tokens if fil.match(w)]
    tokens = [w for w in tokens if not urls.match(w)]

    tokens = [w for w in tokens if len(w) > 3]
    fdist = FreqDist(tokens)
    most_common = fdist.most_common(30)
    ctokens = [w[0] for w in most_common]

    return ctokens


if __name__ == '__main__':

    hardware_posts = get_posts_labeled(Q_HARDWARE, 'Hardware')
    software_posts = get_posts_labeled(Q_SOFTWARE, 'Software')
    ostalo_posts = get_posts_labeled(Q_NONIT, 'Ostalo')
    games_posts = get_posts_labeled(Q_IGRE, 'Igre')

    labeled_posts = hardware_posts[:int(len(hardware_posts)/1.5)] + software_posts[:int(len(software_posts)/1.5)] \
                    + ostalo_posts[:int(len(ostalo_posts)/1.5)] + games_posts[:int(len(games_posts)/1.5)]

    random.shuffle(labeled_posts)
    feature_sets = [(get_features(post), cat) for (post, cat) in labeled_posts]
    train_set, test_set = feature_sets[:len(feature_sets) - 100], feature_sets[len(feature_sets) - 100:]

    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))



    pass
