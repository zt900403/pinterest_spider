# -*- coding: utf-8 -*-
import scrapy
from scrapy.shell import inspect_response

class PinterestSpiderSpider(scrapy.Spider):
    name = "pinterest_spider"
    allowed_domains = ["pinterest.com"]
    start_urls = ['https://www.pinterest.com/resource/UserSessionResource/create/']

    def parse(self, response):
        login_data = {"options": {
                    "username_or_email":"hoarzt02674@chacuo.net",
                    "password":"zhangtao43"
                    },
                    "context": {}
        }
        return scrapy.FormRequest.from_response(
            response,
            formdata={'source_url': '/login/?referrer=home_page', 'data':'{"options":{"username_or_email":"hoarzt02674@chacuo.net","password":"zhangtao43"},"context":{}}' },
            callback=self.after_login
        )
    def after_login(self, response):
        inspect_response(response)
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return
        
        print(response)