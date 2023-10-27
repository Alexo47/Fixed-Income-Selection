#!/usr/bin/env python
# coding: utf-8

# In[1]:


# ## Module-General - Files Operations
# 01 def fpath(dir,filename): return path => Crée le path pour un directory de data avec la filename
# 02 def openFile_Reader(file): return okFlag,fi => Checks file existence - set reader utf8 newline '' delimiter ';'
# 03 def openFile_Writer(file): return okFlag,fo => Checks file existence - set writer utf8 newline '' delimiter ';'
# 04 def openFile_ReadWriter(file_path): return okFlag,fio,win,wout => Checks - set R/W utf8 newline '' delimiter ';'
# 05 def openCSV_Reader(file_path): return okFlag,fi,win => Checks file existence - set csv.reader utf-8 delimiter ';'
# 06 def openCSV_Writer(file_path) => Checks file existence - set csv.writer utf-8 delimiter ';' newline = ''
# 07 def read_file(path): return word_chain => lit fichier avec le traitement d'encoding utf8
# 08 def save_file_jason(index,path): return => sauvegarde fichier d'extension .json - gestion encoding utf-8
# 09 def open_file_jason(path): return index => ouvre et lit fichier extension .json avec encoding utf8
# 10 def restoreSet_jason(file_path): return okFlag,localSet => Check file exist - Restore Set stored in a Jason File
# 11 def createDict_json(newfile): return okFlag,fd => Creates an empty dictionary and save it to a jason file
# 12 def restoreDict_jason(file_path): return okFlag,jasonDict => Check file exist - Restore Dict stored in Jason File
# 13 def saveDict_json(file_path, dict_2_save): return flagOK => Save dictionary in JJson file
# 14 def readln(fr): return line => read new line
# 15 def initializeLogFile (file,hdr): return wout,fo => setup Log File to write including Header Line
# 16 def CSV_2_SCSV_Converter(file):return inFlag,outFlag => transform comma delimited file into a semicolon text file
# 17 def CSV_2_SCSV_CiaRecord_Converter(file): return inFlag,outFlag => Convert csv to ';' file About field preserved
# ##

import string
import os.path
import json
import csv

from Modules.ModGen_ManipulatingPythonStructures import pairlist_to_dict
from Modules.ModGen_CharactersChainText import items_separator_converter

# 01 => Crée le path pour un directory de data avec la filename
def fpath(dir,filename):
    path = dir  +'/' + filename
    return path

# 02 => Checks file existence - set reader utf8 newline '' delimiter ';'
def openFile_Reader(file):
    # file contains the full path of the file
    okFlag = 'True'
    checkfile = os.path.isfile(file)
    print(f"\n===openFile_Reader=> Does File: <{file}> Exists? => {checkfile}")
    if checkfile:
        print(f"\n===openFile_Reader=> checkfile states that <{file}> EXISTS <{checkfile}")
        fi = open(file,'r',encoding = "utf−8", newline = '')
    else:
        print(f"\n===openFile_Reader=> checkfile states that <{file}> DOES NOT EXIST: <{checkfile}")
        okFlag = 'False'
        fi = None
    return okFlag,fi


# 03 => Checks file existence - set writer utf8 newline '' delimiter ';'
def openFile_Writer(file):
    okFlag = 'True'
    fo = 'False'
    checkfile = os.path.isfile(file)
    print(f"\n===openFile_Writer=> Does File: <{file}> Exists? => {checkfile}")
    if checkfile:
        # print(f"\n===openFile_Writer=> checkfile states that <{file}> EXISTS <{checkfile}")
        fo = open(file,'a',encoding = "utf−8", newline = '')
    else:
        # print(f"\n===openFile_Writer=> checkfile states that <{file}> DOES NOT EXIST: <{checkfile} => open new file")
        fo = open(file,'a',encoding = "utf−8", newline = '')
        okFlag = 'False'
    return okFlag,fo

# 04 => Checks file existence - set R/W utf8 newline '' delimiter ';'
def openFile_ReaderWriter(file_path):
    inputFile = file_path + '.txt'
    okFlag = 'True'
    win = 'False'
    wout = 'False'
    fio = 'False'
    checkfile = os.path.isfile(inputFile)
    print(f"\n===openFile_ReaderWriter=> Does File: <{inputFile}> Exists? => {checkfile}")
    if checkfile:
        # print(f"\n===openFile_ReaderWriter=> checkfile states that <{inputFile}> EXISTS <{checkfile}")
        fio = open(inputFile,'r+',encoding = "utf−8", newline = '')
        win = csv.reader(fio, delimiter = ';')
        wout = csv.writer(fio, delimiter = ';')
    else:
        # print(f"\n===openFile_ReaderWriter=> checkfile states that <{inputFile}> DOES NOT EXIST: <{checkfile}")
        okFlag = 'False'
    return okFlag,fio,win,wout

# 05 => Checks file existence - set csv.reader utf-8 delimiter ';'
def openCSV_Reader(file_path):
    inputFile = file_path + '.csv'
    okFlag = 'True'
    win = 'False'
    fi = 'False'
    checkfile = os.path.isfile(inputFile)
    print(f"\n===openCSV_Reader=> Does File: <{inputFile}> Exists? => {checkfile}")
    if checkfile:
        # print(f"\n===openCSV_Reader=> checkfile states that <{inputFile}> EXISTS <{checkfile}")
        fi = open(inputFile,'r',encoding = "utf−8")
        win = csv.reader(fi, delimiter = ';')
    else:
        # print(f"\n===openLogFile_Reader=> checkfile states that <{inputFile}> DOES NOT EXIST: <{checkfile}")
        okFlag = 'False'
    return okFlag,fi,win

# 06 => Checks file existence - set csv.writer utf-8 delimiter ';' newline = ''
def openCSV_Writer(file_path):
    output_file = file_path + '.csv'
    okFlag = 'True'
    wout = 'False'
    fo = 'False'
    checkfile = os.path.isfile(output_file)
    print(f"\n===openCSV_Reader=> Does File: <{output_file}> Exists? => {checkfile}")
    if checkfile:
        # print(f"\n===openCSV_Reader=> checkfile states that <{inputFile}> EXISTS <{checkfile}")
        fo = open(output_file,'a',encoding = "utf−8", newline = '')
        wout = csv.writer(fo, delimiter = ';')
    else:
        # print(f"\n===openLogFile_Reader=> checkfile states that <{inputFile}> DOES NOT EXIST: <{checkfile}")
        okFlag = 'False'
        fo = open(output_file,'a',encoding = "utf−8", newline = '')
        wout = csv.writer(fo, delimiter = ';')

    return okFlag,fo,wout

# 07 Lit fichier avec le traitement d'encoding utf8
def read_file(path):
    with open(path, encoding = "utf−8") as f:
        word_chain = f.read()
    return word_chain






# 08 => Sauvegarde fichier d'extension .json - gestion encoding utf-8
def save_file_jason(index,path):
    filename = path + '.json'
    with open(filename,'w',encoding = 'utf8') as fp:
        json.dump(index,fp,ensure_ascii=False)
        fp.close()
        print(f"\n===save_file_jason=> Just dumped index to {filename}")
    return

# 09 => Ouvre et lit fichier extension .json avec encoding utf8
def open_file_jason(path):
    filename = path + '.json'
    index = {}
    with open(filename,'r', encoding = 'utf8') as fp:
        index = json.load(fp)
        fp.close()
        print(f"\n===open_file_jason=> Just loaded {filename} as returned index")
    return index

# 10 => Check file existence - Restore Set stored in a Jason File
def restoreSet_jason(file_path):
    localSet = {}
    okFlag = 'False'
    outFile = file_path + '.json'
    checkfile = os.path.isfile(outFile)
    print(f"\n===restoreAcronymSet_jason=> Does File: <{outFile}> Exists? => {checkfile}")
    if checkfile:
        # print(f"\n===restoreAcronymSet_jason=> jason file <{outFile}> EXISTS: <{checkfile}")
        localList = open_file_jason(file_path)
        localSet = {item for item in localList}
        okFlag = 'True'
    return okFlag,localSet

# 11 Creates an empty jason file open for write
def createDict_json(newfile):
    """
    If newfile does not exist Create a new file open for write -
    Returns
        > checkfile 'True' if newfile already exists
        > fd : the file pointer
        
    Args:
    newfile: The path to the JSON file to create.
    """

    checkfile = os.path.isfile(newfile)
    print(f"\n===createDict_jason=>  Does File <{newfile}> Exist?: <{checkfile}>")
    fd: open(newfile, "w", encoding = 'utf8')
    return checkfile,fd


# 12 => Check file existence - Restore Dictionary stored in a Jason File
def restoreDict_jason(file_path):
    jasonDict = {}
    okFlag = 'False'
    jason_file = file_path + '.json'
    checkfile = os.path.isfile(jason_file)
    print(f"\n===restoreDict_jason=>  Does File: <{jason_file}> Exist?: <{checkfile}>")
    if checkfile:
        # print(f"===restoreDict_jason=> os.path returned that jason file <{jason_file}> EXISTS: <{checkfile}")
        jasonList = open_file_jason(file_path)
        jasonDict = pairlist_to_dict(jasonList)
        okFlag = 'True'
    return okFlag,jasonDict

# 13 => Save dictionary in a jason file - if jason file does not exists a new file will be created
def saveDict_json(file_path, dict_2_save):
    """Saves a dictionary to a JSON file, if file does not exist create a new one
    Args:
    file_path: The path to the JSON file to save to.
    dict: The dictionary to save.

    Returns: ok Flag = 'True' if file arleady exited
    """
    
    jason_file = file_path + '.json'
    okFlag, fd = createDict_json(jason_file)
     # Save the dictionary to the JSON file.
    json.dump(dict_2_save, fd)
    # Close the JSON file.
    fd.close()

    return okFlag


# 14 => Reads one line in open file 'fr'
def readln(fr):
    line = fr.readline()
    return line

# 15 => setup Log File to write including Header Line
def initializeLogFile (file,hdr):
    checkfile = os.path.isfile(file)
    print(f"\n===initializeLogFile=> Does File: <{file}> Exists?: <{checkfile}>")
    fo = open(file,'a',encoding = "utf−8", newline = '')
    wout = csv.writer(fo, delimiter = ';')
    if checkfile != 'True':
        # print(f"===initializeLogFile=> As <{file}> does not exists creating Header Line")
        wout.writerow(hdr)
    return wout,fo

# 16 => transform a csv comma delimited file into a semicolon delimited text file
def CSV_2_SCSV_Converter(file):
    outFlag = 'False'
    infile = file
    outfile = file.replace('.csv','.txt')
    inFlag,fi = openFile_Reader(infile)
    if not inFlag:
        print(f"\n===CSV_2_SCSV_Converter=> Cannot convert problem with files: inFlag:<{inFlag}> outFlag: <{outFlag}>")
    else:
        outFlag,fo = openFile_Writer(outfile)
        while inputline := fi.readline():
            inputList,inputList_len = items_separator_converter(inputline,',')
            outputline = ''
            for item in inputList:
                outputline = outputline + item +';'
            outputline = outputline[:-1] +'\r\n'
            fo.write(outputline)
        outFlag = 'True'
        fi.close()
        fo.close()
    return inFlag,outFlag

# 17 => transform a csv comma delimited cia file into a semicolon delimited text file preserving the About field
def CSV_2_SCSV_CiaRecord_Converter(file):
    outFlag = 'False'
    infile = file
    outfile = file.replace('.csv','.txt')
    inFlag,fi = openFile_Reader(infile)
    if not inFlag:
        print(f"\n===CSV_2_SCSV_Converter=> Cannot convert problem with files: inFlag:<{inFlag}> outFlag: <{outFlag}>")
    else:
        
        outFlag,fo = openFile_Writer(outfile)
        # let´s first read the header
        headerline = fi.readline()
        headerline = headerline.replace(',',';')
        fo.write(headerline)
        while inputline := fi.readline():
            
            # we are going to extract the About column to preserve it's integrity
            about_pos = inputline.find('"')
            if about_pos < 0:  # the About field is empty and equal to '#X#'?
                about = '#X#'
                record = inputline[:-4]
            else:
                about = inputline[about_pos:]
                record = inputline[0:about_pos]
            record_list,record_list_len = items_separator_converter(record,',')
            outputline = ''
            for item in record_list:
                outputline = outputline + item +';'
            # !! outputline = outputline + about + '\r\n' # '\r'\n' should not be added?
            outputline = outputline + about
            fo.write(outputline)
        outFlag = 'True'
        fi.close()
        fo.close()
    return inFlag,outFlag
        
    


print(f"\n===FixInc Module=> <Files Operations 2021024-vop5>")


# In[ ]:




