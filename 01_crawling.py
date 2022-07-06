from selenium import webdriver
import pandas as pd
from selenium.common.exceptions import NoSuchElementException
import time


options = webdriver.ChromeOptions()
driver = webdriver.Chrome('./chromedriver.exe', options=options)
options.add_argument('lang=ko_KR')

# 노랑풍선 url 주소
# https://www.ybtour.co.kr/eplg/episodeList.yb?pageNo=1     ~1342 페이지까지


# 리뷰 제목 Xpath (1페이지당 20개)
# //*[@id="content"]/table/tbody/tr[1]/td[4]/a
# //*[@id="content"]/table/tbody/tr[2]/td[4]/a
# ...
# //*[@id="content"]/table/tbody/tr[20]/td[4]/a
review_title_xpath = '//*[@id="content"]/table/tbody/tr[1]/td[4]/a'


# 리뷰 Xpath
# //*[@id="content"]/div/div[1]/div
# //*[@id="content"]/div/div[1]/div
# //*[@id="content"]/div/div[1]/div
review_xpath = '//*[@id="content"]/div/div[1]/div'


# 모든 페이지에서
for i in range(1, 1343):
    url = 'https://www.ybtour.co.kr/eplg/episodeList.yb?pageNo={]'.format(i)
    titles = []
    reviews = []
    try:
        # driver.get(url)
        ## 리뷰 제목
        for j in range(1,21):
            driver.get(url)
            time.sleep(0.5)
            review_title_xpath = '//*[@id="content"]/table/tbody/tr[{}]/td[4]/a'.format(j)
            try:
                title = driver.find_element("xpath", review_title_xpath).text    # 리뷰 제목의 텍스트만 받아오기
                driver.find_element("xpath", review_title_xpath).click() # 리뷰 제목 클릭
                time.sleep(0.5)
                ## 리뷰
                try:
                    review = driver.find_element("xpath", review_xpath).text    # 리뷰글의 텍스트만 받아오기
                    # print(title)
                    # print(review)
                    titles.append(title)
                    reviews.append(review)
                    driver.back()   # 뒤로가기
                except:
                    print('review : ', i, j)
        df = pd.DataFrame({'title':titles, 'reviews':reviews})
        df.to_csv('./crawling_data/MovieReview_2020/reviews_{}_{}page.csv'.format(your_year, i), index=False)
    except:
        print('page : ', i) #몇번째 페이지에서 에러났는지
driver.close()
