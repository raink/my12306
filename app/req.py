#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import datetime
import re

import requests

from app import db
from app.util import name2three_code


def get_train_info_value():
    url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js'
    r = requests.get(url, verify=False)
    train_json = json.loads(r.text[16:])
    with db as conn:
        cursor = conn.cursor()
        for running_date, daily_train in train_json.items():
            for train_type, train_info_list in daily_train.items():
                for train_info in train_info_list:
                    train_code = re.findall('(.*)\(', train_info['station_train_code'])
                    for code in train_code:
                        for info in re.findall('\((.*)\)', train_info['station_train_code']):
                            station_list = info.split('-')
                            cursor.execute(
                                'REPLACE INTO '
                                '`TRAIN` (`train_no`, `station_train_code`,`train_type`,'
                                '`running_date`,`from_station`,`to_station`) '
                                'VALUES (?,?,?,?,?,?)',
                                (train_info['train_no'], code, train_type, running_date, station_list[0],
                                 station_list[1]))
    cursor.close()
    conn.commit()


def get_train_list_in_day(from_station, to_station, queryDate=datetime.datetime.now(), purpose_codes='ADULT'):
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query' \
          '?purpose_codes=%s' \
          '&queryDate=%s' \
          '&from_station=%s' \
          '&to_station=%s'
    params = (
        purpose_codes,
        queryDate.strftime('%Y-%m-%d'),
        from_station,
        to_station,
    )
    r = requests.get(url % params, verify=False)
    print(r, r.text)


def get_train_pass_from_train_no(train_no, from_station_telecode, to_station_telecode,
                                 depart_date=datetime.datetime.now()):
    """获取运行中时刻"""
    url = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo' \
          '?train_no=%s' \
          '&from_station_telecode=' \
          '%s&to_station_telecode=%s' \
          '&depart_date=%s'
    params = (train_no, from_station_telecode, to_station_telecode, depart_date.strftime('%Y-%m-%d'))
    r = requests.get(url % params, verify=False)
    from pprint import pprint
    pprint(json.loads(r.text))

# get_train_info_value()
# get_train_list_in_day("AOH", "ZEK")
# get_train_pass_from_train_no('11000C100302', name2three_code('天津'), name2three_code('北京南'))
