# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor


class StorySpider(scrapy.Spider):
    name = 'story'
    allowed_domains = ['lofter.com']
    start_urls = ['http://jishibucuotuo.lofter.com/post/1f9af1a3_ef60c284']

    def parse(self, response):
        le = LinkExtractor(restrict_css='div.txtcont')
        for link in le.extract_links(response):
            yield scrapy.Request(link.url, callback=self.parse_chapter)

    def parse_chapter(self, response):
        part = response.css('div.txtcont')
        title = part.css('strong::text').extract_first()
        paragraph = part.xpath('p/text()').extract()
        index = response.css('h2 a::text').re_first(u'.*（(.*)）.*')
        yield {
            'paragraph': paragraph,
            'title': title,
            'index': index
        }
