# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class dayangwang_societySpider(scrapy.Spider):
    #大洋网
    numCount = 0
    name = 'dayangwang_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        hotnews = ['http://news.dayoo.com/guangzhou/150955_%d.shtml' % d for d in range(2,6)]
        hotnews.append('http://news.dayoo.com/guangzhou/150955.shtml')

        gztoday = ['http://news.dayoo.com/guangzhou/150956_%d.shtml' % d for d in range(2,6)]
        gztoday.append('http://news.dayoo.com/guangzhou/150956.shtml')
        
        jingp = ['http://news.dayoo.com/guangzhou/150951_%d.shtml' % d for d in range(2,6)]
        jingp.append('http://news.dayoo.com/guangzhou/150951.shtml')

        yuanc = ['http://news.dayoo.com/guangzhou/151247_%d.shtml' % d for d in range(2,6)]
        yuanc.append('http://news.dayoo.com/guangzhou/151247.shtml')

        yule = ['http://news.dayoo.com/guangzhou/150953_%d.shtml' % d for d in range(2,6)]
        yule.append('http://news.dayoo.com/guangzhou/150953.shtml')

        sport = ['http://news.dayoo.com/guangzhou/150954_%d.shtml' % d for d in range(2,6)]
        sport.append('http://news.dayoo.com/guangzhou/150954.shtml')

        zw = ['http://news.dayoo.com/guangzhou/151867_%d.shtml' % d for d in range(2,6)]
        zw.append('http://news.dayoo.com/guangzhou/151867.shtml')

        reping = ['http://news.dayoo.com/reping/154230_%d.shtml' % d for d in range(2,6)]
        reping.append('http://news.dayoo.com/reping/154230.shtml')

        rptt = ['http://news.dayoo.com/reping/154229_%d.shtml' % d for d in range(2,6)]
        rptt.append('http://news.dayoo.com/reping/154229.shtml')

        rdpl = ['http://news.dayoo.com/reping/154231_%d.shtml' % d for d in range(2,6)]
        rdpl.append('http://news.dayoo.com/reping/154231.shtml')

        zxgd = ['http://news.dayoo.com/reping/154232_%d.shtml' % d for d in range(2,6)]
        zxgd.append('http://news.dayoo.com/reping/154232.shtml')

        urls1 = hotnews + gztoday + jingp + yuanc + yule + sport + zw + reping + rptt + rdpl + zxgd

        gd = ['http://news.dayoo.com/guangdong/139996_%d.shtml' % d for d in range(2,6)]
        gd.append('http://news.dayoo.com/guangdong/139996.shtml')

        world = ['http://news.dayoo.com/guangzhou/150959_%d.shtml' % d for d in range(2,6)]
        world.append('http://news.dayoo.com/guangzhou/150959.shtml')

        caijing = ['http://news.dayoo.com/guangzhou/150960_%d.shtml' % d for d in range(2,6)]
        caijing.append('http://news.dayoo.com/guangzhou/150960.shtml')

        sport = ['http://news.dayoo.com/guangzhou/150954_%d.shtml' % d for d in range(2,6)]
        sport.append('http://news.dayoo.com/guangzhou/150954.shtml')

        zjtt = ['http://news.dayoo.com/zhongzhi/154588_%d.shtml' % d for d in range(2,6)]
        zjtt.append('http://news.dayoo.com/zhongzhi/154588.shtml')

        zjdt = ['http://news.dayoo.com/zhongzhi/154589_%d.shtml' % d for d in range(2,6)]
        zjdt.append('http://news.dayoo.com/zhongzhi/154589.shtml')

        carfocus = ['http://life.dayoo.com/auto/154617_%d.shtml' % d for d in range(2,6)]
        carfocus.append('http://life.dayoo.com/auto/154617.shtml')

        carfnews = ['http://life.dayoo.com/auto/154618_%d.shtml' % d for d in range(2,6)]
        carfnews.append('http://life.dayoo.com/auto/154618.shtml')

        carnews = ['http://life.dayoo.com/auto/154622_%d.shtml' % d for d in range(2,6)]
        carnews.append('http://life.dayoo.com/auto/154622.shtml')

        eat = ['http://life.dayoo.com/meal/154541_%d.shtml' % d for d in range(2,6)]
        eat.append('http://life.dayoo.com/meal/154541.shtml')

        eatnews = ['http://life.dayoo.com/meal/154545_%d.shtml' % d for d in range(2,6)]
        eatnews.append('http://life.dayoo.com/meal/154545.shtml')

        urls2 = gd + world + caijing + caijing + zjtt + zjdt + carfocus + carfnews + carnews + eat + eatnews

        travel = ['http://life.dayoo.com/travel/154532_%d.shtml' % d for d in range(2,6)]
        travel.append('http://life.dayoo.com/travel/154532.shtml')

        money = ['http://life.dayoo.com/money/154563_%d.shtml' % d for d in range(2,6)]
        money.append('http://life.dayoo.com/money/154563.shtml')

        jrtt = ['http://life.dayoo.com/money/154561_%d.shtml' % d for d in range(2,6)]
        jrtt.append('http://life.dayoo.com/money/154561.shtml')

        jryw = ['http://life.dayoo.com/money/154563_%d.shtml' % d for d in range(2,6)] 
        jryw.append('http://life.dayoo.com/money/154563.shtml')

        xfms = ['http://life.dayoo.com/money/154565_%d.shtml' % d for d in range(2,6)]
        xfms.append('http://life.dayoo.com/money/154565.shtml')

        health = ['http://life.dayoo.com/health/154597_%d.shtml' % d for d in range(2,6)]
        health.append('http://life.dayoo.com/health/154597.shtml')

        jdt = ['http://life.dayoo.com/money/154562_2.shtml']
        jdt.append('http://life.dayoo.com/money/154562.shtml')

        urls3 = travel + jrtt + money + jryw + xfms + health + jdt
        start_urls = urls1 + urls2 + urls3
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//div[@class="dy-list"]//h2/a/@href').extract()
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
           
            item_content = '\n'.join(response.xpath('//div[@id="text_content"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = response.xpath('//div[@id="text_content"]//img/@src').extract()
           
            item_author = ''
           
            item_tags = ''
            item_source = u'大洋网'
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


