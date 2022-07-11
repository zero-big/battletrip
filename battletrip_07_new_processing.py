import pandas as pd
from konlpy.tag import Okt
import re
import os
okt = Okt()
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['차장님', '과장님', '매니저', '매니져', '가이드', '풍선', '노랑', '여행']
df = pd.read_csv('./crawling_data/every_country_reviews.csv')

cleaned_sentences = []
for review in df.reviews:
    # count += 1
    # if count % 10 == 0:
    #     print(',', end='')
    # if count % 100 == 0:
    #     print()
    review = re.sub('[^가-힣0-9 ]', ' ', review)
    token = okt.pos(review, stem=True)  # pos - 형태소 분리를 시켜주고 품사를 지정해서 튜플로 묶어줌
    df_token = pd.DataFrame(token, columns=['word', 'class'])
    df_token = df_token[(df_token['class'] == 'Noun') |
                        (df_token['class'] == 'Adjective') |
                        (df_token['class'] == 'Number')]
    # 불용어 처리-----------------------------
    words = []
    for word in df_token.word:
        if 1 < len(word) < 20:
            if word not in stopwords:
                words.append(word)
    # ----------------------------------------
    # 형태소분리, 불용어 처리 된 단어들로 다시 문장으로 바꿈
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)
df['reviews'] = cleaned_sentences
df = df[['country', 'reviews']]
df.dropna(inplace=True)
df.to_csv(('./crawling_data/new_every_country_reviews.csv'), index=False)
df.info()
