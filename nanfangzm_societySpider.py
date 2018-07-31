# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class nanfangzm_societySpider(scrapy.Spider):
    #南方周末
    numCount = 0
    name = 'nanfangzm_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def struct_url(self,url,page):
        urls = [url % d for d in range(0,page)]
        return urls

    def start_requests(self):
        shiz = self.struct_url('http://www.infzm.com/contents/11/%d',317)
        news = self.struct_url('http://www.infzm.com/contents/2554/%d',1737)
        society = self.struct_url('http://www.infzm.com/contents/12/%d',428)
        finance = self.struct_url('http://www.infzm.com/contents/6/%d',754)
        comment = self.struct_url('http://www.infzm.com/contents/8/%d',919)
        toutiao = self.struct_url('http://www.infzm.com/contents/2553/%d',621)
        green = self.struct_url('http://www.infzm.com/contents/1374/%d',250)
        cuture = self.struct_url('http://www.infzm.com/contents/7/%d',878)
        life = self.struct_url('http://www.infzm.com/contents/10/%d',271)
        zhengwen = self.struct_url('http://www.infzm.com/contents/3033/%d',8)
        start_urls = zhengwen + shiz + news + society + finance + comment + toutiao + green +cuture +life
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//div[@id="leftContain"]/article//h/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//em[@class="pubTime"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//section[@id="articleContent"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = response.xpath('//section[@id="articleContent"]//img/@src').extract()
           
            item_author = ''.join(response.xpath('//em[@id="content_author"]//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_tags = ''
            item_source = u'南方周末'
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


