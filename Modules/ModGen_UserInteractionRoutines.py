#!/usr/bin/env python
# coding: utf-8

# In[2]:


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
#//

#01 => Asks user maximum number of hits
def USR_hitLimit():
    prompt = 'How many entries do you tolerate to select: [n] \n'
    userResp = input(prompt)
    return userResp

#02 => User feedback on a token: Acronym,CommonWord
def USR_tokenFeedback(company,token):
    prompt = 'In Company: ' + company + '\n Token: <' + token +'>' + '\n should we: '     + '{I}gnore? or [A]Acronyme? or [C]ommon? or [S]top?'
    # print(prompt)
    userResp = input(prompt)
    return userResp

#03 => Company not in Neo4j so what do?
def USR_confirmCompany(company):
    foundFlag = 'False'
    companyTitle = company.title()
    prompt = 'Company: ' + companyTitle + ' apparently not in Neo4j database, rectify: {N] / [R] / [D] ??: \n'     ' [N]ew consider as a new Company; [R]ecognize as already registered; [D]iscard this company \n'
    userResp = input(prompt)
    if userResp == 'N' or userResp == 'n':
        companyName = companyTitle
    elif userResp == 'R' or userResp == 'r':
        enterName = 'Please confirm/rectify the company name: ' + companyTitle + '? type [#] to take it as is \n'
        userResp = input(enterName)
        foundFlag = 'True'
        if userResp == '#':
            companyName = companyTitle
        else:
            companyName = userResp
    elif userResp == 'D' or userResp == 'd':
        print(f"\n===USR_Company Print =>  User asked to discard : {company}")
        companyName = companyTitle
        foundFlag = 'Discard'
    else:
        print(f"\n===USR_Company Print =>  User enterd innacurate feedback: {userResp}")
        companyName = companyTitle
        foundFlag = 'Invalid'
    return foundFlag,companyName

#04 => Select Neo4j potential Hits or discard?
def USR_hitlistChoice(company,hitList):
    validResponse = ['D','d',]
    companyTitle = company.title()
    selectFlag = 'False'
    CompanyName = notdefined_token
    hits = len(hitList)
    print(f"\n===USR_Choice=> For Company: {company} Neo4j has found {hits} possible candidates, namely: \n {hitList} ")
    for indx in range(hits):
        print(f"[{indx}] = {hitList[indx]}")   
    prompt = 'For Company: ' + company + ' make your choice [n] to select or [D] to discard the hitList  \n '
    userResp = input(prompt)
    if userResp in numDigit:
        userRank = int(userResp)
        if userRank >= 0 and userRank < hits:      
            CompanyName = hitList[userRank]
            selectFlag = 'True'
    else:
        if userResp == 'D'or userResp == 'd':
            CompanyName = notdefined_token
            selectFlag = 'False'
        else:
            print(f"\n===USR_Choice=> Invalid Input for company {companyTitle} - will be considered as discarded ")
            CompanyName = notdefined_token
            selectFlag = 'False'

    if selectFlag == 'True':
        print(f"\n=== USR_Choice=> User selected Company: {CompanyName} ")
    else:
        print(f"\n===USR_Choice=> User discarded all {hits} hits no selection was made")   
    return selectFlag,CompanyName


#05 => Confirmation for new Company in the database
def USR_companyConfirmation(company):
    prompt = 'Company: <' + company + '>  should we add this company to the Neo4j database:\n '     + '[A]dd? ; [I]gnore? [R/]ename? or [S]top processing?'
    # print(prompt)
    userResp = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {userResp}" )
    return userResp

#06 => shows about and ask for UI confirmation or discard Cia
def USR_companyGoNogo(company):
    prompt = 'Company: ' + company + ' with the about above, go/nogo?: '     + '[A]dd? or [I]gnore?'
    # print(prompt)
    userResp = input(prompt)
    return userResp

#07 => ask user to rectify company name
def USR_rectifyCompanyName(company):
    companyTitle = company.title()
    prompt = 'For Company: <' + companyTitle + '> what final name do you want to register? type [#] to take it as is \n'
    userResp = input(prompt)
    if userResp == '#':
        companyName = companyTitle
    else:
        companyName = userResp
    return companyName


#08 => cvmCiaName keywords highest hits - should we accept, rename or ignore?
def USR_confirmCiaHighestHit(ciaName,n4jName):
    prompt = 'CVM ciaName <' + ciaName + '> Highest Hits with:\n <' + n4jName +'>' + ' should we:\n '     + '{A}ccept? / Yes, but [R/]ename / [I]gnore? or [S]top? '
    # print(prompt)
    userResp = input(prompt)
    return userResp

#09 => Acronym Hits level accept/discard?
def USR_confirmAcronym(acronym,hits):
    prompt = 'Acronym: ' + acronym + ' has <' + str(hits) +'>' + ' hits, should we: '     + '{R}emove? or [I]gnore?'
    # print(prompt)
    userResp = input(prompt)
    return userResp

#10 => Confirmation for a Common Word
def USR_confirmCommonWord(word):
    prompt = 'CommonWord: ' + word + ' should we add to the CommonWordSet: '     + '[A]dd? or [I]gnore?'
    # print(prompt)
    userResp = input(prompt)
    return userResp

#11 =>  [S]tart processing from scratch or [R]esume processing
def USR_StartResume():
    prompt = 'Do you want to start the process from: scratch: [S]? or or you want to: [R]esume last processing?\n=>'
    userResp = input(prompt)
    return userResp

#12 => askUser for company CNPJ
def USR_ciaCNPJ(company):
    prompt = 'Company: <' + company + '>  does not have a CNPJ number can you provide manually?:\n '     + '[A/]dd? ; [I}gnore or [S]top processing?'
    # print(prompt)
    userResp = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {userResp}" )
    return userResp

#13 => askUser for company About
def USR_ciaAbout(company):
    prompt = 'Company: <' + company + '>  does not have an About can you provide manually?:\n '     + '[A/]dd? ; [I}gnore or [S]top processing?'
    # print(prompt)
    userResp = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {userResp}" )
    return userResp

#14 => askUser to manually rescue About
def USR_rescueAbout(ciaName):
    ciaAbout = '#X#'
    userAbout = USR_ciaAbout(ciaName)
    aboutMarker = userAbout.find('A/')
    if userAbout == 'I':
        ciaAbout = '#X#'
        userResp = 'Ignore'
        print(f"\n===aboutUI_Rescue=> for Company <{ciaName}> user [I]gnored ciaAbout unchanged")
    if userAbout == 'S':
        # user wants to stop scanning       
        userResp = 'Stop'
        print(f"\n===aboutUI_Rescue=> for Company <{ciaName}> User asked for STOP")
        return userResp,ciaAbout
    if aboutMarker == 0:
        ciaAbout0 = userAbout.replace('A/','')
        ciaAbout = Mcia.cleanAbout(ciaAbout0)
        ciaAbout = Bard_FilterPlatitudes(ciaAbout)
        userResp = 'Valid'
        print(f"\n===aboutUI_Rescue=>==> For Company <{ciaName}> UI CiaAbout: <{ciaAbout}>  ")
    else:
        print(f"\n===aboutUI_Rescue=> for Company <{ciaName}> UI CiaAbout IGNORED <{userAbout}>  ")
        userResp = 'Invalid'
        ciaAbout = '#X#' # the registered About is meaning less
        outputList[11] = ciaAboutBRD        
    return userResp,ciaAbout

#15 => About looks fishy ask user feedback        
def USR_checkAbout(company,about):
    cleanAbout = about
    # print(f"\n===UI_aboutChecker=> Company: <{company}> About: \n{about}")
    prompt = 'This About looks fishy should we:\n '     + '[A]ccept? ; [D}iscard ; [R/]edact or [S]top processing?'
    userResp = input(prompt)
    marker = userResp.find('R/')
    if userResp == 'A':
        userResp = 'Confirmed'
        cleanAbout = about          

    if userResp == 'D':
        cleanAbout = '#X#'
        userResp = 'Discard'
        # print(f"\n===UI_aboutChecker=> for Company <{company}> user [D]iscard cleanAbout reset to #X#")

    if userResp == 'S':
        # user wants to stop scanning       
        userResp = 'Stop'
        # print(f"\n===aboutUI_Rescue=> for Company <{company}> User asked for STOP")
        return userResp,cleanAbout

    if marker == 0:
        cleanAbout = userResp.replace('R/','')
        userResp = 'Valid'
        # print(f"\n===aboutUI_Rescue=>==> For Company <{ciaName}> UI CiaAbout: <{ciaAbout}>  ")
    else:
        # print(f"\n===aboutUI_Rescue=> for Company <{company}> UI user response Invalidates <{userResp}>  ")
        userResp = 'Invalid'         
    return userResp,cleanAbout

#16 => askUser to manually rescue CNPJ
def USR_rescueCNPJ(ciaName):
    ciaCNPJ ='#X#'
    userCNPJ = USR_ciaCNPJ(ciaName)
    CNPJMarker = userCNPJ.find('A/')
    if userCNPJ == 'I':
        ciaCNPJ = '#X#'
        userResp = 'Ignore'
        print(f"\n===CNPJ_UI_Rescue=> for Company <{ciaName}> user [I]gnored ciaCNPJ unchanged  ")
    if userCNPJ == 'S':
        # user wants to stop scanning
        print(f"\n===CNPJ_UI_Rescue=> for Company <{ciaName}> User asked for STOP")
        userResp = 'Stop'
        return userResp,ciaCNPJ
    if CNPJMarker == 0:
        ciaCNPJ = userCNPJ.replace('A/','')
        userResp = 'Valid'
        # print(f"\n====V1-CNPJUI_Rescue=>==> For Company <{ciaName}> UI CiaCNPJ: <{ciaCNPJ}>  ")
    else:
        print(f"\n====V1-CNPJUI_Rescue=> for Company <{ciaName}> UI CiaCNPJ IGNORED <{userCNPJ}>  ")
        userResp = 'Invalid'
        ciaCNPJ = '#X#' # the registered CNPJ is meaning less
        outputList[11] = ciaCNPJ        
    return userResp,ciaCNPJ
    

      
        
print(f"\n===FixInc Module=> <User Interaction Routines 20230912-v3B>")


# In[ ]:




