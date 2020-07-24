# -*- coding: utf-8 -*-
import re
import numpy as np
from collections import Counter
import MeCab
import itertools
from igraph import *

minfreq =0
m=MeCab.Tagger("-Ochasen")

strOrig="近年、深層学習がスポーツ分野へと活用されつつある。中でも、深層学習が持つ高い特徴抽出能力を活用し、スポーツのプレーについて行動評価を行うシステムが注目されている。行動評価を行う際の基準は主に2種類存在し、一方は投擲を行うスポーツにおける飛距離などの形式的なもの、もう一方はコーチが持つ言語化、データ化、及び情報化等の形式化が難しい知識である。コーチの暗黙知である評価基準を機械学習により形式化・可視化することは、形式的な評価基準からは得られない、プレーを改善するための指針が得られるという点で意義がある。暗黙知である、コーチによる行動評価基準を機械学習により形式化するためには、より高い精度でコーチと同じ評価を行う行動評価モデルを構築する必要がある。しかし、スポーツの評価に機械学習の応用例はプレイヤーの座標を分析する段階にとどまっており、行動評価の精度の観点で最適な行動評価モデルのアーキテクチャは検討されていない。また、暗黙知としての行動評価基準を可視化することはプレーの改善すべき点が容易に認識できるようになる点で意義がある。しかし、この機能に着目した研究・取り組みは行われていない。"
sentenses=re.sub('。', '。\n', strOrig).splitlines()
string=[re.sub(' ', '', u) for u in sentenses if len(u)!=0]

sentensemeishilist=[[v.split()[2] for v in m.parse(sentense).splitlines() if (len(v.split())>=3 and v.split()[3][:2]=="名詞")] for sentense in string]

doubletslist=[list(itertools.combinations(meishilist,2)) for meishilist in sentensemeishilist if len(meishilist)>=2]
alldoublets=[]
for u in doubletslist:
    alldoublets.extend(u)

dcnt = Counter(alldoublets)

print('pair frequency', sorted(dcnt.items(), key=lambda x:x[1], reverse=True)[:30])

restricteddcnt =dict(((k,dcnt[k]) for k in dcnt.keys() if dcnt[k]>=minfreq))
charedges=restricteddcnt.keys()
vertices=list(set([v[0] for v in charedges] + [v[1] for v in charedges]))

edges=[(vertices.index(u[0]), vertices.index(u[1])) for u in charedges]
g=Graph(vertex_attrs={"label":vertices, "name": vertices}, edges=edges, directed=False)
#plot(g, vertex_size=30, bbox=(800,800), vertex_color="white")

print('average path length', g.average_path_length())
print("path length hist\n", g.path_length_hist())

print("eccentricity centrality", sorted( zip(vertices, [1/u for u in list(g.eccentricity())]), key=lambda x:x[1], reverse=True)[:30])
print("closeness", sorted( zip(vertices, list(g.closeness())),key=lambda x: x[1],reverse=True)[:30])
print("degree centrality", sorted( zip(vertices, [u/(len(g.degree())-1)for u in list(g.degree())]), key=lambda x: x[1], reverse=True))
print("eigenvalue-based centrality", sorted(zip(vertices, list(g.evcent())), key=lambda x: x[1], reverse=True)[:30])

print("community info map", g.community_infomap())
