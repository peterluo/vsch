# -*- coding: utf-8 -*-

import scrapy
import datetime
from ..items import MainlandCapitalInHKItem


# from scrapy.contrib.spidermiddleware.httperror import HttpError
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError

class MainlandCapitalSpider(scrapy.Spider):
    name = "mainland_capital_spider"

    def start_requests(self):
        urls = [
            "http://sc.hkexnews.hk/TuniS/www.hkexnews.hk/sdw/search/mutualmarket_c.aspx?t=hk"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,
                                 errback=self.errback_httpbin,
                                 dont_filter=True)


    def parse(self, response):
        try:
            trading_date = response.css('div.form-input-text input::attr(value)').extract_first()
            trading_date = datetime.datetime.strptime(trading_date, "%Y/%m/%d").strftime('%Y-%m-%d')
            for stock in response.xpath('//table/tbody/tr'):
                try:
                    item = MainlandCapitalInHKItem()
                    item['stock_code'] = stock.css('td.col-stock-code .mobile-list-body::text').extract_first()
                    item['stock_name'] = stock.css('td.col-stock-name .mobile-list-body::text').extract_first()
                    item['shareholding'] = stock.css('td.col-shareholding .mobile-list-body::text').extract_first()
                    item['shareholding_percent'] = stock.css('td.col-shareholding-percent .mobile-list-body::text').extract_first()
                    item['trading_date'] = trading_date
                    yield item
                except Exception:
                    pass
        except Exception as e:
            self.log(e)
            pass
        

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