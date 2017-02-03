# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import sqlite3

class DateParse(object):

    def process_item(self, item, spider):

        datum_str = item['post_date']
        time_struct = time.strptime(datum_str[4:], '%d.%m.%Y %H:%M')
        item['post_date'] = time.strftime('%Y-%m-%d %H:%M', time_struct)

        return item

class SQLPersist(object):

    def __init__(self):

        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS mydata (id INTIGER PRIMARY KEY, post_text TEXT, post_link TEXT, post_date TEXT, post_theme TEXT)')

    def process_item(self, item, spider):

        forum_post = [(item['post_text'], item['post_link'], item['post_date'], item['post_theme'])]
        self.cursor.executemany('INSERT INTO mydata VALUES(?,?,?,?)', forum_post)
        self.connection.commit()

        return item