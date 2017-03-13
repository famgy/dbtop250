
drop database if exists pythondb;

create database pythondb character set utf8;

use pythondb;

grant select, insert, update, delete on pythondb.* to 'gpf'@'localhost' identified by 'abcd';

create table dbtop250 (
    `id` VARCHAR(100) not null primary key,
    `rank` VARCHAR(50) not null,
    `ranting` VARCHAR(50),
    `name` VARCHAR(50) not null,
    `alias` VARCHAR(50),
    `quote_tag` VARCHAR(500),
    `url` VARCHAR(500)
) engine=innodb default charset=utf8;

