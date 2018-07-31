# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class aoyiwang_societySpider(scrapy.Spider):
    #奥一网
    numCount = 0
    name = 'aoyiwang_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        global baoliao
        baoliao = ['http://baoliao.oeeee.com/baoliao/getNewList?p=%d' % d for d in range(1,51)]
        global today
        today = ['http://news.oeeee.com/api/channel.php?m=Js4channelNews&a=latest&cid=387&page=%d&row=20' % d for d in range(1,21)]
        global finance
        finance = ['http://news.oeeee.com/api/channel.php?m=Js4channelNews&a=latest&cid=181&page=%d&row=20&callback=lastest' % d for d in range(1,21)]
        global tech
        tech = ['http://life.oeeee.com/3c/%d' % d for d in range(1,20)]
        global health
        health = ['http://health.oeeee.com/api/channel.php?s=index/index/channel/jkkx/pageNum/%d' % d for d in range(1,39)]
        global edu  
        edu = ['http://edu.oeeee.com/api/channel.php?s=index/index/channel/jyzx/pageNum/%d' % d for d in range(1,53)]
        global life
        life = ['http://life.oeeee.com/shopping/%d' % d for d in range(1,2)]
        start_urls = life + baoliao + today + tech + finance + health + edu
        for url in start_urls: 
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        if response.url in baoliao:
            html = re.findall(r'{.*}',response.body)
            text = json.loads(html[0])
            data = text['data']
            link_list = data['list']
            for link in link_list:
                url_id = link['id']
                url = "http://baoliao.oeeee.com/index/show/id/" + url_id
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

        elif response.url in today:
            html = re.findall(r'http://sz.oeeee.com/html/[0-9/]*.html',response.body)
            for url in html:
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)
        
        elif response.url in finance:
            html = re.findall(r'http://finance.oeeee.com/html/[0-9/]*.html',response.body)
            for url in html:
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

        elif response.url in tech:
            urls = response.xpath('//div[@class="article-li"]/h3/a/@href').extract()
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

        elif response.url in health:
            urls = response.xpath('//div[@class="list-box"]/ul//li/h3/a/@href').extract()
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)
        elif response.url in edu:
            urls = response.xpath('//div[@class="list-box"]/ul//li/h3/a/@href').extract()
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

        elif response.url in life:
            urls = response.xpath('//div[@class="article-list"]//h3/a/@href').extract()
            for url in urls:
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//span[@class="time"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="content"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = response.xpath('//div[@class="content"]//img/@src').extract()
           
            item_author = ''.join(response.xpath('//p[@class="username"]/text()').extract()).strip()
           
            item_tags = ''
            item_source = u'奥一网'
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


