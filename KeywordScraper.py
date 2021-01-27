import re

from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver


class KeywordScraper:
    def __init__(self):
        self.browser = self.start_browser()
        self.wait = WebDriverWait(self.browser, 10)
        self.MOBILE_URL = "https://m.coupang.com/"


    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
        return browser

    def extract_keyword(self):
        BANNER = By.CLASS_NAME, "close-banner"
        SEARCH_ICON = By.ID, "searchBtn"
        POP = By.XPATH, '//*[@id="suggest"]/ul[2]'
        self.browser.get(self.MOBILE_URL)
        try:
            banner = self.browser.find_element_by_class_name("close-banner")
            banner.click()
        except:
            pass
        try:
            self.wait.until(EC.presence_of_element_located(SEARCH_ICON))
            self.browser.find_element_by_id("searchBtn").click()
            self.wait.until(EC.presence_of_element_located(POP))
        except:
            pass
        
        html = self.browser.execute_script('return document.documentElement.outerHTML')
        soup = BeautifulSoup(html, 'html.parser')
        pop = soup.find_all('ul',{'class':'pop'})[1]
        extracted = [a.find_all('span')[1].text for a in pop.find_all('a')]
        return extracted
