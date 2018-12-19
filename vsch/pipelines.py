# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import datetime
import settings
from items import HKCapitalInMainlandItem,MainlandCapitalInHKItem,TradeOverviewItem,TradeTopTenItem

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
        self.trade_overview_sql_info = "INSERT IGNORE INTO `trade_overview`(market, direction, trading_date, total_turnover, buy_turnover, sell_turnover,total_trade_count, buy_trade_count, sell_trade_count, dqb, dqb_ratio, create_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.trade_top_ten_sql_info = "INSERT IGNORE INTO `trade_top_ten`(market, direction, trading_date, rank, stock_code, stock_name, total_turnover, buy_turnover, sell_turnover, create_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

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
        elif item.__class__ == TradeOverviewItem:
            try:
                dqb = None if item['dqb'] is None else float(item['dqb'].replace(",", ""))
                self.cursor.execute(
                    self.trade_overview_sql_info,
                    (item['market'],
                     item['direction'],
                     item['trading_date'],
                     float(item['total_turnover'].replace(",", "")),
                     float(item['buy_turnover'].replace(",", "")),
                     float(item['sell_turnover'].replace(",", "")),
                     float(item['total_trade_count'].replace(",", "")),
                     float(item['buy_trade_count'].replace(",", "")),
                     float(item['sell_trade_count'].replace(",", "")),
                     dqb,
                     item['dqb_ratio'],
                     datetime.datetime.now()))
                self.connect.commit()
            except Exception as error:
                print error
        elif item.__class__ == TradeTopTenItem:
            try:
                self.cursor.execute(
                    self.trade_top_ten_sql_info,
                    (item['market'],
                     item['direction'],
                     item['trading_date'],    
                     item['rank'],    
                     item['stock_code'],
                     item['stock_name'],
                     float(item['total_turnover'].replace(",", "")),
                     float(item['buy_turnover'].replace(",", "")),
                     float(item['sell_turnover'].replace(",", "")),
                     datetime.datetime.now()))
                self.connect.commit()
            except Exception as error:
                print error
        else:
            pass

        return item
