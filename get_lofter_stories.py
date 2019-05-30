# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import subprocess
import time
import os
import sys


def modify_spider(url):
    spider_path = "lofter/spiders/story.py"
    spider_file = open(spider_path, 'w', encoding='utf-8')

    with open('spider_template1.txt', 'r', encoding='utf-8') as ff:
        code_buffer = ff.read()
        spider_file.write(code_buffer)

    spider_file.write(url)

    with open('spider_template2.txt', 'r', encoding='utf-8') as ff:
        code_buffer = ff.read()
        spider_file.write(code_buffer)

    spider_file.close()


def book_title_from_content_xml(input_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    item = root.findall('item')[0]
    book_title = item.find('book_title').text
    return book_title


def output_txt_from_content_xml(input_file, output_file):
    tree = ET.parse(input_file)
    root = tree.getroot()

    item_num = 1
    order = {}

    for item in root.findall('item'):
        item_index = item.find('index').text
        if not item_index.isdigit():
            root.remove(item)
        else:
            order[item_index] = item_num
            item_num += 1

    with open(output_file, 'w', encoding='utf-8') as ff:
        for ii in range(1, item_num):
            ff.write("\n")
            element = root.find('.//item[%d]/title' % order[str(ii)])
            title = element.text
            ff.write(title + "\n\n")
            paragraph_list = root.findall(
                './/item[%d]/paragraph/value' % order[str(ii)])
            for paragraph in paragraph_list:
                para_content = paragraph.text
                if para_content is not None:
                    ff.write(para_content + "\n")
            ff.write("\n")


if (__name__ == "__main__"):

    if len(sys.argv) != 2:
        print('''usage:
    python get_lofter_stories.py 'http://jishibucuotuo.lofter.com/post/1f9af1a3_ef60c284'
        ''')
        os._exit()

    modify_spider(sys.argv[1])

    tt = time.localtime()
    temp_filename = "temp_output%s.xml" % time.strftime("%m%d", tt)
    output_filename = "output%s.txt" % time.strftime("%m%d", tt)

    if os.path.exists(temp_filename):
        os.remove(temp_filename)

    cmd = "scrapy crawl story -o %s --nolog" % temp_filename
    subprocess.call(cmd)

    output_txt_from_content_xml(temp_filename, output_filename)
    print('Done.\n')
    print(output_filename + '\n')

    os.remove(temp_filename)
