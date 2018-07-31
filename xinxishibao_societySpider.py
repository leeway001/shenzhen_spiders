# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class xinxishibao_societySpider(scrapy.Spider):
    #信息时报
    numCount = 0
    name = 'xinxishibao_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        news = ['http://www.xxsb.com/findMenu/news/%d.html' % d for d in range(1,1921)]

        szms = ['http://www.xxsb.com/findMenu/edu/%d.html' % d for d in range(1,34)]

        sport = ['http://www.xxsb.com/findMenu/marriage/%d.html' % d for d in range(1,7)]

        goodperson = ['http://www.xxsb.com/findMenu/goodperson/%d.html' % d for d in range(1,13)]

        finance = ['http://www.xxsb.com/findMenu/feelread/%d.html' % d for d in range(1,20)]

        health = ['http://www.xxsb.com/findMenu/guoyin/%d.html' % d for d in range(1,21)]
 
        start_urls = health + news + szms + sport + goodperson + finance
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//a[@onclick="clickcount(812)"]/@href').extract()
        print(urls)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="hd"]/div/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="main_Article"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = '[]'
           
            item_author = ''
           
            item_tags = ''
            item_source = u'信息时报'
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


