import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
import pandas as pd
from sklearn.metrics.pairwise import linear_kernel
from gensim.models import Word2Vec
from scipy.io import mmread
import pickle
import webbrowser
from PyQt5.QtGui import QPixmap
from konlpy.tag import Okt
import re
from PyQt5.QtCore import QStringListModel

form_window = uic.loadUiType('./travel_recommendation.ui')[0]

class Exam(QWidget, form_window):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.url = [None, None, None]
        self.Tfidf_matrix = mmread('./models/Tfidf_trip_review.mtx').tocsr()

        with open('./models/tfidf.pickle', 'rb') as f:
            self.Tfidf = pickle.load(f)
        self.embedding_model = Word2Vec.load('./models/word2vec_battletrip.model')

        self.df_reviews = pd.read_csv('./crawling_data/every_country_reviews.csv')
        img = QPixmap('./ticket1.jpg')
        self.background.setPixmap(img)
        self.cmb_region.currentIndexChanged.connect(self.cmb_region_slot)
        self.cmb_who.currentIndexChanged.connect(self.cmb_who_slot)
        self.cmb_purpose.currentIndexChanged.connect(self.cmb_purpose_slot)
        self.btn_recommendation.clicked.connect(self.btn_slot)
        self.p_btn_0.clicked.connect(self.web_link0_slot)
        self.p_btn_1.clicked.connect(self.web_link1_slot)
        self.p_btn_2.clicked.connect(self.web_link2_slot)


    # def btn_click(self):

    def web_link0_slot(self):
        if self.url[0]:
            webbrowser.open(self.url[0])
    def web_link1_slot(self):
        if self.url[1]:
            webbrowser.open(self.url[1])
    def web_link2_slot(self):
        if self.url[2]:
            webbrowser.open(self.url[2])
    def getRecommendation(self, cosine_sim):
        simScore = list(enumerate(cosine_sim[-1]))
        simScore = sorted(simScore,
                          key=lambda x: x[1],
                          reverse=True)
        simScore = simScore[:3]
        tripIdx = [i[0] for i in simScore]
        recpointList = self.df_reviews.iloc[tripIdx, 0]
        return recpointList



    def cmb_region_slot(self):
        self.cmb_region.currentText()

    def cmb_purpose_slot(self):
        self.cmb_purpose.currentText()

    def cmb_who_slot(self):
        self.cmb_who.currentText()


    def recommendation_by_trip_title(self, country):
        trip_idx = self.df_reviews[self.df_reviews['country'] == country].index[0]
        cosine_sim = linear_kernel(self.Tfidf_matrix[trip_idx], self.Tfidf_matrix)
        recommendation = self.getRecommendation(cosine_sim)
        recommendation = '\n'.join(list(recommendation[1:]))
        return recommendation

    def btn_slot(self):
        keywords = []
        if self.cmb_region.currentText():
            keywords.append(self.cmb_region.currentText())

        if self.cmb_purpose.currentText():
            keywords.append(self.cmb_purpose.currentText())
        if self.cmb_who.currentText():
            keywords.append(self.cmb_who.currentText())
        if self.le_recommendation.text():
            keywords.append(self.le_recommendation.text())

        key = ' '.join(keywords)

        recommendation = self.recommendation_by_keyword(key)

        recommendation = recommendation.split('\n')

        self.lbl_recommendation1.setText(recommendation[0])
        self.lbl_recommendation2.setText(recommendation[1])
        self.lbl_recommendation3.setText(recommendation[2])
        print(recommendation)

        pixmap = []
        for i in range(0, 3):
            pixmap.append(QPixmap('./IMG/{}.png'.format(recommendation[i])))
            self.url[i] = 'https://www.ybtour.co.kr/search/searchPdt.yb?query={}&departDate=&cityList='.format(recommendation[i])
        print(self.url)


        self.lbl_recommendation1.setPixmap(pixmap[0])
        self.lbl_recommendation2.setPixmap(pixmap[1])
        self.lbl_recommendation3.setPixmap(pixmap[2])



    def recommendation_by_keyword(self, keyword):
        if keyword:
            try:
                keyword = keyword.split()
                lb_keyword = keyword[3]
                sim_word = self.embedding_model.wv.most_similar(lb_keyword, topn=10)
                words = [lb_keyword]
                for word, _ in sim_word:
                    words.append(word)
                sentence = []
                count = 7
                for word in words:
                    sentence = sentence + [word] * count
                    count -= 1
                sentence = ' '.join(sentence)
                # print(sentence)


                cleaned_sentence = [keyword[0]]*5 + [keyword[1]] + [keyword[2]] + [sentence]
                cleaned_sentence = ' '.join(cleaned_sentence)
                # print(cleaned_sentence)

                sentence_vec = self.Tfidf.transform([cleaned_sentence])
                # print(sentence_vec)
                cosine_sim = linear_kernel(sentence_vec, self.Tfidf_matrix)

                recommendation = self.getRecommendation(cosine_sim)
                # print(recommendation)


                recommendation = '\n'.join(list(recommendation[:3]))
                return recommendation
            except:
                self.lbl_recommendation.setText("알 수 없는 단어입니다.")
                return 0
        else:
            return 0




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Exam()
    mainWindow.show()
    sys.exit(app.exec_())