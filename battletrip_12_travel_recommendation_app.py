import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle

from PyQt5.QtGui import QPixmap
from konlpy.tag import Okt
import re
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./travel_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 모델 로드
        self.Tfidf_matrix = mmread('./models/Tfidf_trip_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_battletrip.model')

        # 콤보박스에 국가 리스트 추가
        # self.comboBox.addItem('2017~2022 영화 리스트')
        self.df_reviews = pd.read_csv('./crawling_data/every_country_reviews.csv')
        self.country = list(self.df_reviews['country'])
        self.reviews = list(self.df_reviews['reviews'])
        self.country.sort()

        print(len(self.country),self.country)
        # exit()
        # for title in self.country:
        #     self.comboBox.addItem(title)

        # 콤보박스 클릭 시
        self.cmb_region.currentIndexChanged.connect(self.cmb_region_slot)
        self.cmb_who.currentIndexChanged.connect(self.cmb_who_slot)
        self.cmb_purpose.currentIndexChanged.connect(self.cmb_purpose_slot)
        # 추천 버튼 클릭 시
        self.btn_recommendation.clicked.connect(self.btn_slot)

    def getRecommendation(self, cosine_sim):
        print('debug12')
        print(cosine_sim[-1])
        simScore = list(enumerate(cosine_sim[-1]))
        print('debug11')
        simScore = sorted(simScore,
                          key=lambda x: x[1],
                          reverse=True)
        simScore = simScore[:3]
        movieIdx = [i[0] for i in simScore]

        print('debug10')
        recMovieList = self.df_reviews.iloc[movieIdx, 0]
        return recMovieList
        print(recMovieList)


    def cmb_region_slot(self):
        self.cmb_region.currentText()

    def cmb_purpose_slot(self):
        self.cmb_purpose.currentText()

    def cmb_who_slot(self):
        self.cmb_who.currentText()


    def recommendation_by_movie_title(self, country):
        movie_idx = self.df_reviews[self.df_reviews['country'] == country].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation[1:]))
        return recommendation

    def btn_slot(self):
        keywords = []
        # 사용자가 '국가' 콤보박스 지정
        if self.cmb_region.currentText():
            keywords.append(self.cmb_region.currentText())
        # 사용자가 '테마' 콤보박스 지정
        if self.cmb_purpose.currentText():
            keywords.append(self.cmb_purpose.currentText())
        # 사용자가 '일행' 콤보박스 지정
        if self.cmb_who.currentText():
            keywords.append(self.cmb_who.currentText())
        #
        if self.le_recommendation.text():
            keywords.append(self.le_recommendation.text())
        print(keywords)
        key = ' '.join(keywords)
        print(key)
        recommendation = self.recommendation_by_keyword(key)
        print(type(recommendation))
        # 추천 스페인, 서유럽, 중납미
        recommendation = recommendation.split('\n')
        self.lbl_recommendation1.setText(recommendation[0])
        self.lbl_recommendation2.setText(recommendation[1])
        self.lbl_recommendation3.setText(recommendation[2])
        print(recommendation)

        pixmap = []
        for i in range(0, 3):
            print(i)
            pixmap.append(QPixmap('./IMG/{}.png'.format(recommendation[i])))
            # self.lbl_recommendation1.setPixmap(pixmap[i])
        # pixmap1 = QPixmap('./IMG/image.png')
        # pixmap2 = QPixmap('./IMG/image (1).png')
        # pixmap3 = QPixmap('./IMG/image (2).png')
        self.lbl_recommendation1.setPixmap(pixmap[0])
        self.lbl_recommendation2.setPixmap(pixmap[1])
        self.lbl_recommendation3.setPixmap(pixmap[2])


    # 키워드로 추천하는 함수
    def recommendation_by_keyword(self, keyword):
        # 사용자가 키워드 입력 시
        if keyword:
            try:
                keyword = keyword.split()
                lb_keyword = keyword[3]
                print(lb_keyword)
                sim_word = self.embedding_model.wv.most_similar(lb_keyword, topn=10)
                # 유사도 값 큰 순서로 7개 단어 리스트
                words = [lb_keyword]
                for word, _ in sim_word:
                    words.append(word)
                sentence = []
                count = 7
                for word in words:
                    sentence = sentence + [word] * count
                    count -= 1
                sentence = ' '.join(sentence)
                print(sentence)
                print('debug01')
                # sentence_vec = self.Tfidf.transform([sentence])
                # cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
                # recommend = self.getRecommendation(cosine_sim)

                cleaned_sentence = [keyword[0]]*5 + [keyword[1]] + [keyword[2]] + [sentence]
                cleaned_sentence = ' '.join(cleaned_sentence)
                print(cleaned_sentence)
                print('debug02')
                # 모델 적용
                sentence_vec = self.Tfidf.transform([cleaned_sentence])
                print(sentence_vec)
                # 코사인 유사도
                cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)
                print('debug05')
                # 추천
                recommendation = self.getRecommendation(cosine_sim) # 리스트 형태
                print(recommendation)

                print('debug03')
                recommendation = '\n'.join(list(recommendation[:3]))    # 문자열(줄바꿈) 형태
                return recommendation
            # 명사, 형용사/부사, 숫자 아닌 키워드 입력 시
            except:
                self.lbl_recommendation.setText("알 수 없는 단어입니다.")
                return 0
        # 사용자가 키워드 입력하지 않고 추천 버튼만 누른 경우
        else:
            return 0




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())