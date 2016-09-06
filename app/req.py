#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json

import datetime
import requests

from app import db


def get_train_info_value():
    url = 'https://kyfw.12306.cn/otn/resources/js/query/train_list.js'
    r = requests.get(url, verify=False)
    train_json = json.loads(r.text[16:])
    with db as conn:
        cursor = conn.cursor()
        for running_date, daily_train in train_json.items():
            for train_type, train_info_list in daily_train.items():
                for train_info in train_info_list:
                    cursor.execute(
                        'INSERT INTO `TRAIN` (`train_no`, `station_train_code`,`train_type`,`running_date`) VALUES (?,?,?,?)',
                        (train_info['train_no'], train_info['station_train_code'], train_type, running_date))
        cursor.close()
        conn.commit()


def get_train_list_in_day(from_station, to_station, queryDate=datetime.datetime.now(), purpose_codes='ADULT'):
    url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=%s&queryDate=%s&from_station=%s&to_station=%s'
    print(queryDate.today())
    params =(
        purpose_codes,
        queryDate.strftime('%Y-%m-%d'),
        from_station,
        to_station,
    )
    print(params)
    print(url% (purpose_codes,queryDate.strftime('%Y-%m-%d'),from_station,to_station))
    r = requests.get(url%params, verify=False)
    print(r,r.text)


get_train_list_in_day("AOH", "ZEK")
