#!/usr/bin/env python
# coding: utf-8

# In[1]:
# TODO: Need to put this module under VCS/GIT

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
import re

print(f"\n=== Initial Import <Horodateur + Basic Modules")


# In[2]:


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
#11 def cleanReplyAbout(reply): return cleanReply => Removes CR/NL so About one line - replaces <'> by <^> and <;> by <&>
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
### Module-FixIncome - BRD related Routines 20230803 -v1
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
#11  def BRD_getIndustry(ciaName): return troubleFlag,response => requests BRD API for the industry code of a company
#12  def BRD_getIndustryRegenerateSector(ciaName,sectorCode): return troubleFlag,response=> SubIndustry matching format <.IBD.15104030>
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
### FixInc User Interaction Routines - 20230803 -v2
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
#17 def USR_ciaSubIndustry(company): return userResp => askUser for company SubIndustry
#18 def USR_rescueIndustry(ciaName): return userResp,userSector,userIndustry,userSubIndustry => USR help Cia GICS Code
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

### hdr AppRF CDBs created from source AppRF HTML page
## 01: hdrSec_CBD, hdrSec_CBD_Record, hdrSec_CBD_len => Source AppRF
## 02: hdrSec_CVM_CSV. hdrSec_CVM_CSV_Record, hdrSec_CVM_CSV_len => AppRFsource file transformed in a csv database
## 03: hdrSec_XP,hdrSec_XP_Record,hdrSec_XP_len => Source XP manually grabbed from HTML page
## 04: hdrSec_XP_Offer, hdrSec_XP_Offer_Record, hdrSec_XP_Offer_len => XP Primary  UI Market HTML extraction
## 05: hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len => dictionnary of  CVM CiaName normalized,rough
## 06: hdrCia_MoodysRate, hdrCia_MoodysRate_Record, hdrCia_MoodysRate_len => Moodys Rating stuff
## 07: hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len => extracted/edited from CVM HTML page
## 08: hdrImpCia, hdrImpCia_Record, hdrImp_Record_len
## 09: hdrV1ImpCia, hdrV1ImpCia_Record, hdrV1Imp_Record_len
## 10 hdrV2_ImpCia, hdrV2_ImpCia_Record, hdrV2_Imp_Record_len
#//

print(f"\n===Initialising=> <General & FixInc Modules + Global Defs> exec@: {date_stamp()}")

