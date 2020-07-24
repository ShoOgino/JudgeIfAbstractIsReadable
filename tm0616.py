# coding: UTF-8


from collections import Counter

import numpy as np

from numpy.random import *

import nltk

from nltk.corpus.reader.chasen import *





string="近年、深層学習がスポーツ分野へと活用されつつある。中でも、深層学習が持つ高い特徴抽出能力を活用し、スポーツのプレーについて行動評価を行うシステムが注目されている。行動評価を行う際の基準は主に2種類存在し、一方は投擲を行うスポーツにおける飛距離などの形式的なもの、もう一方はコーチが持つ言語化、データ化、及び情報化等の形式化が難しい知識である。コーチの暗黙知である評価基準を機械学習により形式化・可視化することは、形式的な評価基準からは得られない、プレーを改善するための指針が得られるという点で意義がある。暗黙知である、コーチによる行動評価基準を機械学習により形式化するためには、より高い精度でコーチと同じ評価を行う行動評価モデルを構築する必要がある。しかし、スポーツの評価に機械学習の応用例はプレイヤーの座標を分析する段階にとどまっており、行動評価の精度の観点で最適な行動評価モデルのアーキテクチャは検討されていない。また、暗黙知としての行動評価基準を可視化することはプレーの改善すべき点が容易に認識できるようになる点で意義がある。しかし、この機能に着目した研究・取り組みは行われていない。"



delimiter=['「', '」', '…', ' ']



doublets=list(zip(string[:-1],string[1:]))

doublets=filter((lambda x: not((x[0] in delimiter) or (x[1] in delimiter))), doublets)

triplets=list(zip(string[:-2], string[1:-1], string[2:]))

triplets=filter((lambda x: not((x[0] in delimiter) or (x[1] in delimiter) or (x[2] in delimiter))), triplets)



dic2=Counter(doublets)

dic3=Counter(triplets)

for u,v in dic2.items():

    print(u,v)

for u,v in dic3.items():

    print(u,v)