# -*- coding: utf-8 -*-
import scrapy
import pymysql
from air_history.items import ZhiHuItem

class PostsSpider(scrapy.Spider):
    name = 'posts'
    allowed_domains = ['www.zhihu.com/people/mllh/posts']
    start_urls = ['http://www.zhihu.com/people/mllh/posts/']

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
            'select url_token from user_0707 where articles_count>0  ')
        rows = cursor.fetchall()
        for row in rows:
            self.urls.append(row['url_token'])
        db.close()
        for url in self.urls:
            question_url = self.base_url + "people/" + url + "/posts?page=1"
            yield scrapy.Request(url=question_url, callback=self.parse_mid, dont_filter=True,
                                 meta={'user': url, 'type': '12'})

    def parse_mid(self, response):
        print("获取页数")
        list = response.xpath("//*[@id='ProfileMain']/div[1]/ul/li[5]/a/span/text()").get().replace(",","")
        question_num = int(list)
        url = response.meta['user']
        num1 = question_num // 20
        num2 = question_num % 20
        if num1 > 0 and num2 != 0:
            for page in range(1, num1 + 2):
                question_url = self.base_url + "people/" + url + "/posts?page=" + str(page)
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                     meta={'user': url, 'type': '12'})
        if num1 > 0 and num2 == 0:
            for page in range(1, num1 + 1):
                question_url = self.base_url + "people/" + url + "/posts?page=" + str(page)
                yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                     meta={'user': url, 'type': '12'})
        if num1 == 0:
            question_url = self.base_url + "people/" + url + "/posts"
            yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                 meta={'user': url, 'type': '12'})

    def parse_info(self, response):
        print('根据用户名称去问题主页获取问题信息。。。。')
        item = ZhiHuItem()
        type = response.meta['type']
        if type == '12':
            selectorlist = response.xpath("//div[@class='List-item']").getall()
            size = len(selectorlist)
            print(size)
            for i in range(1, size + 1):
                item['url'] = response.meta['user']
                item['ask_name'] = response.xpath(
                    "//div[@class='List-item'][" + str(i) + "]/div/h2/a/text()").get().replace(
                    " ", "")
                tiaojian = len(response.xpath("//div[@class='List-item'][" + str(i) + "]/div/div[2]/div").getall())
                print(tiaojian)
                if tiaojian ==2:
                    answercount = response.xpath(
                        "//div[@class='List-item'][" + str(i) + "]/div/div[2]/div[2]/button[1]/text()").get().strip()
                    follow = response.xpath(
                        "//div[@class='List-item'][" + str(i) + "]/div/div[2]/div[2]/span/button/text()").get()
                else:
                    answercount = response.xpath(
                        "//div[@class='List-item'][" + str(i) + "]/div/div[2]/div[3]/button[1]/text()").get().strip()
                    follow = response.xpath(
                        "//div[@class='List-item'][" + str(i) + "]/div/div[2]/div[3]/span/button/text()").get()
                if(answercount=='添加评论'):
                    answercount='0'
                item['ask_answercount'] = answercount.replace(" 条评论","")

                if follow is  None:
                    follow='0'
                item['follow_count'] =follow.strip().replace("赞同","")
                item['type'] = type
                yield item
