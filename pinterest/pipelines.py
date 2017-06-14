.00# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os, sys
import urllib.request
from scrapy.exceptions import DropItem
import scrapy
import hashlib
import shutil
from scrapy.contrib.pipeline.images import ImagesPipeline
import pymongo
from scrapy.conf import settings
from pymongo import MongoClient
from scrapy import log


class MongoPipeline(object):
    def __init__(self):
        connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem('Missing{0}!'.format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg('question added to mongodb database!',
                    level=log.DEBUG, spider=spider)
        return item


class MyImagesPipeline(ImagesPipeline):
    # save pic with default pipeline
    # move pic to classified folder.
    def get_media_requests(self, item, info):

        for img_url in item['image_urls']:
            yield scrapy.Request(img_url)

    def item_completed(self, results, item, info):
        image_ori_paths = [x['path'] for ok, x in results if ok]
        image_filename = image_ori_paths[0].split('/')[-1]

        imgFolder = settings['FULL_PIC_STORE'] + image_filename[0:2] + '/' + image_filename[2:4] + '/' + image_filename[4:6] + '/'  # 下载图片的保存路径
        if not os.path.isdir(imgFolder):
            os.makedirs(imgFolder)
        if not image_ori_paths:
            raise DropItem("Item contains no images")
        else:
            origin = sys.path[0] + '/Artwork/' + image_ori_paths[0]
            new_classified_path = imgFolder + image_filename
            if os.path.isfile(origin):
                shutil.move(origin, new_classified_path)
                item['image_paths'] = new_classified_path

        old_thumb_folder = settings['IMAGES_STORE'] + '/thumbs/thumbs/'
        new_thumb_folder = settings['THUMB_PIC_STORE'] + image_filename[0:2] + '/' + image_filename[2:4] + '/' + image_filename[4:6] + '/'
        old_thumb_path = old_thumb_folder + image_filename
        new_thumb_path = new_thumb_folder + image_filename

        if not os.path.isdir(new_thumb_path):
            os.makedirs(new_thumb_path)
        if not old_thumb_path:
            raise DropItem("Item contains no images")
        else:
            if os.path.isfile(old_thumb_path):
                shutil.move(old_thumb_path, new_thumb_path)
                item['image_thumbs_paths'] = new_thumb_path
        return item




# Deprecated ImagePipeline
class ImageDownloadPipeline(ImagesPipeline):
    # change filename at file_path. failed.
    def get_media_requests(self, item, info):
        itemtag = item["tags"][0].split()[0]
        for img_url in item['image_urls']:
            yield scrapy.Request(img_url, meta={'itemtag': itemtag})

    def file_path(self, request, response=None, info=None):
        url = request.url
        image_guid = hashlib.sha1(url).hexdigest()  # change to request.url after deprecation
        return 'full/' + request.meta['itemtag'] + '/%s.jpg' % (image_guid)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        # item['image_paths'] = image_paths
        return item


class ImageDownloadPipelineSlow(object):
    # deprecated,save pics
    def process_item(self, item, spider):
        # if 'image_urls' in item:  # 如何‘图片地址’在项目中
        imgPath = "./Artwork/full/" + item["top_tag"].split()[0] + '/'# 下载图片的保存路径
        if not os.path.isdir(imgPath):
            os.makedirs(imgPath)
        for url in item["image_urls"]:
            print("下载:", url)
            hash_filename = hashlib.sha1(url.encode()).hexdigest()
            filename = os.path.join(imgPath, str(hash_filename) + '.jpg')
            urllib.request.urlretrieve(url, filename)
        return item

