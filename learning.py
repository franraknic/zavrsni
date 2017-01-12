import csv
import random
import nltk

def article_len(status):
    return {'article_length': len(status)}

with open('jutarnji.list_facebook_statuses.csv', 'rb') as f:
    reader = csv.reader(f)
    statuses_j = ([(post[1], 'index') for post in reader])

with open('index.hr_facebook_statuses.csv', 'rb') as fa:
    reader = csv.reader(x.replace('\0', '') for x in fa)
    statuses_24 = ([(post[1], '24sata') for post in reader])

labeled_articles = statuses_j[:500] + statuses_24[:200]
random.shuffle(labeled_articles)

featuresets = [(article_len(n), source) for (n, source) in labeled_articles]
train_set, test_set = featuresets[200:], featuresets[:200]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print (nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features()

print classifier.classify(article_len('Jebem ti sunac'))
