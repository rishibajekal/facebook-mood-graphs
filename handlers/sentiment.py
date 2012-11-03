from nltk.classify import NaiveBayesClassifier
from collections import defaultdict
import pickle
import json
import re

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
    for word in words:
        if (word not in STOPWORDS) and word != '':
            sent_dict[word.lower()] = sent_dict[word.lower()] + 1
    return (classifier.classify(sent_dict) - 2.5) / 2.5

def sentimentJSON(sentences_json, classifier):
    sentences = json.loads(sentences_json)
    for sentence_dict in sentences:
        sentence_dict['sentiment'] = sentiment(sentence_dict['message'], classifier)
    return sentences

def classifierTest():
    f = open('classifier.bin')
    classifier = pickle.load(f)
    f.close()

    f = open('rishi_statuses.json')
    j = f.read()
    f.close()

    
    print sentiment("had a blast at the game. Awesome game and great public warmup. On to studying...", classifier)

    d = sentimentJSON(j, classifier)
    
    for ent in d:
        try:
            print 'Message: ' + ent['message'] + ' Sentiment: ' + str(ent['sentiment'])
        except:
            pass

if __name__ == "__main__":
    classifierTest()
