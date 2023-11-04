#!/usr/bin/env python
# coding: utf-8

"""
=> Module-FixIncome - N4J related Routines 20231029-v2
n4j_session => removed
def n4j_get_companies(): ciaList_len,ciaList => Query to download all companies in FixInc Database
def n4j_check_cia_match(cia_name): => Checks if cia_name matches company already in N4j database
def n4j_correct_company_name(company_name): correctCiaName => Checks spelling in N4J database
def n4J_getAcrMatch(token): ciaList_len,ciaList => Query N4J for CiaNames that includes token
def n4j_change_cia_name(name, new_name): ciaList_len,ciaList => Set new_name as cia_name N4J db
def n4j_build_query_merge_cia(record_list): cypher_script => build query to upload new Cia in Neo4j
def n4j_get_company_no_about(session): cia_name => returns one company where about =#X#
def n4j_push_about(session,cia_name,about): responseList => store about in N4J database
"""

# => import n4j module - connects to open a session
from modgen_timestamp import date_stamp
from neo4j import GraphDatabase
from modfin_managing_companies import adjust_cia_name
from modfin_managing_companies import correct_spelling_company_name

data_base_connection = GraphDatabase.driver(
    uri="bolt://localhost:7687", auth=("neo4j", "alexo47@FRA")
)
n4j_session = data_base_connection.session()
print(f"\n N4J session: {n4j_session}")


def n4j_get_companies():
    """
    => Query to N4J to download all companies in FixInc Database
    :parameters; None
    :return: cia_list_len, cia_list
    """
    query = "MATCH(c:Company) RETURN c.cia_name"
    # print(query)
    # # nodes_results contains all the nodes returned by the query Neo4j
    cia_results = n4j_session.run(query)
    # nodes are stored in a entry_list
    cia_list = [j[0] for j in cia_results]
    cia_list_len = len(cia_list)
    return cia_list_len, cia_list


def n4j_check_cia_match(cia_name):
    """
     => Checks if cia_name matches perfectly company already in the N4j database
    :param cia_name:
    :return:
    """
    query = (
        "MATCH(c:Company) "
        + "WHERE (c.cia_name = "
        + "'"
        + cia_name
        + "') RETURN c.cia_name"
    )
    # print(f"\n---n4j_check_cia_match => cia_name: <{cia_name}> query is:\n{query}")
    cia_results = n4j_session.run(query)
    # nodes are stored in a entry_list
    cia_list = [j[0] for j in cia_results]
    cia_list_len = len(cia_list)
    # print(f"\n---n4j_check_cia_match => cia_list has: <{cia_list_len}> entries:\n{cia_list}")
    return cia_list_len, cia_list


def n4j_correct_company_name(company_name):
    """
     => Checks spelling with N4J FixInc Database
    :param company_name:
    :return: correct_cia_name
    """
    actual_cia_name = company_name
    adjusted_cia_name = adjust_cia_name(actual_cia_name)  # <= check this routine
    correct_cia_name = correct_spelling_company_name(adjusted_cia_name)
    if correct_cia_name != actual_cia_name:
        query = (
            "MATCH(c:Company) "
            + "WHERE  c.cia_name = "
            + '"'
            + actual_cia_name
            + '"'
            + "SET c.cia_name = "
            + '"'
            + correct_cia_name
            + '"'
            + "RETURN c.cia_name"
        )
        # print(\
        # f"\n===n4j_correct_company_name=> With <{actual_cia_name}> correct spelling:\
        # <{correct_cia_name}> the query is:\n{query}"\
        # )
        # !! response is not considered should be checked
        response = n4j_session.run(query)
    return correct_cia_name


def n4j_get_acr_match(token):
    """
    => Query N4J for CiaNames that includes token
    :param token:
    :return: cia_list_len, cia_list
    """
    token_title = token.title()
    token_up = token.upper()
    query = (
        "MATCH(c:Company) " + "WHERE  (c.cia_name CONTAINS " + "'" + token + "' )"
        " OR (c.cia_name CONTAINS " + "'" + token_up + "' )"
        " OR (c.cia_name CONTAINS " + "'" + token_title + "' )"
        "RETURN c.cia_name"
    )
    # print(f"\n---n4j_get_acr_match => With Acronym <{token}> The query is:\n{query}")
    cia_results = n4j_session.run(query)
    cia_list = [j[0] for j in cia_results]
    cia_list_len = len(cia_list)
    return cia_list_len, cia_list


def n4j_change_cia_name(name, new_name):
    """
    => Set new cia_name in the N4J database
    :param name:
    :param new_name:
    :return: cia_list_len, cia_list
    """
    query = (
        "MATCH(c:Company) WHERE c.cia_name = '"
        + name
        + "' SET c.cia_name = '"
        + new_name
        + "' RETURN c.cia_name"
    )
    # print(f"\n===n4j_change_cia_name=> N4J query: {query}")
    cia_results = n4j_session.run(query)
    cia_list = [j[0] for j in cia_results]
    cia_list_len = len(cia_list)
    return cia_list_len, cia_list


def n4j_build_query_merge_cia(record_list):
    """
    => build query to upload new Cia (all properties) into N4J Database
    :param record_list:
    :return: cypher_script
    """
    cia_cnpj = record_list[0]
    cia_name = record_list[1]
    cia_name = cia_name.replace(
        "'", "&"
    )  # !! we need to remove the apostrophes for Neo4j query
    sub_industry_code = record_list[2]
    industry_code = record_list[3]
    sector_code = record_list[4]
    region = record_list[5]
    fitch = record_list[6]
    sp = record_list[7]
    moody = record_list[8]
    group = record_list[9]
    about = record_list[10]
    about = about.replace(
        "'", "&"
    )  # !! we need to remove the apostrophes for the Neo4j query

    cypher_script = (
        "MERGE(c:Company {"
        + "cia_cnpj: '"
        + cia_cnpj
        + "' ,"
        + "cia_name: '"
        + cia_name
        + "' ,"
        + "sub_industry_code: '"
        + sub_industry_code
        + "' ,"
        + "industry_code: '"
        + industry_code
        + "' ,"
        + "sector_code: '"
        + sector_code
        + "' ,"
        + "region: '"
        + region
        + "' ,"
        + "fitch: '"
        + fitch
        + "' ,"
        + "sp: '"
        + sp
        + "' ,"
        + "moody: '"
        + moody
        + "' ,"
        + "group: '"
        + group
        + "' ,"
        + "about: '"
        + about
        + "'"
        + "})"
        + "RETURN c"
    )

    return cypher_script


def n4j_get_company_no_about(session):
    """
    => returns one company where about =#X#
    :param session:
    :return: cia_name
    """
    cypher_query = "MATCH(c:Company) WHERE c.about = '#X#' RETURN c.cia_name LIMIT 1"
    cypher_response = session.run(cypher_query)
    response_list = [j[0] for j in cypher_response]
    if len(response_list) == 0:
        cia_name = 0
    else:
        cia_name = response_list[0]
    return cia_name


def n4j_push_about(session, cia_name, about):
    """
    => store About in N4J database
    :param session:
    :param cia_name:
    :param about:
    :return:
    """

    token1 = "MATCH(c:Company) WHERE c.cia_name = '" + cia_name + "' "
    token2 = "SET c.about = '" + about + "'"
    # print(f" query_token1 =<{token1}> \n query_token2 = <{token2}>")
    query = token1 + token2
    # print(f"\n final query is \n\n {setQuery}")
    query_response = session.run(query)
    response_list = [j[0] for j in query_response]
    return response_list


print(
    f"\n===FixIncome N4J Module=> <Variables & Routines 20231029-v2> exec@: {date_stamp()} "
)
