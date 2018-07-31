# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class guangdongxinkuaiwang_societySpider(scrapy.Spider):
    #广东新快网
    numCount = 0
    name = 'guangdongxinkuaiwang_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        gz = ['http://news.xkb.com.cn/guangzhou/list_3_%d.html' % d for d in range(1,11)]
        gd = ['http://news.xkb.com.cn/guangdong/list_4_%d.html' % d for d in range(1,11)]
        zg = ['http://news.xkb.com.cn/zhongguo/list_5_%d.html' % d for d in range(1,11)]
        gj = ['http://news.xkb.com.cn/guoji/list_6_%d.html' % d for d in range(1,11)]
        pl = ['http://news.xkb.com.cn/pinglun/list_72_%d.html' % d for d in range(1,11)]
        cj = ['http://news.xkb.com.cn/caijing/list_9_%d.html' % d for d in range(1,11)]
        cp = ['http://news.xkb.com.cn/caipiao/list_10_%d.html' % d for d in range(1,11)]
        fc = ['http://news.xkb.com.cn/fangchan/list_15_%d.html' % d for d in range(1,11)]
        sport = ['http://news.xkb.com.cn/tiyu/list_7_%d.html' % d for d in range(1,11)]
        yule = ['http://news.xkb.com.cn/yule/list_8_%d.html' % d for d in range(1,11)]
        gy = ['http://news.xkb.com.cn/gongyi/list_269_%d.html' % d for d in range(1,11)]
        health = ['http://news.xkb.com.cn/jiankang/list_11_%d.html' % d for d in range(1,11)]
        car = ['http://news.xkb.com.cn/qiche/list_16_%d.html' % d for d in range(1,11)]
        travel = ['http://news.xkb.com.cn/lvyou/list_13_%d.html' % d for d in range(1,11)]
        shuma = ['http://news.xkb.com.cn/shuma/list_14_%d.html' % d for d in range(1,11)]
        fashion = ['http://news.xkb.com.cn/shishang/list_17_%d.html' % d for d in range(1,11)]
        culture = ['http://news.xkb.com.cn/wenhua/list_391_%d.html' % d for d in range(1,11)]
        edu = ['http://news.xkb.com.cn/jiaoyu/list_18_%d.html' % d for d in range(1,11)]
        start_urls = edu + gz + gd + zg + gj + pl + cj + cp + fc + sport + yule + gy + health + car + travel + shuma + fashion + culture 
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//div[@id="mainC"]/ul//li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="newsTitle fl"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="content fl"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''
           
            item_tags = ''
            item_source = u'广东新快网'
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


