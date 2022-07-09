import pandas as pd
import os

files = os.listdir('./crawling_data/all_data')

df_list = []
city = []
for i in files:
    globals()[i.split('.')[0]] = pd.read_csv(f'./crawling_data/all_data/{i}')
    df_list.append(globals()[i.split('.')[0]])
    city_list = (i.split('.')[0]).split('_')[1]
    city.append(city_list)
lenth = int(len(city))


for i in range(0, lenth):
    df_list[i]['country'] = city[i]  #각 데이터프레임에 'country'의 이름으로 컬럼 추가
    cols = ['title', 'reviews']  # 두 컬럼 정의
    df_list[i]['contents'] = df_list[i][cols].apply(lambda row: ':'.join(row.values.astype(str)), axis=1) #위 두 컬럼을 'contents'컬럼에 합쳐서 작성
    df_list[i].dropna(inplace=True)
    df_list[i].drop_duplicates(inplace=True)
    df_list[i].drop(columns=['title'], inplace=True)
    df_list[i].drop(columns=['reviews'], inplace=True)
    df_list[i].drop_duplicates(inplace=True)
    df_list[i].to_csv('./crawling_data/add_column_data/reviews_{}.csv'.format(city[i]), index=False)
