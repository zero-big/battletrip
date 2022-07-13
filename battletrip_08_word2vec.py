import pandas as pd
from gensim.models import Word2Vec
import os


# 데이터 로드
review_word = pd.read_csv('./crawling_data/new_every_country_reviews.csv')
# df_test = pd.read_csv('crawling_data/one_sentence/cleaned_review_one_2022.csv')
review_word.info()
# exit(0)


# 리뷰 리스트 만들기
cleaned_token_reviews = list(review_word['reviews'])


# 리뷰 리스트 속 형태소만 추출한 리스트 만들기
cleaned_tokens = []
for sentence in cleaned_token_reviews:
    token = sentence.split()
    cleaned_tokens.append(token)


# 모델링 + 벡터라이징
embedding_model = Word2Vec(cleaned_tokens,
                           vector_size=100, # 100차원으로 축소
                           window=4,    # 4개씩 끊어서 학습 ==> Conv1D의 커널사이즈 지정
                           min_count=20,    # 빈도 최소 20번 이상인 단어들만
                           workers=4,   # cpu 코어 수
                           epochs=100,  # 100번 학습
                           sg=1)    # skip-gram 알고리즘 사용


# 모델 저장
embedding_model.save('./models/word2vec_battletrip.model')


