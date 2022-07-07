from selenium import webdriver
import pandas as pd
from selenium.common. exceptions import NoSuchElementException
import time


options = webdriver.ChromeOptions()
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
options.add_argument('lnag=ko_KR')
driver = webdriver.Chrome('./chromedriver.exe', options=options)
review_page_xpath = '//*[@id="content"]/div/div[1]/div'
city = ['중국','일본', '베트남', '태국', '필리핀',
        '싱가포르','코타키나발루','인도','서유럽','동유럽',
        '북유럽','터키','스페인','미서부','미동부',
        '중남미','시드니','뉴질랜드','아프리카', '이집트']

url = 'https://www.ybtour.co.kr/search/searchPdt.yb?query={}&departDate=&cityList={}'.format(city[0],city[0])
driver.get(url)
time.sleep(1.0)
# time.sleep(1.0)
titles = []
reviews = []
driver.find_element('xpath', '//*[@id="container"]/div[2]/div[3]/ul/li[3]/a').click()
time.sleep(1.0)
for i in range(1, 405):
    # back_flag = False

    # time.sleep(1.0)
    title = driver.find_element("xpath", '//*[@id="tab_page"]/div[4]/table/tbody/tr[{}]/td[4]/a'.format(i)).text
    time.sleep(1.0)
    print(title)
    review = driver.find_element('xpath', '//*[@id="tab_page"]/div[4]/table/tbody/tr[{}]/td[4]/a'.format(i)).click()
    time.sleep(1.0)
    review_page = driver.find_element('xpath', review_page_xpath).text
    print(review_page)
    titles.append(title)
    reviews.append(review_page)
    driver.back()
    time.sleep(1.0)
    driver.find_element('xpath', '//*[@id="container"]/div[2]/div[3]/ul/li[3]/a').click()
    time.sleep(1.0)
    print(i)
    df = pd.DataFrame({'title': titles, 'reviews': reviews})
    df.to_csv('./crawling_data/reviews_{}page.csv'.format(i), index=False)
driver.close()