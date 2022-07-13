import pandas as pd
from konlpy.tag import Okt
import re
import os
okt = Okt()
df_stopwords = pd.read_csv('./stopwords.csv')
stopwords = list(df_stopwords['stopword'])
stopwords = stopwords +['차장님', '과장님', '매니저', '매니져', '가이드', '풍선', '노랑', '여행'
                         '노랑풍선', '상품', '덕분', '해주다', '비행기', '감사하다', '되어다',
                         '도착', '‘투어', '가다', '여행', '오다', '많다', '다녀오다',
                         '일정', '한국', '정도', '드리다', '이동', '주다', '보이다',
                         '현지', '크다', '나오다', '자다', '만나다', '받다', '챙기다', '들다',
                         '호텔', '출발', '여행사', '싶다', '아쉽다', '대회', '내부', '여행객',
                         '인솔', '만들다', '들어가다', '마지막', '이렇다', '이용', '위치',
                         '다니다', '찾다', '모습', '오늘', '모르다', '느끼다', '보내다',
                         '타고', '주다', '힘들다', '올라가다', '따다', '찍다', '이동',
                         '세계', '우리나라', '설명', '싶다', '좋다', '기다리다', '가다',
                         '리다', '알다', '시설', '안되다', '어떻다', '괜찮다', '알다',
                         '더욱', '처음', '진행', '상황', '이따', '걱정', '미리',
                         '안내', '마음', '관광객', '하루', '나라', '전화', '준비',
                         '밉다', '지나', '미동', '내내', '모든', '후기', '식사', '자리',
                         '가이드님', '가이드', '인솔자', '인솔자님', '팀장님', '차장님',
                         '과장님', '부장님', '소장님', '반장님','담당자', '담당자님',
                         '매니저', '매니져', '캡틴', '우한', '폐렴', '우한 폐렴', '여행',
                         '패키지', '후기', '노랑풍선', '센스', '쎈쓰', '노랑 풍선', '홈&쇼핑',
                         '프로정신', '여행기', '프로', '아저씨', '풍선', '노랑', '상픔',
                         '여행사', '감사', '덕분', '칭찬', '설명', '일정', '투어', '한국', '우리나라', '일행', '이렇다',
                         '어떻다', '많다','되어다', '가다', '나오다', '오다', '정도', '가지', '리다', '보이', '내내', '타고', '지다', '의하다']

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
