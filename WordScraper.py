import random
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from retry import retry
from bs4 import BeautifulSoup
import pandas as pd
import time

COUPANG = "https://www.coupang.com/"
SEARCH_BAR_ID = "headerSearchKeyword"
POPULAR_WORDS_ID = "headerPopupWords"
RELATED_WORDS_CLASS = "search-query-result"
HEADERS = {
    'referer': 'https://www.coupang.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}


def extract_coupang_words(query_list, delay):
    browser = start_driver()
    wait = WebDriverWait(browser, 10)
    result = []
    for query in query_list:
        data = search_coupang(browser, wait, query)
        result.append(data)
        time.sleep(delay)
    browser.quit()
    df = pd.DataFrame(result)
    df.to_csv(f"result/{query_list[0]}.csv", encoding="utf-8-sig", index=False)
    print('finished!')


def start_driver():
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
    options.add_argument('headless')
    browser = webdriver.Chrome(
        ChromeDriverManager().install(), options=options)
    return browser


@retry(Exception, delay=random.uniform(0, 2), jitter=1)
def search_coupang(browser, wait, query):
    browser.get(COUPANG+f"np/search?component=&q={query}&channel=recent")
    search_bar = browser.find_element_by_id(SEARCH_BAR_ID)
    time.sleep(1)
    search_bar.click()
    wait.until(EC.visibility_of_element_located(
        (By.ID, POPULAR_WORDS_ID)))
    html = browser.execute_script(
        "return document.documentElement.outerHTML;")
    soup = BeautifulSoup(html, 'html.parser')
    popular_words = scrape_popular_words(soup)
    related_words = scrape_related_words(soup)
    data = {
        '검색어': query,
        '자동완성 검색어': popular_words,
        '연관 검색어': related_words
    }
    return data


def scrape_popular_words(soup):
    autocomplete = soup.find('div', {'class': 'autocomplete_wrap'})
    popular_words = (',').join([t.text for t in autocomplete.find_all('a')])
    return popular_words


def scrape_related_words(soup):
    search_related_keywords = soup.find(
        'dl', {'class': 'search-related-keyword'})
    related_words = (',').join(
        [t.text for t in search_related_keywords.find("dd").find_all("a")])
    return related_words
