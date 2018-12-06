# Do what ？
This is a spider for fetch HKEX stock data.

# How ？ 
- use [scrapy](https://doc.scrapy.org/en/latest/intro/tutorial.html) component;
- use [scrapyd](https://scrapyd.readthedocs.io/en/stable/overview.html) as a server;
- use [scrapyd-client](https://github.com/scrapy/scrapyd-client) deploy to server.

# Run

```
 $ pip install scrapy
```
```
 $ pip install scrapyd
```
```
 $ pip install scrapyd-client
```
```
 $ pip install pymysql
``` 
In project root path, execute the following command:
```
 $ scrapyd
```
```
 $ scrapyd-deploy server -p vsch
```
```
 $ curl http://localhost:6800/schedule.json -d project=vsch -d spider=hk_capital_spider
```

