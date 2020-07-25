import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from pandas.plotting import scatter_matrix
from sklearn.model_selection import GridSearchCV

import json
def getModelBest():
    #features2Drop, parametersBest=getParametersHyperBest()
    features2Drop=['NOCharacters', 'NOWordsNum', 'NOWordsEnglish', 'NOWordsConjunction', 'NOCharactersKanji', 'NOWordsUnregistered']
    parametersBest={
        "n_estimators":5,
        "max_depth":5,
        "min_samples_leaf":2,
        "min_samples_split":2,
        "random_state":10
    }
    #getParametersTrainBest(getDatasetsSplit(features2Drop))
    testParametersHyper(features2Drop, parametersBest)
    return 0

def testParametersHyper(features2Drop, parametersBest):
    datasetsSplit=getDatasetsSplit(features2Drop)
    accuraciesTrain=[]
    accuraciesValid=[]
    for patternSplit in range(10):
        train_x=datasetsSplit[patternSplit]["train_x"]
        train_y=datasetsSplit[patternSplit]["train_y"]
        valid_x=datasetsSplit[patternSplit]["valid_x"]
        valid_y=datasetsSplit[patternSplit]["valid_y"]
        model=RandomForestClassifier(
            n_estimators=parametersBest["n_estimators"],
            max_depth=parametersBest["max_depth"],
            min_samples_leaf=parametersBest["min_samples_leaf"],
            min_samples_split=parametersBest["min_samples_split"],
            random_state=parametersBest["random_state"]
        )
        model.fit(train_x, train_y)
        accuraciesTrain.append(model.score(train_x, train_y))
        accuraciesValid.append(accuracy_score(valid_y, model.predict(valid_x)))

    accuracyTrainAverage=sum(accuraciesTrain)/len(accuraciesTrain)
    accuracyValidAverage=sum(accuraciesValid)/len(accuraciesValid)
    print("averageTrain:"+str(accuracyTrainAverage))
    print("averageValid:"+str(accuracyValidAverage))


def getDatasetsSplit(*features2Drop):
    dataset=[]
    datasetSplit=[]
    for i in range(10):
        with open('dataset'+str(i)+'.json') as f:
            d = json.load(f)
        dataset.append(d)
    for trial in range(10):
        dictionary={}
        train={
            "NOSentences":[],
            "NOWords" : [],
            "NOWordsEnglish" : [],
            "NOWordsNum" : [],
            "NOWordsParenthese" : [],
            "NOWordsReadingPoint" : [],
            "NOWordsConjunction" : [],
            "NOWordsPostpositionalParticleNo" : [],
            "NOWordsUnregistered" : [],
            "NOCharacters" : [],
            "NOCharactersKanji" : [],
            "isReadable" : []
        }
        valid={
            "NOSentences":[],
            "NOWords" : [],
            "NOWordsEnglish" : [],
            "NOWordsNum" : [],
            "NOWordsParenthese" : [],
            "NOWordsReadingPoint" : [],
            "NOWordsConjunction" : [],
            "NOWordsPostpositionalParticleNo" : [],
            "NOWordsUnregistered" : [],
            "NOCharacters" : [],
            "NOCharactersKanji" : [],
            "isReadable" : []
        }
        for i in range(10):
            for row in dataset[i]:
                for column in dataset[i][row]:
                    if(i==trial):
                        valid[column].append(dataset[i][row][column])
                    else:
                        train[column].append(dataset[i][row][column])
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)

        features=list(features2Drop)
        train_x = pd.DataFrame(train)
        train_x = train_x.drop(['isReadable'], axis=1)
        for feature in features:
            train_x=train_x.drop(feature, axis=1)
        #train_x = (train_x - train_x.mean())/ train_x.std(ddof=0) #RFでは正規化しない。
        train_y = pd.DataFrame(train)['isReadable']
        valid_x = pd.DataFrame(valid)
        valid_x = valid_x.drop(['isReadable'], axis=1)
        for feature in features:
            valid_x=valid_x.drop(feature, axis=1)
        #valid_x = (valid_x - valid_x.mean())/ valid_x.std(ddof=0) # RFでは正規化しない。
        valid_y = pd.DataFrame(valid)['isReadable']
        dictionary["train_x"]=train_x
        dictionary["train_y"]=train_y
        dictionary["valid_x"]=valid_x
        dictionary["valid_y"]=valid_y
        datasetSplit.append(dictionary)
    return datasetSplit


def getParametersHyperBest():
    features=[
        "NOSentences",
        "NOWords",
        "NOWordsEnglish",
        "NOWordsNum",
        "NOWordsParenthese",
        "NOWordsReadingPoint",
        "NOWordsConjunction",
        "NOWordsPostpositionalParticleNo",
        "NOWordsUnregistered",
        "NOCharacters",
        "NOCharactersKanji",
    ]
    accuracies=[]
    features2Drop=[]
    for trialFeature in range(10):
        accuracyBest=0
        featureWorst=""
        for index, feature in enumerate(features):
            print(features2Drop)
            print(feature)
            datasetsSplit = getDatasetsSplit(features2Drop+[feature])
            parametersBest, accuracy=getParametersTrainBest(datasetsSplit)
            if(accuracyBest<accuracy):
                accuracyBest = accuracy
                featureWorst = feature
        accuracies.append(accuracyBest)
        features2Drop.append(featureWorst)
        features.remove(featureWorst)
    print(features2Drop)
    print(accuracies)
    max_idx=accuracies.index(max(accuracies))
    datasetsSplit = getDatasetsSplit(features2Drop[:max_idx])
    parametersBest, accuracy = getParametersTrainBest(datasetsSplit)
    return features2Drop[:max_idx], parametersBest


def getParametersTrainBest(datasetsSplit):
    accuracyBest=0
    parametersBest={
        "n_estimators":0 ,
        "random_state":0,
        "max_depth":0,
        "min_samples_leaf":0,
        "min_samples_split":0
    }
    parameters2Tune = {#5, 3, 2, 2, 0
        'n_estimators'     :[2, 3, 5, 10],
        'max_depth'        :[2, 3, 5],
        'min_samples_leaf' :[2, 5],
        'min_samples_split':[2, 5],
        'random_state'     :[0, 7, 10]
    }
    for n_estimators in parameters2Tune["n_estimators"]:
        for max_depth in parameters2Tune["max_depth"]:
            for min_samples_leaf in parameters2Tune["min_samples_leaf"]:
                for min_samples_split in parameters2Tune["min_samples_split"]:
                    for random_state in parameters2Tune["random_state"]:
                        print("n_estimators: "+str(n_estimators))
                        print("max_depth: "+str(max_depth))
                        print("min_samples_leaf: "+str(min_samples_leaf))
                        print("min_samples_split: "+str(min_samples_split))
                        print("random_state: "+str(random_state))
                        accuraciesTrain=[]
                        accuraciesValid=[]
                        for patternSplit in range(10):
                            train_x=datasetsSplit[patternSplit]["train_x"]
                            train_y=datasetsSplit[patternSplit]["train_y"]
                            valid_x=datasetsSplit[patternSplit]["valid_x"]
                            valid_y=datasetsSplit[patternSplit]["valid_y"]
                            model=RandomForestClassifier(
                                n_estimators=n_estimators,
                                max_depth=max_depth,
                                min_samples_leaf=min_samples_leaf,
                                min_samples_split=min_samples_split,
                                random_state=random_state
                            )
                            model.fit(train_x, train_y)
                            accuraciesTrain.append(model.score(train_x, train_y))
                            accuraciesValid.append(accuracy_score(valid_y, model.predict(valid_x)))

                        accuracyTrainAverage=sum(accuraciesTrain)/len(accuraciesTrain)
                        accuracyValidAverage=sum(accuraciesValid)/len(accuraciesValid)
                        print("averageTrain:"+str(accuracyTrainAverage))
                        print("averageValid:"+str(accuracyValidAverage))
                        if(accuracyBest<accuracyValidAverage):
                            accuracyBest=accuracyValidAverage
                            parametersBest={
                                "n_estimators":n_estimators ,
                                "random_state":random_state,
                                "max_depth":max_depth,
                                "min_samples_leaf":min_samples_leaf,
                                "min_samples_split":min_samples_split
                            }
    print(accuracyBest)
    print(parametersBest)
    return parametersBest, accuracyBest

def main():
    getModelBest()

if __name__ == '__main__':
    main()
