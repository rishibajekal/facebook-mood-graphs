from nltk.classify import NaiveBayesClassifier
from collections import defaultdict
import pickle
import json

def sentiment(sentence, classifier):
    sent_dict = defaultdict(int)
    words = sentence.split(' ')
    for word in words:
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

    print sentimentJSON(j, classifier)

if __name__ == "__main__":
    classifierTest()
