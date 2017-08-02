# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsCustSpiderItem(scrapy.Item):
    url = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    reference_urls = scrapy.Field()
    reference_url_content = scrapy.Field()
    image_urls = scrapy.Field()
    image_path = scrapy.Field()







