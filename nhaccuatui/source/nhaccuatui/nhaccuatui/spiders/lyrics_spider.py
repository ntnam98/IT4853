# -*- coding: utf-8 -*-
import scrapy
from nhaccuatui.items import NhaccuatuiItem

class QuotesSpider(scrapy.Spider):
    name = "lyric"
    # https://www.nhaccuatui.com/bai-hat/tru-tinh-moi.html 1003
    # https://www.nhaccuatui.com/bai-hat/nhac-tre-moi.html  944
    # https://www.nhaccuatui.com/bai-hat/tien-chien-moi.html 996
    # https://www.nhaccuatui.com/bai-hat/nhac-trinh-moi.html 999
    # https://www.nhaccuatui.com/bai-hat/cach-mang-moi.html 1000
    start_urls = [
        'https://www.nhaccuatui.com/bai-hat/tien-chien-moi.1.html'
    ]

    def parse(self, response):
        finalPage = response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="box_pageview"]/a/@href')[-1].extract()
        totalPage = int(finalPage.split(".")[-2])
        for page in range(totalPage):
            link = finalPage.replace(str(totalPage), str(page + 1))
            # print(link)
            yield scrapy.Request(link, callback=self.crawlLyric)

    def crawlLyric(self, response):
        for linkLyric in response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@class="list_music_full"]/div[@class="fram_select"]/div[@class="list_music listGenre"]/div[@class="fram_select"]/ul[@class="listGenre"]/li/div[@class="box-content-music-list"]/div[@class="info_song"]/a[@class="avatar_song"]/@href').extract():
            yield scrapy.Request(linkLyric, callback=self.saveFile)

    def saveFile(self, response):
      lyricRaw = response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/p[@id="divLyric"]/text()').extract()
      lyric = " ".join(lyricRaw)
      name = response.xpath('//div[@class="box-content"]/div[@class="wrap"]/div[@class="content-wrap"]/div[@class="box-left"]/div[@id="box_playing_id"]/div[@class="info_name_songmv"]/div[@class="name_title"]/h1[@itemprop="name"]/text()').extract()
      item = NhaccuatuiItem()
      item['name'] = name[0].encode("utf-8")
      item['lyric'] = lyric.encode("utf-8")
      item['link'] = response.url.encode("utf-8")
      yield(item)