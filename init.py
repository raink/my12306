#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sqlite3


def init():
    """第一次运行"""
    with sqlite3.connect('12306.sqlite') as conn:
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE `TRAIN` (`train_no`,`station_train_code`,`train_type`,`running_date`,'
                       'CONSTRAINT pk PRIMARY KEY (train_no,station_train_code,train_type,running_date))')
        conn.commit()


init()
