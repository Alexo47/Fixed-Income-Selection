#!/usr/bin/env python
# coding: utf-8

# In[6]:


### Import Basic Modules + Horodateur

import time

from datetime import datetime  # on veut tracer les executions
def date_stamp():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

import csv
# import datetime
from datetime import date, timedelta
import string
import os.path
import json

print(f"\n=== Initial Import <Horodateur + Basic Modules")


# In[9]:


### Initialising- General & FixInc Modules + Global Definitions

import ModFin_GlobalDefinitions as Mgv
### Module-FixIncome - Global Definitions
# fileDir: points to the main Jupiter directory
# token variables : EOR_token, EOF_token, broker_token, errpr_token
# ln: new line
# Headers & Records; cvmInputHeader, cvmOutputHeader, impCiaHeader (Neo4j import company file)
#//

import ModFin_ManagingCompanies as Mcia
### Module-FixIncome - ManagingCompanies 20230803 - v2
#01 match_CiaName(company): return foundFlag,CompanyName => Scan Cia Name as tokens to search Neo4j + User Interaction
#02 def testAcronymToken(token,limit): return limitFlag,ciaMatchHits => checks if Neo4j Hits > than user set limit
#03 def adjustCiaName(Name): return CompanyName => Adjusts auxilary words that do not need Capital letters
#04 def correctSpellingCompanyName(cia_name): return cia_name => Checks mispelled words in Company Names
#05 def cleanCompanyName(cia_name): return cia_name /* Removes Companies registration status suchas S.A., etc
#06 def checkCNPJFormat(cnpj): return okFlag => cheks if Cia CNPJ data looks like a CNPJ number
#07 def findMarkerCNPJ(cleanResponse,marker): return cnpjFlag,ciaCNPJ => scan a string to find a cnpj format sequence 
#08 def initAcronymsFile(File,Header): return fio,win,wout => Sets the csv readers/writers to start acronym processing
#09 def restoreAcronymSet(file): return acronymSet,len(acronymSet) => Process file containg acronyms to a set
#10 def open_AcronymsImport_Read(file): return okFlag,fi,win => Checks file existence Open file csv.reader
#11 def getAbout_chatGPT(CiaName): return About => Ask chatGPT about a company
#12 def cleanReplyAbout(reply): return cleanReply => Removes CR/NL so About one line - replaces <'> by <^> and <;> by <&>
#//

import ModFin_N4J as Mn4j
### Module-FixIncome - N4J related Routines as Mn4j
#01 N4J_session => import n4j module - connects to open a session
#02 def N4J_getCompanies(): return ciaList_len,ciaList => Query to N4J to download all companies in FixInc Database
#03 def N4J_checkCiaMatch(ciaName): => Checks if CiaName matches perfectly company already in the N4j database
#04 def N4J_correctCompanyName(companyName): return correctCiaName => Checks spelling with N4J FixInc Database
#05 def N4J_getAcrMatch(token): return ciaList_len,ciaList => Query N4J for CiaNames that includes token
#06 def N4J_changeCiaName(name, newName): return ciaList_len,ciaList => Set newName as CiaName in the N4J database
#07 def N4J_buildQuery_MergeCia(recordList): return cypher_script => build query to upload new Cia into N4J Database
#08 def N4J_getCompany_noAbout(session): return ciaName => returns one company where About =#X#
#09 def N4J_pushAbout(session,CiaName,About): return responseList => store About in N4J database
#//

import ModFin_BRD as Mbrd
### Module-FixIncome - BRD related Routines 20230803 -v1 as Mbrd
#01 BRD_KeyAPI => BRD API key extracted form cookies
#02a BRD_InoperativeList => BRD meaningless About responses
#02b BRD_InoperativeList_len => len(BRD_InoperativeList)
#03a BRD_InoperativeSet =>
#03b BRD_InoperativeSet_len =>
#04a BRD_PlatitudesList => BRD Platitudes About responses:
#04b BRD_PlatitudesList_len => len(BRD_PlatitudesList)
#05 def BRD_CiaAbout(ciaName): return troubleFlag,ciaAbout => Prompts BRD for an About of a company
#06  def BRD_cleanReplyAbout(reply): return cleanReply => Removes special characters + BRD Noise
#07  def BRD_CiaCNPJ(ciaName): return troubleFlag,cnpjFlag,ciaCNPJ => Prompts BRD for CNPJ of a company
#08  def BRD_checkTrafficTrouble(reply): return troubleFlag => Checks if BRD is operational (network accessible)
#09  def BRD_checkAbooutPertinence(about):return okFlag => check if BRD reply is non operative
#10  def BRD_FilterPlatitudes(about): return about => remove BRD boilerplate platitudes
#//

import ModFin_GPT as Mgpt
### Module-FixIncome - GPT related Routines  20230803 -v1 as Mgpt
#01  GPT_keyAPI => connection key to activate chatGPT API
#02a GPT_InoperativeList => List of useless sentences used by chatGPT
#02b GPT_InoperativeList_len = len(GPT_InoperativeList_len)
#03  def GPT_getAbout(CiaName): return About => Activates chatGPT prompting for an About
#04  def GPT_cleanAbout(reply): return cleanReply => Replace some characters + remove chatGPT boilerplate text
#//

import ModGen_UserInteractionRoutines as Musr
### FixInc User Interaction Routines - 20230803-v2
#01 def USR_hitLimit(): return userResp  Asks user maximum number of hits
#02 def USR_tokenFeedback(company,token): return userResp  User feedback on a token: Acronym,CommonWord
#03 def USR_confirmCompany(company): return foundFlag,companyName  Company not in Neo4j so what do?
#04 def USR_hitListChoice(company,hitList): return selectFlag,CompanyName  Select Neo4j potential Hits or discard?
#05 def USR_companyConfirmation(company): return userResp => Confirmation for new Company in the database
#06 def USR_companyGoNogo(company): return userResp => shows about and ask for UI confirmation or discard Cia
#07 def USR_rectifyCompanyName(company): return companyName => ask user to rectify company name
#08 def USR_confirmCiaHighestHit(cvmName,n4jName): return userResp => cvmCiaName highest hit:accept,rename or ignore?
#09 def USR_confirmAcronym(acronym,hits): return userResp  Acronym Hits level accept/discard?
#10 def USR_confirmCommonWord(word): return userResp  Confirmation for a Common Word
#11 def USR_StartResume(): return userResp  [S]tart processing from scratch or [R]esume processing
#12 def USR_ciaCNPJ(company): return userResp => askUser for company CNPJ
#13 def USR_ciaAbout(company): return userResp => askUser for company About
#14 def USR_rescueAbout(ciaName): return userResp,ciaAbout => askUser to manually rescue About
#15 def USR_checkAbout(company,about): return userResp,cleanAbout => About looks fishy ask user feedback
#16 def USR_rescueCNPJ(ciaName): return userResp,ciaCNPJ => askUser to manually rescue CNPJ
#//

import ModGen_ManipulatingPythonStructures as Mpst
#// Module-General - Gestion de Structures
#01 def takeSecond(elem): return elem[1]  => take second element for sort
#02 def build_dict (word_list): return dict_words_occurrences => Builddictionnary [word:number of occureences] from a chain
#03 def pairlist_to_dict(list): return dict => Take double entry list and transform it in a dictionnary
#04 def dict_to_pairlist(dict): return list => Take dictionnary and transform it in a pair entry key list
#05 def short_list_elements(list,n): return shorted_list => Select N first elements of a sorted list
#06 def get_words(dict,lang,count): return words => Retrieve key words in dictionnary
#07 def list_average(list): return avg => Calculate average of values in a list
#//

import ModGen_FilesOperations as Mfil
#// Module-General - Files Operations
#01 def fpath(dir,filename): return path /# Crée le path pour un directory de data avec la filename
#02 def openFile_Reader(filePath): return okFlag,fi,win /# Checks file existence - set reader utf8 newline '' delimiter ';'
#03 def openFile_Writer(filePath): return okFlag,fo,wout /# Checks file existence - set writer utf8 newline '' delimiter ';'
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
#//

import ModGen_CharactersChainText as Mnlp
#// Module_General_CharactersChainText_Manipulation
#01 def split_words(chain): return word_list #01 => Simple split chain to words
#02 def items_comma_converter(line): return liste,len(liste) => Converts a line with commas into a list
#03 def items_separator_converter(line,separator): return liste,len(liste) => Converts a line with separator char into a list
#//

import ModFin_Headers as Mhdr
## 01: hdrSec_CBD, hdrSec_CBD_Record, hdrSec_CBD_len => Source AppRF
## 02: hdrSec_CVM_CSV. hdrSec_CVM_CSV_Record, hdrSec_CVM_CSV_len => AppRFsource file transformed in a csv database
## 03: hdrSec_XP,hdrSec_XP_Record,hdrSec_XP_len => Source XP manually grabbed from HTML page
## 04: hdrSec_XP_Offer, hdrSec_XP_Offer_Record, hdrSec_XP_Offer_len => XP Primary  UI Market HTML extraction
## 05: hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len => dictionnary of  CVM CiaName normalized,rough
## 06: hdrCia_MoodysRate, hdrCia_MoodysRate_Record, hdrCia_MoodysRate_len => Moodys Rating stuff
## 07: hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len => extracted/edited from CVM HTML page

print(f"\n===Initialising=> <General & FixInc Modules + Global Defs> exec@: {date_stamp()}")


# In[3]:


### ROB-CIA_N4J_BARD_CSV_V1-DataBuilderUpgraded BEGINS HERE
# This routine is an upgraded version of PRG-CIA_N4J_BARD_CSV_V1-DataBuilder
# It works with N4j-CIA_CSV_UpdatedExtractedRecords which has 12 column format (two Abouts),: namely:
# CiaCNPJ;CiaName;SubIndustryCode;IndustryCode;SectorCode;Region;Fitch;SP;Moody;Group;About;aboutBRD
# This file indicates completely what are the fields missing '#X#' and hence the Engine will sollicitate Bard
# Moreover it employs Bard filters (Inoperative Set and Platitudes List ) as a first cleaning process

# ModFin_GlobalDefinitions as Mgv
# ModFin_ManagingCompanies as Mcia
# ModFin_UserInteractionsRoutines as Mui
# ModFin_Headers as Mhdr
# ModGen_CharactersChainText as Mnlp
# ModGen_ ModGen_FilesOperations as Mfil
# ModGen_ManipulatingPythonStructures as Mpst

print(f"\n===### ROB-CIA_N4J_BARD_CSV_V1-DataBuilder=> <BEGINS HERE> exec@: {date_stamp()}")


# In[4]:


### ROB-CIA_N4J_BARD_CSV_V1-DataBuilderUpgraded BARD API SetUp

bard = Bard(token=Mbrd.BRD_KeyAPI)

bardText = "Hello Bard! Please take note of the following:\n\n (1) I am not personnally interacting with you "\
"but through a python program via bardapi therefore my program does not understand polite boilerplate sentences such as:\n " \
"<I hope this helps!> or <Is there anything else I can help you with?>\n But if you must insert such polite statements "\
"please stick to the same formulation and avoid variants such as:\n<Sure!> , <Sure.> or <Sure,> \n" \
"(2) My current task is to find the CNPJ register of Brazilian companies.\n "\
"Every Brazilian company (large,small, public, private,...) has a CNPJ number that is widely published "\
"and public available, there is absolutely no confidential information so you should not have any problem\n "\
"(3) In your response, please braket the CNPJ number with two asteriscs ** such as in the following reply:\n"\
"<Sure, the CNPJ number for Energisa-MGS Distribuidora de Energia is **19.527.639/0001-58**.> \n" \
"(4) In your response if you reference the company name, please use the same name I provided you in my request\n"\
"(5) Use only English language \n"
cnpjTest = "As a test, please provide me CNPJ number for this Brazilian company:\n"\
"<Dektop Sigmanet Comunicação Multimidia>"

query = bardText + '\n' + cnpjTest
print(query)
response = bard.get_answer(query)
print(response)
    

print(f"\n===V1-DataBuilderUpgraded=> <BARD API setup> exec@: {date_stamp()}")


# In[4]:


### ROB-CIA_N4J_BARD_CSV_V1-DataBuilderUpgraded - Specific Routines

def V1_HeaderConverter(inList):
    outList =[None]*12
    outList[0] = inList[1]
    outList[1:5] = inList[2:6]
    outList[5] = inList[7]
    outList[6:10] = inList[9:13]
    outList[10] = inList[13]
    outList[11] = '#X#'
    return outList


def writeCia_V1Record(fo,outList):

    lineRecord = ''
    for indx in range(len(outList)):
        lineRecord = lineRecord + outList[indx] + ';' # the last ; will be removed removed 
    # print(f"===writeCia_V1Record> After loop Before corrections; rough lineRecord:\n{lineRecord} ")
    lineRecord = lineRecord[:-1] + '\r\n'
    # print(f"===writeCia_V1Record> After loop After Corrections cleaned lineRecord:\n{lineRecord} ")
    fo.write(lineRecord)

    return lineRecord
    

           
print(f"\n===V1-DataBuilderUpgraded=> <Specific Routines> exec@: {date_stamp()}")


# In[8]:


### ROB-CIA_N4J_CSV_About-CNPJ_V1-DataBuilderUpgraded - Initializing InOutFiles

"""
# v0 CiaImp Header
hdrInput[0] = 'CiaCode'
hdrInput[1] = 'CiaCNPJ'    
hdrInput[2] = 'CiaName'    
hdrInput[3] = 'SubIndustryCode'
hdrInput[4] = 'IndustryCode'
hdrInput[5] = 'SectorCode'
hdrInput[6] = 'InternalCode'
hdrInput[7] = 'Region'    
hdrInput[8] = 'Sym6C'
hdrInput[9] = 'Fitch'
hdrInput[10] = 'SP'
hdrInput[11] = 'Moody'
hdrInput[12] = 'Group' 
hdrInput[13] = 'About'

# v1 CiaImp Header
hdrOutput[0] = 'CiaCNPJ'    
hdrOutput[1] = 'CiaName'
hdrOutput[2] = 'SubIndustryCode'
hdrOutput[3] = 'IndustryCode'
hdrOutput[4] = 'SectorCode'
hdrOutput[5] = 'Region'
hdrOutput[6] = 'Fitch'
hdrOutput[7] = 'SP'
hdrOutput[8] = 'Moody'
hdrOutput[9] = 'Group' 
hdrOutput[10] = 'aboutGPT'
hdrOutput[11] = 'aboutBRD'

"""
inFileName = 'N4j-CIA_CSV_UpdatedExtractedRecords_20230728-v1'
inFilePath = Mgv.filesDir + "/" + inFileName
inFile = inFilePath +'.txt'

outFileName = 'N4j-CIA_UI_BRD_CSV_V1-UpgradedRecords_20230728-v1'
outFilePath = Mgv.filesDir + "/" + outFileName
outFile = outFilePath +'.txt'

logFileName = 'RF$-LOG_N4j-CIA_UI_BRD_CSV_V1-UpgragedRecords_20230728-v1'
logFilePath = Mgv.filesDir + "/" + logFileName
logFile = logFilePath + '.txt'
hdrLog = ['Records', 'LastCia']
logRecord =[None]*2

# Let's check if User wants to start from scratch or resume Operations
resumeFlag = 'False'# by default
ciaFound = 'False' # by default
logFlag = 'False'
dataFlag = 'False'
userResp = Mui.askUser_StartResume()
if userResp == 'R' or userResp == 'r':
    resumeFlag ='True'
    logFlag,fi_log = Mfil.openFile_Reader(logFile)
    if logFlag == 'False':
        print(f"\n===Start/Resume=> LogFile <{logFileName}> Status: {logFlag} => Not Possible to Resume")
    else:
        # we are going to loop on Log File to read the last record to find the last Cia processed
        recordCount = 0
        foundCount = 0
        logHeaderLine = fi_log.readline()
        while line := fi_log.readline():
            # print(f"\n===Start/Resume=> LogFile Current Line: {line})
            logLine = line
        # print(f"\n===Start/Resume=> LogFileLast Line: {line})
        logList,logList_len = Mnlp.items_separator_converter(logLine,';')
        recordCount = recordCount + int(logList[0])
        lastCiaName = logList[1]
        print(f"\n===Start/Resume=> LogFile <{logFileName}> indicates: <{lastCiaName}> as last Cia processed")
        # we need now to set inputfile to the next Cia position
        inFlag,fi = Mfil.openFile_Reader(inFile)
        inHeader = fi.readline()
        if inFlag == 'False':
            print(f"\n===Start/Resume=> LogFile <{inFileName}> Status: {inFlag} => Impossible to Resume - Key Data missing")
        else:
            dataFlag = 'True'
            while inputLine := fi.readline():
                # print(f"\n===Start/Resume=> Current Cia Input Line:\n{inputLine} ")
                inputList,inputList_len = Mnlp.items_separator_converter(inputLine,';')
                currentCiaName = inputList[1]
                # print(f"\n===Start/Resume=> Current Cia Name: <{currentCiaName}> ")
                if currentCiaName == lastCiaName: # we finished scanning
                    ciaFound = 'True'
                    break
                       
# we need now to finish initialization accordingly
if resumeFlag == 'True':
    if dataFlag == 'True' and ciaFound == 'True':
        outFlag,fo = Mfil.openFile_Writer(outFile)
        fi_log.close()
        logFlag,fo_log = Mfil.openFile_Writer(logFile)
    else:
        print(f"===Start/Resume=> dataFlag: {dataFlag} or ciaFound: {ciaFound} => Impossible to Resume")

else: # we are starting from Scratch
    inFlag,fi = Mfil.openFile_Reader(inFile)
    inHeader = fi.readline()
    print(f"\n===V1-DataBuilderUpgraded=> Initialization inputFile Header: \n{inHeader}")
    outFlag,fo = Mfil.openFile_Writer(outFile)
    hdr_len = len(Mhdr.hdrV1ImpCia)
    hdrLine = ''
    for indx in range(hdr_len):
        hdrLine = hdrLine + Mhdr.hdrV1ImpCia[indx] + ';'
    hdrLine = hdrLine + 'aboutBRD' +'\r\n' # no <;> on the last columns
    print(f"\n===V1-DataBuilderUpgraded=> Initialization OutputFile Header: \n{hdrLine}")    
    fo.write(hdrLine)
    wout_log,fo_log = Mfil.initializeLogFile (logFile,hdrLog)

                    

print(f"\n===V1-DataBuilderUpgraded=> <Initializing InOutFiles> exec@: {date_stamp()}")


# In[9]:


### ROB-CIA_N4J_CSV_About-CNPJ_V1-DataBuilderUpgraded=> ENGINE - Looping on input file records building N4J CCSV file >


userContinue = 'True'
recordCount = 0
ciaNameListProcessed = []
#pauseTimer = 20
#pauseTimer = 10
pauseTimer = 7


while inputLine := fi.readline():
    if userContinue == 'False':
        break
    recordCount += 1
    # print(f"\n===V1-DataBuilderUpgraded=> Current cycle Record# {recordCount} is: \n{inputLine}")

    inputList,inputList_len = Mnlp.items_separator_converter(inputLine,';')
    # outputList = V1_HeaderConverter(inputList) # there is no conversion both files are v0.5 impCiaHeader
    outputList = inputList

    ciaCNPJ = outputList[0]
    ciaName = outputList[1]
    ciaAboutGPT = outputList[10]
    ciaAboutBRD = outputList[11]
    ciaNameListProcessed.append(ciaName)
    print('\n')
    print('x' * 120)
    print(f"===V1-DataBuilderUpgraded=> Processing: Record# {recordCount} Cia: <{ciaName}> CNPJ: <{ciaCNPJ}>")
    print('x' * 120)
    if ciaCNPJ == '#X#':
        time.sleep(pauseTimer)
        trafficTroubleFlag,brdFlag,brdCNPJ = Mbrd.BRD_CiaCNPJ(ciaName)      
        if trafficTroubleFlag == 'True' or brdFlag == 'False':
            print(f"\n===V1-DataBuilderUpgraded=> For Company <{ciaName}> API return not satisfactory ")
            # we bypass automation and ask for UI help
            userResp,uiCNPJ = Musr.USR_rescueCNPJ(ciaName)
            if userResp == 'Stop':
                # user wants to stop scanning
                userContinue = 'False'
                print(f"\n===V1-DataBuilderUpgraded==> For Company <{ciaName}> UI said STOP: <{userResp}>  ")
                break
            else: # rescue provides a corrrect and processed value for CNPJ
                outputList[0]= uiCNPJ
                print(f"\n===V1-DataBuilderUpgraded==> For Company <{ciaName}> UI CiaCNPJ: <{uiCNPJ}>  ")                      
        else:
            outputList[0] = brdCNPJ
            print(f"\n===V1-DataBuilderUpgraded==> For Company <{ciaName}> BRD CiaCNPJ: <{brdCNPJ}>  ") 
    else:
        print(f"\n===V1-DataBuilderUpgraded=> Cia: <{ciaName}> ; CNPJ Alredy Stored => {ciaCNPJ}") 

# we are going now to request BRD for an About
    if ciaAboutBRD == '#X#':
        print(f"\n===V1-DataBuilderUpgraded=> For Company <{ciaName}> ciaAboutBRD NOT Stored")
        time.sleep(pauseTimer)
        trafficTroubleFlag,ciaAboutBRDCrude = Mbrd.BRD_CiaAbout(ciaName)
        print(f"\n===V1-DataBuilderUpgraded=> BRD=> Trouble?: {trafficTroubleFlag} ; BRD About:\n{ciaAboutBRDCrude}")
        if trafficTroubleFlag == 'True':
            print(f"\n===V1-DataBuilderUpgraded=> For Company <{ciaName}> BRD About detected traffic trouble=> UI rescue")
            # we bypass automation and ask for UI help
            userResp,uiAboutBRD = Musr.USR_rescueAbout(ciaName)
            print(f"\n===V1-DataBuilderUpgraded=> UI=> resp: {userResp} ; UI About:\n{uiAboutBRD}")
            if userResp == 'Stop':
                # user wants to stop scanning
                userContinue = 'False'
                print(f"\n===V1-DataBuilderUpgraded==> For Company <{ciaName}> UI said STOP: <{userResp}>  ")
                break
            else: # rescue provides a corrrect and processed valu for aboutBRD
                outputList[11]= uiAboutBRD
                print(f"\n===V1-DataBuilderUpgraded==> For Company <{ciaName}> UI CiaAbout: <{uiAboutBRD}>  ")                      
        else:
            aboutBRDFlag = Mbrd.BRD_checkAboutPertinence(ciaAboutBRDCrude)
            if aboutBRDFlag == 'False':
                # we are going to ask UI to provide an about
                print(f"\n===V1-DataBuilderUpgraded=> BRD response rejected UI for rescue") 
                userResp,uiAboutBRD = Musr.USR_rescueAbout(ciaName)
                print(f"\n===V1-DataBuilderUpgraded=> UI=> resp: {userResp} ; UI About:\n{uiAboutBRD}")
                if userResp == 'Stop':
                    # user wants to stop scanning
                    userContinue = 'False'
                    print(f"\n===V1-DataBuilderUpgraded==> For Company <{ciaName}> UI said STOP: <{userResp}>  ")
                else: # rescue provides a corrrect and processed valu for aboutBRD
                    outputList[11]= uiAboutBRD
                    print(f"\n===V1-DataBuilderUpgraded==> For Company <{ciaName}> UI CiaAbout: <{uiAboutBRD}>  ")                                     
            else:
                # There is some goood stuff let´s try to clean the boilerplate sentences
                ciaAboutBRD = Mbrd.BRD_FilterPlatitudes(ciaAboutBRDCrude)
                outputList[11] = ciaAboutBRD
    else:
        print(f"\n===V1-DataBuilderUpgraded=> Cia: <{ciaName}> ; About Alredy Stored,namely:\n {ciaAboutBRD}")        

    if userContinue == 'True':
        # we are going now to write record @ output file
        outputLine = writeCia_V1Record(fo,outputList)
        # print(f"\n===V1-DataBuilderUpgraded=> For Company <{ciaName}> BRD provided an About:\n {ciaAboutBRD}  ")
    else:
        # we will abandon the current Cia because user asked for Stop}
        print(f"\n======V1-DataBuilderUpgraded=>=> current Cia {ciaName} abandonned UI asked for Stop")
        break

# we finished looping we are going now to save the processing log
if recordCount > 1:
    lastCiaName = ciaNameListProcessed[-2]
    print(f"\n===V1-DataBuilderUpgraded=> Cias Processed {ciaNameListProcessed}\nLast = <{lastCiaName}>")
    logLine = ''
    logline = logLine + str(recordCount) + ';' + lastCiaName + '\r\n'
    fo_log.write(logline)
    print(f"\n===V1-DataBuilderUpgraded=> Processed {recordCount} records with Last record CiaName: <{lastCiaName}>")
else:
    print(f"\n===V1-DataBuilderUpgraded=> Processed {recordCount} => No processing - No Log")

# we need to close open files
fi.close()
fo.close()
fo_log.close()

print(f"\n===V1-DataBuilderUpgraded=> <ENGINE> exec@: {date_stamp()}")


# In[ ]:


### ROB-CIA_N4J_CSV_About-CNPJ_V1-DataBuilderUpgraded=> Recovery after execution interrupted or crash 

if recordCount > 1:
    lastCiaName = ciaNameListProcessed[-2]
    print(f"\n===V1-DataBuilderUpgraded=> Cias Processed {ciaNameListProcessed}\nLast = <{lastCiaName}>")
    logLine = ''
    logline = logLine + str(recordCount) + ';' + lastCiaName + '\r\n'
    fo_log.write(logline)
    print(f"\n===V1-DataBuilderUpgraded=> Processed {recordCount} records with Last record CiaName: <{lastCiaName}>")
else:
    print(f"\n===V1-DataBuilderUpgraded=> Processed {recordCount} => No processing - No Log")

fi.close()
fo.close()
fo_log.close()
    
print(f"\n===V1-DataBuilderUpgraded=> <ENGINE> exec@: {date_stamp()}")


# In[ ]:


fi.close()
fo.close()
fo_log.close()
print(f"\n===MatchingNames-NewCia=> <RESCUE - closing ressources > exec@: {date_stamp()}")


# In[ ]:


large = len('===V1-DataBuilderUpgraded=> Cias Processed [CESP Companhia Energetica de São Paulo, CGTEE Companhia de Geração e Transmissão')
print(large)
print('\n')
print('x' * 120)


# In[ ]:


print(bardText)
print(cnpjTest)


# In[ ]:




