# crawling_data 폴더 안에 add_column_data 폴더를 추가하세요.

import pandas as pd
import os

path = './crawling_data/all_data'  # all_data에는 크롤링이 완료된 리뷰가 들어있도록 합의하였습니다
files = os.listdir(path)

df_list = []
city_list = []
for i in files:
    df = pd.read_csv('./crawling_data/all_data/{}'.format(i))
    df_list.append(df)
    city = i.split('.')[0].split('_')[1]
    city_list.append(city)
city_nums = len(city_list)
# print(city_nums)  # 크롤링 완료한 지역 개수를 알고 싶으면 주석을 푸세요

# country별 리뷰로 재정의
for i in range(0, city_nums):
    df_list[i]['country'] = city_list[i]  # 각 데이터프레임에 'country'의 이름으로 컬럼 추가
    cols = ['title', 'reviews']  # 두 컬럼 정의
    df_list[i]['contents'] = df_list[i][cols].apply(lambda row: ':'.join(row.values.astype(str)), axis=1)  # 위 두 컬럼을 'contents'컬럼에 합쳐서 작성
    df_list[i].dropna(inplace=True)
    df_list[i].drop_duplicates(inplace=True)
    df_list[i].drop(columns=['title'], inplace=True)
    df_list[i].drop(columns=['reviews'], inplace=True)
    df_list[i].drop_duplicates(inplace=True)  # 기존의 column들을 제거한 후 다시 한번 중복값을 제거
    df_list[i].to_csv('./crawling_data/add_column_data/reviews_{}.csv'.format(city_list[i]), index=False)