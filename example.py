import gensim

path = ''
id_w2v = gensim.models.word2vec.Word2Vec.load('./model/idwiki_word2vec.model')
print(id_w2v.most_similar('raja'))
