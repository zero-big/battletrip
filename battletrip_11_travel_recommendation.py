import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from gensim.models import Word2Vec

# def getRecommendation(cosin_sim):
#     simScore = list(enumerate(cosin_sim[-1]))
#     simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
#     simScore = simScore[:11]
#     movieIdx = [i[0] for i in simScore]
#     recMovieList = df_reviews.iloc[movieIdx, 0]
#     return recMovieList


# 데이터 로드
df_reviews = pd.read_csv('./crawling_data/new_every_country_reviews.csv')
Tfidf_matrix = mmread('./models/Tfidf_movie_review.mtx').tocsr()


# TFIDF모델 로드
with open('./models/tfidf.pickle', 'rb') as f:
    Tfidf = pickle.load(f)


# # 1. 영화 제목 / index를 이용
# movie_idx = df_reviews[df_reviews['country'] == '보라카이'].index[0]
#
# ## 코사인 유사도
# cosine_sim = linear_kernel(Tfidf_matrix[movie_idx], Tfidf_matrix)
# recommendation = getRecommendation(cosine_sim)
# print(recommendation[1:11])


# 2. keyword 이용
## Word2Vec모델 로드
embedding_model = Word2Vec.load('./models/word2vec_battletrip.model')

## 키워드 지정
keyword = '행복'
sim_word = embedding_model.wv.most_similar(keyword, topn=10)

## 유사도 값 큰 순서로 3개 단어 리스트
# words = [keyword]
words = []
for word, _ in sim_word:
    words.append(word)
sentence = []   # sentence = [words[0]] * 3 + [word[1] * 2 + ...]
count = 3
for word in words:
    sentence = sentence + [word] * count
    count -= 1
sentence = ' '.join(sentence)

## 모델 적용
sentence_vec = Tfidf.transform([sentence])

## 코사인 유사도
cosine_sim = linear_kernel(sentence_vec, Tfidf_matrix)

## 코사인 유사도값(1에 가까울수록)으로 추천해주는 함수 생성
def getRecommendation(cosine_sim):
    simScore = list(enumerate(cosine_sim[-1]))
    ## 코사인 유사도값 기준으로 내림차순 정렬
    simScore = sorted(simScore, key=lambda x:x[1], reverse=True)
    simScore = simScore[:11]   # 0번(코사인 유사도 max, 키워드 자기자신)은 처음부터 제외됐었으니 다시 포함
    countryIdx = [i[0] for i in simScore]
    countryList = df_reviews.iloc[countryIdx, 0]
    return countryList

## 추천 알고리즘
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


