#!/usr/bin/env python
# coding: utf-8
# from IPython import get_ipython


### ROB-SET_GPT-BRD_MergeAbouts BEGINS HERE
# This routine Merges AboutGPT with about Bard in order to create one single about
# It works with the latest file N4J-CIA_SCSV_AboutIndustryRecords
# which has 12 column format (two Abouts),: namely:
# CiaCNPJ;cia_name;SubIndustryCode;IndustryCode;SectorCode;Region;Fitch;SP;Moody;Group;
# about;aboutBRD
# This routine version v.1 just concatenate the two abouts if they are meaningful, discarding platitudes.
# For that it will use cleaning filters: (1) brd_filter_platitudes(about) and (2) gpt_clean_about(reply)
# with learned lists of Inoperative Set and Platitudes List )
# => When chatGPT and Bard APIs will work again, they will be sollicited to produce a best merge
#//


# import Modules.ModHead
from Modules.ModHead import *

import textwrap

print(f"\n===PRG-CIA_N4J_BRD_UI_SCSV_IndustryCode=> <BEGINS HERE>")

### BARD API Setup
import Modules.modfin_brd as Mbrd

from bardapi import Bard
# myToken = 'awh5YWTO8IrYw-mmk3qAFGi6T6X_XUo27w4b44wNu_T3gCzDOXyqzOdtBksLWj5O4mQu1A.' # valid untill 2025??
# myToken = "bAh5YZa9CV1fancVHQZX6ayt-aX5S5FiLnE4XsKsR4Qt-uNq1z-CKeBfP0zykLxvbzhKeQ." # till 19/09/2025??
myToken = Mbrd.BRD_KeyAPI
bard = Bard(token = myToken)
#
response = bard.get_answer("Tell me about this Brazilian Company: 'Desktop Sigmanet Comunicação Multimidia'")
print(response)

print(f"\n===BRD API=> <Setup> exec@: {date_stamp()}")



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
# nn USR_check_boutMerge(company,about): return userResp => request USR - to check cleaned Text of the about

# nn => request USR - to check Bard merge (cleaned Text) of the Abouts for company SubIndustry
def BRD_aboutMerge(company, about_BRD,about_GPT):
    query_BRD = 'Topic = Merge Text -  I JUST NEED THE MERGED TEXT - Below you will find to texts (About1 and About2)'\
            'containing descriptions about Brazilian company: ' + company + ' Can you merge About1 & About2 into'\
            ' a single non redundant about without missing any key point and without explicitly referencing'\
            'the original texts (About1 and About2) - \n'\
            'I JUST NEED THE MERGED TEXT - DO NOT INCLUDE CHANGES MADE - AVOID BOILER PLATES sentences '
    about1 = 'About1 = ' + '\'' +  about_BRD + '\''
    about2 = 'About2 = ' + '\''+  about_GPT +'\''
    brd_platitude0 = 'Sure, here is the merged text about ' + company + ':'
    brd_platitude1 = 'I can do that. Here is the merged text about ' + company + ':'
    brd_platitude2 = 'I have merged the two texts without explicitly referencing the original text, and I have removed'\
                     'any redundant information.'
    brd_platitude3 = 'I have merged the two texts by removing the redundant information'\
                     'and combining the sentences to create a smooth and concise text.'
    brd_platitude4 = 'I have also avoided explicitly referencing the original texts (About1 and About2) in order'\
                     'to make the text more readable.'
    brd_platitude5 = 'I hope this is what you are looking for.'
    brd_platitude6 = 'I hope this is helpful!'
    prompt_BRD = '\n' + query_BRD + '\n' +'\n' + about1 +  '\n' +'\n' + about2 +'\n'
    mergedAbout_dict = bard.get_answer(prompt_BRD)
    mergedAbout_rough = mergedAbout_dict['content']
    print(f"===BRD_aboutMerge=> Crude content: {mergedAbout_rough}")
    mergedAbout_clean = mergedAbout_rough.replace(brd_platitude0,'')
    mergedAbout_clean = mergedAbout_clean.replace(brd_platitude1, '')
    mergedAbout_clean = mergedAbout_clean.replace(brd_platitude2, '')
    mergedAbout_clean = mergedAbout_clean.replace(brd_platitude3, '')
    mergedAbout_clean = mergedAbout_clean.replace(brd_platitude4, '')
    mergedAbout_clean = mergedAbout_clean.replace(brd_platitude5, '')
    mergedAbout_clean = mergedAbout_clean.replace(brd_platitude6, '')
    mergedAbout_clean = Mbrd.brd_clean_reply_about(mergedAbout_clean)
    print('\n\n')
    print('-' * 80)
    print(textwrap.fill(mergedAbout_clean,80))
    print('-' * 80)

    prompt_UI = 'For Company: <' + company + '> BRD manually merged Abouts you want to: \n'\
                                          '[A]ccept new merged text? ; [I]gnore or [S]top processing: \n?'
    # print(prompt)
    user_Resp = input(prompt_UI)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {userResp}" )
    return user_Resp, mergedAbout_clean


print(f"\n===MergingAbouts=> <Modulable Routines> exec@: {date_stamp()}")

### PRG-CIA_N4J_BRD_UI_SCSV_IndustryCode - Initializing InOutFiles

"""
# v0 CiaImp header
hdrInput[0] = 'CiaCode'
hdrInput[1] = 'CiaCNPJ'    
hdrInput[2] = 'cia_name'
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
hdrInput[13] = 'about'

# v1 CiaImp header
hdrOutput[0] = 'CiaCNPJ'    
hdrOutput[1] = 'cia_name'
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

# v2 CiaImp header
hdrOutput[0] = 'CiaCNPJ'    
hdrOutput[1] = 'cia_name'
hdrOutput[2] = 'SubIndustryCode'
hdrOutput[3] = 'IndustryCode'
hdrOutput[4] = 'SectorCode'
hdrOutput[5] = 'Region'
hdrOutput[6] = 'Fitch'
hdrOutput[7] = 'SP'
hdrOutput[8] = 'Moody'
hdrOutput[9] = 'Group' 
hdrOutput[10] = 'about'


"""

files_names_FileName = 'FilesNames_MergedAbouts'
files_names_FilePath = Mgv.FILES_DIR + "/" + files_names_FileName
files_names = files_names_FilePath + '.txt'
files_names_Flag, files_names_fi = Mfil.open_file_reader(files_names)

inFileName = files_names_fi.readline()
inFileName = inFileName.replace('\r\n','')
inFilePath = Mgv.FILES_DIR + "/" + inFileName
inFile = inFilePath + '.txt'

outFileName = files_names_fi.readline()
outFileName = outFileName.replace('\r\n','')
outFilePath = Mgv.FILES_DIR + "/" + outFileName
outFile = outFilePath + '.txt'

logFileName = files_names_fi.readline()
logFileName = logFileName.replace('\r\n','')
logFilePath = Mgv.FILES_DIR + "/" + logFileName
logFile = logFilePath + '.txt'

files_names_fi.close()

hdrLog = ['Records', 'LastCia']
logRecord = [None] * 2

# Let's check if User wants to start from scratch or resume Operations
resumeFlag = 'False'  # by default
ciaFound = 'False'  # by default
logFlag = 'False'
dataFlag = 'False'
userResp = Musr.usr_start_resume()
if userResp == 'R' or userResp == 'r':
    resumeFlag = 'True'
    logFlag, fi_log = Mfil.open_file_reader(logFile)
    if logFlag == 'False':
        print(f"\n===Start/Resume=> LogFile <{logFileName}> Status: {logFlag} => Not Possible to Resume")
    else:
        # we are going to loop on Log file to read the last record to find the last Cia processed
        recordCount = 0
        foundCount = 0
        logHeaderLine = fi_log.readline()
        while line := fi_log.readline():
            # print(f"\n===Start/Resume=> LogFile Current Line: {one_line})
            logLine = line
        # print(f"\n===Start/Resume=> LogFileLast Line: {one_line})
        logList, logList_len = Mnlp.items_separator_converter(logLine, ';')
        recordCount = recordCount + int(logList[0])
        lastCiaName = logList[1]
        print(f"\n===Start/Resume=> LogFile <{logFileName}> indicates: <{lastCiaName}> as last Cia processed")
        # we need now to set inputfile to the next Cia position
        inFlag, fi = Mfil.open_file_reader(inFile)
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
                # print(f"\n===Start/Resume=> Current Cia name: <{currentCiaName}> ")
                if currentCiaName == lastCiaName:  # we finished scanning
                    ciaFound = 'True'
                    break

# we need now to finish initialization accordingly
if resumeFlag == 'True':
    if dataFlag == 'True' and ciaFound == 'True':
        outFlag, fo = Mfil.open_file_writer(outFile)
        fi_log.close()
        logFlag, fo_log = Mfil.open_file_writer(logFile)
    else:
        print(f"===Start/Resume=> dataFlag: {dataFlag} or ciaFound: {ciaFound} => Impossible to Resume")

else:  # we are starting from Scratch
    inFlag, fi = Mfil.open_file_reader(inFile)
    inHeader = fi.readline()
    print(f"\n===V1-DataBuilderUpgraded=> Initialization inputFile header: \n{inHeader}")
    outFlag, fo = Mfil.open_file_writer(outFile)
    hdr_len = len(Mhdr.hdrV1ImpCia)
    hdrLine = ''
    for indx in range(hdr_len):
        hdrLine = hdrLine + Mhdr.hdrV1ImpCia[indx] + ';'
    hdrLine = hdrLine + 'aboutBRD' + '\r\n'  # no <;> on the last columns
    print(f"\n===V1-DataBuilderUpgraded=> Initialization OutputFile header: \n{hdrLine}")
    fo.write(hdrLine)
    wout_log, fo_log = Mfil.initialize_log_file(logFile, hdrLog)

gptFileName = 'GPT_MergedText'
gptFilePath = Mgv.FILES_DIR + "/" + gptFileName
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
        gptAbout = Mgpt.gpt_clean_about(ciaAboutGPT)
        # ciaAbout = '<CHAT-GPT>$$$:' + gptAbout
    if ciaAboutBRD != '#X#':
        brdAbout = Mbrd.brd_clean_reply_about(ciaAboutBRD)
        # ciaAbout = '<BARD>$$$:' + brdAbout
        # print(f"\n===MergingAbouts=> Combined about: \n {ciaAbout}")
# we need know to ask USR for confirmation if there are two about
    if userContinue == 'True':
        if ciaAboutGPT != '#X#' and ciaAboutBRD != '#X#':
            userResponse, mergedAbout = BRD_aboutMerge(ciaName, ciaAboutGPT,ciaAboutBRD)
            if userResponse == 'A' or userResponse == 'a':
                ciaAbout = mergedAbout
            elif userResponse == 'I' or userResponse == 'i': # User does not want to change anything
                print(f"\n===MergingAbouts=> User rejected mergedAbout -ciaAbout = #X# ")
                ciaAbout = ciaAbout # unchanged
            elif userResponse == 'S' or userResponse == 's': # user wants to stop the the process and resume later
                userContinue = 'False'
            else: # USR response not recognized we will make no changes to ciaAbout
                ciaAbout = ciaAbout # unchanged

        # we need to deal with the case were just one chatGPT or BARD about field is filled and take it
        # !!! Not tested !!!
        else:
            if ciaAboutGPT != '#X#':
                ciaAbout = ciaAboutGPT
            else:
                ciaAbout = ciaAboutBRD
        if userContinue == 'True':
            # we are going now to write record @ output file
            outputList[10] = ciaAbout
            outputLine = writeCia_V1Record(fo, outputList)
            # print(f"\n===MergingAbouts=> Company <{cia_name}> We have the following merged about: {outputList[10]} ")
        else:
            # we will abandon the current Cia because user asked for Stop}
            print(f"\n===MergingAbouts=> current Cia {ciaName} about processing abandoned USR asked for Stop")
            break

# we finished looping we are going now to save the processing log
if recordCount > 1:
    lastCiaName = ciaNameListProcessed[-2]
    print(f"\n===MergingAbouts=> Cias Processed {ciaNameListProcessed}\nLast = <{lastCiaName}>")
    logLine = ''
    logline = logLine + str(recordCount) + ';' + lastCiaName + '\r\n'
    fo_log.write(logline)
    print(f"\n===MergingAbouts=> Processed {recordCount} records with Last record cia_name: <{lastCiaName}>")
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
    print(f"\n===V1-DataBuilderUpgraded=> Processed {recordCount} records with Last record cia_name: <{lastCiaName}>")
else:
    print(f"\n===V1-DataBuilderUpgraded=> Processed {recordCount} => No processing - No Log")

fi.close()
fo.close()
fo_log.close()

print(f"\n===V1-DataBuilderUpgraded=> <ENGINE> exec@: {date_stamp()}")

"""



