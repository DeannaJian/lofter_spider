# -*- coding: utf-8 -*-
import time
import os
import sys
import re
from scrapy.crawler import CrawlerProcess
import scrapy


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


def grab_and_output(url, author, output_folder):
    """
        Grab posts of an author starting from the page specified by the url
            until the latest post is obtained. Then output to a text file.
        :param url: the oldest lofter post to grab.
        :param author: the author's Lofter name.
        :param output_folder: the folder for saving the output txt file.
        :returns: full path of the output file
    """
    import random

    if not os.path.exists(output_folder):
        return ''

    StorySpider = type('StorySpider', (scrapy.Spider,),
                       dict(name='story',
                            allowed_domains=['lofter.com'],
                            start_urls=[url],
                            parse=parse))

    tt = time.localtime()
    temp_filename = "temp_output%s.xml" % time.strftime("%m%d", tt)
    while os.path.exists(temp_filename):
        temp_filename = ("temp_output%s(%d).xml" %
                         (time.strftime("%m%d", tt), random.randint(0, 9)))

    ii = 1
    output_filename = output_folder + \
        '\\%s_%s.txt' % (author, time.strftime('%m%d', tt))
    while os.path.exists(output_filename):
        output_filename = output_folder + '\\%s_%s(%d).txt' \
            % (author, time.strftime('%m%d', tt), ii)
        ii += 1

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'xml',
        'FEED_URI': temp_filename,
        'LOG_ENABLED': 'false'
    })

    process.crawl(StorySpider)
    process.start()

    output_txt_from_xml(temp_filename, output_filename, True)

    os.remove(temp_filename)
    return output_filename


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

    matchObj = re.match(r'http(s*)://(.*).lofter.com(.*?)', url)
    if not matchObj:
        os._exit(-1)

    author = matchObj.group(2)

    output_filename = grab_and_output(url, author)
    print('\nDone.\n')
    print('Save to: %s\n' % output_filename)
