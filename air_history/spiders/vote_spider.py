# -*- coding: utf-8 -*-
import time

import pymysql
import scrapy

from air_history.items import AirHistoryItem


class VoteSpiderSpider(scrapy.Spider):
    name = 'vote_spider'
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
        cursor.execute('SELECT question_url  from (select *,row_number() over(PARTITION by user_name order by question_time) as rn from questions )a where rn=1  ')
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
        question_item = AirHistoryItem()
        comment_item = AirHistoryItem()
        comment_num = response.xpath("//div[@class='pb15']/text()").get().split()[0]
        question_item['question_url'] = response.meta['question_url']
        question_item['question_volume'] = response.xpath("//div[@class='block-for-right-border']/div[1]/span/text()").get()
        question_item['comment_num'] = comment_num
        question_item['type'] = '04'
        yield question_item
        size = int(comment_num)
        for i in range(1, size + 1):
            comment_item['question_url'] = response.meta['question_url']
            comment_item['comment_content'] = response.xpath("string(//article[contains(@class,'clearfix widget-answers__item')]["+str(i)+"]/div[@class='post-offset']/div[1])").get().replace(" ","")
            comment_item['comment_vote'] = response.xpath("//article[contains(@class,'clearfix widget-answers__item')]["+str(i)+"]/div[@class='post-col']/div[1]/span/text()").get()
            comment_item['sfcn'] = response.xpath("//article[contains(@class,'clearfix widget-answers__item')]["+str(i)+"]/div[@class='post-col']/div[2]/span/text()").get()
            comment_time = response.xpath("//div[@class='answer__info--date']["+str(i)+"]").get().replace(" ","").replace("回答","")
            if "月" in comment_time:
                comment_time = '2019-'+comment_time.replace("月","-").replace("日","")
            comment_item['comment_time'] = comment_time
            comment_item['type'] = '05'
            yield comment_item