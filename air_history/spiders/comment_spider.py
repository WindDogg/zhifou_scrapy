# -*- coding: utf-8 -*-
import time

import pymysql
import scrapy

from air_history.items import AirHistoryItem


class CommentSpiderSpider(scrapy.Spider):
    name = 'comment_spider'
    allowed_domains = ['segmentfault.com']
    start_urls = ['http://segmentfault.com/']
    base_url = "https://segmentfault.com"
    urls = []

    def parse(self, response):
        db = pymysql.connect(
            host='localhost',
            database='test',
            user='root',
            password='123456',
            port=3306,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True)

        cursor = db.cursor()
        cursor.execute('select question_url from c')
        rows = cursor.fetchall()
        for row in rows:
            self.urls.append(row['question_url'])
        db.close()
        for url in self.urls:
            question_url = self.base_url + url
            yield scrapy.Request(url=question_url, callback=self.parse_info, dont_filter=True,
                                 meta={'question_url': url})

    def parse_info(self, response):
        print('根据用户名称去问题主页获取问题信息。。。。')
        comment_item = AirHistoryItem()
        comment_num = response.xpath("//div[@id='comment-total']/text()").get().split()[0]
        size = int(comment_num)
        for i in range(1, size + 1):
            comment_item['question_url'] = response.meta['question_url']
            comment_item['comment_content'] = response.xpath("string(//div[@class='card mb-2 border-0']["+str(i)+"]/div/div/div/article)").get().replace(" ","")
            comment_item['comment_vote'] = response.xpath("//div[@class='card mb-2 border-0']["+str(i)+"]/div/div/div/div[2]/div/div[1]/div[1]/button[1]/span[2]/text()").get()
            comment_item['sfcn'] = response.xpath("//div[@class='card mb-2 border-0']["+str(i)+"]/div/div/div/div[2]/div/div[1]/button/text()").get()
            comment_time = response.xpath("//div[@class='card mb-2 border-0']["+str(i)+"]/div/div/div/div[2]/div/div[2]/span[@class='text-secondary']/text()").get()
            if comment_time is not None and "月" in comment_time :
                comment_time = '2019-'+comment_time.replace("月","-").replace("日","")
            comment_item['comment_time'] = comment_time
            comment_item['type'] = '05'
            yield comment_item