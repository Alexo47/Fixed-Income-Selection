#!/usr/bin/env python
# coding: utf-8

"""
=> Module-FixIncome - Global Definitions 20231029-v2
FILES_DIR: points to the main oroject directory
Token variables : EOR_TOKEN, EOF_TOKEN, BROKER_TOKEN, ERROR_TOKEN
NEW_LINE: new one_line

"""

# ## Import Basic Modules + TimeStamp

from modgen_timestamp import date_stamp


FILES_DIR = 'D:/FinKB$/#FixedIncome/FixInc-DB'

EOR_TOKEN = '#EOR#'
EOF_TOKEN = '#EOF#'
BROKER_TOKEN = '#+#'
UNDEFINED_TOKEN = '#X#'
ERROR_TOKEN = '#ERROR#'
NEW_LINE = '\n'

DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

print(f"\n===FixInc Module=> <Global Definitions 20231029-v2 exec@: {date_stamp()}")
