# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ForumPost(Item):

    post_text = Field()
    post_link = Field()
    post_theme = Field()
    post_date = Field()
