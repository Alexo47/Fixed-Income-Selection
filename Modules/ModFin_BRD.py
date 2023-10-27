#!/usr/bin/env python
# coding: utf-8


# == Module-FixIncome - BRD related Routines 20230803 -v1
# 01 BRD_KeyAPI => BRD API key extracted form cookies
# 02a BRD_InoperativeList => BRD meaningless About responses
# 02b BRD_InoperativeList_len => len(BRD_InoperativeList)
# 03a BRD_InoperativeSet =>
# 03b BRD_InoperativeSet_len =>
# 04a BRD_PlatitudesList => BRD Platitudes About responses:
# 04b BRD_PlatitudesList_len => len(BRD_PlatitudesList)
# 05 def BRD_CiaAbout(ciaName): return troubleFlag,ciaAbout => Prompts BRD for an About of a company
# 06 def BRD_cleanReplyAbout(reply): return cleanReply => Removes special characters + BRD Noise
# 07 def BRD_CiaCNPJ(ciaName): return troubleFlag,cnpjFlag,ciaCNPJ => Prompts BRD for CNPJ of a company
# 08 def findMarkerCNPJ(cleanResponse,marker): return cnpjFlag,ciaCNPJ => finds cnpj string in BARDs response
# 09 def checkCNPJFormat(cnpj): return okFlag => checks if matches dd.ddd.ddd/dddd-dd  (20.223.016/0001-70)
# 10 def BRD_checkTrafficTrouble(reply): return troubleFlag => Checks if BRD is operational (network accessible)
# 11  def BRD_checkAbooutPertinence(about):return okFlag => check if BRD reply is non operative
# 12  def BRD_FilterPlatitudes(about): return about => remove BRD boilerplate platitudes
# 13  def BRD_getIndustry(ciaName): return troubleFlag,response => requests BRD API for the industry code of a company
# 14  def BRD_getIndustryRegenerateSector(ciaName,sectorCode):return troubleFlag,response=> SubIndformat <.IBD.15104030>
# ==

from bardapi import Bard
import re

# 01 => BRD API key extracted form cookies
# BRD_KeyAPI = 'ZAh5YWaPE7QLc9Ymhbp8dxbv1QjnQKEeWs5RchFY4qMuiF3iWaJLyDIWUQzfRINEXghK0g.'
# BRD_KeyAPI = 'awh5YWTO8IrYw-mmk3qAFGi6T6X_XUo27w4b44wNu_T3gCzDOXyqzOdtBksLWj5O4mQu1A.'
BRD_KeyAPI = 'bAh5YZa9CV1fancVHQZX6ayt-aX5S5FiLnE4XsKsR4Qt-uNq1z-CKeBfP0zykLxvbzhKeQ.'
BRD_bard = Bard(token=BRD_KeyAPI)

# 02 => BRD meaningless About responses:
BRD_InoperativeList = ['It could be a small, local company that has not gained much visibility,'
                       'or it could be a fictitious company.',
                       'it would be appreciated if you could provide additional information about the company you'
                       'are talking about''However, upon conducting some research, I could not find any information'
                       'about a Brazilian company named',
                       'is a lesser known company or a new company that has not yet'
                       'established a significant online presence.',
                       'Can you provide me with more information or '
                       'context about the company you are referring to in order to'
                       'I don^t have access to the latest information or knowledge about Brazilian companies.',
                       'current information, but as of my training data I can give you some information about',
                       'verify the credibility of a company before investing or sharing personal information.',
                       'context or specific information about the company or the question you have in mind?',
                       'current or updated information beyond what is publicly available on the internet.',
                       'current information about companies in Brazil, and there is no information about',
                       'I do not have the ability to browse the internet to find the current information'
                       'Furthermore, there are no results found on the internet about a company called',
                       'some general information about the Brazilian agriculture and livestock sector.',
                       'I don^t have access to the latest information - please note that the data',
                       'this company may not exist, or it may have a different name or spelling.',
                       'as it does not seem to be a legitimate financial institution in Brazil.',
                       'I was not able to find any information on a Brazilian company called',
                       'there is no information available about a Brazilian company called',
                       'real-time database and updates about all Brazilian companies.',
                       'Below is the available information on this Brazilian company',
                       'Please provide accurate details for me to assist you better.',
                       'I don^t have access to real-time information and databases.',
                       'the current information and updates related to the company',
                       'Without more information, this is as much as I can provide.',
                       'the latest news and information about specific companies.',
                       'is no longer in operation or is a small, local business.',
                       'it is a small or local financial institution in Brazil.',
                       'However, here is the information we could find online.',
                       'I am not privy to the latest updates or news regarding',
                       'you with some general information on the company.',
                       'provided below may be out-of-date or inaccurate.',
                       'any information about a Brazilian company named',
                       'as it does not seem to be a well-known company.',
                       'browse the internet and access information that current information, but here is what I found',
                       'If you have any more information or details,',
                       'I don^t have access to current information.',
                       'real-time information on certain companies.',
                       'to aid me in providing an accurate answer.',
                       'and I would be happy to help you further.',
                       'the latest information or current events.',
                       'I^m sorry, but as an AI language model, ',
                       'Unfortunately, as an AI language model,',
                       'you with some general information about',
                       'but I cannot provide information about',
                       'I cannot provide information regarding',
                       'There may be several reasons for this.',
                       'However, here is a brief overview of',
                       'However, to the best of my knowledge,',
                       'up-to-date information on companies.',
                       'Can I help you with anything else?',
                       'I could not find a company named',
                       'you some basic information about',
                       'It^s possible that this company',
                       'Sorry, as an AI language model,',
                       'However, based on my research,',
                       'about this Brazilian company,',
                       'Can you please provide more ',
                       'I have no information about',
                       'is not publicly available.',
                       'It is highly possible that',
                       'as an AI language model, ',
                       'As an AI language model,',
                       'I do not have access to ',
                       'However, I can provide ',
                       'I don^t have access to ',
                       'on the current state of',
                       'real-time information.',
                       'the latest information',
                       'details or context?',
                       'It is possible that',
                       'please let me know ',
                       'assist you better?',
                       'It is important to',
                       'I couldn^t find',
                       'I^m sorry, but',
                       'I am sorry, ']
BRD_InoperativeList_len = len(BRD_InoperativeList)


# 03 => Brad inoperative sentences grouped in a python set structure
BRD_InoperativeSet = set()
for indx in range(BRD_InoperativeList_len):
    BRD_InoperativeSet.add(BRD_InoperativeList[indx])
BRD_InoperativeSet_len = len(BRD_InoperativeSet)
# print(f"\n===BRD API=> Inoperative Set has <{BRD_InoperativeSet_len}> entries:\n {BRD_InoperativeSet}")

# 04 => BRD Platitudes About responses:
BRD_PlatitudesList = ["Claro!",
                      "Claro,  aqui está alguma informação sobre a ",
                      "Claro.", "Claro. Aqui está alguma informação sobre a ",
                      "Claro. Aqui está algumas informações sobre a ",
                      "Claro., ''",
                      "Do you have any other questions for me?",
                      "Do you have any other questions for me?, ''",
                      "Do you have other questions?",
                      "Do you have other questions?, ''",
                      "here is some information about ",
                      "Here is some information about ",
                      'Here are some additional details about',
                      "Here^s what I found about",
                      'Here is the merged text:',
                      "I am still under development and learning to follow instructions carefully.",
                      "I apologize for any inconvenience this may cause., ''",
                      "I apologize for providing additional information in my previous response. ",
                      "I don^t have any information about that company. ",
                      "I hope this helps!", "I hope this information is helpful. ",
                      "I will not provide any additional information about the company.",
                      "Is there anything else I can help you with?",
                      "Let me know if you have any other questions.",
                      "Please let me know if you have any other questions.",
                      "Sure! ", "Sure! Here is some information about ",
                      "Sure,  I understand.", "Sure, ",
                      "Sure."'I can merge the two texts into a single non-redundantAbout',
                      'without missing any key points',
                      'without explicitly referencing the original text.']
BRD_PlatitudesList_len = len(BRD_PlatitudesList)

# 05 => Prompts BRD for an About of a company
def BRD_CiaAbout(ciaName):
    response = ''
    query = "Tell me About this Brazilian company:" + ciaName + "? "
    response = BRD_bard.get_answer(query)['content']
    # print(f"===BRD_CiaAbout=> BRD Response to company {ciaName} is:\n{response}")
    troubleFlag = BRD_checkTrafficTrouble(response)
    ciaAbout = BRD_cleanReplyAbout(response)
    return troubleFlag,ciaAbout

# 06 => Removes special characters + BRD Noise
def BRD_cleanReplyAbout(reply):
    cleanReply = reply.replace('\r\n','')
    cleanReply = cleanReply.replace('\n\n','')
    cleanReply = cleanReply.replace('\r\n','')
    cleanReply = cleanReply.replace('\n','')
    cleanReply = cleanReply.replace('\r','')
    cleanReply = cleanReply.replace("\'",'^')
    cleanReply = cleanReply.replace(";",'&')

    # remove boiler plate statements
    for platitude in BRD_PlatitudesList:
        cleanReply = cleanReply.replace(platitude,'')
    cleanReply = cleanReply.strip()    
    return cleanReply


# 07 => Prompts BRD for CNPJ of a company
def BRD_CiaCNPJ(ciaName):
    twoStars ='**'
    response = ''
    query = "Please do not provide any additional company information than the CNPJ number bracketed with \'**\':\n"     "What is the CNPJ number for this Brazilian company:"  + ciaName + "?"
    response = BRD_bard.get_answer(query)['content']
    print(f"\n===BRD_CiaCNPJ=> For Cia: <{ciaName}> BRD CNPJ CRUDE response:\n{response}" )
    troubleFlag = BRD_checkTrafficTrouble(response)
    cleanResponse = BRD_cleanReplyAbout(response)
    # print(f"\n===BRD_CiaCNPJ=> For Cia: <{ciaName}> BRD CNPJ CLEANED response:\n{cleanResponse}" )
    starFlag,starCNPJ = findMarkerCNPJ(cleanResponse,twoStars)
    if starFlag == 'False': # we are in the case BRD has not provided the ** mark
        posmark = cleanResponse.find(".")
        ciaCNPJ = cleanResponse[posmark-2:posmark+16]
        cnpjFlag = checkCNPJFormat(ciaCNPJ)
    else:
        cnpjFlag = starFlag
        ciaCNPJ = starCNPJ
    return troubleFlag,cnpjFlag,ciaCNPJ

# 08 finds cnpj string in BARDs response
def findMarkerCNPJ(cleanResponse,marker):
    cnpjFlag = 'False'
    ciaCNPJ = '#X#'
    pos1 = cleanResponse.find(marker)
    if pos1 > 0:
        cleanResponseTruncated = cleanResponse[pos1+2:]
        # print(f"n===findMarkerCNPJ=> responseTruncated: {cleanResponseTruncated}")
        pos2 = cleanResponseTruncated.find(marker)
        if pos2 > 0:
            ciaCNPJ = cleanResponseTruncated[:pos2]
            # print(f"n===findMarkerCNPJ=> CNPJ selected: <{ciaCNPJ}>")
            cnpjFlag = checkCNPJFormat(ciaCNPJ)
    return cnpjFlag,ciaCNPJ

# 09 checks if the cnpj data similar to format format = 20.223.016/0001-70 (dd.ddd.ddd/dddd-dd)
def checkCNPJFormat(cnpj):

    okFlag = 'False'
    pos1 = cnpj.find('.')
    cnpj2 = cnpj[pos1+1:]
    pos2 = cnpj2.find('.')
    pos3 = cnpj2.find('/')
    pos4 = cnpj2.find('-')
    # print(f"\n===checkCNPJFormat=> pos1: {pos1} ; pos2: {pos2} ; pos3: {pos3} ; pos4:{pos4} ; length: {len(cnpj)}")
    if len(cnpj) == 18 and pos1 == 2 and pos2 == 3 and pos3 == 7 and pos4 == 12:
        okFlag = 'True'
    return okFlag


#09 => Checks if BRD is operational (network accessible)
def BRD_checkTrafficTrouble(reply):
    troubleFlag = 'False'
    errorMark = reply.find('Response Error:')
    networkMark = reply.find('Temporarily unavailable due to traffic or an error in cookie values')
    if errorMark >= 0 or networkMark >= 0:
        # print(f"\n===BRD_checkTrouble=> Flags raised: Error: {errorMark} Traffic: {networkMark} in reply:\n {reply}" )
        troubleFlag = 'True'
    return troubleFlag

#10 => check if BRD reply is non operative
def BRD_checkAboutPertinence(about):
    okFlag = 'True'
    if about in BRD_InoperativeSet:
        okFlag = 'False'
    return okFlag

#11 => remove BRD boilerplate platitudes
def BRD_FilterPlatitudes(about):
    for indx in range(len(BRD_PlatitudesList)):
        about = about.replace(BRD_PlatitudesList[indx],'')
    return about

#12 => requests BRD API for the industry code of a company
def BRD_getIndustry(ciaName):
    response = ''
    query = 'Looking for Brazilian companies GICS Industry Code. Provide the GICS code bracketed with the characters **''(the format looks like this **.IBD.XXXXXXXX** where X is a digit - code MUST comprise 8 digits):'' What is the GICS Industry code for this Brazilian company:' +  ciaName +' ?' 
    response = BRD_bard.get_answer(query)['content']
    troubleFlag = BRD_checkTrafficTrouble(response)
    return troubleFlag,response

#13 => requests BRD API to regenerate response due to erroneous sector
def BRD_getIndustryRegenerateSector(ciaName,sectorCode):
    response = ''
    query = ' For brazilian company: ' + ciaName + 'you provided <' +sectorCode + '> as GICS Sector Code:'' This is incorrect because GICS sector code must take on of the values in this list:''sectorList= [10,15,20,35,40,45,50,55,60,65]''Provide the GICS code bracketed with the characters ** .''Watch your regenerated response more carefully'' What is the GICS Industry code for this Brazilian company:' +  ciaName +' ?' 
    response = BRD_bard.get_answer(query)['content']
    troubleFlag = BRD_checkTrafficTrouble(response)
    return troubleFlag,response

#14 => SubIndustry pattern matching in a text string in format <.IBD.15104030>
def ciaSearch_SubIndustry(text):
    GICS_sectorList = ['10','15','20','25','30','35','40','45','50','55','60']
    # industry format = .IBD.15104030
    okFlag = 'False'
    ciaSector = '#X#'
    ciaIndustry = '#X#'
    ciaSubIndustry = '#X#'
    regexSubIndustry = re.compile(r'.IBD.\d\d\d\d\d\d\d\d')
    if regexSubIndustry.search(text):
        resultSubIndustry = regexSubIndustry.search(text)
        groupSubIndustry = resultSubIndustry.group()
        ciaSubIndustry = groupSubIndustry.replace('.IBD.','')
        ciaSector = ciaSubIndustry[0:2]
        if ciaSector in GICS_sectorList:
            okFlag = 'SectorIncorrect'
            ciaIndustry = ciaSubIndustry[0:6]
            okFlag = 'True'
        else:
            okFlag = 'SectorIncorrect'
    else: # Bard is not trustful and keeps missing the last digit
        regexSubIndustry = re.compile(r'.IBD.\d\d\d\d\d\d\d')
        if regexSubIndustry.search(text):
            resultSubIndustry = regexSubIndustry.search(text)
            groupSubIndustry = resultSubIndustry.group()
            ciaSubIndustry = groupSubIndustry.replace('.IBD.','') + '0' # the last digit BRD is missing
            ciaSector = ciaSubIndustry[0:2]
            if ciaSector in GICS_sectorList:            
                ciaIndustry = ciaSubIndustry[0:6]
                okFlag = 'Suspicious'
            else:
                okFlag = 'SectorIncorrect'        
    return okFlag,ciaSector,ciaIndustry,ciaSubIndustry



print(f"\n===FixIncome Module=> <BRD Variable and Related Routines> 20230923-v3 ")


