import pandas as pd
from gensim.models import Word2Vec
import os
review_word = pd.read_csv('./crawling_data/new_every_country_reviews.csv')
# df_test = pd.read_csv('crawling_data/one_sentence/cleaned_review_one_2022.csv')
review_word.info()
# exit(0)
cleaned_token_reviews = list(review_word['reviews'])

cleaned_tokens = []
for sentence in cleaned_token_reviews:
    token = sentence.split()
    cleaned_tokens.append(token)


embedding_model = Word2Vec(cleaned_tokens, vector_size=100, window=4, min_count=20, workers=4, epochs=100, sg=1)
embedding_model.save('./models/word2vec_battletrip.model')


