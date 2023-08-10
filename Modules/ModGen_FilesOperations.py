#!/usr/bin/env python
# coding: utf-8

# In[1]:


#// Module-General - Files Operations
#01 def fpath(dir,filename): return path /# Crée le path pour un directory de data avec la filename
#02 def openFile_Reader(file): return okFlag,fi /# Checks file existence - set reader utf8 newline '' delimiter ';'
#03 def openFile_Writer(file): return okFlag,fo /# Checks file existence - set writer utf8 newline '' delimiter ';'
#04 def openFile_ReadWriter(filePath): return okFlag,fio,win,wout /# Checks file - set R/W utf8 newline '' delimiter ';'
#05 def openCSV_Reader(filePath): return okFlag,fi,win /# Checks file existence - set csv.reader utf-8 delimiter ';'
#06 def openCSV_Writer(filePath) /# Checks file existence - set csv.writer utf-8 delimiter ';' newline = ''
#07 def read_file(path): return word_chain /# lit fichier avec le traitement d'encoding utf8
#08 def save_file_jason(index,path): return /# sauvegarde fichier d'extension .json - gestion encoding utf-8
#09 def open_file_jason(path): return index /# ouvre et lit fichier extension .json avec encoding utf8
#10 def restoreSet_jason(filePath): return okFlag,localSet /# Check file existence - Restore Set stored in a Jason File
#11 def restoreDict_jason(filePath): return okFlag,jasonDict /# Check file existence - Restore Dict stored in a Jason File
#12 def readln(fr): return line /# read new line
#13 def initializeLogFile (file,hdr): return wout,fo => setup Log File to write including Header Line
#14 def CSV_2_SCSV_Converter(file):return inFlag,outFlag => transform comma delimited file into a semicolon text file
#//

import string
import os.path
import json
import csv

from ModGen_ManipulatingPythonStructures import pairlist_to_dict
from ModGen_CharactersChainText import items_separator_converter

#01 /# Crée le path pour un directory de data avec la filename
def fpath(dir,filename):
    path = dir  +'/' + filename
    return path

#02 /# Checks file existence - set reader utf8 newline '' delimiter ';'
def openFile_Reader(file):
    # file contains the full path of the file
    okFlag = 'True'
    fi = 'False'
    checkFile = os.path.isfile(file)
    print(f"\n===openFile_Reader=> Does File: <{file}> Exists? => {checkFile}")
    if checkFile:
        # print(f"\n===openFile_Reader=> checkFile states that <{file}> EXISTS <{checkFile}")
        fi = open(file,'r',encoding = "utf−8", newline = '')
    else:
        # print(f"\n===openFile_Reader=> checkFile states that <{file}> DOES NOT EXIST: <{checkFile}")
        okFlag = 'False'
    return okFlag,fi


#03 /# Checks file existence - set writer utf8 newline '' delimiter ';'
def openFile_Writer(file):
    okFlag = 'True'
    fo = 'False'
    checkFile = os.path.isfile(file)
    print(f"\n===openFile_Writer=> Does File: <{file}> Exists? => {checkFile}")
    if checkFile:
        # print(f"\n===openFile_Writer=> checkFile states that <{file}> EXISTS <{checkFile}")
        fo = open(file,'a',encoding = "utf−8", newline = '')
    else:
        # print(f"\n===openFile_Writer=> checkFile states that <{file}> DOES NOT EXIST: <{checkFile} => open new file")
        fo = open(file,'a',encoding = "utf−8", newline = '')
        okFlag = 'False'
    return okFlag,fo

#04 /# Checks file existence - set R/W utf8 newline '' delimiter ';'
def openFile_ReaderWriter(filePath):
    inputFile = filePath + '.txt'
    okFlag = 'True'
    win = 'False'
    wout = 'False'
    fio = 'False'
    checkFile = os.path.isfile(inputFile)
    print(f"\n===openFile_ReaderWriter=> Does File: <{inputFile}> Exists? => {checkFile}")
    if checkFile:
        # print(f"\n===openFile_ReaderWriter=> checkFile states that <{inputFile}> EXISTS <{checkFile}")
        fio = open(inputFile,'r+',encoding = "utf−8", newline = '')
        win = csv.reader(fio, delimiter = ';')
        wout = csv.writer(fio, delimiter = ';')
    else:
        # print(f"\n===openFile_ReaderWriter=> checkFile states that <{inputFile}> DOES NOT EXIST: <{checkFile}")
        okFlag = 'False'
    return okFlag,fio,win,wout

#05 /# Checks file existence - set csv.reader utf-8 delimiter ';'
def openCSV_Reader(filePath):
    inputFile = filePath + '.csv'
    okFlag = 'True'
    win = 'False'
    fi = 'False'
    checkFile = os.path.isfile(inputFile)
    print(f"\n===openCSV_Reader=> Does File: <{inputFile}> Exists? => {checkFile}")
    if checkFile:
        # print(f"\n===openCSV_Reader=> checkFile states that <{inputFile}> EXISTS <{checkFile}")
        fi = open(inputFile,'r',encoding = "utf−8")
        win = csv.reader(fi, delimiter = ';')
    else:
        # print(f"\n===openLogFile_Reader=> checkFile states that <{inputFile}> DOES NOT EXIST: <{checkFile}")
        okFlag = 'False'
    return okFlag,fi,win

#06 /# Checks file existence - set csv.writer utf-8 delimiter ';' newline = ''
def openCSV_Writer(filePath):
    outputtFile = filePath + '.csv'
    okFlag = 'True'
    wout = 'False'
    fo = 'False'
    checkFile = os.path.isfile(outputFile)
    print(f"\n===openCSV_Reader=> Does File: <{outputFile}> Exists? => {checkFile}")
    if checkFile:
        # print(f"\n===openCSV_Reader=> checkFile states that <{inputFile}> EXISTS <{checkFile}")
        fo = open(outputFile,'a',encoding = "utf−8", newline = '')
        wout = csv.writer(fo, delimiter = ';')
    else:
        # print(f"\n===openLogFile_Reader=> checkFile states that <{inputFile}> DOES NOT EXIST: <{checkFile}")
        okFlag = 'False'
        fo = open(outputFile,'a',encoding = "utf−8", newline = '')
        wout = csv.writer(fo, delimiter = ';')

    return okFlag,fo,wout

#07 Lit fichier avec le traitement d'encoding utf8
def read_file(path):
    with open(path, encoding = "utf−8") as f:
        word_chain = f.read()
    return word_chain

#08 /# Sauvegarde fichier d'extension .json - gestion encoding utf-8
def save_file_jason(index,path):
    filename = path + '.json'
    with open(filename,'w',encoding = 'utf8') as fp:
        json.dump(index,fp,ensure_ascii=False)
        fp.close()
        print(f"\n===save_file_jason=> Just dumped index to {filename}")
    return

#09 /# Ouvre et lit fichier extension .json avec encoding utf8
def open_file_jason(path):
    filename = path + '.json'
    index = {}
    with open(filename,'r',encoding = 'utf8') as fp:
        index = json.load(fp)
        fp.close()
        print(f"\n===open_file_jason=> Just loaded {filename} as returned index")
    return index

#10 /# Check file existence - Restore Set stored in a Jason File
def restoreSet_jason(filePath):
    localSet = {}
    okFlag = 'False'
    outFile = filePath + '.json'
    checkFile = os.path.isfile(outFile)
    print(f"\n===restoreAcronymSet_jason=> Does File: <{outFile}> Exists? => {checkFile}")
    if checkFile:
        # print(f"\n===restoreAcronymSet_jason=> jason file <{outFile}> EXISTS: <{checkFile}")
        localList = open_file_jason(filePath)
        localSet = {item for item in localList}
        okFlag = 'True'
    return okFlag,localSet

#11 /# Check file existence - Restore Dictionnary stored in a Jason File
def restoreDict_jason(filePath):
    jasonDict = {}
    okFlag = 'False'
    jasonFile = filePath + '.json'
    checkFile = os.path.isfile(jasonFile)
    print(f"\n===restoreDict_jason=>  Does File: <{jasonFile}> Exist?: <{checkFile}>")
    if checkFile:
        # print(f"===restoreDict_jason=> os.path returned that jason file <{jasonFile}> EXISTS: <{checkFile}")
        jasonList = open_file_jason(filePath)
        jasonDict = pairlist_to_dict(jasonList)
        okFlag = 'True'
    return okFlag,jasonDict

#12 /# read new line
def readln(fr):
    line = fr.readline()
    return line

#13 => setup Log File to write including Header Line
def initializeLogFile (file,hdr):
    checkFile = os.path.isfile(file)
    print(f"\n===initializeLogFile=> Does File: <{file}> Exists?: <{checkFile}>")
    fo = open(file,'a',encoding = "utf−8", newline = '')
    wout = csv.writer(fo, delimiter = ';')
    if checkFile != 'True':
        # print(f"===initializeLogFile=> As <{file}> does not exists creating Header Line")
        wout.writerow(hdr)
    return wout,fo

#14 => transform a csv comma delimited file into a semicolon delimited text file
def CSV_2_SCSV_Converter(file):
    outFlag = 'False'
    infile = file
    outfile = file.replace('.csv','.txt')
    inFlag,fi = openFile_Reader(infile)
    if inFlag =='False':
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
        
    


print(f"\n===FixInc Module=> <Files Operations 20230801-vop4>")


# In[ ]:




