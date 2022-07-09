import pandas as pd
from konlpy.tag import Okt
import re
import os
okt = Okt()
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords + ['차장님', '과장님', '매니저', '매니져', '가이드', '풍선', '노랑']

files = os.listdir('./crawling_data/add_column_data')

df_list = []
city = []
for i in files:
    globals()[i.split('.')[0]] = pd.read_csv(f'./crawling_data/add_column_data/{i}')
    df_list.append(globals()[i.split('.')[0]])
    city_list = (i.split('.')[0]).split('_')[1]
    city.append(city_list)

lenth = int(len(city))

for i in range(0, lenth):
    cleaned_sentences = []
    for review in df_list[i].contents:
        # count += 1
        # if count % 10 == 0:
        #     print(',', end='')
        # if count % 100 == 0:
        #     print()
        review = re.sub('[^가-힣0-9 ]', ' ', review)
        token = okt.pos(review, stem=True)      #pos - 형태소 분리를 시켜주고 품사를 지정해서 튜플로 묶어줌
        df_list_token = pd.DataFrame(token, columns=['word', 'class'])
        df_list_token = df_list_token[(df_list_token['class'] == 'Noun') |
                                      (df_list_token['class'] == 'Verb') |
                                      (df_list_token['class'] == 'Adjective') |
                                      (df_list_token['class'] == 'Number')]
        #불용어 처리-----------------------------
        words = []
        for word in df_list_token.word:
            if 1 < len(word) < 20:
                if word not in stopwords:
                    words.append(word)
        # ----------------------------------------
        # 형태소분리, 불용어 처리 된 단어들로 다시 문장으로 바꿈
        cleaned_sentence = ' '.join(words)
        cleaned_sentences.append(cleaned_sentence)
    df_list[i]['cleaned_sentences'] = cleaned_sentences
    df = df_list[i][['country', 'cleaned_sentences']]
    df.dropna(inplace=True)
    df.to_csv('./crawling_data/clean_data/clean_data_{}.csv'.format(city[i]), index=False)
    df.info()
