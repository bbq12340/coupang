import requests, json
from bs4 import BeautifulSoup
import pandas as pd

class CoupangScraper():
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
            'listSize': 48,
            'page':page
        }
        r = requests.get(self.API_URL, params=param, headers=self.headers)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            item_list = soup.find_all('li', {'class': 'search-product'})
            for li in item_list:
                links.append(self.COUPANG+li.find('a')['href'])
            return links
        return
    
    def scrape_seller(self, q, c1, c2, c3):
        URL = f"https://www.coupang.com/vp/products/{c1}/items/{c2}/vendoritems/{c3}"
        headers = {
            "referer": f"https://www.coupang.com/vp/products/{c1}?itemId={c2}&vendorItemId={c3}&isAddedCart=",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
        }
        r = requests.get(URL, headers=headers).json()
        seller = r['returnPolicyVo']['sellerDetailInfo']
        data = {
            '키워드': q,
            '사업자번호': seller['bizNum'],
            '통신판매업신고번호': seller['ecommReportNum'],
            '이메일': seller['repEmail'],
            '전화번호': seller['repPhoneNum']
        }
        df = pd.DataFrame([data])
        return df