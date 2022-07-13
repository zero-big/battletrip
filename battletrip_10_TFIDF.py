import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from scipy.io import mmwrite, mmread
import pickle
import numpy as np

df_reviews = pd.read_csv('./crawling_data/new_every_country_reviews.csv')
print(df_reviews)

#TF-IDF 스코어 확인을 위한 데이터프레임 작성
document = df_reviews['reviews']
print(document)

vectorizer = CountVectorizer()
dtm = vectorizer.fit_transform(document)
tf = pd.DataFrame(dtm.toarray(), columns = vectorizer.get_feature_names())
df = tf.astype(bool).sum(axis = 0)
D = len(tf)

# Inverse Document Frequency
idf = np.log((D+1) / (df+1)) + 1
tfidf = tf * idf
tfidf = tfidf / np.linalg.norm(tfidf, axis = 1, keepdims = True)

print(tfidf)
tfidf.to_csv('./tfidf.csv')

Tfidf = TfidfVectorizer(sublinear_tf=True)
Tfidf_matrix = Tfidf.fit_transform(df_reviews['reviews'])
print(Tfidf_matrix.shape)
# (3182, 84461)
print(Tfidf_matrix[0].shape)
# (1, 84461)
with open('./models/tfidf.pickle', 'wb') as f:
    pickle.dump(Tfidf, f)

mmwrite('./models/Tfidf_travel_review.mtx', Tfidf_matrix)

