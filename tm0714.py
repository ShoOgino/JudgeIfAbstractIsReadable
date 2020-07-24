# -*- coding: utf-8 -*-

from nltk.corpus import wordnet as wn
import MeCab
import re
from collections import Counter
str="近年、深層学習がスポーツ分野へと活用されつつある。中でも、深層学習が持つ高い特徴抽出能力を活用し、スポーツのプレーについて行動評価を行うシステムが注目されている。行動評価を行う際の基準は主に2種類存在し、一方は投擲を行うスポーツにおける飛距離などの形式的なもの、もう一方はコーチが持つ言語化、データ化、及び情報化等の形式化が難しい知識である。コーチの暗黙知である評価基準を機械学習により形式化・可視化することは、形式的な評価基準からは得られない、プレーを改善するための指針が得られるという点で意義がある。暗黙知である、コーチによる行動評価基準を機械学習により形式化するためには、より高い精度でコーチと同じ評価を行う行動評価モデルを構築する必要がある。しかし、スポーツの評価に機械学習の応用例はプレイヤーの座標を分析する段階にとどまっており、行動評価の精度の観点で最適な行動評価モデルのアーキテクチャは検討されていない。また、暗黙知としての行動評価基準を可視化することはプレーの改善すべき点が容易に認識できるようになる点で意義がある。しかし、この機能に着目した研究・取り組みは行われていない。"


m= MeCab.Tagger("-Ochasen")

parse=m.parse(str)
lines=parse.split("\n")
items = (re.split('[\t,]', line) for line in lines)
#for item in items:
#    print(item[3])
words = [item[0] for item in items if (item[0] not in ('EOS', '', 't', 'ー')  and "名詞" in item[3])]

counter = Counter(words)
common0=counter.most_common()[0][0]
common1=counter.most_common()[2][0]
c0=wn.synsets(common0,lang='jpn')[0]
c1=wn.synsets(common1,lang='jpn')[0]
print(c0.hypernyms())
print(c1.hypernyms())

print(c0.hyponyms())
print(c1.hyponyms())

print(wn.synsets(common0, lang="jpn")[0].path_similarity(wn.synsets(common1, lang="jpn")[0]))
