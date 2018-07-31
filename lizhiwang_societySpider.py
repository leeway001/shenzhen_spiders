# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class lizhiwang_societySpider(scrapy.Spider):
    #荔枝网
    numCount = 0
    name = 'lizhiwang_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        politics = ['http://www.gdtv.cn/politics/index_%d.html' % d for d in range(2,21)]
        politics.append('http://www.gdtv.cn/politics/index.html')
        society = ['http://www.gdtv.cn/local/index_%d.html' % d for d in range(2,21)]
        society.append('http://www.gdtv.cn/local/')
        world = ['http://www.gdtv.cn/world/index_%d.html' % d for d in range(2,21)]
        world.append('http://www.gdtv.cn/world/')
        tech = ['http://www.gdtv.cn/tech/index_%d.html' % d for d in range(2,21)]
        tech.append('http://www.gdtv.cn/tech/')
        finance = ['http://www.gdtv.cn/finance/index_%d.html' % d for d in range(2,21)]
        finance.append('http://www.gdtv.cn/finance/')
        junshi = ['http://www.gdtv.cn/mil/index_%d.html' % d for d in range(2,21)]
        junshi.append('http://www.gdtv.cn/mil/')
        wy = ['http://www.gdtv.cn/ent/index_%d.html' % d for d in range(2,21)]
        wy.append('http://www.gdtv.cn/ent/')
        start_urls = wy + politics + society + world + tech + finance + junshi
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//div[@class="glist"]/ul/li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//span[@class="datetime"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="article-main"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = response.xpath('//div[@class="article-main"]//img/@src').extract()
           
            item_author = ''
           
            item_tags = ''
            item_source = u'梅州网'
            item_summary = item_content[:100]

            item_img = str(CommonParse.array_uft8_parse(item_img))
            item_time = item_time[:16]
            item_time = TimeParse.time_parse(item_time)

            item = item.getItem(url=item_url, title=item_title, tags=item_tags, source=item_source,
                                publish_date=item_time, content=item_content, author=item_author,
                                type=item_type, img=item_img, summary=item_summary,
                                crawl_time=item_crawl_time)
            item.parseStr(item)
            yield item
        except Exception as e:
            print '=' * 100
            print e, response.url
            with open('%s.txt' % self.name, 'a') as f:
                f.write('%s - %s\n' % (e, response.url))


