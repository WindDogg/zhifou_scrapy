# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AirHistoryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #list="https://segmentfault.com/u/akabu" str=list.split("/u/")[1]  str2=list.split("/u/")
    user_name = scrapy.Field() #日期
    praise_points = scrapy.Field() #点赞数
    register_time = scrapy.Field() #注册时间
    renown = scrapy.Field() # 声望值
    browse_volume = scrapy.Field() #浏览量
    badge = scrapy.Field() #徽章
    badge_jin = scrapy.Field()
    badge_yin = scrapy.Field()
    badge_tong = scrapy.Field()
    badge_desc = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    university = scrapy.Field()
    person_web = scrapy.Field()
    person_profile = scrapy.Field()
    answer_count = scrapy.Field()
    question_count = scrapy.Field()

    answer = scrapy.Field() #回答
    answer_vote = scrapy.Field()
    answer_url = scrapy.Field()
    answer_time =scrapy.Field() #回答时间

    question_name = scrapy.Field() #问题
    question_volume =scrapy.Field() #问题浏览量
    comment_num = scrapy.Field() #评论数
    question_vote = scrapy.Field() #投票数
    question_url = scrapy.Field()
    question_time = scrapy.Field()

    comment_content = scrapy.Field()
    comment_vote = scrapy.Field()
    sfcn = scrapy.Field()
    comment_time = scrapy.Field()

    type = scrapy.Field()

class ZhiHuItem(scrapy.Item):
    url = scrapy.Field()
    ask_name = scrapy.Field()
    ask_time = scrapy.Field()
    ask_answercount = scrapy.Field()
    follow_count = scrapy.Field()
    type = scrapy.Field()




