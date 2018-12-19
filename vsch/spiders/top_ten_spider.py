# -*- coding: utf-8 -*-

import scrapy
import datetime
import json
from ..items import TradeOverviewItem, TradeTopTenItem


# from scrapy.contrib.spidermiddleware.httperror import HttpError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

class TopTenSpider(scrapy.Spider):
    name = "top_ten_spider"

    def start_requests(self):
        matching_url = "https://sc.hkex.com.hk/TuniS/www.hkex.com.hk/chi/csm/DailyStat/data_tab_daily_{}c.js"
        urls = []
        
        today = datetime.datetime.now()
        today_in_week_num = today.strftime('%w')
        if(today_in_week_num == 5 or today_in_week_num == 6):
            return
        
        year = today.year
        day = today.day
        month = today.month
        if month < 10:
            month = "0" + str(month)
        if day < 10:
            day = "0" + str(day)
        urls.append(matching_url.format(str(year)+str(month)+str(day)))

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)


    def parse(self, response):
        try:
            jsonstr = response.text.split("=")[1]
            data = json.loads(jsonstr)
            sse_northbond = data[0]
            sse_northbond_overview_item = self.parseTradeOverviewItem(sse_northbond, "sse", "north")
            yield sse_northbond_overview_item
            sse_northbond_top_ten_items = self.parseTradeTopTenItem(sse_northbond, "sse", "north")
            for i in range(int(len(sse_northbond_top_ten_items))):
                yield sse_northbond_top_ten_items[i]


            sse_southbond = data[1]
            sse_southbond_overview_item = self.parseTradeOverviewItem(sse_southbond, "sse", "south")
            yield sse_southbond_overview_item
            sse_southbond_top_ten_items = self.parseTradeTopTenItem(sse_southbond, "sse", "south")
            for i in range(len(sse_southbond_top_ten_items)):
                yield sse_southbond_top_ten_items[i]

            szse_northbond = data[2]
            szse_northbond_overview_item = self.parseTradeOverviewItem(szse_northbond, "szse", "north")
            yield szse_northbond_overview_item
            szse_northbond_top_ten_items = self.parseTradeTopTenItem(szse_northbond, "szse", "north")
            for i in range(len(szse_northbond_top_ten_items)):
                yield szse_northbond_top_ten_items[i]

            szse_southbond = data[3]
            szse_southbond_overview_item = self.parseTradeOverviewItem(szse_southbond, "szse", "south")
            yield szse_southbond_overview_item
            szse_southbond_top_ten_items = self.parseTradeTopTenItem(szse_southbond, "szse", "south")
            for i in range(len(szse_southbond_top_ten_items)):
                yield szse_southbond_top_ten_items[i]

        except Exception as e:
            self.log(e)
            pass
        
    def parseTradeOverviewItem(self, need_parse_data, market, direction):
        trade_overview_tr = need_parse_data["content"][0]["table"]["tr"]
        item = TradeOverviewItem()
        item['market'] = market
        item['direction'] = direction
        item['trading_date'] = need_parse_data["date"]
        item['total_turnover'] = trade_overview_tr[0]["td"][0][0]
        item['buy_turnover'] = trade_overview_tr[1]["td"][0][0]
        item['sell_turnover'] = trade_overview_tr[2]["td"][0][0]
        item['total_trade_count'] = trade_overview_tr[3]["td"][0][0]
        item['buy_trade_count'] = trade_overview_tr[4]["td"][0][0]
        item['sell_trade_count'] = trade_overview_tr[5]["td"][0][0]
        if need_parse_data["market"] == "SSE Northbound" or need_parse_data["market"] == "SZSE Northbound":
            item['dqb'] = trade_overview_tr[6]["td"][0][0]
            item['dqb_ratio'] = trade_overview_tr[7]["td"][0][0]
        else:
            item['dqb'] = None
            item['dqb_ratio'] = None

        return item

    def parseTradeTopTenItem(self, need_parse_data, market, direction):
        trade_top_ten_tr = need_parse_data["content"][1]["table"]["tr"]
        items = []
        for i in range(10):
            item = TradeTopTenItem()
            item['market'] = market
            item['direction'] = direction
            item['trading_date'] = need_parse_data["date"]
            item['rank'] = trade_top_ten_tr[i]["td"][0][0]
            item['stock_code'] = trade_top_ten_tr[i]["td"][0][1]
            item['stock_name'] = trade_top_ten_tr[i]["td"][0][2]
            item['buy_turnover'] = trade_top_ten_tr[i]["td"][0][3]
            item['sell_turnover'] = trade_top_ten_tr[i]["td"][0][4]
            item['total_turnover'] = trade_top_ten_tr[i]["td"][0][5]
            items.append(item)
        
        return items


    def errback_httpbin(self, failure):
        # log all errback failures,
        # in case you want to do something special for some errors,
        # you may need the failure's type
        self.logger.error(repr(failure))

        # if isinstance(failure.value, HttpError):
        if failure.check(HttpError):
            # you can get the response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        # elif isinstance(failure.value, DNSLookupError):
        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        # elif isinstance(failure.value, TimeoutError):
        elif failure.check(TimeoutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)