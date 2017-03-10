#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests
import pdb
import logging

import orm

from configloader import configs
from lxml import etree
from model import Movie, next_id

logging.basicConfig(level = logging.INFO)

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def get_movie_info(url, session):
    req = session.get(url, headers = header)

    req.encoding = 'utf8'
    html_src = etree.HTML(req.content)
    items = html_src.xpath('//ol/li/div[@class="item"]')

    for item in items:
        rank, name, alias, rating_num, quote, url = "", "", "", "", "", ""
        try:
            url = item.xpath('./div[@class="pic"]/a/@href')[0]
            rank = item.xpath('./div[@class="pic"]/em/text()')[0]
            title = item.xpath('./div[@class="info"]//a/span[@class="title"]/text()')
            name = title[0].encode('gb2312','ignore').decode('gb2312')
            alias = title[1].encode('gb2312','ignore').decode('gb2312') if len(title)==2 else ""
            alias_name = alias.encode('gb2312','ignore').decode('gb2312').replace('/','')

            rating_num = item.xpath('.//div[@class="bd"]//span[@class="rating_num"]/text()')[0]
            quote_tag = item.xpath('.//div[@class="bd"]//span[@class="inq"]')
            if len(quote_tag) is not 0:
                quote = quote_tag[0].text.encode('gb2312','ignore').decode('gb2312').replace('\xa0','')

                logging.info('%s %s 《%s》（%s） %s %s' % (rank, rating_num, name.encode('gb2312','ignore').decode('gb2312'), alias_name, quote, url))

                uid = next_id()
                movie = Movie(id = uid, rank = rank, ranting = ranting, name = name, alias = alias, quote_tag = quote_tag, url = url)
                movie.save()

        except:
            print('faild!')
            pass


orm.create_pool(**configs.database)

session = requests.Session()
for id in range(0, 251, 25):
    #pdb.set_trace()
    url = 'http://movie.douban.com/top250/?start=' + str(id)

    get_movie_info(url, session)



