#!/usr/bin/env python
# coding: utf-8

# In[1]:
import csv

#// Module-General - Gestion de Structures
# 01 def takeSecond(elem): return elem[1]  => take second element for sort
# 02 def build_dict (word_list): return dict_words_occurrences => Builddictionnary [word:number of occureences] from a chain
# 03 def pairlist_to_dict(list): return dict => Take double entry list and transform it in a dictionnary
# 04 def dict_to_pairlist(dict): return list => Take dictionnary and transform it in a pair entry key list
# 05 def split_csvrow_into_dict(row): return row_dict  => Splits a CSV row semicolon ';' separated into a dictionary
# 06 def short_list_elements(list,n): return shorted_list => Select N first elements of a sorted list
# 07 def get_words(dict,lang,count): return words => Retrieve key words in dictionnary
# 08 def list_average(list): return avg => Calculate average of values in a list
#//


# 01 => take second element for sort
def takeSecond(elem):
    return elem[1] 

# 02 => Builddictionnary [word:number of occureences] from a chain
def build_dict (word_list):
    dict_words_occurrences = {}
    for current_word in word_list:
        if current_word not in dict_words_occurrences: 
            dict_words_occurrences [current_word]=1 # nouvelle entrée
        else:
            dict_words_occurrences[current_word]+=1 # le mot existe déjà on augmente son compteur d'occurrences
    return dict_words_occurrences


# 03 => Take double entry list and transform it in a dictionnary 
def pairlist_to_dict(list):
    #print(f"\n### pairlist_to_dictionnary ### received as input the following list \n {list}")    
    dict = {}
    for indx in range(len(list)):
        key = list[indx][0]
        value = list[indx][1]
        dict[key] = value
    #print(f"\n### pairlist_to_dictionnary ### delivered the following dictionnary \n {dict}")     
    return dict


# 04 => Take dictionnary and transform it in a pair entry key list
def dict_to_pairlist(dict):
    #print(f"\n### dict_to_pairlist ### received as input the following dict \n {dict}") 
    list =[]
    for key, value in dict.items():
        [list.append([key,value])]
    #print(f"\n### dict_to_pairlist ###delivered the following list \n {list}") 
    return list


# 05 => Splits a CSV row semicolon ';' separated into a dictionary
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
        key_list = keys.split(';')
        value_list = values.split(';')
        print(f"\n===split_csvrow_into_dict=> The key List is: {key_list} with {len(key_list)} items")
        print(f"\n===split_csvrow_into_dict=> The value List: {value_list} with \n {len(key_list)} items")
        for index in range(len(key_list)):
            row_dict[key_list[index]] = value_list[index]
    
    return row_dict

# 06 => Select N first elements of a sorted list
def short_list_elements(list,n):
    shorted_list = []
    for indx in range(n):
        shorted_list.append(list[indx])
    return shorted_list

# 07 => Retrieve key words in dictionnary
def get_words(dict,lang,count):
    #print(f"\n>>> Get Words input variable dict looks like this{dict}" )
    dict_entry = dict[lang]
    #print(f"&&& Selected dictionnary entry looks like this \n {dict_entry}")
    list =[]
    for keys, values in dict_entry.items():
        list.append(keys)
    #print(f"\n### The extracted list is {list}")
    words =[]
    for index in range(count):
        words.append(list[index])
    # print(f"\n=== List from dictionnary looks like this {list}")
    return words

# 08 => Calculate average of values in a list
def list_average(list):
    avg = sum(list)/len(list)
    return avg





print(f"\n===FixInc Module=> <Gestion de Structures Python 20230619-vop1>")


# In[ ]:




