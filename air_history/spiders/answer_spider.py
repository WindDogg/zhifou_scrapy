# -*- coding: utf-8 -*-
import time

import scrapy
from air_history.items import AirHistoryItem
import pymysql

class AnswerSpiderSpider(scrapy.Spider):
    name = 'answer_spider'
    allowed_domains = ['segmentfault.com']
    base_url = "https://segmentfault.com"
    start_urls = ['http://segmentfault.com/']
    urls = []
    pageNum = 1

    def parse(self, response):
        db = pymysql.connect(
            host='localhost',
            database='test',
            user='root',
            password='123456',
            port=3306,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True
        )
        cursor = db.cursor()
        cursor.execute('SELECT user_name FROM user u WHERE u.question_count >=1 and u.answer_count >=1 and not EXISTS (select 1 from b where u.user_name=b.user_name)')
        rows = cursor.fetchall()
        for row in rows:
            self.urls.append(row['user_name'])
        db.close()
        for url in self.urls:
            question_url = self.base_url + "/u/" + url + "/answers?page=1"
            yield scrapy.Request(url=question_url, callback=self.parse_mid, dont_filter=True,
                                 meta={'user': url, 'type': '03'})

    def parse_mid(self, response):
        print("获取页数")
        question_num = int(response.xpath("//div[@class='row']/div[1]/ul/li[3]/a/span[@class='count']/text()").get())
        url = response.meta['user']
        num1 = question_num // 20
        num2 = question_num % 20
        if num1 > 0 and num2 != 0:
            for page in range(1, num1 + 2):
                question_url = self.base_url + "/u/" + url + "/answers?page=" + str(page)
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                    meta={'user': url, 'type': '03'})
        if num1 > 0 and num2 == 0:
            for page in range(1, num1 + 1):
                question_url = self.base_url + "/u/" + url + "/answers?page=" + str(page)
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                     meta={'user': url, 'type': '03'})
        if num1 == 0:
            question_url = self.base_url + "/u/" + url + "/answers?page=" + str(self.pageNum)
            yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                 meta={'user': url, 'type': '03'})

    def parse_info(self, response):
        print('根据用户名称去问题主页获取问题信息。。。。')
        item = AirHistoryItem()
        type = response.meta['type']
        if type == '03':
            selectorlist = response.xpath("//ul[@class='profile-mine__content']/li").getall()
            size = len(selectorlist)
            for i in range(1,size+1):
                item['user_name'] = response.meta['user']
                item['answer_vote'] = response.xpath("//ul[@class='profile-mine__content']/li["+ str(i)+"]/div[1]/div[1]/span/text()").get().replace(" ","").replace("票","")
                item['answer'] = response.xpath("//ul[@class='profile-mine__content']/li["+ str(i)+"]/div[1]/div[2]/a/text()").get().strip()
                item['answer_url'] = response.xpath("//ul[@class='profile-mine__content']/li["+ str(i)+"]/div[1]/div[2]/a/@href").get().strip()
                answer_time = response.xpath("//ul[@class='profile-mine__content']/li["+ str(i)+"]/div[1]/div[3]/span/text()").get().strip()
                if "前" in answer_time:
                    answer_time = time.strftime('%Y-%m-%d',time.localtime(time.time()))
                if "月" in answer_time:
                    answer_time = "2019-"+answer_time.replace("月","-").replace("日","")
                item['answer_time'] = answer_time
                item['type'] = type
                yield item