# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy



class PinterestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comment_count = scrapy.Field()
    created_at = scrapy.Field()
    description = scrapy.Field()
    domain = scrapy.Field()
    dominant_color = scrapy.Field()
    id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    like_count = scrapy.Field()
    link = scrapy.Field()
    repin_count = scrapy.Field()
    type = scrapy.Field()
    origin_pin_id = scrapy.Field()
    tags = scrapy.Field()
    width = scrapy.Field()
    height = scrapy.Field()
    item = scrapy.Field()
    top_tag = scrapy.Field()
    image_paths = scrapy.Field()
