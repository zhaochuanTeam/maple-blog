#!/usr/bin/env python
# -*- coding: utf-8 -*-
# **************************************************************************
# Copyright © 2017 jianglin
# File Name: utils.py
# Author: jianglin
# Email: xiyang0807@gmail.com
# Created: 2017-03-17 13:50:42 (CST)
# Last Update:星期日 2017-8-27 22:54:28 (CST)
#          By:
# Description:
# **************************************************************************
from flask import current_app
from datetime import datetime, timedelta


def gen_order_by(query_dict=dict(), keys=[], date_key=True):
    keys.append('id')
    if date_key:
        keys += ['created_at', 'updated_at']
    order_by = ['id']
    descent = query_dict.pop('descent', None)
    if descent is not None:
        descent = descent.split(',')
        descent = list(set(keys) & set(descent))
        order_by = ['-%s' % i for i in descent]
    return tuple(order_by)


def gen_filter_date(query_dict=dict(),
                    date_key='created_at',
                    date_format='%Y-%m-%d'):
    '''raise 时间格式错误'''
    filter_dict = {}
    start_date = query_dict.pop('start_date', None)
    end_date = query_dict.pop('end_date', None)
    if start_date is not None:
        start_date = datetime.strptime(start_date, date_format)
        key = '%s__gte' % date_key
        filter_dict.update(**{key: start_date})
    if end_date is not None:
        end_date = datetime.strptime(end_date, date_format)
        key = '%s__lte' % date_key
        filter_dict.update(**{key: end_date + timedelta(days=1)})
    if (start_date and end_date) and (start_date > end_date):
        raise ValueError
    return filter_dict


def gen_filter_dict(query_dict=dict(), keys=[], equal_key=[], user=None):
    filter_dict = {}
    keys = list(set(keys) & set(query_dict.keys()))
    for k in keys:
        if k in equal_key:
            filter_dict.update(**{k: query_dict[k]})
        else:
            new_k = '%s__contains' % k
            filter_dict.update(**{new_k: query_dict[k]})
    if user is not None and user.is_authenticated:
        filter_dict.update(author__id=user.id)
    return filter_dict
