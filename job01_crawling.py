from selenium import webdriver
import pandas as pd
from selenium.common. exceptions import NoSuchElementException
import time


options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
options.add_argument('lnag=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)
review_page_xpath = '//*[@id="content"]/div/div[1]/div'

for i in range(1, 3):
    url = 'https://www.ybtour.co.kr/eplg/episodeList.yb?pageNo={}'.format(i)
    titles = []
    reviews = []
    for j in range(1, 21):
        back_flag = False
        driver.get(url)
        title = driver.find_element("xpath", '//*[@id="content"]/table/tbody/tr[{}]/td[4]/a'.format(j)).text
        # print(title)
        review = driver.find_element('xpath', '//*[@id="content"]/table/tbody/tr[{}]/td[4]/a'.format(j)).click()
        time.sleep(0.5)
        review_page = driver.find_element('xpath', review_page_xpath).text
        # print(review_page)
        titles.append(title)
        reviews.append(review_page)
        time.sleep(0.5)
        driver.back()
        time.sleep(0.5)
    df = pd.DataFrame({'title': titles, 'reviews': reviews})
    df.to_csv('./crawling_data/reviews_{}page.csv'.format(i), index=False)
driver.close()