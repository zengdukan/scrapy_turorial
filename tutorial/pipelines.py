# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import logging

class MysqlPipeline(object):

    def __init__(self, db_host, db_port, db_user, db_passwd, db_name, db_charset):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_passwd = db_passwd
        self.db_name = db_name
        self.db_charset = db_charset
        logging.info('%s,%s,%s,%s,%s,%s', self.db_host, self.db_port, self.db_user, self.db_passwd, self.db_name, self.db_charset)

    @classmethod
    def from_crawler(cls, crawler):
        return cls (
            db_host = crawler.settings.get('HOST'),
            db_port = crawler.settings.get("PORT"),
            db_user = crawler.settings.get("USER"),
            db_passwd = crawler.settings.get("PASSWORD"),
            db_name = crawler.settings.get('DB_NAME'),
            db_charset = crawler.settings.get('CHARSET')
        )

    def process_item(self, item, spider):
        with self.conn.cursor() as cursor:
            sql = "insert into quote (text, author, tags) values (%s,%s,%s)"
            cursor.execute(sql, (item['text'], item['author'], str(item['tags'])))
            self.conn.commit()
            
        return item

    def open_spider(self, spider):
        logging.info('%s,%s,%s,%s,%s,%s', self.db_host, self.db_port, self.db_user, self.db_passwd, self.db_name, self.db_charset)
        self.conn = pymysql.connect(
                host = self.db_host,
                port = self.db_port,
                user = self.db_user,
                password = self.db_passwd,
                db = self.db_name,
                charset = self.db_charset
            )
        logging.info('connect db')
    
    def close_spider(self, spider):
        self.conn.close()
        logging.info('close db')