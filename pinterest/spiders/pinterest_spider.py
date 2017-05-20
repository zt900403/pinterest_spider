# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from pinterest.items import PinterestItem

import json


class PinterestSpiderSpider(scrapy.Spider):
    name = "pinterest_spider"
    allowed_domains = ["pinterest.com"]
    start_urls = ['https://www.pinterest.com/pin/188306828149812775/']

    RelatedPinFeedResource_headers = {
        'accept': "application/json, text/javascript, */*; q=0.01",
        'accept-encoding': "gzip, deflate, sdch, br",
        'accept-language': "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
        'connection': "keep-alive",
        'host': "www.pinterest.com",
        'x-requested-with': "XMLHttpRequest",
        'cache-control': "no-cache",
        'postman-token': "0c461037-7738-63b4-b69d-c8d66c4f39ed"
    }

    def parse(self, response):
        url_pre = 'https://www.pinterest.com/resource/RelatedPinFeedResource/get/'
        for one in response.xpath('//div[@class="GrowthUnauthPinImage"]/a/@href'):
            pinID = one.extract().replace('/pin/', '').replace('/', '')
            url_suf = '?source_url=/pin/%s/&data={"options":{"pin":"%s","page_size":25,"pins_only"' \
            ':true,"bookmarks":[],"offset":0,"field_set_key":"unauth_react"},"context":{}}' % (pinID, pinID)
            yield scrapy.Request(url_pre + url_suf, headers=self.RelatedPinFeedResource_headers, meta={'pinID': pinID},
                                 callback=self.relate_pin_parser)

    def relate_pin_parser(self, response):

        jdata = json.loads(response.body.decode("utf-8"))
        items = jdata['resource_response']['data']
        for i in items:
            scraped_item = PinterestItem()
            scraped_item['comment_count'] = i['comment_count']
            scraped_item['created_at'] = i['created_at']
            scraped_item['description'] = i['description']
            scraped_item['domain'] = i['domain']
            scraped_item['dominant_color'] = i['dominant_color']
            scraped_item['id'] = i['id']
            scraped_item['image_urls'] = [ i['images']['orig']['url'] ]
            scraped_item['like_count'] = i['like_count']
            scraped_item['link'] = i['link']
            scraped_item['repin_count'] = i['repin_count']
            scraped_item['type'] = i['type']
            scraped_item['origin_pin_id'] =jdata['client_context']['visible_url'].replace('/pin/', '').replace('/', '')
            yield scraped_item

