#!/usr/bin/env python
# coding: utf-8
# from IPython import get_ipython


# ## ROB-CIA_BRD_SCSV_REPAIR_MissingAbout BEGINS HERE
# This routine repairs records with no about by requesting BRD to provide the content
# The file to be repaired is the latest version of generated file created by MergingAbouts (MANUAL or AUTO)
# ##

# !! Pending Bugs
# 1 LogHeader is flawed - comma separated characters and not words hdrLog must be a entry_list -CORRECTED
# 2 Not sure EOF processing is correct - test if inputLine after the while is not empty - ToDo
# 3 ciaNameListProcessed wrong - Check the append accumulation - Repaired - CORRECTED - check imediate Stop

# import Modules.ModHead
from Modules.ModHead import *
import textwrap
import time

# ## BARD API Setup
import Modules.modfin_brd as Mbrd

# from bardapi import Bard
# myToken = 'awh5YWTO8IrYw-mmk3qAFGi6T6X_XUo27w4b44wNu_T3gCzDOXyqzOdtBksLWj5O4mQu1A.' # valid untill 2025??
# myToken = "bAh5YZa9CV1fancVHQZX6ayt-aX5S5FiLnE4XsKsR4Qt-uNq1z-CKeBfP0zykLxvbzhKeQ." # till 19/09/2025??
ad_token = Mbrd.BRD_KeyAPI
ad_bard = Mbrd.BRD_bard

response = ad_bard.get_answer("Hello Bard - ready to work?'")
print(response)

print(f"\n===ROB-CIA_BRD_SCSV_REPAIR_MissingAbout=> <BEGINS HERE>")



# ## ROB-CIA_BRD_SCSV_REPAIR_MissingAbout - Specific Routines

def write_cia_v1record(out_file, out_list):
    line_record = ''
    for indx in range(len(out_list)):
        line_record = line_record + out_list[indx] + ';'  # the last ; will be removed
    # print(f"===write_cia_v1record> After loop Before corrections; rough line_record:\n{line_record} ")
    line_record = line_record[:-1] + '\r\n'
    # print(f"===write_cia_v1record> After loop - Corrections cleaned line_record:\n{line_record} ")
    out_file.write(line_record)

    return line_record

def readFile_cleanAbout(f):
    flag, about_file = Mfil.open_file_reader(f)
    if flag == 'False':
        print(f"\n===readFile_cleanAbout=> File <{f}> Status: {flag} => Impossible to Read - File does not exist")
    about = about_file.read()
    about = about.replace('\r\n', '')
    about = about.replace("\'", '^')
    about = about.replace("\\", '')
    return flag, about

def askUser_fillAbout(company, file):
    prompt = 'Company: <' + company + '>  does not have an about can you provide manually in' + file + '?:\n ' \
             + '[A]dd? ; [I}gnore or [S]top processing?'
    user_response = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {user_response}" )
    flag = 'False'
    text = '#X#'
    if user_response == 'A' or user_response == 'a':
        flag, text = readFile_cleanAbout(aboutFile)
    elif user_response == 'I' or user_response == 'i':  # User does not want to change anything
        print(f"\n===askUser_fillAbout=> User rejected filling about for {company} ")

    elif user_response == 'S' or user_response == 's':  # user wants to stop the process and resume later
        print(f"\n===askUser_fillAbout=> User asked to stop processing while in company: {company} ")
    else:  # USR response not recognized we will make no changes to ciaAbout
        print(f"\n===askUser_fillAbout=> User entry Invalid while on company: {company} ")
    return flag, text, user_response



# ## ROB-CIA_BRD_SCSV_REPAIR_MissingAbout - Modulable Routines
# nn USR_check_boutMerge(company,about): return userResp => request USR - to check cleaned Text of the about
"""
def BRD_aboutQuery(company):
    query_BRD = 'Topic = about Brazilian Company-  I JUST NEED THE ABOUT TEXT'\
            '- Refrain from explaining what or how you did it - Just the generated about'\
            'What can you tell me ABOUT this Brazilian company: ' + company + ' ?'
    brd_platitude0 = 'I hope this is what you are looking for.'
    brd_platitude1 = 'I hope this is helpful!'
    prompt_BRD = '\n' + query_BRD + '\n'
    ciaAbout_dict = ad_bard.get_answer(prompt_BRD)
    ciaAbout_rough = ciaAbout_dict['content']
    # print(f"===BRD_aboutQuery=> Company: <{company}> Crude about content:\n")
    # print(textwrap.fill(ciaAbout_rough, 80))
    ciaAbout_clean = Mbrd.BRD_cleanReplyAbout(ciaAbout_rough)
    print('\n\n')
    print('-' * 80)
    print(f"===BRD_aboutQuery=> Company: <{company}> Crude about content:\n")
    print(textwrap.fill(ciaAbout_clean,80))
    print('-' * 80)

    prompt_UI = 'For Company: <' + company + '> BRD produced the about shown above: \n'\
                                          '[A]ccept as is? ; [F]ile text in CIA_AboutEdited file? or  [I]gnore: \n=>'
    # print(prompt)
    user_Resp = input(prompt_UI)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {userResp}" )
    return user_Resp, ciaAbout_clean
"""

print(f"\n===ROB-CIA_BRD_SCSV_REPAIR_MissingAbout=> <Specific Routines> exec@: {date_stamp()}")


# ## ROB-CIA_BRD_SCSV_REPAIR_MissingAbout - Initializing InOutFiles

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

files_names_FileName = 'FilesNames_BRD-GetAbout'
files_names_FilePath = Mgv.FILES_DIR + "/" + files_names_FileName
files_names = files_names_FilePath + '.txt'
files_names_Flag, files_names_fi = Mfil.open_file_reader(files_names)

inFileName = files_names_fi.readline()
inFileName = inFileName.replace('\r\n', '')
inFilePath = Mgv.FILES_DIR + "/" + inFileName
inFile = inFilePath + '.txt'




outFileName = files_names_fi.readline()
outFileName = outFileName.replace('\r\n', '')
outFilePath = Mgv.FILES_DIR + "/" + outFileName
outFile = outFilePath + '.txt'

logFileName = files_names_fi.readline()
logFileName = logFileName.replace('\r\n', '')
logFilePath = Mgv.FILES_DIR + "/" + logFileName
logFile = logFilePath + '.txt'

aboutFileName = files_names_fi.readline()
aboutFileName = aboutFileName.replace('\r\n', '')
aboutFilePath = Mgv.FILES_DIR + "/" + aboutFileName
aboutFile = aboutFilePath + '.txt'

files_names_fi.close()


inFlag, fi = Mfil.open_file_reader(inFile)

if inFlag == 'True':
    inHeader = fi.readline()
    print(f"\n===ROB-CIA_BRD_SCSV_REPAIR_MissingAbout=>  {inFileName}: \n{inHeader}")
else:
    print(f"\n===ROB-CIA_BRD_SCSV_REPAIR_MissingAbout=> File to repair: {inFileName} could not be opened - Fatal Error")
    exit(10)

outFlag, fo = Mfil.open_file_writer(outFile)
fo.write(inHeader)  # The output file same header than file to be repaired


hdrLog = ['Records','LastCia']
wout_log, fo_log = Mfil.initialize_log_file(logFile, hdrLog)


print(f"\n===ROB-CIA_BRD_SCSV_REPAIR_MissingAbout=> <InOutFiles Initialized> exec@: {date_stamp()}")


# ## ROB-CIA_BRD_SCSV_REPAIR_MissingAbout=> ENGINE - Parsing file to be repaired (in_)>




class RepairMissingAbout:
    pass

recordCount = 0
cia_updated_count = 0
ciaNameListProcessed = []
pauseTimer = 30

while inputLine := fi.readline():
    recordCount += 1
    inputList, inputList_len = Mnlp.items_separator_converter(inputLine, ';')
    outputList = inputList  # both files have the same header; only the about field is concerned
    ciaCNPJ = outputList[0]
    ciaName = outputList[1]
    ciaIndustry = outputList[3]
    ciaAbout = outputList[10]
    
    # We are going now to check if in the current record the about field is empty (='#X#')
    if ciaAbout == '#X#':  # is empty then we will request BARD
        print('\n')
        print('x' * 120)
        print(f"===ROB-REPAIR_MissingAbout=> Record# {recordCount} Cia: <{ciaName}> Industry: <{ciaIndustry}>")
        print('x' * 120)
        time.sleep(pauseTimer)
        brdFlag, brd_ciaAbout = Mbrd.brd_cia_about(ciaName)
        if brdFlag == 'False':
            print(f"\n====ROB-REPAIR_MissingAbout=> For Company <{ciaName}> BRD API Not OK,ciaAbout:\n{ciaAbout} ")
            about_flag, about_text, user_reply = askUser_fillAbout(ciaName, aboutFile)
            if user_reply == 'A' or user_reply == 'a':
                if about_flag == 'True':
                    ciaAbout = about_text
                    ciaNameListProcessed.append(ciaName)
                    cia_updated_count += 1
                    print(textwrap.fill(ciaAbout, 80))
                else:
                    ciaAbout = '#X#'
            elif user_reply == 'I' or user_reply == 'i':
                ciaAbout = '#X#'
            elif user_reply == 'S' or user_reply == 's':
                break
        else:
            ciaAbout = brd_ciaAbout
            ciaNameListProcessed.append(ciaName)
            cia_updated_count += 1
            print(f"===ROB-REPAIR_MissingAbout=> 'BRD provided via API the following about for <{ciaName}>:\n")

            print(textwrap.fill(ciaAbout, 80))

    else:
        ciaAbout = ciaAbout  # it's a do nothing

    # we are going now to write record @ output file
    outputList[10] = ciaAbout  # final set
    outputLine = write_cia_v1record(fo, outputList)


# we finished looping we are going now to save the processing log
if cia_updated_count >= 1:
    lastCiaName = ciaNameListProcessed[-1]
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

print(f"\n===ROB-Repair-MergingAbouts=> <ENGINE> exec@: {date_stamp()}")
