# -*- coding: utf-8 -*-
import scrapy
import pymysql
from air_history.items import ZhiHuItem


class FollowedandvideoSpider(scrapy.Spider):
    name = 'followedandvideo'
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
            "select url_token from user_0707")
        rows = cursor.fetchall()
        for row in rows:
            self.urls.append(row)
        db.close()
        for url in self.urls:
            question_url = self.base_url + "people/" + url['url_token']
            yield scrapy.Request(url=question_url, callback=self.parse_focusnuminfo, dont_filter=True,
                                 meta={'user': url['url_token'],  'type': '15'})

    def parse_focusnuminfo(self, response):
        print('根据用户名称去主页获取关注了数量。。。。')
        item = ZhiHuItem()
        type = response.meta['type']
        if type == '15':
            item['url'] = response.meta['user']
            item['type'] = type
            item['ask_answercount'] = response.xpath("//*[@id='ProfileMain']/div[1]/ul/li[3]/a/span/text()").get()
            follow = response.xpath("//div[@class='Card FollowshipCard']/div/a[1]/div/strong/text()").get()
            item['follow_count'] = follow.replace(",","")
            yield item

