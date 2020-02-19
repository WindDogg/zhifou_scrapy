# -*- coding: utf-8 -*-
import scrapy
from air_history.items import AirHistoryItem
import pymysql
class AreaSpiderSpider(scrapy.Spider):
    name = 'area_spider'
    allowed_domains = ['segmentfault.com/']  # 爬取的域名，不会超出这个顶级域名
    base_url = "https://segmentfault.com"
    start_urls = [base_url]
    usernamelist=[]
    def parse(self, response):
        print('开始爬取。。')

        # city_list = response.xpath("//div[@class='all']/div[@class='bottom']/ul/div[2]/li/a/text()").extract()  # 城市名称
        # self.pageNum = self.pageNum + 1
        # if self.pageNum <5:
        for pageNum in range(1002,1400):
          nexturl = self.base_url + "/questions?page=" + str(pageNum)
          yield scrapy.Request(url=nexturl, callback=self.parse_user, method="GET",dont_filter=True)

    def parse_user(self, response):
        print('爬取首页问答模块获取用户名称....')
        user_list = response.xpath("//section[contains(@class,'stream-list__item')]/div[@class='summary']/ul[1]/li/a[1]/@href").extract()  # 全部链接
        print(user_list)
        for url in user_list:
            if url not in self.usernamelist:
               self.usernamelist.append(url)
               url = self.base_url + url
               username = url.split("/u/")[1]
               yield scrapy.Request(url=url, callback=self.parse_info,dont_filter=True,meta={'user':username,'type':'01'})

    def parse_info(self,response):
        print('根据用户名称去用户主页获取用户基本信息。。。。')
        item = AirHistoryItem()
        type = response.meta['type']
        if type == '01':
            item['user_name'] = response.meta['user']
            item['praise_points'] = response.xpath("//div[@class='col-md-3']/div[1]/ul/li[1]/text()").get().replace(" ","").replace("获得","").replace("次点赞","")
            register_time = response.xpath("//div[@class='profile__skill--other']/p[1]/text()[1]").get().replace(" ","").replace("注册于","")
            if "月" in register_time:
                register_time = "2019-"+register_time.replace("月","-").replace("日","")
            item['register_time'] = register_time
            item['company'] = response.xpath("//div[@class='profile__heading--other']/span[contains(@class,'profile__heading--other-item ')]/span[@class='profile__company']/text()").get()
            item['city'] = response.xpath("//div[@class='profile__heading--other']/span[contains(@class,'profile__heading--other-item ')]/span[@class='profile__city']/text()").get()
            item['university'] = response.xpath("//div[@class='profile__heading--other']/span[contains(@class,'profile__heading--other-item ')]/span[@class='profile__school']/text()").get()
            item['person_web'] = response.xpath("//div[@class='profile__heading--other']/span[contains(@class,'profile__heading--other-item ')]/span[@class='profile__site']/a[1]/@href").get()
            item['person_profile'] = response.xpath("//div[@class='profile__heading--desc-body']/div[@class='profile__desc']/p[1]/text()").get()
            item['renown'] = response.xpath("//div[@class='profile__heading--award']/a/span[1]/text()").get()
            item['browse_volume'] = response.xpath("//div[@class='profile__skill--other']/p[1]/text()[2]").get().replace(" ","").replace("个人主页被","").replace("人浏览","")
            item['badge'] = response.xpath("//ul[@class='authlist']/li[2]/text()").get().replace(" ","").replace("获得","").replace("枚徽章","")
            badge_desc = response.xpath("//ul[@class='authlist']/li[2]/cite/text()").get().replace(" ","").replace("获得","")
            item['badge_jin'] = badge_desc.split(',')[0].replace("枚金徽章","")
            item['badge_yin'] = badge_desc.split(',')[1].replace("枚银徽章", "")
            item['badge_tong'] = badge_desc.split(',')[2].replace("枚铜徽章", "")
            item['badge_desc'] = badge_desc
            item['answer_count'] = response.xpath("//div[@class='row']/div[1]/ul/li[3]/a/span[@class='count']/text()").get()
            item['question_count'] = response.xpath("//div[@class='row']/div[1]/ul/li[4]/a/span[@class='count']/text()").get()
            item['type'] = type
        # item = AirHistoryItem()
        # node_list = response.xpath("//div[@class='row']")
        # # node_list.pop(0)  # 去除第一行标题栏
        # for node in node_list:
        #     item['data'] = node.xpath("./div[@class='col-md-3']/div[1]/ul/li/text()").get()
        #     # item['city'] = response.meta['city']
        #     # item['aqi'] = node.xpath('./td[2]/text()').get()
        #     # item['level'] = node.xpath('./td[3]/text()').get()
        #     # item['pm2_5'] = node.xpath('./td[4]/text()').get()
        #     # item['pm10'] = node.xpath('./td[5]/text()').get()
        #     # item['so2'] = node.xpath('./td[6]/text()').get()
        #     # item['co'] = node.xpath('./td[7]/text()').get()
        #     # item['no2'] = node.xpath('./td[8]/text()').get()
        #     # item['o3'] = node.xpath('./td[9]/text()').get()
        yield item