# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime
import settings
from items import HKCapitalInMainlandItem,MainlandCapitalInHKItem

class VschPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            port=settings.MYSQL_PORT,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USER_NAME,
            passwd=settings.MYSQL_PASSWORD,
            charset=settings.MYSQL_CHARSET
            )
        self.cursor = self.connect.cursor()
        self.hk_capital_sql_info = "INSERT IGNORE INTO `hk_capital_in_mainland_stock`(stock_code, stock_name, trading_date, shareholding, shareholding_percent, create_time) VALUES(%s,%s,%s,%s,%s,%s)"
        self.mainland_capital_sql_info = "INSERT IGNORE INTO `mainland_capital_in_hk_stock`(stock_code, stock_name, trading_date, shareholding, shareholding_percent, create_time) VALUES(%s,%s,%s,%s,%s,%s)"

    def process_item(self, item, spider):
        if item.__class__ == HKCapitalInMainlandItem:
            try:
                self.cursor.execute(
                    self.hk_capital_sql_info,
                    (item['stock_code'],
                     item['stock_name'],
                     item['trading_date'],
                     float(item['shareholding'].replace(",", "")),
                     item['shareholding_percent'],
                     datetime.datetime.now()))
                self.connect.commit()
            except Exception as error:
                print error
        elif item.__class__ == MainlandCapitalInHKItem:
            try:
                self.cursor.execute(
                    self.mainland_capital_sql_info,
                    (item['stock_code'],
                     item['stock_name'],
                     item['trading_date'],
                     float(item['shareholding'].replace(",", "")),
                     item['shareholding_percent'],
                     datetime.datetime.now()))
                self.connect.commit()
            except Exception as error:
                print error
        else:
            pass

        return item
