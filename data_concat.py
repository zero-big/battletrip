import pandas as pd
import os

print(os.getcwd())


df1 = pd.read_csv('C:/works/python/battletrip_crawling/crawling_data/all_data/reviews_중국.csv')
df2 = pd.read_csv('C:/works/python/battletrip_crawling/crawling_data/reviews_장가계.csv')

df1.info()
df2.info()
df3 = pd.concat([df1, df2], ignore_index=True)
df3.to_csv('./concat_data/reviews_중국.csv', index=False)
df3.info()