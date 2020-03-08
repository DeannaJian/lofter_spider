# -*- coding: utf-8 -*-
import scrapy


class StorySpider(scrapy.Spider):
    name = 'story'
    allowed_domains = ['lofter.com']
    start_urls = ['https://leeenciel.lofter.com/post/3abd38_1c738d6f0']

    def parse(self, response):
        date = response.css('div.info div.label a::text').extract_first()
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
