# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class jiangmenwang_societySpider(scrapy.Spider):
    #中国江门网
    numCount = 0
    name = 'jiangmenwang_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        jmnews = ['http://www.jmnews.com.cn/a/jmxw_%d.htm' % d for d in range(2,16)]
        jmnews.append('http://www.jmnews.com.cn/a/jmxw.htm')
        zhyw =['http://www.jmnews.com.cn/a/zhyw_%d.htm' % d for d in range(2,16)]
        zhyw.append('http://www.jmnews.com.cn/a/zhyw.htm')
        global finance
        finance = ['http://www.jmnews.com.cn/a/node_47481_%d.htm' % d for d in range(2,31)]
        finance.append('http://www.jmnews.com.cn/a/node_47481.htm')
        global cuture
        cuture = ['http://www.jmnews.com.cn/a/node_47271_%d.htm' % d for d in range(2,15)]
        cuture.append('http://www.jmnews.com.cn/a/node_47271.htm')
        global life
        life = ['http://www.jmnews.com.cn/a/shfw_%d.htm' % d for d in range(2,15)]
        life.append('http://www.jmnews.com.cn/a/shfw.htm')
        global meishi
        meishi = ['http://www.jmnews.com.cn/a/meishi_%d.htm' % d for d in range(2,16)]
        meishi.append('http://www.jmnews.com.cn/a/meishi.htm')
        start_urls = meishi + jmnews + zhyw + finance + cuture + life
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        if response.url in finance:
            urls = response.xpath('//div[@class="clis"]/ul//li/a/@href').extract()
            for url in urls:
                url = "http://www.jmnews.com.cn/a/" + url
                yield scrapy.Request(url, callback=self.finance_content, headers=self.headers)

        elif response.url in cuture:
            urls = response.xpath('//div[@class="list"]/ul//li/h2/a/@href').extract()
            for url in urls:
                url = "http://www.jmnews.com.cn/a/" + url
                yield scrapy.Request(url, callback=self.cuture_content, headers=self.headers)

        elif response.url in life:
            urls = response.xpath('//div[@class="web_listbox"]/ul//li/a/@href').extract()
            for url in urls:
                url = "http://www.jmnews.com.cn/a/" + url
                yield scrapy.Request(url, callback=self.life_content, headers=self.headers)

        elif response.url in meishi:
            urls = response.xpath('//div[@class="page-list"]/ul//li/a/@href').extract()
            for url in urls:
                url = "http://www.jmnews.com.cn/a/" + url
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)


        else:
            urls = response.xpath('//div[@class="web_listbox"]/ul//li/a/@href').extract()
            for url in urls:
                url = "http://www.jmnews.com.cn/a/" + url
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//div[@class="tit_bar"]/h1//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="tit_from"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="content"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''.join(response.xpath('//div[@class="bj"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_tags = ''
            item_source = u'中国江门网'
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


    def finance_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//div[@class="nr"]/h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="nr"]/p/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="zw"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''
           
            item_tags = ''
            item_source = u'中国江门网'
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


    def cuture_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="info"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="content"]//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''
           
            item_tags = ''
            item_source = u'中国江门网'
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

    def life_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="info"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="content"]//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''
           
            item_tags = ''
            item_source = u'中国江门网'
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
