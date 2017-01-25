from nltk.corpus.reader import plaintext
from nltk.probability import FreqDist

class CorpusReader(plaintext.PlaintextCorpusReader):

    pass

reader = CorpusReader('F:\zavrsni\corp_make', '.*\.txt', encoding='utf-8')

print(len(reader.words()))

words = reader.words()

#print(sorted(set(words)))

fdist = FreqDist(words)
print(fdist.most_common(200))