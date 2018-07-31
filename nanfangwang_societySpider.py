# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class nanfangwang_societySpider(scrapy.Spider):
    #南方网
    numCount = 0
    name = 'nanfangwang_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def struct_url(self,url,page):
        page_url = url[:-4] + "_%d.htm"
        urls = [page_url % d for d in range(2,page)]
        urls.append(url)
        return urls



    def start_requests(self):

        yaowen = self.struct_url('http://www.southcn.com/pc2016/yw/node_346416.htm',51)
        gd = self.struct_url('http://news.southcn.com/gd/default.htm',51)
        china = self.struct_url('http://news.southcn.com/china/default.htm',51)
        world = self.struct_url('http://news.southcn.com/international/default.htm',51)
        community = self.struct_url('http://news.southcn.com/community/default.htm',51)
        news = yaowen + gd + china + world + community
        #经济
        jjgz = self.struct_url('http://economy.southcn.com/e/node_321237.htm',51)
        jjtt = self.struct_url('http://economy.southcn.com/node_165839.htm',51)
        cgc = self.struct_url('http://economy.southcn.com/node_321240.htm',44)
        cgh = self.struct_url('http://economy.southcn.com/node_323572.htm',21)
        cfd = self.struct_url('http://economy.southcn.com/node_257516.htm',30)
        cfs = self.struct_url('http://economy.southcn.com/node_167471.htm',51)
        yc = self.struct_url('http://economy.southcn.com/node_196431.htm',51)
        gdjj = self.struct_url('http://economy.southcn.com/node_321243.htm',51)
        gdsc = self.struct_url('http://economy.southcn.com/node_374552.htm',6)
        zsj = self.struct_url('http://economy.southcn.com/node_321352.htm',39)
        smhz = self.struct_url('http://economy.southcn.com/node_321250.htm',18)
        qygc = self.struct_url('http://economy.southcn.com/node_321247.htm',51)
        jjhb = self.struct_url('http://economy.southcn.com/node_290152.htm',17)
        qydt = self.struct_url('http://economy.southcn.com/node_321248.htm',31)
        xhxx = self.struct_url('http://economy.southcn.com/node_321249.htm',8)
        money = jjgz + jjtt + cgc + cgh + cfd + cfs + yc + gdjj + gdsc + zsj + smhz + qygc + jjhb + qydt + xhxx
        chinajj = self.struct_url('http://economy.southcn.com/node_321252.htm',51)
        worldjj = self.struct_url('http://economy.southcn.com/node_321253.htm',51)
        cysc = self.struct_url('http://economy.southcn.com/node_165813.htm',51)
        hlw = self.struct_url('http://economy.southcn.com/node_321261.htm',51)
        syd = self.struct_url('http://economy.southcn.com/node_165838.htm',51)
        fmrw = self.struct_url('http://economy.southcn.com/node_321263.htm',11)
        hybd = self.struct_url('http://economy.southcn.com/node_321262.htm',8)
        jjfz = self.struct_url('http://economy.southcn.com/node_321255.htm',24)
        Macroscopic = chinajj + worldjj + cysc + hlw + syd + fmrw + hybd + jjfz
        #金融
        bond = self.struct_url('http://economy.southcn.com/node_321264.htm',51)
        Bank = self.struct_url('http://economy.southcn.com/node_321851.htm',51)
        Insurance =self.struct_url('http://economy.southcn.com/node_321265.htm',51)
        lc = self.struct_url('http://economy.southcn.com/node_321266.htm',51)
        ssgs = self.struct_url('http://economy.southcn.com/node_321267.htm',51)
        cmjj = self.struct_url('http://economy.southcn.com/node_321268.htm',40)
        lottery = self.struct_url('http://economy.southcn.com/node_165811.htm',27)
        finance = bond + Bank + Insurance + lc + ssgs + cmjj + lottery 
        nfkb = self.struct_url('http://kb.southcn.com/default.htm',51)
        wp = self.struct_url('http://news.southcn.com/g/node_74681.htm',14)
        start_urls = news + money + Macroscopic + finance + nfkb + wp
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        urls = response.xpath('//div[@class="pw"]/h3/a/@href').extract()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h2[@id="article_title"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//span[@id="pubtime_baidu"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@id="content"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = response.xpath('//div[@id="content"]//img/@src').extract()
           
            item_author = ''.join(response.xpath('//div[@class="m-editor"]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_tags = ''
            item_source = u'南方网'
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


