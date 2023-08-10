#!/usr/bin/env python
# coding: utf-8

# In[1]:


### Module-FixIncome - N4J related Routines 20230803 -v1
#01 N4J_session => removed
#02 def N4J_getCompanies(): return ciaList_len,ciaList => Query to N4J to download all companies in FixInc Database
#03 def N4J_checkCiaMatch(ciaName): => Checks if CiaName matches perfectly company already in the N4j database
#04 def N4J_correctCompanyName(companyName): return correctCiaName => Checks spelling with N4J FixInc Database
#05 def N4J_getAcrMatch(token): return ciaList_len,ciaList => Query N4J for CiaNames that includes token
#06 def N4J_changeCiaName(name, newName): return ciaList_len,ciaList => Set newName as CiaName in the N4J database
#07 def N4J_buildQuery_MergeCia(recordList): return cypher_script => build query to upload new Cia into N4J Database
#08 def N4J_getCompany_noAbout(session): return ciaName => returns one company where About =#X#
#09 def N4J_pushAbout(session,CiaName,About): return responseList => store About in N4J database
#//

#01 => import n4j module - connects to open a session
from neo4j import GraphDatabase
data_base_connection = GraphDatabase.driver(uri = "bolt://localhost:7687", auth=("neo4j", "alexo47fra"))
N4J_session = data_base_connection.session()
print(f"\n N4J session: {N4J_session}")


#02 => Query to N4J to download all companies in FixInc Database
def N4J_getCompanies():
    query = 'MATCH(c:Company) RETURN c.CiaName'
    # print(query)
    ciaResults = session.run(query) # nodes_results contiens les noeuds retournés par N4J suite requête query
    ciaList = [j[0] for j in ciaResults] # on enregistre le retour sous forme de liste de noeuds
    ciaList_len = len(ciaList)
    return ciaList_len,ciaList

#03  => Checks if CiaName matches perfectly company already in the N4j database
def N4J_checkCiaMatch(ciaName):
    query = 'MATCH(c:Company) ' + 'WHERE  (c.CiaName = ' + '\'' + ciaName  + '\' ) RETURN c.CiaName'
    # print(f"\n---N4J_checkCiaMatch => CiaName: <{ciaName}> query is:\n{query}")
    ciaResults = session.run(query)
    ciaList = [j[0] for j in ciaResults] # on enregistre le retour sous forme de liste de noeuds
    ciaList_len = len(ciaList)
    #print(f"\n---N4J_checkCiaMatch => ciaList has: <{ciaList_len}> entries, namely:\n{ciaList}")
    return ciaList_len,ciaList

#04  => Checks spelling with N4J FixInc Database
def N4J_correctCompanyName(companyName):
    actualCiaName = companyName
    adjustedCiaName = adjustCiaName(actualCiaName) # <= check this routine
    correctCiaName = DBcorrectSpellingCiaName(adjustedCiaName)
    if correctCiaName != actualCiaName:
        query = 'MATCH(c:Company) ' + 'WHERE  c.CiaName = ' + '\"'+ actualCiaName  + '\"' + ' SET c.CiaName = '         + '\"' + correctCiaName  + '\"  RETURN c.CiaName'
        # print(f"\n$$$ With <{actualCiaName}> correct spelling: <{correctCiaName}> the query is:\n{query}")
        response = session.run(query)
    return correctCiaName

#05 => Query N4J for CiaNames that includes token
def N4J_getAcrMatch(token):
    tokenTitle = token.title()
    tokenUp = token.upper()
    query = 'MATCH(c:Company) ' + 'WHERE  (c.CiaName CONTAINS ' + '\'' + token  + '\' )'     ' OR (c.CiaName CONTAINS ' + '\'' + tokenUp  + '\' )'     ' OR (c.CiaName CONTAINS ' + '\'' + tokenTitle  + '\' )'     'RETURN c.CiaName'
    #print(f"\n---N4J_getAcrMatch => With Acronym <{token}> The query is:\n{query}")
    ciaResults = session.run(query)
    ciaList = [j[0] for j in ciaResults] # on enregistre le retour sous forme de liste de noeuds
    ciaList_len = len(ciaList)
    return ciaList_len,ciaList

#06 Set new CiaName in the N4J database
def N4J_changeCiaName(name, newName):
    query = 'MATCH(c:Company) WHERE c.CiaName = \'' + name + '\' SET c.CiaName = \'' + newName + '\' RETURN c.CiaName'
    # print(f"\n===N4J_changeCiaName=> N4J query: {query}")
    ciaResults = session.run(query) # nodes_results contiens les noeuds retournés par N4J suite requête query
    ciaList = [j[0] for j in ciaResults] # on enregistre le retour sous forme de liste de noeuds
    ciaList_len = len(ciaList)
    return ciaList_len,ciaList

#07 => build query to upload new Cia (all properties) into N4J Database 
def N4J_buildQuery_MergeCia(recordList):
    CiaCode = recordList[0]
    CiaCNPJ = recordList[1]
    CiaName = recordList[2]
    SubIndustryCode = recordList[3]
    IndustryCode = recordList[4]
    SectorCode = recordList[5]
    InternalCode = recordList[6]
    Region = recordList[7]
    Sym6C = recordList[8]
    Fitch = recordList[9]
    SP = recordList[10]
    Moody = recordList[11]
    Group = recordList[12]
    About = recordList[13]

    cypher_script = "MERGE(c:Company {CiaCNPJ:" + '\''+ CiaCNPJ +'\' })' + ' SET c.CiaCode = \'' + CiaCode + '\' ,' + ' c.CiaName = \'' +  CiaName+ '\' ,' + ' c.SubIndustryCode = \''+ SubIndustryCode +'\' ,' + ' c.IndustryCode = \'' +  IndustryCode +'\' ,' + ' c.SectorCode = \'' + SectorCode + '\' ,' + ' c.InternalCode = \'' + InternalCode + '\' ,' + ' c.Region = \''+ Region +'\' ,' + ' c.Sym6C = \'' + Sym6C  +'\' ,' + ' c.Fitch = \'' + Fitch  +'\' ,' + ' c.SP = \'' + SP  +'\' ,' + ' c.Moody = \''+ Moody  +'\' ,' + ' c.Group = \'' + Group +'\' ,' + ' c.About = \'' + About +'\'' + ' RETURN c'
    return cypher_script

#08 => returns one company where About =#X#
def N4J_getCompany_noAbout(session):
    cypherQuery = "MATCH(c:Company) WHERE c.About = \'#X#\' RETURN c.CiaName LIMIT 1"
    cypherResponse = session.run(cypherQuery)
    response_list = [j[0] for j in cypherResponse]
    if len(response_list) == 0:
        CiaName = 0
    else:
        CiaName = response_list[0]
    return CiaName

#09 => store About in N4J database
def N4J_pushAbout(session,CiaName,About):
    
    Token1 = "MATCH(c:Company) WHERE c.CiaName = \'" + CiaName + "\' "
    Token2 = "SET c.About = \'" + About +"\'"
# print(f" query_token1 =<{Token1}> \n query_token2 = <{Token2}>")
    Query = Token1 + Token2
#print(f"\n final query is \n\n {setQuery}")
    queryResponse = session.run(Query)
    responseList = [j[0] for j in queryResponse]
    return responseList


print(f"\n===FixIncome Module=> <N4J Variables and Related Routines 20230802-v1> ")


# In[ ]:




