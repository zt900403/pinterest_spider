# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response
from pinterest.items import PinterestItem
import sys
import os
from scrapy.linkextractors import LinkExtractor

import json


class PinterestSpiderSpider(scrapy.Spider):
    name = "pinterest_spider"
    allowed_domains = ["pinterest.com"]
    start_urls = ['https://www.pinterest.com/pin/431923420492871843/']

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
        for _ in response.xpath('//div[@class="GrowthUnauthPin_brioPin"]'):
            relatedPin_getbody = self.relatedPin_getbody_gen(pinID)
            yield scrapy.Request(self.relatedPin_baseurl + relatedPin_getbody, cookies=None, headers=self.headers,
                                 callback=self.related_pin_parser)

    def relatedPin_getbody_gen(self, pinID):
        return '?source_url=/pin/%s/&data={"options":{"pin":"%s","page_size":25,"pins_only"' \
               ':true,"bookmarks":[],"add_vase":true, "offset":0,"field_set_key":"unauth_react"},"context":{}}' % (
               pinID, pinID)

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
            scraped_item['image_urls'] = [item['images']['orig']['url']]
            scraped_item['like_count'] = item['like_count']
            scraped_item['link'] = item['link']
            scraped_item['repin_count'] = item['repin_count']
            scraped_item['type'] = item['type']
            pinID = item['id']
            scraped_item['tags'] = item['pin_join']['visual_annotation']
            a = tags_statistic_top3(item['pin_join']['visual_annotation'])
            scraped_item['top_tag'] = a[0]
            f = open('tags.txt', 'a')
            f.write(a[0] + ' ' + a[1] + ' ' + a[2]+'\n')
            f.close()
            relatedPin_getbody = self.relatedPin_getbody_gen(pinID)

            yield scrapy.Request(self.relatedPin_baseurl + relatedPin_getbody, cookies=None, headers=self.headers,
                                 callback=self.related_pin_parser)
            yield scraped_item


def tags_statistic_top3(tags):
    excepted_word = ["to", "the", "a", "on", "of", "and", "with", "for", "st", "or", "have", "has", "had"]
    if tags.__len__() <= 0:
        return []
    else:
        word = []
        for words in tags:
            for i in words.split():
                word.append(i)
        word_count = {}
        for w in word:
            lower_w = w.lower()
            if lower_w not in excepted_word:
                if lower_w not in word_count:
                    word_count[lower_w] = 1
                else:
                    word_count[lower_w] += 1
        a = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
        top3 = [a[0][0], a[1][0], a[2][0]]
        return top3
