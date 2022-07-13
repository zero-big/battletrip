
import background as background
import family
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import collections
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

font_path = 'crawling_data/malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')

df= pd.read_csv('./crawling_data/new_every_country_reviews.csv')
words = df[df['country'] == '코타키나발루']['reviews']
print(words.iloc[0])
words = words.iloc[0].split()
print(words)

worddict = collections.Counter(words)
worddict = dict(worddict)
print(worddict)

wordcloud_img = WordCloud(
    background_color='white', max_words=2000,
    font_path=font_path).generate_from_frequencies(worddict)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud_img, interpolation='bilinear')
plt.axis('off')
plt.show()