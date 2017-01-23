from nltk import word_tokenize
import nltk

raw = open('corp.txt', encoding='utf-8').read()

# punkt tokenizer
tokens = word_tokenize(raw)

#sortirano
words = [w.lower() for w in tokens]
vocab = sorted(set(words))

#pretvori u nltk objekt text
text = nltk.Text(words)
text.concordance('hdz')
print(text.collocations())
