import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

def getRecommendation(cosin_sim):
    simScore = list(enumerate(cosin_sim[-1]))
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:4]
    tripIdx = [i[0] for i in simScore]
    recpointList = df_reviews.iloc[tripIdx, 0]
    return recpointList


df_reviews = pd.read_csv('./crawling_data/new_every_country_reviews.csv')
Tfidf_matrix = mmread('./models/Tfidf_trip_review.mtx').tocsr()
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)

# 영화 제목 / index를 이용
trip_idx = df_reviews[df_reviews['country'] == '보라카이'].index[0]

cosine_sim = linear_kernel(Tfidf_matrix[trip_idx], Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation[1:11])

# keyword 이용
embedding_model = Word2Vec.load('./models/word2vec_battletrip.model')
keyword = '행복'
sim_word = embedding_model.wv.most_similar(keyword, topn=3)
words = [keyword]
for word, _ in sim_word:
    words.append(word)
sentence = []
count = 3
for word in words:
    sentence = sentence + [word] * count
    count -= 1
sentence = ' '.join(sentence)
sentence_vec = Tfidf.transform([sentence])
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
recommendation = getRecommendation(cosine_sim)
print(recommendation)

# 문장 이용
# okt = Okt()
# sentence = '화려한 액션과 소름 돋는 반전이 있는 영화'
# review = re.sub('[^가-힣 ]', ' ', sentence)
#
# token = okt.pos(review, stem=True)
#
# df_token = pd.DataFrame(token, columns=['word', 'class'])
# df_token = df_token[(df_token['class'] == 'Noun') |
#                     (df_token['class'] == 'Verb') |
#                     (df_token['class'] == 'Adjective')]
# words = []
# for word in df_token.word:
#     if 1 < len(word):
#         words.append(word)
# cleaned_sentence = ' '.join(words)
# print(cleaned_sentence)
# sentence_vec = Tfidf.transform([cleaned_sentence])
# cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation)


