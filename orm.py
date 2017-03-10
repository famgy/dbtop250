#!/usr/bin/python3
# -*- coding:utf-8 -*-

import logging
import aiomysql
import mysql.connector

#logging.basicConfig(level = logging.INFO)

def log_sql(sql, arg = ()):
    logging.info('SQL: %s (arg: %s)' % (sql, arg))


def create_pool(**kw):
    logging.info('create database connection pool...')
    global __pool
    __pool = mysql.connector.create_pool(
        host = kw.get('host', 'localhost'),
        port = kw.get('port', 3306),
        user = kw['gpf'],
        password = kw['abcd'],
        db = kw['pythondb'],
        charset = kw.get('charset', 'utf8'),
        autocommit = kw.get('autocommit', True),
        maxsize = kw.get('maxsize', 10),
        minsize = kw.get('minsize', 1),
    )


async def close_pool():
    logging.info('close database connection pool...')
    global __pool
    __pool.close()
    await __pool.wait_closed()


async def select(sql, args, size=None):
    log_sql(sql, args)
    global __pool
    async with __pool.get() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(sql.replace('?', '%s'), args or ())
            if size:
                rs = await cur.fetchmany(size)
            else:
                rs = await cur.fetchall()
            logging.info('rows returned: %s' % len(rs))
            return rs


async def execute(sql, args, autocommit = True):
    log_sql(sql, args)
    async with __pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            async with conn.cursor(aiomysql.DictCursor) as cur:
                await cur.execute(sql.replace('?', '%s'), args)
                rows = cur.rowcount
            if not autocommit:
                await conn.commit()
        except BaseException:
            if not autocommit:
                await conn.rollback()
            raise
        return rows


class Field(object):

    def __init__(self, name, col_type, primary_key, default):
        self.name = name
        self.col_type = col_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s: %s>' % (self.__class__.__name__, self.col_type, self.name)


class StringField(Field):

    def __init__(self, name = None, primary_key = False, default = None, col_type = 'varchar(100)'):
        super().__init__(name, col_type, primary_key, default)


class IntField(Field):

    def __init__(self, name=None, primary_key=False, default=0, col_type='int'):
        super().__init__(name, col_type, primary_key, default)


class Model(dict, metaclass = ModelMetaclass):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, Key):
        value = getattr(self, Key, None)
        if value is None:
            field = self.__mappings__[key]
            value = field.default() if callable(field.default) else field.default
            logging.debug('Using default value for %s: %s' % (key, str(value)))
            setattr(self, key, value)
        return value

    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('Failed to insert record: affected rows:%s' % rows)









