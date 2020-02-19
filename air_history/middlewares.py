from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


class AreaSpiderMiddleware(object):
    def process_request(self, request, spider):
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        # 指定谷歌浏览器路径
        self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'G:\GameDownload\chromedriver_win32\chromedriver.exe')
        # if request.url != 'https://segmentfault.com/questions':
        #     self.driver.get(request.url)
        #     time.sleep(1)
        #     html = self.driver.page_source
        #     self.driver.quit()
        #     return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
        #                                     request=request)