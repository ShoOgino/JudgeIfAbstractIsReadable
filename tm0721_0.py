# -*- coding: utf-8 -*-
import gensim, logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
sentences =gensim.models.word2vec.Text8Corpus("wp2txt/jpwall.txt")

model=gensim.models.word2vec.Word2Vec(sentences, min_count=5)
print("model gen complete")
model.save("jpwmodel")