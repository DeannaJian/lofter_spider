# -*- coding: utf-8 -*-
import time
import os
import sys
import re
from scrapy.crawler import CrawlerProcess
import scrapy


def modify_spider(url):
    """
        Modify story.py by embedding the url of the first page to crawl.
        :param url: url of the first(oldest) article to crawl.
    """
    spider_path = "story.py"
    spider_file = open(spider_path, 'w', encoding='utf-8')

    with open('spider_template1.txt', 'r', encoding='utf-8') as ff:
        code_buffer = ff.read()
        spider_file.write(code_buffer)

    spider_file.write(url)

    with open('spider_template2.txt', 'r', encoding='utf-8') as ff:
        code_buffer = ff.read()
        spider_file.write(code_buffer)

    spider_file.close()


def output_txt_from_xml(input_file, output_file, silent=False):
    """
        Convert the crawled xml file into a txt file.
        :param input_file: file path of the xml file.
        :param output_file: file path of the output txt file.
    """
    import xml.etree.ElementTree as ET

    tree = ET.parse(input_file)
    root = tree.getroot()

    item_num = len(root.findall('item')) + 1

    with open(output_file, 'w', encoding='utf-8') as ff:
        for ii in range(1, item_num):
            if not silent:
                print('Converting Paragraph %d...' % ii)
            element = root.find('.//item[%d]/title' % ii)
            title = ('%d. ' % ii) + element.text
            ff.write(title + '\n')
            element = root.find('.//item[%d]/date' % ii)
            date = element.text
            ff.write(date + '\n\n')
            paragraph_list = root.findall(
                './/item[%d]/paragraph/value' % ii)
            for paragraph in paragraph_list:
                para_content = paragraph.text
                if para_content is not None:
                    ff.write(para_content + "\n")
            if (ii % 50) == 0:
                ff.flush()
            ff.write("\n")


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


def grab_and_output(url, author):
    """
        Grab posts of an author starting from the page specified by the url
            until the latest post is obtained. Then output to a text file.
        :param url: the oldest lofter post to grab.
        :param author: the author's Lofter name.
    """
    # modify_spider(url)
    # from story import StorySpider

    StorySpider = type('StorySpider', (scrapy.Spider,),
                       dict(name='story',
                            allowed_domains=['lofter.com'],
                            start_urls=[url],
                            parse=parse))

    tt = time.localtime()
    temp_filename = "temp_output%s.xml" % time.strftime("%m%d", tt)
    output_filename = "%s_%s.txt" % (author, time.strftime("%m%d", tt))

    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'xml',
        'FEED_URI': temp_filename,
        'LOG_ENABLED': 'false'
    })

    process.crawl(StorySpider)
    process.start()

    output_txt_from_xml(temp_filename, output_filename, True)
    print('\nDone.\n')
    print('Save to: %s\n' % output_filename)

    os.remove(temp_filename)


if (__name__ == "__main__"):
    if len(sys.argv) != 2:
        print('''
Usage:
    python get_lofter_stories.py \
https://XXX.lofter.com/post/XXXXXXXXXXXX

    This spider crawls Lofter posts listed in a users's archive page.
    Specify the oldest post you wish to crawl. Then it downloads all
    of the posts till the latest one is obtained. The downloaded posts
    will be saved in a txt file (XXX.txt).
        ''')
        os._exit(-1)

    url = sys.argv[1]

    matchObj = re.match(r'http(.*)://(.*).lofter.com(.*?)', url)
    if not matchObj:
        os._exit(-1)

    author = matchObj.group(2)

    grab_and_output(url, author)
