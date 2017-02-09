# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import sqlite3
from scrapy import log
import re


class DateParse(object):

    def process_item(self, item, spider):

        datum_str = item['post_date']
        time_struct = time.strptime(datum_str[4:], '%d.%m.%Y %H:%M')
        item['post_date'] = time.strftime('%Y-%m-%d %H:%M', time_struct)

        return item


class CleanHTML(object):

    def process_item(self, item, spider):

        text = item['post_text']
        text = re.sub(r"(?is)<(script|style).*?>.*?(</\1>)", "", text.strip()) # inline js and css
        text = re.sub(r"(?s)<!--(.*?)-->[\n]?", "", text) # html comments
        text = re.sub(r"(?s)<.*?>", " ", text) # tags
        text = re.sub(r"&nbsp;", " ", text) # whitespace
        text = re.sub(r"  ", " ", text)
        text = re.sub(r"  ", " ", text)
        item['post_text'] = text

        return item


class SQLPersist(object):

    def __init__(self):

        self.connection = sqlite3.connect('data.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('CREATE TABLE `scraped` ( `id` INTEGER PRIMARY KEY AUTOINCREMENT, `link` TEXT, `tema` TEXT, `date_scraped` TEXT, `date_posted` TEXT )')

    def process_item(self, item, spider):

        self.cursor.execute('SELECT * FROM scraped WHERE link=?', (item['post_link'],))
        result = self.cursor.fetchone()

        if result:
            log.msg('Item %s in database!' % item['post_link'], level=log.DEBUG)
        else:
            forum_post = [(None, item['post_link'], item['post_text'], item['post_theme'], item['post_date'],  )]
            self.cursor.executemany('INSERT INTO mydata VALUES(?,?,?,?,?)', forum_post)
            self.connection.commit()

        return item

if __name__ == '__main__':

    c = sqlite3.connect('data.db')
    cur = c.cursor()
    cur.execute('SELECT * FROM mydata')
    data = cur.fetchall()
    print (type(data))
    print
