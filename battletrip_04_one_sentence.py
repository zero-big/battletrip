import pandas as pd
import os

files = os.listdir('./crawling_data/clean_data')
print(files)
df_list = []
city = []
for i in files:
    globals()[i.split('.')[0]] = pd.read_csv(f'./crawling_data/clean_data/{i}')
    df_list.append(globals()[i.split('.')[0]])
    city_list = (i.split('.')[0]).split('_')[2]
    city.append(city_list)
lenth = int(len(city))


for i in range (0, lenth):
    df_list[i].dropna(inplace=True)
    print(df_list[i].info())
    one_sentences = []
    for title in df_list[i]['country'].unique():
        print(df_list[i]['country'])
        temp = df_list[i][df_list[i]['country'] == city[i]]
        print(temp)
        one_sentence = ' '.join(temp['cleaned_sentences'])
        one_sentences.append(one_sentence)
        print(one_sentence)
    df_list[i] = pd.DataFrame({'country':df_list[i]['country'].unique(), 'reviews':one_sentences})

    df_list[i].to_csv('./crawling_data/one_sentence_data/review_one_{}.csv'.format(city[i]), index=False)
