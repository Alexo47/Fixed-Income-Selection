#!/usr/bin/env python
# coding: utf-8

"""
# ## Module-General - Managing Python structures 20231102-v2
def take_second(elem): elem[1]  => take second element for sort
def build_dict (word_list): dict_words_occurrences => Build dictionary [word:number of occurrences]
def pairlist_to_dict(entry_list): dictionary => double entry entry_list transformed in a dictionary
def dict_to_pairlist(dictionary): entry_list => Dictionary transformed in pair entry key entry_list
def split_csvrow_into_dict(row): row_dict  => Splits a CSV row ';' separated into a dictionary
def short_list_elements(entry_list,n): shorted_list => Select N first elements of sorted entry_list
def get_words(dictionary,lang,count): words => Retrieve keywords in dictionary
def list_average(entry_list): avg => Calculate average of values in an entry_list
"""
from modgen_timestamp import date_stamp


def take_second(elem):
    """
    => take second element for sort
    :param elem:
    :return: elem[1]
    """
    return elem[1]


def build_dict(word_list):
    """
    => Build Dictionary [word:number of occurrences] from a chain
    :param word_list:
    :return: dict_words_occurrences
    """
    dict_words_occurrences = {}
    for current_word in word_list:
        if current_word not in dict_words_occurrences:
            dict_words_occurrences[current_word] = 1  # new entry
        else:
            dict_words_occurrences[current_word] += 1  # the word exists already
    return dict_words_occurrences


def pairlist_to_dict(entry_list):
    """
    => Take double entry entry_list and transform it in a dictionary
    :param entry_list:
    :return:
    """
    # print(f"\n===pairlist_to_dictionary=> Received as input entry_list \n {entry_list}")
    dictionary = {}
    for key, value in entry_list:
        dictionary[key] = value
    # print(f"\===pairlist_to_dictionary=> delivered the following dictionary \n {dictionary}")
    return dictionary


def dict_to_pairlist(dictionary):
    """
    => Take dictionary and transform it in a pair of [entry key, entry_list]
    :param dictionary:
    :return:
    """
    # print(f"\n===dict_to_pairlist=> Received as input the following dictionary \n {dictionary}")
    output_list = []
    for key, value in dictionary.items():
        output_list.append([key, value])
    # print(f"\n===dict_to_pairlist=> Delivered the following entry_list \n {entry_list}")
    return output_list


def split_csvrow_into_dict(row):
    """
    Splits a CSV row into a dictionary with each item separated by a semicolon.

    Args:
    row: A CSV row as a string.

    Returns:
    A dictionary containing the CSV row items.
    """
    row_dict = {}
    for keys, values in row.items():
        # print(f"===split_csvrow_into_dict=> current key = <{key}> with corresponding <{value}>")
        key_list = keys.split(";")
        value_list = values.split(";")
        print(
            f"\n===split_csvrow_into_dict=> Key List is: {key_list} with {len(key_list)} items"
        )
        print(
            f"\n===split_csvrow_into_dict=> Value List: {value_list} -> \n {len(key_list)} items"
        )
        for index in enumerate(key_list):
            row_dict[key_list[index]] = value_list[index]
    return row_dict


def short_list_elements(entry_list, n):
    """
    => Select N first elements of a sorted entry_list
    :param entry_list:
    :param n:
    :return: shorted_list
    """
    shorted_list = []
    for index in range(n):
        shorted_list.append(entry_list[index])
    return shorted_list


def get_words(dictionary, lang, count):
    """
    => Retrieve keywords in dictionary
    :param dictionary:
    :param lang:
    :param count:
    :return: words
    """
    # print(f"\n===get_words=> input variable dictionary looks like this {dictionary}" )
    dict_entry = dictionary[lang]
    # print(f"===get_words=> Selected dictionary entry looks like this \n {dict_entry}")
    aux_list = []
    for keys in dict_entry.items():
        aux_list.append(keys)
    # print(f"\n### The extracted entry_list is {entry_list}")
    words = []
    for index in range(count):
        words.append(aux_list[index])
    # print(f"\n===get_words=> List from dictionary looks like this {entry_list}")
    return words


def list_average(entry_list):
    """
    => Calculate average of values in an entry_list
    :param entry_list:
    :return: avg
    """
    avg = sum(entry_list) / len(entry_list)
    return avg


print(f"\n===FixInc Module=> <Gestion de Structures Python 20231102-v2> {date_stamp()}")
