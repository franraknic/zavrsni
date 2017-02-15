import nltk
import sqlite3
from nltk import TweetTokenizer
import re
from nltk import FreqDist
import random
from stemmer.Croatian_stemmer_port import kor_tokens

#hardware - Ostale hardverske teme, Benchmark, Tvrdi i optički diskovi, Mrežni hardver, Grafičke kartice, Overclocking, Periferija
#software - FB developers, Razvoj web-stranica, Programiranje, Ostale softverske teme, Sigurnosni softver, Programiranje za mobilne platforme
#igre - Komentari Games Master vijesti, PC igre, Web igre, Igraće konzole, Igre - općenito,
#non-it - Filmovi, TV serije, glazba..., Sport, Ostalo, Automobili, motori, bicikli..., Komentari Osobnog stava


limit = ""

Q_HARDWARE = "select text from scraped where scraped.tema = 'Ostale hardverske teme' or scraped.tema = 'Benchmark' or scraped.tema = 'Tvrdi i optički diskovi' or scraped.tema = 'Mrežni hardver' or scraped.tema = 'Grafičke kartice' or scraped.tema = 'Overclocking' or scraped.tema = 'Periferija'" + limit
Q_SOFTWARE = "select text from scraped where scraped.tema = 'FB developers' or scraped.tema = 'Razvoj web-stranica' or scraped.tema = 'Programiranje' or scraped.tema = 'Ostale softverske teme' or scraped.tema = 'Sigurnosni softver' or scraped.tema = 'Programiranje za mobilne platforme'" + limit
Q_IGRE = "select text from scraped where scraped.tema = 'Komentari Games Master vijesti' or scraped.tema = 'PC igre' or scraped.tema = 'Web igre' or scraped.tema = 'Igraće konzole' or scraped.tema = 'Igre - općenito'" + limit
Q_NONIT = "select text from scraped where scraped.tema = 'Filmovi, TV serije, glazba...' or scraped.tema = 'Sport' or scraped.tema = 'Ostalo' or scraped.tema = 'Automobili, motori, bicikli...' or scraped.tema = 'Komentari Osobnog stava'" + limit


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


def get_features(post, category_corps):

    features = {}

    tknz = TweetTokenizer(preserve_case=False)
    tokens = tknz.tokenize(post)

    fil = re.compile('.*[A-Za-z0-9].*')
    urls = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    tokens = [w for w in tokens if fil.match(w)]
    tokens = [w for w in tokens if not urls.match(w)]

    #features['number_tokens'] = len(tokens)
    #features['first_token'] = tokens[0]

    tokens = [w for w in tokens if len(w) >= 4]
    #tokens = kor_tokens(tokens) #korjenovanje

    for corp in category_corps:
        counter = 0
        for t in corp[0]:
            counter += tokens.count(t)
        features[corp[1]] = counter

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

    tokens = [w for w in tokens if len(w) >= 4]
    #tokens = kor_tokens(tokens)
    fdist = FreqDist(tokens)
    most_common = fdist.most_common(30)
    ctokens = [w[0] for w in most_common]

    return ctokens


if __name__ == '__main__':

    hardware_tokens = (cat_tokens(Q_HARDWARE), 'hardware')
    software_tokens = (cat_tokens(Q_SOFTWARE), 'software')
    igre_tokens = (cat_tokens(Q_IGRE), 'igre')
    ostalo_tokens = (cat_tokens(Q_NONIT), 'ostalo')

    category_corps = [hardware_tokens, software_tokens, igre_tokens, ostalo_tokens]

    hardware_posts = get_posts_labeled(Q_HARDWARE, 'Hardware')
    software_posts = get_posts_labeled(Q_SOFTWARE, 'Software')
    ostalo_posts = get_posts_labeled(Q_NONIT, 'Ostalo')
    games_posts = get_posts_labeled(Q_IGRE, 'Igre')

    labeled_posts = hardware_posts + software_posts \
                    + ostalo_posts + games_posts

    random.shuffle(labeled_posts)
    feature_sets = [(get_features(post, category_corps), cat) for (post, cat) in labeled_posts]
    train_set, test_set = feature_sets[:len(feature_sets) - 1500], feature_sets[len(feature_sets) - 1501:]

    classifier = nltk.NaiveBayesClassifier.train(train_set)
    print(nltk.classify.accuracy(classifier, test_set))
    print(classifier.show_most_informative_features(40))



    pass
