# -*- coding: utf-8 -*-
import scrapy
from nhaccuatui.items import NhaccuatuiItem


class QuotesSpider(scrapy.Spider):

    name = "lyric"

    allowed_domains = ['nhaccuatui.com']

    start_urls = [
        # 'https://www.nhaccuatui.com/bai-hat/tru-tinh-moi.html', T
        # 'https://www.nhaccuatui.com/bai-hat/nhac-tre-moi.html', T
        # 'https://www.nhaccuatui.com/bai-hat/tien-chien-moi.html', T
        # 'https://www.nhaccuatui.com/bai-hat/nhac-trinh-moi.html', T
        # 'https://www.nhaccuatui.com/bai-hat/cach-mang-moi.html', T
        # 'https://www.nhaccuatui.com/bai-hat/rock-viet-moi.html', T 
        # 'https://www.nhaccuatui.com/bai-hat/rap-viet-moi.html', T
        # 'https://www.nhaccuatui.com/bai-hat/pop-moi.html', T 
        # 'https://www.nhaccuatui.com/bai-hat/rock-moi.html', T  
        # 'https://www.nhaccuatui.com/bai-hat/thieu-nhi-moi.html', T
        'https://www.nhaccuatui.com/bai-hat/remix-viet-moi.html'
        ]

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    
    def parse(self, response):
        finalPage = response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="box_pageview"]/a/@href')[-1].extract()
        totalPage = int(finalPage.split(".")[-2])
        for page in range(totalPage):
            link = finalPage.replace(str(totalPage), str(page + 1))
            # print(link)
            yield scrapy.Request(link, callback=self.crawlLyric)

    def crawlLyric(self, response):
        for linkLyric in response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="list_music_full"]/div[@class="fram_select"]/div[@class="list_music listGenre"]/div[@class="fram_select"]/ul[@class="listGenre"]/li/div[@class="box-content-music-list"]/div[@class="info_song"]/a[@class="avatar_song"]/@href').getall():
            yield scrapy.Request(linkLyric, callback=self.saveFile)

    def saveFile(self, response):
        lyricRaw = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/p[@id="divLyric"]/text()'
            ).getall()
        
        lyric = "\n".join(lyricRaw)

        name = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@id="box_playing_id"]/div[@class="info_name_songmv"]/div[@class="name_title"]/h1[@itemprop="name"]/text()'
            ).getall()
        
        singerRaw = response.xpath(
            '//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@id="box_playing_id"]/div[@class="info_name_songmv"]/div[@class="name_title"]/h2[@class="name-singer"]/a[@class="name_singer"]/text()'
            ).getall() 

        singer = ",".join(singerRaw)

        tagRaw = response.xpath(
            '//*[contains(concat( " ", @class, " " ), concat( " ", "detail_info_playing_now", " " ))]//a/text()'
            )[-1].getall()

        tag = ".".join(tagRaw)
        
        item = NhaccuatuiItem()
        item['name']   = name[0].encode("utf-8")
        item['lyric']  = lyric.encode("utf-8")
        item['link']   = response.url.encode("utf-8")
        item['tag']   = tag.encode("utf-8")
        item['singer'] = singer.encode("utf-8")
        yield(item)
