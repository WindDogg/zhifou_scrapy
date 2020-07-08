# -*- coding: utf-8 -*-
import scrapy
import pymysql
from air_history.items import ZhiHuItem

class VideosSpider(scrapy.Spider):
    name = 'videos'
    allowed_domains = ['www.zhihu.com/people/mllh/zvideos']
    start_urls = ['http://www.zhihu.com/people/mllh/zvideos/']

    base_url = "https://www.zhihu.com/"
    urls = []
    dict = {}
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
            "select url_token,videos_count from user_0707 where videos_count>0")
        rows = cursor.fetchall()
        for row in rows:
            self.urls.append(row)
        db.close()
        for url in self.urls:
            question_url = self.base_url + "people/" + url['url_token'] +"/zvideos"
            yield scrapy.Request(url=question_url, callback=self.parse_mid, dont_filter=True,
                                 meta={'user': url['url_token'],'count':url['videos_count'], 'type': '14'})

    def parse_mid(self, response):
        print("获取页数")
        list = response.meta['count']
        question_num = int(list)
        print(question_num)
        url = response.meta['user']
        num1 = question_num // 20
        num2 = question_num % 20
        if num1 > 0 and num2 != 0:
            for page in range(1, num1 + 2):
                question_url = self.base_url + "people/" + url + "/zvideos?page=" + str(page)
                if page==num1+1:
                    size=num2
                else:
                    size=20
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                     meta={'user': url,'size':size, 'type': '14'})
        if num1 > 0 and num2 == 0:
            for page in range(1, num1 + 1):
                question_url = self.base_url + "people/" + url + "/zvideos?page=" + str(page)
                size = 20
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                     meta={'user': url,'size':size, 'type': '14'})
        if num1 == 0:
            question_url = self.base_url + "people/" + url + "/zvideos?page=" + str(self.pageNum)
            size = num2
            yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                 meta={'user': url,'size':size, 'type': '14'})

    def parse_info(self, response):
        print('根据用户名称去问题主页获取问题信息。。。。')

        item = ZhiHuItem()
        type = response.meta['type']
        size = response.meta['size']
        if type == '14':
            selectorlist = response.xpath("//div[@class='List-item']").getall()
            size = int(size)
            print(size)
            for i in range(1, size + 1):
                print(i)
                item['url'] = response.meta['user']
                path = "//div[@class='List-item'][" + str(i) + "]/div/h2/a/text()"
                print(path)
                ask = response.xpath(path).get()
                print(ask)
                item['ask_name'] = ask.replace(" ", "")
                answercount = response.xpath(
                    "//div[@class='List-item'][" + str(i) + "]/div/div[2]/div[3]/div/button[1]/text()").get().strip()
                follow = response.xpath(
                    "//div[@class='List-item'][" + str(i) + "]/div/div[2]/div[3]/div/span/button[1]/text()").get()
                if (answercount == '添加评论'):
                    answercount = '0'
                item['ask_answercount'] = answercount.replace(" 条评论", "")

                if follow is None:
                    follow = '0'
                item['follow_count'] = follow.strip().replace("赞同", "")
                item['type'] = type
                yield item

