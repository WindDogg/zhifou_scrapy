# -*- coding: utf-8 -*-
import pymysql
import scrapy
from air_history.items import ZhiHuItem

class ZhihuaskSpider(scrapy.Spider):
    name = 'zhihuask'
    allowed_domains = ['www.zhihu.com/people/F_falcon']
    start_urls = ['http://www.zhihu.com/']
    base_url = "https://www.zhihu.com/"
    urls = []
    pageNum = 1

    def parse(self, response):
        db = pymysql.connect(
            host='localhost',
            database='zhihu',
            user='root',
            password='123456',
            port=3306,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        cursor = db.cursor()
        cursor.execute(
            'SELECT url_token FROM 0525user limit 5 ')
        rows = cursor.fetchall()
        for row in rows:
            self.urls.append(row['url_token'])
        db.close()
        for url in self.urls:
            question_url = self.base_url + "people/" + url + "/asks?page=1"
            yield scrapy.Request(url=question_url, callback=self.parse_mid, dont_filter=True,
                                 meta={'user': url, 'type': '11'})

    def parse_mid(self, response):
        print("获取页数")
        question_num = int(response.xpath("//*[@id='ProfileMain']/div[1]/ul/li[4]/a/span/text()").get())
        url = response.meta['user']
        num1 = question_num // 20
        num2 = question_num % 20
        if num1 > 0 and num2 != 0:
            for page in range(1, num1 + 2):
                question_url = self.base_url + "people/" + url + "/asks?page=" + str(page)
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                     meta={'user': url, 'type': '11'})
        if num1 > 0 and num2 == 0:
            for page in range(1, num1 + 1):
                question_url = self.base_url + "people/" + url + "/asks?page=" + str(page)
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                     meta={'user': url, 'type': '11'})
        if num1 == 0:
            question_url = self.base_url + "people/" + url + "/asks?page=" + str(self.pageNum)
            yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                 meta={'user': url, 'type': '11'})

    def parse_info(self, response):
        print('根据用户名称去问题主页获取问题信息。。。。')
        item = ZhiHuItem()
        type = response.meta['type']
        if type == '11':
            selectorlist = response.xpath("//div[@class='List-item']").getall()
            size = len(selectorlist)
            for i in range(1, size + 1):
                item['url'] = response.meta['user']
                item['ask_name'] = response.xpath(
                    "//div[@class='List-item'][" + str(i) + "]/div/h2/div/a/text()").get().replace(
                    " ", "")
                item['ask_time'] = response.xpath(
                    "//div[@class='List-item'][" + str(i) + "]/div/div/span[1]/text()").get().strip()
                item['ask_answercount'] = response.xpath(
                    "//div[@class='List-item'][" + str(i) + "]/div/div/span[2]/text()").get().strip()
                item['follow_count'] =  response.xpath(
                    "//div[@class='List-item'][" + str(i) + "]/div/div/span[3]/text()").get().strip()
                item['type'] = type
                yield item
