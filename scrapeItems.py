import requests
from bs4 import BeautifulSoup

class ItemScraper():
    def __init__(self):
        self.COUPANG = "https://www.coupang.com"
        self.API_URL = "https://www.coupang.com/np/search"
        self.headers = {
            "referer": "https://www.coupang.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
    def query(self, q, page):
        links = []
        param = {
            'q':q,
            'channel':'user',
            'page':page
        }
        r = requests.get(self.API_URL, params=param, headers=self.headers)
        soup = BeautifulSoup(r.text, 'html.parser')
        item_list = soup.find_all('li', {'class': 'search-product'})
        for li in item_list:
            links.append(self.COUPANG+li.find('a')['href'])
        return links