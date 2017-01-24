# -*- coding: utf-8 -*-

from scrapy import Spider, Request

class ForumSpider(Spider):

    name = 'forum_spider'
    base_url = 'http://www.bug.hr'
    allowed_domains = ['bug.hr']

    def parse(self, response):

        teme = response.xpath(u'//tr/td/div/a/@href').extract()

        for t in teme:
            yield Request(url=(self.base_url + t), callback=self.parse_tema)

    def parse_tema(self, response):

        s_str = response.xpath(u'//dt/a[text() = "sljedeća"]/@href').extract_first()

        if s_str is not None:
            yield Request((s_str + self.base_url), callback=self.parse_tema)