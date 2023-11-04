#!/usr/bin/env python
# coding: utf-8

"""
Module General - TimeStamp marker for all modules/programs 220231030-v1

"""

from datetime import datetime

def date_stamp():
    """
    => Returns date_stamp for prints
    :return: date_time
    """
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

# print("===FixIncome Module=> <TimeStamp> 20231030-v1")