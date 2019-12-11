####
"""
@author: Kannan Chandrasekaran (kach@microsoft.com)

Google's pre-trained model: https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit
Doc2vec tutorial: https://medium.com/@mishra.thedeepak/doc2vec-simple-implementation-example-df2afbbfbad5
"""

#Import all the dependencies
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize

data = ["I love machine learning. Its awesome.",
        "I love coding in python",
        "I love building chatbots",
        "they chat amagingly well"]

tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in enumerate(data)]

max_epochs = 100
vec_size = 20
alpha = 0.025

model = Doc2Vec(size=vec_size,
                alpha=alpha, 
                min_alpha=0.00025,
                min_count=1,
                dm =1)
  
model.build_vocab(tagged_data)

for epoch in range(max_epochs):
    print('iteration {0}'.format(epoch))
    model.train(tagged_data,
                total_examples=model.corpus_count,
                epochs=model.iter)
    # decrease the learning rate
    model.alpha -= 0.0002
    # fix the learning rate, no decay
    model.min_alpha = model.alpha

model.save("d2v.model")
print("Model Saved")

#Note: dm defines the training algorithm. If dm=1 means ‘distributed memory’ (PV-DM) 
#and dm =0 means ‘distributed bag of words’ (PV-DBOW). Distributed Memory model 
#preserves the word order in a document whereas Distributed Bag of words just uses 
#the bag of words approach, which doesn’t preserve any word order.

from gensim.models.doc2vec import Doc2Vec

model= Doc2Vec.load("d2v.model")

#to find the vector of a document which is not in training data
sentence1 = word_tokenize("I love chatbots".lower())
v1 = model.infer_vector(sentence1)

sentence2=word_tokenize("i like python".lower())
v2=model.infer_vector(sentence1)

from scipy import spatial
sen1_sen2_similarity =  1 - spatial.distance.cosine(v1,v2)
print(sen1_sen2_similarity)