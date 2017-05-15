# -*- coding: utf-8 -*-
import scrapy


class PinterestSpiderSpider(scrapy.Spider):
    name = "pinterest_spider"
    allowed_domains = ["pinterest.com"]
    start_urls = ['http://pinterest.com/']

    def parse(self, response):
        pass
