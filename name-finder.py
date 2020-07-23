import nltk
from collections import defaultdict
import sys
nltk.download('averaged_perceptron_tagger')
nltk.download('punkt')
text = ''
for filename in sys.argv[1:]:
    text += open(filename).read()

name_counts = defaultdict(int)
for name in [name for (name, pos) in nltk.pos_tag(nltk.word_tokenize(text)) if pos=='NNP']:
    name_counts[name] += 1
for name, count in sorted(name_counts.items(), key=lambda x: x[1], reverse=True):
    print(f'{name} : ({count})')

