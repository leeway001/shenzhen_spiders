# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class meizhou_societySpider(scrapy.Spider):
    #梅州网
    numCount = 0
    name = 'meizhou_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        mzdt = ['http://www.meizhou.cn/meizhou/meizhounews/mzdongtai/%d.shtml' % d for d in range(1,41)]
        shbt = ['http://www.meizhou.cn/meizhou/sociology/societywideangle/%d.shtml' % d for d in range(1,41)]
        mzqy = ['http://www.meizhou.cn/meizhou/meizhounews/mzqy/%d.shtml' % d for d in range(1,41)]
        gdxw = ['http://www.meizhou.cn/meizhou/guangdongxw/%d.shtml' % d for d in range(1,41)]
        guonei = ['http://www.meizhou.cn/meizhou/gnxw/%d.shtml' % d for d in range(1,41)]
        guoji = ['http://www.meizhou.cn/meizhou/gjxw/%d.shtml' % d for d in range(1,41)]
        news = mzdt + shbt + mzqy + gdxw + guonei + guoji
        finances = ['http://www.meizhou.cn/meizhou/finance/finances/%d.shtml' % d for d in range(1,41)]
        football = ['http://www.meizhou.cn/meizhou/sports/football/%d.shtml' % d for d in range(1,27)]
        basketball = ['http://www.meizhou.cn/meizhou/sports/basketball/%d.shtml' % d for d in range(1,13)]
        mzsport = ['http://www.meizhou.cn/meizhou/sports/meizhousports/%d.shtml' % d for d in range(1,41)]
        sport = finances + football + basketball + mzsport
        gnfashion = ['http://www.meizhou.cn/meizhou/entertainment/domesticentertainme/%d.shtml' % d for d in range(1,41)]
        internation = ['http://www.meizhou.cn/meizhou/entertainment/internationalentert/%d.shtml' % d for d in range(1,4)]
        movies = ['http://www.meizhou.cn/meizhou/entertainment/movies/%d.shtml' % d for d in range(1,11)]
        mzyule = ['http://www.meizhou.cn/meizhou/entertainment/meizhouentertainmen/%d.shtml' % d for d in range(1,7)] 
        shiping = ['http://www.meizhou.cn/meizhou/sp/%d.shtml' % d for d in range(1,41)]
        fashion = gnfashion + internation + movies + mzyule + shiping
        cityleaders = ['http://www.meizhou.cn/meizhou/focusnews/cityleaders/%d.shtml' % d for d in range(1,41)]
        xfrx = ['http://www.meizhou.cn/meizhou/ms/xfrx/%d.shtml' % d for d in range(1,15)]
        bmdt = ['http://www.meizhou.cn/meizhou/meizhounews/bmdt/%d.shtml' % d for d in range(1,41)]
        msxw = ['http://www.meizhou.cn/meizhou/ms/msxw/%d.shtml' % d for d in range(1,41)]
        msgt = ['http://www.meizhou.cn/meizhou/ms/msgt/%d.shtml' % d for d in range(1,41)]
        msly = ['http://www.meizhou.cn/meizhou/ms/msly/%d.shtml' % d for d in range(1,41)]
        xwzz = ['http://www.meizhou.cn/meizhou/ms/xwzz/%d.shtml' % d for d in range(1,41)]
        society = ['http://www.meizhou.cn/meizhou/2017xsy/shehuidingbu/']
        fashion = cityleaders + xfrx + bmdt + msxw + msgt + msly + xwzz + society
        start_urls = news + sport + fashion + fashion
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//div[@class="hover"]/ul//li/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h2/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//span[@id="SP_RELEASE_TIME"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//span[@id="LB_MATTER"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''.join(response.xpath('//div[@id="editor"]/text()').extract()).strip()
           
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


