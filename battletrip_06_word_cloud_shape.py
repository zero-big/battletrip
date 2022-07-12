
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

font_path = './malgun.ttf'
font_name = font_manager.FontProperties(
    fname=font_path).get_name()
plt.rc('font', family='NanumBarunGothic')

df= pd.read_csv('./crawling_data/new_every_country_reviews.csv')
words = df[df['country'] == '서유럽']['reviews']
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


import matplotlib as mpl
import matplotlib.font_manager as fm
print('설정파일 위치:', mpl.matplotlib_fname())
# exit()



im = Image.open('./crawling_data/airplane.jpg')  # 이미지 파일 읽어오기
mask_arr = np.array(im)  # 픽셀 값 배열 형태 변환

wordcloud = WordCloud(font_path='./NanumBarunGothic.ttf', background_color='white', colormap='autumn',
                      width=700, height=700, random_state=43, mask=mask_arr,
                      prefer_horizontal=True).generate_from_frequencies(worddict)

plt.figure(figsize=(12, 12))
plt.imshow(wordcloud)
plt.title("Word Frequency", size=13)

plt.axis('off')

plt.show()