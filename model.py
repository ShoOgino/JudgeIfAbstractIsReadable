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

import json

def createModel():
  # parameters = {
  #     'n_estimators' :[3,5,10,30,50],#作成する決定木の数
  #     'random_state' :[7,42,80],
  #     'max_depth' :[3,5,8,10],#決定木の深さ
  #     'min_samples_leaf': [2,5,10,20,50],#分岐し終わったノードの最小サンプル数
  #     'min_samples_split': [2,5,10,20,50]#決定木が分岐する際に必要なサンプル数
  # }
    parameters = {
        'n_estimators' :[10],#作成する決定木の数
        'random_state' :[7],
        'max_depth' :[3],#決定木の深さ
        'min_samples_leaf': [2],#分岐し終わったノードの最小サンプル数
        'min_samples_split': [10]#決定木が分岐する際に必要なサンプル数
    }
    best=0
    parameterBest={
        "n_estimators":0 ,
        "random_state":0,
        "max_depth":0,
        "min_samples_leaf":0,
        "min_samples_split":0
        }
    dataset=[]
    for i in range(10):
        with open('dataset'+str(i)+'.json') as f:
            d = json.load(f)
        dataset.append(d)

    for n_estimators in parameters["n_estimators"]:
        print("n_estimators: "+str(n_estimators))
        for random_state in parameters["random_state"]:
            print("random_state: "+str(random_state))
            for max_depth in parameters["max_depth"]:
                print("max_depth: "+str(max_depth))
                for min_samples_leaf in parameters["min_samples_leaf"]:
                    print("min_samples_leaf: "+str(min_samples_leaf))
                    for min_samples_split in parameters["min_samples_split"]:
                        print("min_samples_split: "+str(min_samples_split))

                        accuracies=[]
                        for trial in range(10):
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

                            train_x = pd.DataFrame(train).drop(['isReadable'], axis=1)
                            train_x = (train_x - train_x.mean())/ train_x.std(ddof=0)
                            train_y = pd.DataFrame(train)['isReadable']
                            valid_x = pd.DataFrame(valid).drop(['isReadable'], axis=1)
                            valid_x = (valid_x - valid_x.mean())/ valid_x.std(ddof=0)
                            valid_y = pd.DataFrame(valid)['isReadable']

                            #from sklearn.model_selection import GridSearchCV
                            #clf = GridSearchCV(estimator=RandomForestClassifier(),     param_grid=parameters, cv=2)
                            #
                            #clf.fit(train_x, train_y)
                            #
                            #best_clf = clf.best_estimator_ #ここにベストパラメータの組み合わせが入っ    ています
                            #print('score: {:.2%}'.format(best_clf.score(train_x, train_y)))
                            #y_pred = clf.predict(test_x)
                            #print('score: {:.2%}'.format(best_clf.score(test_x, test_y)))
                            #



                            random_forest = RandomForestClassifier(
                                max_depth=max_depth,
                                n_estimators=n_estimators,
                                random_state=random_state,     min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf
                            )
                            random_forest.fit(train_x, train_y)

                            #trainaccuracy_random_forest = random_forest.score(train_x, train_y)
                            #print('TrainAccuracy: {}'.format(trainaccuracy_random_forest))

                            y_pred = random_forest.predict(valid_x)

                            accuracy_random_forest = accuracy_score(valid_y, y_pred)
                            accuracies.append(accuracy_random_forest)
                            #print('Accuracy: {}'.format(accuracy_random_forest))
                        accuracyAverage=sum(accuracies)/len(accuracies)
                        print("average:"+str(accuracyAverage))
                        if(best<accuracyAverage):
                            best=accuracyAverage
                            parameterBest={
                                "n_estimators":n_estimators ,
                                "random_state":random_state,
                                "max_depth":max_depth,
                                "min_samples_leaf":min_samples_leaf,
                                "min_samples_split":min_samples_split
                            }
    print(best)
    print(parameterBest)


def main():
    createModel()

if __name__ == '__main__':
    main()
