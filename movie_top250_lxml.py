#!/usr/bin/python3
#-*- coding: utf-8 -*-

import requests
import pdb
import logging
import time
import uuid
import sys

import mysql.connector

from lxml import etree

logging.basicConfig(level = logging.INFO)

header = {'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)

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

                movie_id = next_id()
                movie_rank = rank.encode("utf8")
                movie_ranting = rating_num.encode("utf8")
                movie_name = name.encode("utf8")
                movie_alias = alias_name.encode("utf8")
                movie_quote_tag = quote.encode("utf8")
                movie_url = url.encode("utf8")

                cur = cnx.cursor()

                add = ("INSERT INTO dbtop250 (id, rank, ranting, name, alias, quote_tag, url) VALUES (%s, %s, %s, %s, %s, %s, %s)")
                data = (movie_id, movie_rank, movie_ranting, movie_name, movie_alias, movie_quote_tag, movie_url)
                cur.execute(add, data)

                cnx.commit()
                cur.close()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            pass


config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "gpf",
    "password": "abcd",
    "db": "pythondb",
}

cnx = mysql.connector.connect(**config)

session = requests.Session()
for id in range(0, 251, 25):
    #pdb.set_trace()
    url = 'http://movie.douban.com/top250/?start=' + str(id)

    get_movie_info(url, session)

cnx.close()

