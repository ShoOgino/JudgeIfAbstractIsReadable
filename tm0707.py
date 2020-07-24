# -*- coding: utf-8 -*-
from nltk.tokenize import word_tokenize
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy

def format_sentense(sentense):
    return {word: True for word in word_tokenize(sentense)}

with open('rt-polaritydata/rt-polarity.pos',encoding="latin-1") as f:
    pos_data = [[format_sentense(line),'pos'] for line in f]
with open('rt-polaritydata/rt-polarity.neg',encoding="latin-1") as f:
    neg_data = [[format_sentense(line),'neg'] for line in f]

training_data=pos_data[:4000]+neg_data[:4000]
training_data=pos_data[4000:]+neg_data[4000:]

model=NaiveBayesClassifier.train(training_data)

s1 = 'This is a nice article'
s2 = 'This is a bad article'

print (s1, "--->", model.classify(format_sentense(s1)))
print (s2, "--->", model.classify(format_sentense(s2)))

print('accuracy', accuracy(model, testing_data))