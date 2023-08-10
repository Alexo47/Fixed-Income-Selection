#!/usr/bin/env python
# coding: utf-8

# In[1]:


#// Module_General_CharactersChainText_Manipulation_vop1
#01 def split_words(chain): return word_list #01 /# Simple split chain to words
#02 def items_comma_converter(line): return liste,len(liste) /# Converts a line with commas into a list
#03 def items_separator_converter(line,separator): return liste,len(liste) /# Converts a line with separator char into a list
#//

#01 /# Simple split chain to words
def split_words(chain):
    word_list = chain.split()
    return word_list

#02 /# Converts a line with commas into a list
def items_comma_converter(line):
    line_len = len(line)
    liste = []
    item = ''
    for indx in range(line_len):
        if line[indx] != ',':
            item = item + line[indx]  
        else:
            item = item.strip()
            liste.append(item)
            item = ''      
# we have now finished parsing the line but we may have a last item 
    if len(item) >= 1:
        item = item.strip()
        liste.append(item)

    return liste,len(liste)

#03 /# Converts a line with separator char into a list
def items_separator_converter(line,separator):
    line_len = len(line)
    liste = []
    item = ''
    for indx in range(line_len):
        if line[indx] != separator:
            item = item + line[indx]
        else:
            item = item.strip()
            liste.append(item)
            item = ''
# we have now finished parsing the line but we may have a last item 
    if len(item) >= 1:
        item = item.strip()
        liste.append(item)

    return liste,len(liste)


print(f"\n===FixInc Module=> <CharactersChainText_Manipulation 20230619-vop1>")


# In[ ]:




