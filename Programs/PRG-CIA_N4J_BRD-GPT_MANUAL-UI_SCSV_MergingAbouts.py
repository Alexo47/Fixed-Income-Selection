#!/usr/bin/env python
# coding: utf-8
# from IPython import get_ipython


### ROB-SET_GPT-BRD_MergeAbouts BEGINS HERE
# This routine Merges AboutGPT with About Bard in order to create one single about
# It works with the latest file N4J-CIA_SCSV_AboutIndustryRecords
# which has 12 column format (two Abouts),: namely:
# CiaCNPJ;CiaName;SubIndustryCode;IndustryCode;SectorCode;Region;Fitch;SP;Moody;Group;
# About;aboutBRD
# This routine version v.1 just concatenate the two abouts if they are meaningful, discarding platitudes.
# For that it will use cleaning filters: (1) BRD_FilterPlatitudes(about) and (2) GPT_cleanAbout(reply)
# with learned lists of Inoperative Set and Platitudes List )
# => When chatGPT and Bard APIs will work again, they will be sollicited to produce a best merge
#//


# import Modules.ModHead
from Modules.ModHead import *

import textwrap

print(f"\n===PRG-CIA_N4J_BRD_UI_SCSV_IndustryCode=> <BEGINS HERE>")

"""
### BARD API Setup
import Modules.ModFin_BRD as Mbrd

from bardapi import Bard
# myToken = 'awh5YWTO8IrYw-mmk3qAFGi6T6X_XUo27w4b44wNu_T3gCzDOXyqzOdtBksLWj5O4mQu1A.' # valid untill 2025??
myToken = Mbrd.BRD_KeyAPI
bard = Bard(token = myToken)
#
response = bard.get_answer("Tell me About this Brazilian Company: 'Desktop Sigmanet Comunicação Multimidia'")
print(response)

print(f"\n===BRD API=> <Setup> exec@: {date_stamp()}")
"""


### BRD-GPT_UI_SCSV_MergingAbouts - Specific Routines

def V0_HeaderConverter(inList):
    outList = [None] * 11
    for indx in range(len(outList)-1):
        outList[indx] = inList[indx]
    outList[10] = '#X#'
    return outList


def writeCia_V1Record(fo, outList):
    lineRecord = ''
    for indx in range(len(outList)):
        lineRecord = lineRecord + outList[indx] + ';'  # the last ; will be removed removed
    # print(f"===writeCia_V1Record> After loop Before corrections; rough lineRecord:\n{lineRecord} ")
    lineRecord = lineRecord[:-1] + '\r\n'
    # print(f"===writeCia_V1Record> After loop After Corrections cleaned lineRecord:\n{lineRecord} ")
    fo.write(lineRecord)

    return lineRecord

print(f"\n===BRD-GPT_UI_SCSV_MergingAbouts=> <Specific Routines> exec@: {date_stamp()}")



### PRG-CIA_N4J_BRD-GPT_UI_SCSV_MergingAbouts - Modulable Routines
# nn USR_check_boutMerge(company,about): return userResp => request USR - to check cleaned Text of the About

# nn => request USR - to check Bard merge (cleaned Text) of the Abouts for company SubIndustry
def USR_checkGPT_aboutMerge(company, aboutBRD,aboutGPT):
    queryGPT = 'Topic = Merge Text -  Below you will find to texts (About1 and About2) containing descriptions'\
            ' about Brazilian company: ' + company + ' Can you merge About1 & About2 into a single non redundant About'\
            ' without missing any key point and without explicitly referencing the original text (About1 and About2)?'
    about1 = 'About1 = ' + '\'' +  aboutBRD + '\''
    about2 = 'About2 = ' + '\''+  aboutGPT +'\''

    promptGPT = '\n' + queryGPT + '\n' +'\n' + about1 +  '\n' +'\n' + about2 +'\n'
    print('\n\n')
    print('-' * 80)
    print(textwrap.fill(promptGPT,80))
    print('-' * 80)
    # print(f"\n===USR_check_aboutMerge=> GPT About Looks like this: \n")
    # print(textwrap.fill(aboutGPT,100))
    prompt = 'For Company: <' + company + '> GPT manually merged Abouts you want to: \n'\
                                          '[F]ile contains new GPT text ; [I]gnore or [S]top processing: \n?'
    # print(prompt)
    userResp = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {userResp}" )
    return userResp

def GPT_readFile_cleanAbout(f):
    flag, file = Mfil.openFile_Reader(f)
    if flag == 'False':
        print(f"\n===GPT_readFile_cleanAbout=> File <{f}> Status: {flag} => Impossible to Read - File does not exist")
    about0 = file.read()
    about = Mgpt.GPT_cleanAbout(about0)
    return flag,about

print(f"\n===MergingAbouts=> <Modulable Routines> exec@: {date_stamp()}")

### PRG-CIA_N4J_BRD_UI_SCSV_IndustryCode - Initializing InOutFiles

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

# v2 CiaImp Header
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
hdrOutput[10] = 'About'


"""
inFileName = input("FileName of Input file containing the SCSV data with two Abouts:? ")
inFilePath = Mgv.filesDir + "/" + inFileName
inFile = inFilePath + '.txt'

outFileName = input("FileName of Outputfile where you want to store SCSV data with one merged About? ")
outFilePath = Mgv.filesDir + "/" + outFileName
outFile = outFilePath + '.txt'

logFileName = input("FileName of Log file where you want to store scanning process? ")
logFilePath = Mgv.filesDir + "/" + logFileName
logFile = logFilePath + '.txt'
hdrLog = ['Records', 'LastCia']
logRecord = [None] * 2

gptFileName = input("FileName of Input file where you store GPT results of merging two Abouts? ")
gptFilePath = Mgv.filesDir + "/" + gptFileName
gptFile = gptFilePath + '.txt'


# Let's check if User wants to start from scratch or resume Operations
resumeFlag = 'False'  # by default
ciaFound = 'False'  # by default
logFlag = 'False'
dataFlag = 'False'
userResp = Musr.USR_StartResume()
if userResp == 'R' or userResp == 'r':
    resumeFlag = 'True'
    logFlag, fi_log = Mfil.openFile_Reader(logFile)
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
        logList, logList_len = Mnlp.items_separator_converter(logLine, ';')
        recordCount = recordCount + int(logList[0])
        lastCiaName = logList[1]
        print(f"\n===Start/Resume=> LogFile <{logFileName}> indicates: <{lastCiaName}> as last Cia processed")
        # we need now to set inputfile to the next Cia position
        inFlag, fi = Mfil.openFile_Reader(inFile)
        inHeader = fi.readline()
        if inFlag == 'False':
            print(
                f"\n===Start/Resume=> LogFile <{inFileName}> Status: {inFlag} => Impossible to Resume - Key Data missing")
        else:
            dataFlag = 'True'
            while inputLine := fi.readline():
                # print(f"\n===Start/Resume=> Current Cia Input Line:\n{inputLine} ")
                inputList, inputList_len = Mnlp.items_separator_converter(inputLine, ';')
                currentCiaName = inputList[1]
                # print(f"\n===Start/Resume=> Current Cia Name: <{currentCiaName}> ")
                if currentCiaName == lastCiaName:  # we finished scanning
                    ciaFound = 'True'
                    break

# we need now to finish initialization accordingly
if resumeFlag == 'True':
    if dataFlag == 'True' and ciaFound == 'True':
        outFlag, fo = Mfil.openFile_Writer(outFile)
        fi_log.close()
        logFlag, fo_log = Mfil.openFile_Writer(logFile)
    else:
        print(f"===Start/Resume=> dataFlag: {dataFlag} or ciaFound: {ciaFound} => Impossible to Resume")

else:  # we are starting from Scratch
    inFlag, fi = Mfil.openFile_Reader(inFile)
    inHeader = fi.readline()
    print(f"\n===V1-DataBuilderUpgraded=> Initialization inputFile Header: \n{inHeader}")
    outFlag, fo = Mfil.openFile_Writer(outFile)
    hdr_len = len(Mhdr.hdrV1ImpCia)
    hdrLine = ''
    for indx in range(hdr_len):
        hdrLine = hdrLine + Mhdr.hdrV1ImpCia[indx] + ';'
    hdrLine = hdrLine + 'aboutBRD' + '\r\n'  # no <;> on the last columns
    print(f"\n===V1-DataBuilderUpgraded=> Initialization OutputFile Header: \n{hdrLine}")
    fo.write(hdrLine)
    wout_log, fo_log = Mfil.initializeLogFile(logFile, hdrLog)

gptFileName = 'GPT_MergedText'
gptFilePath = Mgv.filesDir + "/" + gptFileName
gptFile = gptFilePath + '.txt'

print(f"\n===MergingAbouts=> <Initializing InOutFiles> exec@: {date_stamp()}")


### ROB-CIA_N4J_CSV_About-CNPJ_V1-DataBuilderUpgraded=> ENGINE - Looping on input file records building N4J CCSV file >


userContinue = 'True'
recordCount = 0
ciaNameListProcessed = []
# pauseTimer = 20
# pauseTimer = 10
pauseTimer = 7


class MergingAbouts:
    pass


while inputLine := fi.readline():
    if userContinue == 'False':
        break
    recordCount += 1
    # print(f"\n===V1-DataBuilderUpgraded=> Current cycle Record# {recordCount} is: \n{inputLine}")

    inputList, inputList_len = Mnlp.items_separator_converter(inputLine, ';')
    outputList = V0_HeaderConverter(inputList) # there is no conversion both files are v0.5 impCiaHeader

    ciaCNPJ = outputList[0]
    ciaName = outputList[1]
    ciaSubIndustry = outputList[2]
    ciaIndustry = outputList[3]
    ciaSector = outputList[4]
    ciaAboutGPT = inputList[10]
    ciaAboutBRD = inputList[11]
    ciaNameListProcessed.append(ciaName)
    print('\n')
    print('x' * 120)
    print(f"===MergingAbouts=> Processing: Record# {recordCount} Cia: <{ciaName}> Industry: <{ciaIndustry}>")
    print('x' * 120)
    if ciaAboutGPT != '#X#':
        gptAbout = Mgpt.GPT_cleanAbout(ciaAboutGPT)
        ciaAbout = '<CHAT-GPT>$$$:' + gptAbout
    if ciaAboutBRD != '#X#':
        brdAbout = Mbrd.BRD_cleanReplyAbout(ciaAboutBRD)
        ciaAbout = '<BARD>$$$:' + brdAbout
        # print(f"\n===MergingAbouts=> Combined About: \n {ciaAbout}")
# we need know to ask USR for confirmation if there are two About
    if userContinue == 'True':
        if ciaAboutGPT != '#X#' and ciaAboutBRD != '#X#':
            userResponse = USR_checkGPT_aboutMerge(ciaName, ciaAboutGPT,ciaAboutBRD)
            if userResponse == 'F' or userResponse == 'f':
                gptFlag,gptMerged = GPT_readFile_cleanAbout(gptFile)
                if gptFlag == 'True':
                    ciaAbout = gptMerged
                else:
                    ciaAbout = ciaAbout # no change
            elif userResponse == 'I' or userResponse == 'i': # User does not want to change anything
                print(f"\n===MergingAbouts=> User rejected mergedAbout -ciaAbout = #X# ")
                ciaAbout = ciaAbout # unchanged
            elif userResponse == 'S' or userResponse == 's': # user wants to stop the the process and resume later
                userContinue = 'False'
            else: # USR response not recognized we will make no changes to ciaAbout
                ciaAbout = ciaAbout # unchanged
        if userContinue == 'True':
            # we are going now to write record @ output file
            outputList[10] = ciaAbout
            outputLine = writeCia_V1Record(fo, outputList)
            # print(f"\n===MergingAbouts=> Company <{ciaName}> We have the following merged About: {outputList[10]} ")
        else:
            # we will abandon the current Cia because user asked for Stop}
            print(f"\n===MergingAbouts=> current Cia {ciaName} About processing abandoned USR asked for Stop")
            break

# we finished looping we are going now to save the processing log
if recordCount > 1:
    lastCiaName = ciaNameListProcessed[-2]
    print(f"\n===MergingAbouts=> Cias Processed {ciaNameListProcessed}\nLast = <{lastCiaName}>")
    logLine = ''
    logline = logLine + str(recordCount) + ';' + lastCiaName + '\r\n'
    fo_log.write(logline)
    print(f"\n===MergingAbouts=> Processed {recordCount} records with Last record CiaName: <{lastCiaName}>")
    # print(f"\n===MergingAbouts=> BREAKPOINT DUMMY INSTRUCTION ")
else:
    print(f"\n===MergingAbouts=> Processed {recordCount} => No processing - No Log")

# we need to close open files
fi.close()
fo.close()
fo_log.close()

print(f"\n===MergingAbouts=> <ENGINE> exec@: {date_stamp()}")

# In[ ]:

"""
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

"""



