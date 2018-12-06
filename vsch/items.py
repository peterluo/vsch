# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HKCapitalInMainlandItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    stock_name = scrapy.Field()
    trading_date = scrapy.Field()
    shareholding = scrapy.Field()
    shareholding_percent = scrapy.Field()


class MainlandCapitalInHKItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    stock_code = scrapy.Field()
    stock_name = scrapy.Field()
    trading_date = scrapy.Field()
    shareholding = scrapy.Field()
    shareholding_percent = scrapy.Field()

