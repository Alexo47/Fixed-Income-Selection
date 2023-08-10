#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Module-FixIncome - ManagingCompanies 20230803 - v2
#01 match_CiaName(company): return foundFlag,CompanyName => Scan Cia Name as tokens to search Neo4j + User Interaction
#02 def testAcronymToken(token,limit): return limitFlag,ciaMatchHits => checks if Neo4j Hits > than user set limit
#03 def adjustCiaName(Name): return CompanyName => Adjusts auxilary words that do not need Capital letters
#04 def correctSpellingCompanyName(cia_name): return cia_name => Checks mispelled words in Company Names
#05 def cleanCompanyName(cia_name): return cia_name /* Removes Companies registration status suchas S.A., etc
#06 def checkCNPJFormat(cnpj): return okFlag => cheks if Cia CNPJ data looks like a CNPJ number
#07 def searchCNPJ(text): return okFlag,ciaCNPJ =>
#07 def findMarkerCNPJ(cleanResponse,marker): return cnpjFlag,ciaCNPJ => scan a string to find a cnpj format sequence 
#08 def initAcronymsFile(File,Header): return fio,win,wout => Sets the csv readers/writers to start acronym processing
#09 def restoreAcronymSet(file): return acronymSet,len(acronymSet) => Process file containg acronyms to a set
#10 def open_AcronymsImport_Read(file): return okFlag,fi,win => Checks file existence Open file csv.reader
#11 def cleanReplyAbout(reply): return cleanReply => Removes CR/NL so About one line - replaces <'> by <^> and <;> by <&>
#//
import re

#01 => Scan Cia Name as tokens to search Neo4j + User Interaction
def match_CiaName(company):
    CompanyName = company.strip()
    companyWords = nlp(company)
    foundFlag = 'False'
    # print(f"\n===match_CiaName=> CompanyName: {companyWords}")
    for token in companyWords:
        if foundFlag == 'False':
            if token.text.lower() in acronymSet:
                hits,hitList = Neo4j_getAcrMatch(token.text)
                # print(f"\n===match_CiaName=> For {token} Neo4j returned: {hits} hits")
                if hits >= 1: # There are at least one match
                    # print(f"\n===match_CiaName=> Neo4j FOUND {hits} ENTRIES for acronym {token.text} in Company: {CompanyName}")
                    # print(f"\n===match_CiaName=>  The multiple entries found are: {hitList}")
                    foundFlag, CompanySelected = getUserChoice(CompanyName,hitList)
                else:
                    # print(f"\n===match_CiaName=> Neo4j DID NOT MATCH the acronym <{token.text}> in Company: {company}")
                    foundFlag = 'False'

    if foundFlag == 'False':    
        foundFlag,CompanyName = getUserCompany(company)
    
    # print(f"\n===match_CiaName=> returns: {CompanyName}")
    return foundFlag,CompanyName

#02 => Checks if Neo4j Hits > than user set limit
def testAcronymToken(token,limit):
    limitFlag = 'False'
    # print(f"\n===testAcronymToken=> Token: {token}")
    ciaMatchHits,ciaMatchList = Neo4j_getAcrMatch(token)
    # print(f"\n===testAcronymToken=> For {token} Neo4j returned: {ciaMatchHits} hits")
    if ciaMatchHits > limit:
        limitFlag = 'True'  
        # print(f"\n===testAcronymToken=> For <{token}> overflow detected {ciaMatchHits} hits")
    return limitFlag,ciaMatchHits

#03 => Adjusts auxilary words that do not need Capital letters
def adjustCiaName(Name):
    CompanyName = Name
    CompanyName = CompanyName.replace(' De ',' de ')
    CompanyName = CompanyName.replace(' Do ',' do ')
    CompanyName = CompanyName.replace(' Da ',' da ')
    CompanyName = CompanyName.replace(' Das ',' das ')
    CompanyName = CompanyName.replace(' E ',' & ')
    return CompanyName

#04 => Checks mispelled words in Company Names
# this version is clunky we need to manage with a dictionnary structure with save/restore is jason file
def correctSpellingCompanyName(cia_name):

    # adjustements
    # cia_name = cia_name.replace(',',' ' ) comma replacement must be done @Excel level 
    
    # eXTENSION aCRONYMES
    cia_name = cia_name.replace(' ADM ',' ADMINISTRAÇÃO ')
    cia_name = cia_name.replace(' ART. ',' ARTIGOS ')
    cia_name = cia_name.replace(' BRA ',' BRASILEIRA ')
    cia_name = cia_name.replace('CIA ','COMPANHIA  ')
    cia_name = cia_name.replace('CIA. ','COMPANHIA  ')
    cia_name = cia_name.replace(' CRED. ',' CRÉDITO ')
    cia_name = cia_name.replace(' COM. ',' COMÉRCIO ')
    cia_name = cia_name.replace(' EMPREEND ',' EMPREENDIMENTOS ')
    cia_name = cia_name.replace(' EMPREENDS ',' EMPREENDIMENTOS ')
    cia_name = cia_name.replace(' EMPRS ',' EMPRESA ')
    cia_name = cia_name.replace(' ENERG ',' ENERGIA ')
    cia_name = cia_name.replace(' ENG. ',' ENERGIA ')
    cia_name = cia_name.replace(' EQUIP. ',' EQUIPAMENTOS ')
    cia_name = cia_name.replace(' FIN. ',' FINANCEIRO ')
    cia_name = cia_name.replace(' GER. ',' GERACÂO ')
    cia_name = cia_name.replace(' HOSP. ',' HOSPITALARES ')
    cia_name = cia_name.replace(' IND. ',' INDUSTRIA ')
    cia_name = cia_name.replace(' INDs ',' INDUSTRIAS ')
    cia_name = cia_name.replace(' INFRA ',' INFRAESTUTURA ')
    cia_name = cia_name.replace(' PARTICIP ',' PARTICIPAÇÕES ')
    cia_name = cia_name.replace(' PROP ',' PROPRIEDADES ')
    cia_name = cia_name.replace(' PUB ',' PUBLICA ')
    cia_name = cia_name.replace(' PARTS ',' PARTICIPAÇÕES ')
    cia_name = cia_name.replace(' TRANSM ',' TRANSMISSÃO ')

# CORRECTIONS ORTHOGRAPHES

    cia_name = cia_name.replace('ACO','AÇO')
    cia_name = cia_name.replace('AGUAS','ÁGUAS')
    cia_name = cia_name.replace('CONCESSIONARIA ','CONCESSIONÁRIA ')
    cia_name = cia_name.replace('COMERCIO','COMÉRCIO')
    cia_name = cia_name.replace('COSMETICO','COSMÉTICOS')
    cia_name = cia_name.replace('EDUCACAO','EDUCAÇÃO')
    cia_name = cia_name.replace('ELETRICA','ELÉTRICA')
    cia_name = cia_name.replace('GAS','GÁS')
    cia_name = cia_name.replace('GERACAO','GERAÇÃO')
    cia_name = cia_name.replace('OLEO','OLÉO')
    cia_name = cia_name.replace('PARTICIPAÇOES','PARTICIPAÇÕES')
    cia_name = cia_name.replace('TRANSMISSAO','TRANSMISSÃO')
    cia_name = cia_name.replace('TRANSMISSAO','TRANSMISSÃO')
    cia_name = cia_name.strip()
    return cia_name

#05 /* Removes Companies registration status suchas S.A., etc
def cleanCompanyName(cia_name):
    cia_name = cia_name.strip()
    cia_name = cia_name.replace(' S/A.','')
    cia_name = cia_name.replace(' S/A','')
    cia_name = cia_name.replace(' S.A.','')
    cia_name = cia_name.replace(' S.A.','')
    cia_name = cia_name.replace(' S.A','')
    cia_name = cia_name.replace(' Ltd.','')
    tokenSA = cia_name[-3:]
    if tokenSA == ' SA':
        cia_name = cia_name.replace(' SA','')
    # we need to replace <'> by '^'
    cianame = cia_name.replace("'",'^')
    return cia_name

#06 => cheks if Cia CNPJ data looks like a CNPJ number
def checkCNPJFormat(cnpj):
    # cnpj format = 20.223.016/0001-70
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

#07 => serach CNPJ pattern in a text
def searchCNPJ(text):
    # cnpj format = 20.223.016/0001-70
    okFlag = 'False'
    ciaCNPJ = '#X#'
    regexCNPJ = re.compile(r'\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d')
    if regexCNPJ.search(text):
        cnpj = regexCNPJ.search(text)
        ciaCNPJ = cnpj.group()
        okFlag = 'True'
    return okFlag,ciaCNPJ

#08 =>scnan a string to find a cnpj format sequence
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

#09 => Sets the csv readers/writers to start acronym processing
# this routine has to be review and upgraded
def initAcronymsFile(File,Header):
    File_path = filesDir + "/" + File + '.txt'
    checkFile = os.path.isfile(File_path)
    # print(f"\n===initAcronymFile=> for file <{File}> checkFile gives: <{checkFile}>")
    if checkFile:
        print(f"\n===initAcronymFile=> CheckFile states that Acronym File <{File_path}> EXISTS: <{checkFile}")
        fio = open(File_path,'r+',encoding = "utf−8", newline = '')
        wout = csv.writer(fio, delimiter = ';')
        win = csv.reader(fio, delimiter = ';')
    else:
        print(f"\n===initAcronymFile=> CheckFile states that Acronym File <{File_path}> DOES NOT EXIST: <{checkFile}")
        fio = open(File_path,'a',encoding = "utf−8", newline = '')
        wout = csv.writer(fio, delimiter = ';')
        win = '#X#'
        wout.writerow(Header)
    return fio,win,wout

#10 => Process file containg acronyms to a set
# The csv file containing acronyms has been replaced by a jason file with def restoreSet_jason(filePath):
def restoreAcronymSet(file):
    okFlag,fi,win = open_AcronymsImport_Read(file)
    if okFlag == 'True':
        # print(f"\n Return from open_AcronymsImport Reader After if okFlag: {okFlag} ")
        acronymSet = set()
        # we skip the input file header
        headerLine = fi.readline()
        while inputLine := fi.readline():
            inputList,inputList_len = items_separator_converter(inputLine,';')
            # print(f"\n InputList in: {inputLine} , has {inputList_len} items, namely:\n{inputList}")
            acronymSet.add(inputList[2])
        fi.close()
    else:
        acronymSet = set()
        acronymCount = 0
    return acronymSet,len(acronymSet)

#11 => Checks file existence Open file csv.reader
# this routine can be replaced by def openFile_Reader(filePath): return okFlag,fi,win
def open_AcronymsImport_Read(file):
    inputFile_path = filesDir + "/" + file + '.txt'
    okFlag = 'True'
    win = 'False'
    fi = 'False'
    checkFile = os.path.isfile(inputFile_path)
    # print(f"\n !!! Acronyms checkFile: <{checkFile}>")
    if checkFile:
        print(f"\n===open_AcronymsImport_Read=> CheckFile states that ACRONYMS file <{inputFile_path}> EXISTS <{checkFile}")
        fi = open(inputFile_path,'r',encoding = "utf−8", newline = '')
        win = csv.reader(fi, delimiter = ';')
    else:
        print(f"\n===open_AcronymsImport_Read=> CheckFile states that ACRONYMS file <{inputFile_path}> DOES NOT EXIST: <{checkFile}")
        okFlag = 'False'
    return okFlag,fi,win

#12 =>  => Removes CR/NL to make About in one line - replaces <'> by <^> and <;> by <&>
def cleanAbout(reply):
        cleanReply = reply.replace('\n','')
        cleanReply = cleanReply.replace("\'",'^')
        cleanReply = cleanReply.replace(";",'&')
        return cleanReply

print(f"\n===FixInc Module=> <ManagingCompanies 20230803-v4>")


# In[ ]:




