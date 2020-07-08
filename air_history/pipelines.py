# -*- coding: utf-8 -*-
import copy

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi


class AirHistoryPipeline(object):
    # def open_spider(self,spider):
    #     self.file = open('area.json','w')
    #
    # def process_item(self, item, spider):
    #     context = json.dumps(dict(item),ensure_ascii=False) + '\n'
    #     self.file.write(context)
    #     return item
    #
    # def close_spider(self,spider):
    #     self.file.close()
    # 函数初始化
    def __init__(self, db_pool):
        self.db_pool = db_pool

    @classmethod
    def from_settings(cls, settings):
        """类方法，只加载一次，数据库初始化"""
        db_params = dict(
            host=settings['MYSQL_HOST'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            port=settings['MYSQL_PORT'],
            database=settings['MYSQL_DBNAME'],
            charset=settings['MYSQL_CHARSET'],
            use_unicode=True,
            # 设置游标类型
            cursorclass=cursors.DictCursor
        )
        # 创建连接池
        db_pool = adbapi.ConnectionPool('pymysql', **db_params)
        # 返回一个pipeline对象
        return cls(db_pool)

    def process_item(self, item, spider):
        """
        数据处理
        :param item:
        :param spider:
        :return:
        """
        type = item["type"]
        if type == '01':
            myItem = {}
            myItem["user_name"] = item["user_name"]
            myItem["praise_points"] = item["praise_points"]
            myItem["register_time"] = item["register_time"]
            myItem["company"] = item["company"]
            myItem["city"] = item["city"]
            myItem["university"] = item["university"]
            myItem["person_web"] = item["person_web"]
            myItem["person_profile"] = item["person_profile"]
            myItem["renown"] = item["renown"]
            myItem["browse_volume"] = item["browse_volume"]
            myItem["badge"] = item["badge"]
            myItem["badge_jin"] = item["badge_jin"]
            myItem["badge_yin"] = item["badge_yin"]
            myItem["badge_tong"] = item["badge_tong"]
            myItem["badge_desc"] = item["badge_desc"]
            myItem["answer_count"] = item["answer_count"]
            myItem["question_count"] = item["question_count"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_into, asynItem)
        if type == '02':
            myItem = {}
            myItem["user_name"] = item["user_name"]
            myItem["question_vote"] = item["question_vote"].replace(" ","")
            myItem["question_name"] = pymysql.escape_string(item["question_name"])
            myItem["question_url"] = item["question_url"]
            myItem["question_time"] = item["question_time"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_into_question, asynItem)
        if type == '03':
            myItem = {}
            myItem["user_name"] = item["user_name"]
            myItem["answer_vote"] = item["answer_vote"]
            myItem["answer"] = pymysql.escape_string(item["answer"])
            myItem["answer_url"] = item["answer_url"]
            myItem["answer_time"] = item["answer_time"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_into_answer, asynItem)
        if type == '04':
            myItem = {}
            myItem["question_volume"] = item["question_volume"]
            myItem["comment_num"] = item["comment_num"]
            myItem["question_url"] = item["question_url"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.update_question, asynItem)
        if type == '05':
            myItem = {}
            myItem["question_url"] = item["question_url"]
            myItem["comment_content"] = pymysql.escape_string(item["comment_content"])
            myItem["comment_vote"] = item["comment_vote"]
            myItem["sfcn"] = item["sfcn"]
            myItem["comment_time"] = item["comment_time"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_into_vote, asynItem)
        if type == '11':
            myItem = {}
            myItem["url"] = item["url"]
            myItem["ask_name"] = item["ask_name"]
            myItem["ask_time"] = item["ask_time"]
            myItem["ask_answercount"] = item["ask_answercount"]
            myItem["follow_count"] = item["follow_count"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_into_zhihu_ask, asynItem)
        if type == '12':
            myItem = {}
            myItem["url"] = item["url"]
            myItem["title"] = item["ask_name"]
            myItem["post_answercount"] = item["ask_answercount"]
            myItem["follow_count"] = item["follow_count"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_into_zhihu_post, asynItem)

        if type == '14':
            myItem = {}
            myItem["url"] = item["url"]
            myItem["title"] = item["ask_name"]
            myItem["answer_count"] = item["ask_answercount"]
            myItem["follow_count"] = item["follow_count"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.insert_into_zhihu_video, asynItem)

        if type == '13':
            myItem = {}
            myItem["url"] = item["url"]
            myItem["follow_count"] = item["follow_count"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)

            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.update_zhihu_videos, asynItem)

        if type == '15':
            myItem = {}
            myItem["url"] = item["url"]
            myItem["follow_count"] = item["follow_count"]
            myItem["ask_answercount"] = item["ask_answercount"]
            logging.warning(myItem)
            # 对象拷贝，深拷贝  --- 这里是解决数据重复问题！！！
            asynItem = copy.deepcopy(myItem)
            # 把要执行的sql放入连接池
            query = self.db_pool.runInteraction(self.update_zhihu_focus, asynItem)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, myItem, spider)
        return myItem

    # 处理sql函数
    def insert_into(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO user (user_name,praise_points,register_time,renown,browse_volume,badge,badge_jin,badge_yin,badge_tong,badge_desc,city,university,company,person_web,person_profile,answer_count,question_count) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            item['user_name'],item['praise_points'],item['register_time'],item["renown"],item["browse_volume"],item["badge"],item["badge_jin"],item["badge_yin"],item["badge_tong"],item["badge_desc"],item["city"],item["university"],item["company"],item["person_web"],item["person_profile"],item["answer_count"],item["question_count"])
        # 执行sql语句
        cursor.execute(sql)

    def insert_into_question(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO questions (user_name,question_name,question_url,question_time,question_vote) VALUES ('{}','{}','{}','{}','{}')".format(
            item['user_name'], item['question_name'], item['question_url'], item['question_time'], item['question_vote'])
        # 执行sql语句
        cursor.execute(sql)

    def insert_into_answer(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO answers (user_name,answer,answer_url,answer_time,answer_vote) VALUES ('{}','{}','{}','{}','{}')".format(
            item['user_name'], item['answer'], item['answer_url'], item['answer_time'],
            item['answer_vote'])
        # 执行sql语句
        cursor.execute(sql)
    def update_question(self, cursor, item):
        # 创建sql语句
        sql = "update questions set question_volume='{}',comment_num='{}' where question_url='{}'".format(
            item['question_volume'], item['comment_num'], item['question_url'])
        # 执行sql语句
        cursor.execute(sql)
    def insert_into_vote(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO comment_desc (question_url,comment_content,comment_vote,sfcn,comment_time) VALUES ('{}','{}','{}','{}','{}')".format(
            item['question_url'], item['comment_content'], item['comment_vote'], item['sfcn'],item['comment_time'])
        # 执行sql语句
        cursor.execute(sql)
    def insert_into_zhihu_ask(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO asks_0707 (url,ask_name,ask_time,ask_answercount,follow_count) VALUES ('{}','{}','{}','{}','{}')".format(
            item['url'], item['ask_name'], item['ask_time'], item['ask_answercount'],item['follow_count'])
        # 执行sql语句
        cursor.execute(sql)
    def insert_into_zhihu_post(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO posts_0707 (url,title,post_answercount,follow_count) VALUES ('{}','{}','{}','{}')".format(
            item['url'], item['title'],item['post_answercount'],item['follow_count'])
        # 执行sql语句
        cursor.execute(sql)

    def insert_into_zhihu_video(self, cursor, item):
        # 创建sql语句
        sql = "INSERT INTO videos_0707 (url,title,answer_count,follow_count) VALUES ('{}','{}','{}','{}')".format(
            item['url'], item['title'],item['answer_count'],item['follow_count'])
        # 执行sql语句
        cursor.execute(sql)

    def update_zhihu_videos(self, cursor, item):
        # 创建sql语句
        sql = "update 0525user set videos_count='{}' where url_token='{}'".format(
            item['follow_count'], item['url'])
        # 执行sql语句
        cursor.execute(sql)

    def update_zhihu_focus(self, cursor, item):
        # 创建sql语句
        sql = "update user_0707 set focus_count='{}',videos_count='{}' where url_token='{}'".format(
            item['follow_count'],item['ask_answercount'], item['url'])
        # 执行sql语句
        cursor.execute(sql)
    # 错误函数
    def handle_error(self, failure, item, spider):
        # #输出错误信息
        print("failure", failure)