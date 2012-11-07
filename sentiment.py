from nltk.classify import NaiveBayesClassifier
from collections import defaultdict
import pickle
import json
import re, itertools
from nltk.corpus import wordnet as wn

clean = r'\w+'

CLEAN_RE = re.compile(r'\w+')
STOPWORDS = set(['a','able','about','across','after','all','almost','also','am','among',\
             'an','and','any','are','as','at','be','because','been','but','by','can',\
             'cannot','could','dear','did','do','does','either','else','ever','every',\
             'for','from','get','got','had','has','have','he','her','hers','him','his',\
             'how','however','i','if','in','into','is','it','its','just','least','let',\
             'like','likely','may','me','might','most','must','my','neither','no','nor',\
             'not','of','off','often','on','only','or','other','our','own','rather','said',\
             'say','says','she','should','since','so','some','than','that','the','their',\
             'them','then','there','these','they','this','tis','to','too','twas','us',\
             'wants','was','we','were','what','when','where','which','while','who',\
             'whom','why','will','with','would','yet','you','your'])


GOOD_SYNSETS = wn.synsets('good')
BAD_SYNSETS = wn.synsets('bad')
BASE_SYN = 0.8


def getWords(sent):
    outList = []
    for a in sent.split(' '):
        try:
            outList.append(re.match(CLEAN_RE, a).group(0))
        except:
            pass
    return outList

def sentiment(sentence, classifier):
    sent_dict = defaultdict(int)
    words = getWords(sentence)
    coeff_cache = defaultdict(float)
    for word in words:
        if (word not in STOPWORDS) and word != '':
            sent_dict[word.lower()] = sent_dict[word.lower()] + 1
    return (((classifier.classify(sent_dict) - 1) / 4) * 2) - 1

def sentimentJSON(sentences_json, classifier):
    sentences = json.loads(sentences_json)
    for sentence_dict in sentences:
        sentence_dict['sentiment'] = sentiment(sentence_dict['message'], classifier)
    return sentences

