#!/usr/bin/python3
# -*- coding:utf-8 -*-


import time
import uuid

from orm import Model, StringField, IntField


def next_id():
    return '%015d%s000' % (int(time.time() * 1000), uuid.uuid4().hex)


class Movie(Model):
    __table__ = 'movie'
    id = StringField(primary_key = True, default = next_id, col_type = 'varchar(50)')
    rank = IntField()
    ranting = StringField(col_type = 'varchar(50)')
    name = StringField(col_type = 'varchar(50)')
    alias = StringField(col_type = 'varchar(50)')
    quote_tag = StringField(col_type = 'varchar(500)')
    url = StringField(col_type = 'varchar(500)')
