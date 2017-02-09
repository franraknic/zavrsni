from nltk.corpus.reader import plaintext
from nltk.probability import FreqDist
from nltk.tokenize import *

reader = plaintext.PlaintextCorpusReader('F:\zavrsni\corp_make', 'developers_facebook_statuses_corp.txt', encoding='utf-8', word_tokenizer=WhitespaceTokenizer())

print(reader.words())
print(len(reader.words()))