# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time

class DateParse(object):

    def process_item(self, item, spider):

        datum_str = item['post_date']
        time_struct = time.strptime(datum_str[4:], '%d.%m.%Y %H:%M')
        item['post_date'] = time.strftime('%Y-%m-%d %H:%M', time_struct)

        return item
