import pandas as pd
from konlpy.tag import Okt
import re
import os


# 데이터 로드
df = pd.read_csv('./crawling_data/one_sentence_data/review_one_캄보디아.csv')
df.info()


# 데이터 전처리
## tokenizer 로드
okt = Okt()

## stopword 로드
df_stopwords = pd.read_csv('./crawling_data/stopwords.csv')
stopwords = list(df_stopwords['stopword'])
# 영화와 직접적으로 관련된 stopword 추가
stopwords = stopwords + ['가이드님', '가이드', '인솔자', '인솔자님', '팀장님', '차장님', '과장님', '부장님', '소장님', '반장님',
                         '담당자', '담당자님', '매니저', '매니져', '캡틴', '우한', '폐렴', '우한 폐렴', '여행', '패키지', '후기',
                         '노랑풍선', '센스', '쎈쓰', '노랑 풍선', '홈&쇼핑', '프로정신', '여행기', '프로', '아저씨', '풍선', '노랑',
                         '상픔', '여행사', '감사', '덕분', '칭찬', '설명', '일정', '투어', '한국', '우리나라', '일행', '이렇다',
                         '어떻다', '많다']
stopwords = stopwords + ['되어다', '가다', '나오다', '오다', '정도', '가지', '리다', '보이', '내내', '타고', '지다', '의하다']

## 한글 제외 모두 제거
cleaned_sentences = []
for review in df.reviews:
    ## 형태소 분리
    review = re.sub('[^가-힣0-9 ]', ' ', review)
    token = okt.pos(review, stem=True)  # pos - 형태소 분리를 시켜주고 품사를 지정해서 튜플로 묶어줌
    df_list_token = pd.DataFrame(token, columns=['word', 'class'])
    df_list_token = df_list_token[(df_list_token['class'] == 'Noun') |
                                  # (df_list_token['class'] == 'Verb') |
                                  (df_list_token['class'] == 'Adjective') |
                                  (df_list_token['class'] == 'Number')]

    ## 불용어 제거
    words = []
    for word in df_list_token.word:
        ## 한 글자 제거
        if len(word) > 1:
            if word not in stopwords:
                words.append(word)
    # 형태소 리스트 + 품사 리스트
    cleaned_sentence = ' '.join(words)
    cleaned_sentences.append(cleaned_sentence)  # [형태소 + 품사]
# clean_sentences 컬럼 추가
df['reviews'] = cleaned_sentences
# review 컬럼 제거
df = df[['country', 'reviews']]

# 결측치 제거
df.dropna(inplace=True)

# 저장
df.to_csv('./crawling_data/new_one_sentence_data/new_review_one_캄보디아.csv', index=False)
