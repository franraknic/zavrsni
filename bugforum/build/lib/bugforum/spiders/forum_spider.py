# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from bugforum.items import ForumPost

class ForumSpider(Spider):

    name = 'forum_spider'
    base_url = 'http://www.bug.hr'
    allowed_domains = ['bug.hr']
    start_urls = ['http://www.bug.hr/forum/']

    def parse(self, response):

        teme = response.xpath(u'//tr/td/div/a/@href').extract()

        for t in teme:
            yield Request(url=(self.base_url + t), callback=self.parse_tema)

    def parse_tema(self, response):

        threads = response.xpath(u'//tr/td/a[@class = "naslov"]/@href').extract()

        for t in threads:
            yield Request((self.base_url + t), callback=self.parse_post)

        s_str = response.xpath(u'//dt/a[text() = "sljedeća"]/@href').extract_first()

        if s_str is not None:
            yield Request((self.base_url + s_str), callback=self.parse_tema)

    def parse_post(self, response):

        item = ForumPost()
        item['post_text'] = response.xpath(u'//div[@class = "poruka porukabody"][text()]').extract_first()
        item['post_date'] = response.xpath(u'//div[@class = "datumContainer"]/div[@class = "datum"]/text()').extract_first()
        item['post_theme'] = response.xpath(u'//dl[@class = "f_breadcrumb"]/dt/a/text()').extract()[-1]
        item['post_link'] = response._get_url()

        return item
