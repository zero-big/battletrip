import pandas as pd

df0 = pd.read_csv('./crawling_data/all_data/reviews_미서부.csv')
df1 = pd.read_csv('./crawling_data/all_data/reviews_베트남.csv')
df2 = pd.read_csv('./crawling_data/all_data/reviews_대만.csv')
df3 = pd.read_csv('./crawling_data/all_data/reviews_북유럽.csv')
df4 = pd.read_csv('./crawling_data/all_data/reviews_서유럽.csv')
df5 = pd.read_csv('./crawling_data/all_data/reviews_스페인.csv')
df6 = pd.read_csv('./crawling_data/all_data/reviews_싱가포르.csv')
df7 = pd.read_csv('./crawling_data/all_data/reviews_인도.csv')
df8 = pd.read_csv('./crawling_data/all_data/reviews_일본.csv')
df9 = pd.read_csv('./crawling_data/all_data/reviews_중국.csv')
df10 = pd.read_csv('./crawling_data/all_data/reviews_코타키나발루.csv')
df11 = pd.read_csv('./crawling_data/all_data/reviews_태국.csv')
df12 = pd.read_csv('./crawling_data/all_data/reviews_필리핀.csv')
df13 = pd.read_csv('./crawling_data/all_data/reviews_동유럽.csv')
df14 = pd.read_csv('./crawling_data/all_data/reviews_뉴질랜드.csv')
df15 = pd.read_csv('./crawling_data/all_data/reviews_아프리카.csv')
df16 = pd.read_csv('./crawling_data/all_data/reviews_중남미.csv')
df17 = pd.read_csv('./crawling_data/all_data/reviews_이집트.csv')
df18 = pd.read_csv('./crawling_data/all_data/reviews_시드니.csv')
df19 = pd.read_csv('./crawling_data/all_data/reviews_터키.csv')
city = ['미서부','베트남','대문','북유럽','서유럽','스페인',
        '싱가포르','인도','일본','중국','코타키나발루',
        '태국','필리핀','동유럽','뉴질랜드','아프리카',
        '중남미','이집트','시드니','터키']
df_list = [df0, df1, df2, df3, df4, df5, df6, df7, df8, df9, df10, df11, df12, df14, df15, df16, df17, df18, df19]

for i in range(19, 20):
    df_list[i]['country'] = city[i]
    cols = ['title', 'reviews']
    df_list[i]['contents'] = df_list[i][cols].apply(lambda row: ':'.join(row.values.astype(str)), axis=1)
    df_list[i].dropna(inplace=True)
    df_list[i].drop_duplicates(inplace=True)
    # cols = ['title', 'reviews']
    # df_list[i]['contents'] = df_list[i][cols].apply(lambda row: ':'.join(row.values.astype(str)), axis=1)
    df_list[i].drop(columns=['title'],inplace=True)
    df_list[i].drop(columns=['reviews'],inplace=True)
    df_list[i].drop_duplicates(inplace=True)



