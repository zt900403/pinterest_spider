# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from pinterest.items import PinterestItem
from scrapy.linkextractors import LinkExtractor

import json


class PinterestSpiderSpider(scrapy.Spider):
    name = "pinterest_spider"
    allowed_domains = ["pinterest.com"]
    start_urls = ['https://www.pinterest.com/pin/188306828149812775/']

    headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-encoding': "gzip, deflate, sdch, br",
        'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
        'connection': "keep-alive",
        'host': "www.pinterest.com",
        'x-requested-with': "XMLHttpRequest",
    }
    pinResource_baseurl = 'https://www.pinterest.com/resource/PinResource/get/'
    relatedPin_baseurl = 'https://www.pinterest.com/resource/RelatedPinFeedResource/get/'
    def parse(self, response):
        pinID = response.url.split('/')[4]

        for brioPin in response.xpath('//div[@class="GrowthUnauthPin_brioPin"]'):
            tags = brioPin.xpath('//a[@role="contentinfo"]/text()').extract()
            pinResource_getbody = '?source_url=/pin/%s/' \
                        '&data={"options":{"id":"%s","field_set_key":"detailed"},"context":{}}' % (pinID, pinID)
            yield scrapy.Request(self.pinResource_baseurl + pinResource_getbody, cookies=None, headers=self.headers,
                                meta={
                                        'tags': tags
                                      },
                                callback=self.pin_self_parser)
            relatedPin_getbody = self.relatedPin_getbody_gen(pinID)
            yield scrapy.Request(self.relatedPin_baseurl + relatedPin_getbody, cookies=None, headers=self.headers,
                                callback=self.related_pin_parser)


    def relatedPin_getbody_gen(self, pinID):
        return '?source_url=/pin/%s/&data={"options":{"pin":"%s","page_size":25,"pins_only"' \
        ':true,"bookmarks":[],"add_vase":true, "offset":0,"field_set_key":"unauth_react"},"context":{}}' % (pinID, pinID)

    def pin_self_parser(self, response):
        jdata = json.loads(response.body.decode('utf-8'))
        item = jdata['resource_response']['data']
        scraped_item = PinterestItem()
        scraped_item['comment_count'] = item['comment_count']
        scraped_item['created_at'] = item['created_at']
        scraped_item['description'] = item['description']
        scraped_item['domain'] = item['domain']
        scraped_item['dominant_color'] = item['dominant_color']
        scraped_item['id'] = item['id']
        scraped_item['image_urls'] = [item['images']['orig']['url']]
        scraped_item['like_count'] = item['like_count']
        scraped_item['link'] = item['link']
        scraped_item['repin_count'] = item['repin_count']
        scraped_item['type'] = item['type']
        scraped_item['tags'] =response.meta['tags']

        yield scraped_item

    def related_pin_parser(self, response):
        jdata = json.loads(response.body.decode('utf-8'))
        items = jdata['resource_response']['data']
        for item in items:
            scraped_item = PinterestItem()
            scraped_item['comment_count'] = item['comment_count']
            scraped_item['created_at'] = item['created_at']
            scraped_item['description'] = item['description']
            scraped_item['domain'] = item['domain']
            scraped_item['dominant_color'] = item['dominant_color']
            scraped_item['id'] = item['id']
            scraped_item['image_urls'] = [ item['images']['orig']['url'] ]
            scraped_item['like_count'] = item['like_count']
            scraped_item['link'] = item['link']
            scraped_item['repin_count'] = item['repin_count']
            scraped_item['type'] = item['type']
            pinID = item['id']
            scraped_item['tags'] = item['pin_join']['visual_annotation']

            relatedPin_getbody = self.relatedPin_getbody_gen(pinID)
            yield scrapy.Request(self.relatedPin_baseurl + relatedPin_getbody, cookies=None, headers=self.headers,
                                 callback=self.related_pin_parser)

            yield scraped_item

