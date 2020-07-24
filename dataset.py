# -*- coding: utf-8 -*-
import csv
import neologdn
import re
import MeCab
import copy
import pandas as pd
import json
def getDatasRaw(path):
    with open(path, encoding="utf-8") as f:
        characters2replace={
            '，': '、',
            '．': '。',
            }
        reader = csv.reader(f)
        rows = [row for row in reader]
    for row in rows:
        row[1] = row[1].translate(str.maketrans(characters2replace)).lower()
        neologdn.normalize(row[1])
    return rows
def makeDataset(path):
    def getNOSentences(text):
        return text.count('。')
    def getWords(text):
        words=list()
        m= MeCab.Tagger("-Ochasen")
        node = m.parseToNode(text)
        while node:
            word = node.surface
            wclass = node.feature.split(',')
            if(wclass[0] != u'BOS/EOS'):
                words.append((word, wclass[0], node.stat))
            node = node.next
        return words
    def getNOWords(text):
        return len(getWords(text))
    def getNOWordsEnglish(text):
        count=0
        words = getWords(text)
        reAlpha = re.compile(r'^[a-zA-Z]+$')
        for word in words:
            if reAlpha.match(word[0]) is not None:
                count=count+1
        return count
    def getNOWordsNum(text):
        count=0
        words = getWords(text)
        reDigit = re.compile(r'^[0-9]+$')
        for word in words:
            if reDigit.match(word[0]) is not None:
                count=count+1
        return count
    def getNOWordsParenthese(text):
        return len(re.findall("\(|\)|\[|\]|\{|\}|「|」|『|』", text))
    def getNOWordsReadingPoint(text):
        return text.count('、')
    def getNOWordsConjunction(text):
        count=0
        words=getWords(text)
        for word in words:
            if "接続詞" in word[1]:
                count=count+1
        return count
    def getNOWordsPostpositionalParticleNo(text):
        count=0
        words=getWords(text)
        for word in words:
            if ("助詞" in word[1]) and (word[0]=="の"):
                count=count+1
        return count
    def getNOWordsUnregistered(text):
        count=0
        words=getWords(text)
        reDigit = re.compile(r'^[0-9]+$')
        #reSymbol = re.compile("\(|\)|\[|\]|\{|\}|「|」|『|』|%|/|\.")
        for word in words:
            if word[2]==1 and len(word[0])!=1 and reDigit.match(word[0]) is None:
                count=count+1
        return count
    def getNOCharacters(text):
        return len(text)
    def getNOCharactersKanji(text):
        url = 'https://raw.githubusercontent.com/cjkvi/cjkvi-tables/15569eaae99daef9f99f0383e9d8efbec64a7c5a/joyo2010.txt'
        df = pd.read_csv(url, header=None, skiprows=1, delimiter='\t')
        kanji = ''.join(df.iloc[:, 0])
        p = re.compile('[{}]'.format(kanji))
        return len(p.findall(text))

    dataset={}
    rows = getDatasRaw(path)
    for row in rows:
        data={
            "NOSentences":0,
            "NOWords" : 0,
            "NOWordsEnglish" : 0,
            "NOWordsNum" : 0,
            "NOWordsParenthese" : 0,
            "NOWordsReadingPoint" : 0,
            "NOWordsConjunction" : 0,
            "NOWordsPostpositionalParticleNo" : 0,
            "NOWordsUnregistered" : 0,
            "NOCharacters" : 0,
            "NOCharactersKanji" : 0,
            "isReadable" : 0
            }
        data["NOSentences"]=getNOSentences(row[1])
        data["NOWords"]=getNOWords(row[1])
        data["NOWordsEnglish"]=getNOWordsEnglish(row[1])
        data["NOWordsNum"]=getNOWordsNum(row[1])
        data["NOWordsParenthese"]=getNOWordsParenthese(row[1])
        data["NOWordsReadingPoint"]=getNOWordsReadingPoint(row[1])
        data["NOWordsConjunction"]=getNOWordsConjunction(row[1])
        data["NOWordsPostpositionalParticleNo"]=getNOWordsPostpositionalParticleNo(row[1])
        data["NOWordsUnregistered"]=getNOWordsUnregistered(row[1])
        data["NOCharacters"]=getNOCharacters(row[1])
        data["NOCharactersKanji"]=getNOCharactersKanji(row[1])
        data["isReadable"]= int(row[2])
        dataset[row[0]]=data
    with open('dataset.json', 'w') as f:
        json.dump(dataset, f, indent=4)


def main():
    makeDataset("dataRaw.csv")

if __name__ == '__main__':
    main()
