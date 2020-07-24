# -*- coding: utf-8 -*-
import re
import numpy as np
import pandas as pd
import MeCab
from sklearn.feature_extraction.text import TfidfVectorizer

m=MeCab.Tagger("-Owakati")

files= ["0.txt","1.txt","2.txt"]
readtext=[]
for file in files:
    with open(file, encoding="utf-8") as f:
        readtext.append(f.read())
wakatilist=[m.parse(u).rstrip() for u in readtext]
wakatilist=np.array(wakatilist)

vectorizer = TfidfVectorizer(use_idf=True, norm="l2", token_pattern=u'(?u)\\b\\w+\\b')
tfidf=vectorizer.fit_transform(wakatilist)
tfidfpd=pd.DataFrame(tfidf.toarray())
itemlist=sorted(vectorizer.vocabulary_.items(), key=lambda x: x[1])
tfidfpd.columns=[u[0] for u in itemlist]

for u in tfidfpd.index:
    print(tfidfpd.T.sort_values(by=u, ascending=False).iloc[:10, u])

for u, v in [(0,1), (0,2),(1,2), (0,0), (1,1)]:
    x=(tfidfpd.iloc[u,:]).dot(tfidfpd.iloc[v,:])
    print(x)