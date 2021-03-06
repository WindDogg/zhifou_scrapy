from scrapy import signals
import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from air_history.settings import USER_AGENT_LIST

class AreaSpiderMiddleware(object):
    # def process_request(self, request, spider):
    #     chrome_options = Options()
    #     chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
    #     chrome_options.add_argument('--disable-gpu')
    #     chrome_options.add_argument('--no-sandbox')
    #     # 指定谷歌浏览器路径
    #     self.driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=r'E:\1\chromedriver.exe')
        # if request.url != 'https://segmentfault.com/questions':
        #     self.driver.get(request.url)
        #     time.sleep(1)
        #     html = self.driver.page_source
        #     self.driver.quit()
        #     return scrapy.http.HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8',
        #                                     request=request)
    def process_request(self, request, spider):
        # proxy = random.choice(PROXY)
        # request.meta['proxy'] = proxy
        user_agent = random.choice(USER_AGENT_LIST)
        if user_agent:
            request.headers.setdefault('User-Agent', user_agent)