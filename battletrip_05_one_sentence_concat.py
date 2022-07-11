import pandas as pd
import glob
df = pd.DataFrame()
data_paths = glob.glob('./crawling_data/one_sentence_data/*')


for path in data_paths:
    df_temp = pd.read_csv(path)
    df_temp.dropna(inplace=True)
    df_temp.drop_duplicates(inplace=True)
    df = pd.concat([df, df_temp], ignore_index=True)
df.drop_duplicates(inplace=True)
df.info()

df.to_csv('./crawling_data/every_country_reviews.csv', index=False)


