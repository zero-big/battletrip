import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
from konlpy.tag import Okt
import re
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./travel_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Tfidf_matrix = mmread('./models/Tfidf_trip_review.mtx').tocsr()
        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_battletrip.model')
        # self.comboBox.addItem('2017~2022 영화 리스트')
        self.df_reviews = pd.read_csv('./crawling_data/every_country_reviews.csv')
        self.country = list(self.df_reviews['country'])
        self.reviews = list(self.df_reviews['reviews'])
        self.country.sort()
        # for title in self.country:
        #     self.comboBox.addItem(title)
        self.cmb_region.currentIndexChanged.connect(self.cmb_region_slot)
        # self.comboBox.currentIndexChanged.connect(self.cmb_who_slot)
        # self.comboBox.currentIndexChanged.connect(self.cmb_purpose_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)

        # model = QStringListModel()
        # model.setStringList(self.titles)
        # completer = QCompleter()  # 자동완성객체
        # completer.setModel(model)
        # self.le_recommendation.setCompleter(completer)

    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore,
                          key=lambda x: x[1],
                          reverse=True)
        # simScore = simScore[1:11]
        simScore = simScore[:3]
        movieIdx = [i[0] for i in simScore]
        recMovieList = self.df_reviews.iloc[movieIdx, 0]
        return recMovieList

    def cmb_region_slot(self):
        self.cmb_region.currentText()

    def cmb_purpose_slot(self):
        self.cmb_purpose.currentText()

    def cmb_who_slot(self):
        self.cmb_who.currentText()
        # recommendation = self.recommendation_by_keyword(keyword)
        # self.lbl_recommendation.setText(recommendation)

    # def cmb_who_slot(self):
    #     who = self.comboBox.currentText()
    #     recommendation = self.recommendation_by_movie_title(who)
    #     self.lbl_recommendation.setText(recommendation)
    #
    # def cmb_purpose_slot(self):
    #     purpose = self.comboBox.currentText()
    #     recommendation = self.recommendation_by_movie_title(purpose)
    #     self.lbl_recommendation.setText(recommendation)

    def recommendation_by_movie_title(self, country):
        movie_idx = self.df_reviews[self.df_reviews['country'] == country].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[movie_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation[1:]))
        return recommendation

    def btn_slot(self):
        keywords = []
        if self.cmb_region.currentText():
            keywords.append(self.cmb_region.currentText())
        elif self.cmb_purpose.currentText():
            keywords.append(self.cmb_purpose.currentText())
        elif self.cmb_who.currentText():
            keywords.append(self.cmb_who.currentText())
        elif self.le_recommedation.text():
            keywords.append(self.le_recommedation.text)
        cleaned_sentence = ' '.join(keywords)
        recommendation = self.recommendation_by_keyword(cleaned_sentence)
        self.lbl_recommendation.setText(recommendation)
        # key_word = self.le_recommendation.text()
        # recommendation = self.recommendation_by_movie_title(key_word)
        # if key_word in self.country:
        #     self.recommendation_by_movie_title(key_word)
        # else:
        #     recommendation = self.recommendation_by_keyword(key_word)
        if recommendation:  # 입력받고 버튼 눌렀을 때만 텍스트가 뜨게
            self.lbl_recommendation.setText(recommendation)

    def recommendation_by_keyword(self, keyword):
        if keyword:  # le_recommendation에 입력됐을 때만 실행
            keyword = keyword.split()[0]
            try:
                sim_word = self.embedding_model.wv.most_similar(keyword, topn=10)
            except:
                self.lbl_recommendation.setText("알 수 없는 단어입니다.")
                return 0
            words = []
            for word, _ in sim_word:
                words.append(word)
            sentence = []
            count = 10
            for word in words:
                sentence = sentence + [word] * count
                count -= 1
            sentence = ' '.join(sentence)
            sentence_vector = self.Tfidf.transform([sentence])
            cosine_sim = linear_kernel(sentence_vector, self.Tfidf_matrix)
            recommendation = self.getRecommendation(cosine_sim)
            recommendation = '\n'.join(list(recommendation[:10]))
            return recommendation
        else:
            return 0

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())