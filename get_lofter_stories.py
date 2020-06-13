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

    title_patents = ('title', 'title2')
    paragraph_patents = ('paragraph', 'paragraph2', 'paragraph3')

    with open(output_file, 'w', encoding='utf-8') as ff:
        for ii in range(1, item_num):
            if not silent:
                print('Converting Paragraph %d...' % ii)

            ff.write('%d. \n' % ii)

            for jj in range(0, len(title_patents)):
                pattent = './/item[%d]/%s' % (ii, title_patents[jj])
                title = root.find(pattent).text
                if title != 'None':
                    ff.write('  ' + title + '\n')

            element = root.find('.//item[%d]/date' % ii)
            date = element.text
            if date != 'None':
                ff.write('  ' + date + '\n\n')

            month = root.find('.//item[%d]/month' % ii).text
            day = root.find('.//item[%d]/day' % ii).text
            if ((month != 'None') & (day != 'None')):
                ff.write('  %s-%s\n\n' % (month, day))

            for jj in range(0, len(paragraph_patents)):
                paragraph_list = root.findall(
                    './/item[%d]/%s/value' % (ii, paragraph_patents[jj]))
                for paragraph in paragraph_list:
                    para_content = paragraph.text
                    if para_content is not None:
                        ff.write('  ' + para_content + '\n')

            if (ii % 50) == 0:
                ff.flush()
            ff.write("\n")


def parse(self, response):
    date = response.css('div.info div.label a::text').extract_first()
    day = response.css('div.day a::text').extract_first()
    month = response.css('div.month a::text').extract_first()
    title = response.css('div.text h2 a::text').extract_first()
    title2 = response.css('.ttl').xpath('//h2/a/text()').extract_first()
    paragraph = response.css('.content').css('.text').xpath(
        '//div/p/text()').extract()
    paragraph2 = response.css('.txtc').xpath('//p/text()').extract()
    paragraph3 = response.css('.cont').css('.text').xpath(
        '//div/p/text()').extract()

    yield {
        'date': date,
        'month': month,
        'day': day,
        'title': title,
        'title2': title2,
        'paragraph': paragraph,
        'paragraph2': paragraph2,
        'paragraph3': paragraph3
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
    if len(sys.argv) != 3:
        print('''
Usage:
    python get_lofter_stories.py \
https://XXX.lofter.com/post/XXXXXXXXXXXX f:\\temp

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

    output_filename = grab_and_output(url, author, sys.argv[2])
    print('\nDone.\n')
    print('Save to: %s\n' % output_filename)
