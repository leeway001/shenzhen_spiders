# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class dahuawang_societySpider(scrapy.Spider):
    #大华网
    numCount = 0
    name = 'dahuawang_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        shantou = ['http://news.dahuawang.com/shantou/index_%d.html' % d for d in range(2,21)]
        shantou.append('http://news.dahuawang.com/shantou/index.html')
        yuedong = ['http://news.dahuawang.com/yuedong/index_%d.html' % d for d in range(2,8)]
        yuedong.append('http://news.dahuawang.com/yuedong/')
        shiping = ['http://news.dahuawang.com/shiping/index_%d.html' % d for d in range(2,6)]
        shiping.append('http://news.dahuawang.com/shiping/')
        china = ['http://news.dahuawang.com/tianxia/guonei_%d.html' % d for d in range(2,21)]
        china.append('http://news.dahuawang.com/tianxia/guonei.html')
        world = ['http://news.dahuawang.com/tianxia/guoji_%d.html' % d for d in range(2,20)]
        world.append('http://news.dahuawang.com/tianxia/guoji.html')
        finance = ['http://news.dahuawang.com/caijing/index_%d.html' % d for d in range(2,9)]
        finance.append('http://news.dahuawang.com/caijing/')
        sport = ['http://news.dahuawang.com/tianxia/tiyu_%d.html' % d for d in range(2,11)]
        sport.append('http://news.dahuawang.com/tianxia/tiyu.html')
        society = ['http://news.dahuawang.com/tianxia/shehui_%d.html' % d for d in range(2,8)]
        society.append('http://news.dahuawang.com/tianxia/shehui.html')
        distraction = ['http://news.dahuawang.com/tianxia/wenyu_%d.html' % d for d in range(2,4)]
        distraction.append('http://news.dahuawang.com/tianxia/wenyu.html')
        science  = ['http://news.dahuawang.com/tianxia/keji_%d.html' % d for d in range(2,6)]
        science.append('http://news.dahuawang.com/tianxia/keji.html')
        shanx = ['http://news.dahuawang.com/shanxing/index_%d.html' % d for d in range(2,4)]
        shanx.append('http://news.dahuawang.com/shanxing/')
        start_urls = shanx
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//div[@id="colList"]/ul/li/a/@href').extract()
        for url in urls:
            if 'http' in url:
                yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h4/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//span[@class="artPdate"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="artContent"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''
           
            item_tags = ''
            item_source = u'大华网'
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


