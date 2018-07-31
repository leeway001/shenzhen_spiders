# -*- coding: utf-8 -*-

import scrapy
from newsSpider.items import NewsspiderItem
from newsSpider.utils.commonUtils import *
from scrapy.exceptions import CloseSpider
import json
import re


class shenzhennews_societySpider(scrapy.Spider):
    #深圳新闻网
    numCount = 0
    name = 'shenzhennews_societySpider'

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
               'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
               'Connection': 'keep-alive',
               'upgrade-insecure-requests:': '1',
               'accept-encoding': 'gzip, deflate, br'
               }

    def start_requests(self):
        gn = ['http://news.sznews.com/node_18029_%d.htm' % d for d in range(2,101)]
        gn.append('http://news.sznews.com/node_18029.htm')

        gj = ['http://news.sznews.com/node_150128_%d.htm' % d for d in range(2,101)]
        gj.append('http://news.sznews.com/node_150128.htm')

        gat = ['http://news.sznews.com/node_134907_%d.htm' % d for d in range(2,101)]
        gat.append('http://news.sznews.com/node_134907.htm')

        shehui = ['http://news.sznews.com/node_18236_%d.htm' % d for d in range(2,51)]
        shehui.append('http://news.sznews.com/node_18236.htm')

        global gund
        gund = ['http://news.sznews.com/node_150127_%d.htm' % d for d in range(2,51)]
        gund.append('http://news.sznews.com/node_150127.htm')

        pl = ['http://news.sznews.com/node_150186_%d.htm' % d for d in range(2,51)]
        pl.append('http://news.sznews.com/node_150186.htm')

        caijing = ['http://news.sznews.com/node_31220_%d.htm' % d for d in range(2,51)]
        caijing.append('http://news.sznews.com/node_31220.htm')

        shiz = ['http://news.sznews.com/node_31182_%d.htm' % d for d in range(2,51)]
        shiz.append('http://news.sznews.com/node_31182.htm')

        global falv
        pfdt = ['http://www.sznews.com/zhuanti/node_231328_%d.htm' % d for d in range(2,11)]
        pfdt.append('http://www.sznews.com/zhuanti/node_231328.htm')

        rdzz = ['http://www.sznews.com/zhuanti/node_231327_%d.htm' % d for d in range(2,7)]
        rdzz.append('http://www.sznews.com/zhuanti/node_231327.htm')

        global edu
        jyrd = ['http://www.sznews.com/education/node_204671_%d.htm' % d for d in range(2,51)]
        jyrd.append('http://www.sznews.com/education/node_204671.htm')

        jybg = ['http://www.sznews.com/education/node_204670_%d.htm' % d for d in range(2,5)]
        jybg.append('http://www.sznews.com/education/node_204670.htm')

        school = ['http://www.sznews.com/education/node_204658_%d.htm' % d for d in range(2,31)]
        school.append('http://www.sznews.com/education/node_204658.htm')

        teacher = ['http://www.sznews.com/education/node_204657_%d.htm' % d for d in range(2,6)]
        teacher.append('http://www.sznews.com/education/node_204657.htm')

        global culture
        wyhs = ['http://www.sznews.com/culture/node_192827_%d.htm' % d for d in range(2,13)]
        wyhs.append('http://www.sznews.com/culture/node_192827.htm')

        zlyc = ['http://www.sznews.com/culture/node_192828_%d.htm' % d for d in range(2,25)]
        zlyc.append('http://www.sznews.com/culture/node_192828.htm')

        ttxw = ['http://www.sznews.com/culture/node_12059_%d.htm' % d for d in range(2,51)]
        ttxw.append('http://www.sznews.com/culture/node_12059.htm')

        wywx = ['http://www.sznews.com/culture/node_192831_%d.htm' % d for d in range(2,27)]
        wywx.append('http://www.sznews.com/culture/node_192831.htm')

        ysxj = ['http://www.sznews.com/culture/node_192830_%d.htm' % d for d in range(2,17)]
        ysxj.append('http://www.sznews.com/culture/node_192830.htm')

        rwtd = ['http://www.sznews.com/culture/node_192826_%d.htm' % d for d in range(2,23)]
        rwtd.append('http://www.sznews.com/culture/node_192826.htm')

        global tech
        czsz = ['http://www.sznews.com/tech/node_10336_%d.htm' % d for d in range(2,13)]
        czsz.append('http://www.sznews.com/tech/node_10336.htm')

        jsxw = ['http://www.sznews.com/tech/node_18064_%d.htm' % d for d in range(2,51)]
        jsxw.append('http://www.sznews.com/tech/node_18064.htm')

        kjjz = ['http://www.sznews.com/tech/node_10337_%d.htm' % d for d in range(2,30)]
        kjjz.append('http://www.sznews.com/tech/node_10337.htm')

        mrtj = ['http://www.sznews.com/tech/node_31952_%d.htm' % d for d in range(2,51)]
        mrtj.append('http://www.sznews.com/tech/node_31952.htm')

        tech = mrtj + kjjz + jsxw + czsz
        culture = rwtd + ysxj + wywx + ttxw + zlyc + wyhs
        edu = jybg + jyrd + school + teacher
        falv = rdzz + pfdt 
        start_urls = pl + caijing + shiz + gund + gn + gj + gat + shehui + falv + edu + culture + tech
        for url in start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        # 从middleware接收重复数量，终止爬虫时有延迟。
        if self.numCount > ExistNum.ENUM:
            print '8' * 100
            raise CloseSpider('Finished scrape latest news!!' + self.name)

        if response.url in gund:
            urls = response.xpath('//div[@class="c"]/div//ul/li/a/@href').extract()
            for url in urls:
                if 'http' not in url:
                    url = "http://news.sznews.com/" + url
                    yield scrapy.Request(url, callback=self.gund_content, headers=self.headers)
                else:
                    yield scrapy.Request(url, callback=self.gund_content, headers=self.headers)
        elif response.url in falv:
            urls = response.xpath('//div[@class="c"]/div//ul/li/a/@href').extract()
            for url in urls:
                if 'http' not in url:
                    url = "http://www.sznews.com/zhuanti/" + url
                    yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)
        elif response.url in edu:
            urls = response.xpath('//div[@class="c"]/div//ul/li/a/@href').extract()
            for url in urls:
                if 'http' not in url:
                    url = "http://www.sznews.com/education/" + url
                    yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)
        elif response.url in culture:
            urls = response.xpath('//div[@class="c"]/div//ul/li/a/@href').extract()
            for url in urls:
                if 'http' not in url:
                    url = "http://www.sznews.com/culture/" + url
                    yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)

        elif response.url in tech:
            urls = response.xpath('//div[@class="c"]/div//ul/li/a/@href').extract()
            for url in urls:
                if 'http' not in url:
                    url = "http://www.sznews.com/tech/" + url
                    yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)



        else:
            urls = response.xpath('//div[@class="c"]/div//ul/li/a/@href').extract()
            for url in urls:
                if 'http' not in url:
                    url = "http://news.sznews.com/" + url
                    yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)
                else:
                    yield scrapy.Request(url, callback=self.parse_content, headers=self.headers)



    def parse_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="share yahei cf"]/div[2]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@class="article-content cf new_txt"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''
           
            item_tags = ''
            item_source = u'甘肃经济网'
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

    def gund_content(self, response):
        try:
            item = NewsspiderItem()
            item_type = 'society'
            item_url = response.url
            item_crawl_time = GetCrawlTime.CrawlTime
            item_title = ' '.join(response.xpath('//h1/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_time = ''.join(response.xpath('//div[@class="bigPhoto-source cf"]/div[2]/text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_content = '\n'.join(response.xpath('//div[@id="con_arc_content"]//p//text()').extract()).strip().replace(u'\xa0', u' ')
           
            item_img = ''
           
            item_author = ''
           
            item_tags = ''
            item_source = u'甘肃经济网'
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

