#!/usr/bin/env python
# coding: utf-8

"""
# ## modgen_chain_manipulation <20231104-v2>
def split_words(chain): word_list => Simple split chain to words
def items_comma_converter(one_line): local_list, len(local-list) => Line with ',' into a list
def items_separator_converter(one_line,separator): local_list, len(local-list) => Line Separation
# ##
"""
from modgen_timestamp import date_stamp


def split_words(chain):
    """
    #01 /# Simple split chain to words
    :param chain:
    :return: word_list
    """
    word_list = chain.split()
    return word_list


def items_comma_converter(one_line):
    """
    => Converts a one_line with commas into an entry_list
    :param one_line:
    :return:
    """
    local_list = []
    new_chain = ""
    for character in one_line:
        if character != ",":
            new_chain = new_chain + character
        else:
            new_chain = new_chain.strip()
            local_list.append(new_chain)
            new_chain = ""
    # we have now finished parsing the one_line, but we may have a last new_chain
    if len(new_chain) >= 1:
        new_chain = new_chain.strip()
        local_list.append(new_chain)

    return local_list, len(local_list)


def items_separator_converter(one_line, separator):
    """
    => Converts a one_line with separator char into an entry_list
    :param one_line:
    :param separator:
    :return: local_list, len(local_list)
    """
    local_list = []
    new_chain = ""
    for character in one_line:
        if character != separator:
            new_chain = new_chain + character
        else:
            new_chain = new_chain.strip()
            local_list.append(new_chain)
            new_chain = ""
    # we have now finished parsing the one_line, but we may have a last new_chain
    if len(new_chain) >= 1:
        new_chain = new_chain.strip()
        local_list.append(new_chain)

    return local_list, len(local_list)


print(f"\n===FixInc Module=> <chain_manipulation 20231104-v2> exec@: {date_stamp()}")
