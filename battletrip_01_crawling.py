from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from selenium.common. exceptions import NoSuchElementException
import time


options = webdriver.ChromeOptions()
# options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 1})
options.add_argument('lnag=ko_KR')
print('debug3')
driver = webdriver.Chrome('./chromedriver.exe', options=options)
print('debug4')
# driver.implicitly_wait(10)

review_page_xpath = '//*[@id="content"]/div/div[1]/div'
print('debug5')
city = ['푸켓']
print('debug6')
# review_range = driver.find_element('xpath', '//*[@id="tab_page"]/div[4]/table/tbody/tr[1]/td[1]').text
# review_range = review_range.replace(',', '')
# review_range = int(review_range) + 1
for i in city[0:1]:
    print('debug7')
    url = 'https://www.ybtour.co.kr/search/searchPdt.yb?query={}&departDate=&cityList={}'.format(i, i)
    print('debug1')
    driver.get(url)
    print('debug2')
    time.sleep(2.0)
# time.sleep(1.0)
    titles = []
    reviews = []
    driver.find_element('xpath', '//*[@id="container"]/div[2]/div[3]/ul/li[3]/a').click()
    review_range = driver.find_element('xpath', '//*[@id="tab_page"]/div[4]/table/tbody/tr[1]/td[1]').text
    review_range = review_range.replace(',', '')
    review_range = int(review_range) + 1
    time.sleep(2.0)
    print(review_range)
    for j in range(189, review_range):
        try:
            # back_flag = False
            driver.find_element('xpath', '//*[@id="container"]/div[2]/div[3]/ul/li[3]/a').click()
            time.sleep(3)
            title = driver.find_element("xpath",
                                        '// *[ @ id = "tab_page"] / div[4] / table / tbody / tr[{}] / td[4] / a'.format(
                                            j)).text
            time.sleep(0.5)
            print(title)
            review = driver.find_element('xpath',
                                         '//*[@id="tab_page"]/div[4]/table/tbody/tr[{}]/td[4]/a'.format(j)).click()
            time.sleep(4)
            review_page = driver.find_element('xpath', review_page_xpath).text
            # print(review_page)
            titles.append(title)
            reviews.append(review_page)
            time.sleep(0.5)
            driver.back()
            time.sleep(3.0)
            # driver.find_element('xpath', '//*[@id="container"]/div[2]/div[3]/ul/li[3]/a').click()
            # time.sleep(2.0)
            df = pd.DataFrame({'title': titles, 'reviews': reviews})
            df.to_csv('./crawling_data/{}/reviews_{}.csv'.format(i, j), index=False)
        except:
            print('page', i, j)
            driver.get(url)
            time.sleep(2.0)
    df = pd.DataFrame({'title': titles, 'reviews': reviews})
    df.to_csv('./crawling_data/{}/reviews_{}.csv'.format(i, i), index=False)
print('debug9')
driver.close()
