# -*- coding: utf-8 -*-
import scrapy


class StorySpider(scrapy.Spider):
    name = 'story'
    allowed_domains = ['lofter.com']
    start_urls = ['http://sauceshasi.lofter.com/post/1d0873d6_1c83546f3']

    def parse(self, response):
        date = response.css('div.info a::text').extract_first()
        title = response.css('div.text h2 a::text').extract_first()
        paragraph = response.css('.text').xpath('//div/p/text()').extract()
        yield {
            'date': date,
            'title': title,
            'paragraph': paragraph
        }

        next_pages = response.xpath('//*[@id="__prev_permalink__"]/@href')

        if next_pages:
            yield scrapy.Request(next_pages.extract_first(),
                                 callback=self.parse)