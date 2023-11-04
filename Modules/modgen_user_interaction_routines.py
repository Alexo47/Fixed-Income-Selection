#!/usr/bin/env python
# coding: utf-8

from modgen_timestamp import date_stamp
from modfin_global_definitions import UNDEFINED_TOKEN, DIGITS
from modfin_managing_companies import clean_about
from modfin_brd import brd_filter_platitudes


"""
=> FixInc User Interaction Routines - 20231029 -v2
def usr_hit_limit(): userResp  Asks user maximum number of hits
def usr_token_feedback(company,token): userResp => User feedback on a token: Acronym,CommonWord
def usr_confirm_company(company): foundFlag,company_name => Company not in Neo4j so what do?
def USR_hitlist_choice(company,hitlist): selectFlag,CompanyName => Sel potential Hits or discard?
def usr_company_confirmation(company): userResp => Confirmation for new Company in the database
def usr_company_go_nogo(company): userResp => shows about and ask for UI confirmation or discard Cia
def usr_rectify_company_name(company): company_name => ask user to rectify company name
def usr_confirm_cia_highest_hit(cvmName,n4j_name): userResp => highest hit accept,rename or ignore?
def usr_confirm_acronym(acronym,hits): userResp => Acronym Hits level accept/discard?
def usr_confirm_common_word(word): userResp => Confirmation for a Common Word
def usr_start_resume(): userResp => [S]tart processing from scratch or [R]esume processing
def usr_cia_cnpj(company): userResp => askUser for company CNPJ
def usr_cia_about(company): userResp => askUser for company about
def usr_rescue_about(cia_name): userResp,ciaAbout => askUser to manually rescue about
def usr_check_about(company,about): userResp,clean_about => about looks fishy ask user feedback
def usr_rescue_cnpj(cia_name): userResp,ciaCNPJ => askUser to manually rescue CNPJ
"""


def usr_hit_limit():
    """
    => Asks user maximum number of hits
    :return:
    """
    prompt = "How many entries do you tolerate to select: [n] \n"
    user_resp = input(prompt)
    return user_resp


def usr_token_feedback(company, token):
    """
    => User feedback on a token: Acronym,CommonWord
    :param company:
    :param token:
    :return:
    """
    prompt = (
        "In Company: "
        + company
        + "\n Token: <"
        + token
        + ">"
        + "\n should we: "
        + "{I}gnore? or [A]Acronyme? or [C]ommon? or [S]top?"
    )
    # print(prompt)
    user_resp = input(prompt)
    return user_resp


def usr_confirm_company(company):
    """
    => Company not in Neo4j so what do?
    :param company:
    :return: found_flag, company_name
    """

    found_flag = "False"
    company_title = company.title()
    prompt = (
        "Company: "
        + company_title
        + " apparently not in Neo4j database, rectify: {N] / [R] / [D] ??: \n"
        " [N]ew consider as a new Company; [R]ecognize as already registered; [D]iscard this"
        " company \n"
    )
    user_resp = input(prompt)
    if user_resp == "N" or user_resp == "n":
        company_name = company_title
    elif user_resp == "R" or user_resp == "r":
        enter_name = (
            "Please confirm/rectify the company name: "
            + company_title
            + "? type [#] to take it as is \n"
        )
        user_resp = input(enter_name)
        found_flag = "True"
        if user_resp == "#":
            company_name = company_title
        else:
            company_name = user_resp
    elif user_resp == "D" or user_resp == "d":
        print(f"\n===USR_Company Print =>  User asked to discard : {company}")
        company_name = company_title
        found_flag = "Discard"
    else:
        print(
            f"\n===USR_Company Print =>  User entered inaccurate feedback: {user_resp}"
        )
        company_name = company_title
        found_flag = "Invalid"
    return found_flag, company_name


def usr_hitlist_choice(company, hitlist):
    """
    => Select Neo4j potential Hits or discard?
    :param company:
    :param hitlist:
    :return: select_flag, company_name
    """
    company_title = company.title()
    select_flag = "False"
    company_name = UNDEFINED_TOKEN
    hits = len(hitlist)
    print(
        f"\n===USR_Choice=> For Company: {company} Neo4j has found {hits}"
        f" possible candidates, namely: \n {hitlist} "
    )
    for indx in range(hits):
        print(f"[{indx}] = {hitlist[indx]}")
    prompt = (
        "For Company: "
        + company
        + (" make your choice [n] " "to select or [D] to discard the hitlist  \n ")
    )
    user_resp = input(prompt)
    if user_resp in DIGITS:
        user_rank = int(user_resp)
        if user_rank >= 0 and user_rank < hits:
            company_name = hitlist[user_rank]
            select_flag = "True"
    else:
        if user_resp == "D" or user_resp == "d":
            company_name = UNDEFINED_TOKEN
            select_flag = "False"
        else:
            print(
                f"\n===USR_Choice=> Invalid Input for company {company_title}"
                f" - will be considered as discarded "
            )
            company_name = UNDEFINED_TOKEN
            select_flag = "False"

    if select_flag == "True":
        print(f"\n=== USR_Choice=> User selected Company: {company_name} ")
    else:
        print(f"\n===USR_Choice=> User discarded all {hits} hits no selection was made")
    return select_flag, company_name


def usr_company_confirmation(company):
    """
    => Confirmation for new Company in the database
    :param company:
    :return:
    """
    prompt = (
        "Company: <"
        + company
        + ">  should we add this company to the Neo4j database:\n "
        + "[A]dd? ; [I]gnore? [R/]ename? or [S]top processing?"
    )
    # print(prompt)
    user_resp = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {user_resp}" )
    return user_resp


def usr_company_go_nogo(company):
    """
    => shows about and ask for UI confirmation or discard Cia
    :param company:
    :return:
    """
    prompt = (
        "Company: "
        + company
        + " with the about above, go/nogo?: "
        + "[A]dd? or [I]gnore?"
    )
    # print(prompt)
    user_resp = input(prompt)
    return user_resp


def usr_rectify_company_name(company):
    """
    => ask user to rectify company name
    :param company:
    :return: company_name
    """
    company_title = company.title()
    prompt = (
        "For Company: <"
        + company_title
        + "> what final name do you want to register? type [#] to take it as is \n"
    )
    user_resp = input(prompt)
    if user_resp == "#":
        company_name = company_title
    else:
        company_name = user_resp
    return company_name


def usr_confirm_cia_highest_hit(cia_name, n4j_name):
    """
    => cvmCiaName keywords highest hits - should we accept, rename or ignore?
    :param cia_name:
    :param n4j_name:
    :return: user_resp
    """
    prompt = (
        "CVM cia_name <"
        + cia_name
        + "> Highest Hits with:\n <"
        + n4j_name
        + ">"
        + " should we:\n "
        + "{A}ccept? / Yes, but [R/]ename / [I]gnore? or [S]top? "
    )
    # print(prompt)
    user_resp = input(prompt)
    return user_resp


def usr_confirm_acronym(acronym, hits):
    """
    => Acronym Hits level accept/discard?
    :param acronym:
    :param hits:
    :return: user_resp
    """
    prompt = (
        "Acronym: "
        + acronym
        + " has <"
        + str(hits)
        + ">"
        + " hits, should we: "
        + "{R}emove? or [I]gnore?"
    )
    # print(prompt)
    user_resp = input(prompt)
    return user_resp


def usr_confirm_common_word(word):
    """
    => New Common Word: Accept or Discard
    :param word:
    :return:
    """
    prompt = (
        "CommonWord: "
        + word
        + " should we add to the CommonWordSet: "
        + "[A]dd? or [I]gnore?"
    )
    # print(prompt)
    user_resp = input(prompt)
    return user_resp


def usr_start_resume():
    """
    =>  [S]tart processing from scratch or [R]esume processing
    :return: user_resp
    """
    prompt = (
        "Do you want to start the process from: scratch:"
        " [S]? or or you want to: [R]esume last processing?\n=>"
    )
    user_resp = input(prompt)
    return user_resp


def usr_cia_cnpj(company):
    """
    => askUser for company CNPJ
    :param company:
    :return:
    """
    prompt = (
        "Company: <"
        + company
        + ">  does not have a CNPJ number can you provide manually?:"
        "\n " + "[A/]dd? ; [I}gnore or [S]top processing?"
    )
    # print(prompt)
    user_resp = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {user_resp}" )
    return user_resp


def usr_cia_about(company):
    """
    => askUser for company about
    :param company:
    :return:
    """
    prompt = (
        "Company: <" + company + ">  does not have an about can you provide manually?:"
        "\n " + "[A/]dd? ; [I}gnore or [S]top processing?"
    )
    # print(prompt)
    user_resp = input(prompt)
    # print(f"\n===USR_Confirmation_Company=> For company {company} user responded: {user_resp}" )
    return user_resp


def usr_rescue_about(cia_name):
    """
    => askUser to manually rescue about
    :param cia_name:
    :return:
    """
    cia_about = "#X#"
    user_about = usr_cia_about(cia_name)
    about_marker = user_about.find("A/")
    if user_about == "I":
        cia_about = "#X#"
        user_resp = "Ignore"
        print(
            f"\n===aboutUI_Rescue=> for Company <{cia_name}> user [I]gnored cia_about unchanged"
        )
    if user_about == "S":
        # user wants to stop scanning
        user_resp = "Stop"
        print(f"\n===aboutUI_Rescue=> for Company <{cia_name}> User asked for STOP")
        return user_resp, cia_about
    if about_marker == 0:
        cia_about0 = user_about.replace("A/", "")
        cia_about = clean_about(cia_about0)
        cia_about = brd_filter_platitudes(cia_about)
        user_resp = "Valid"
        print(
            f"\n===aboutUI_Rescue=>==> For Company <{cia_name}> UI CiaAbout: <{cia_about}>  "
        )
    else:
        print(
            f"\n===aboutUI_Rescue=> for Company <{cia_name}>"
            f" UI CiaAbout IGNORED <{user_about}>  "
        )
        user_resp = "Invalid"
        cia_about = "#X#"  # the registered about is meaning less
        """
        # !! The instruction below is out of it´s context and must be re3moved
        # outputList[11] = ciaAboutBRD
        """
    return user_resp, cia_about


def usr_check_about(company, about):
    """
    => about looks fishy ask user feedback
    :param company:
    :param about:
    :return: user_resp, about_clean
    """
    about_clean = about
    # print(f"\n===UI_aboutChecker=> Company: <{company}> about: \n{about}")
    prompt = (
        "This about looks fishy should we:\n "
        + "[A]ccept? ; [D}iscard ; [R/]edact or [S]top processing?"
    )
    user_resp = input(prompt)
    marker = user_resp.find("R/")
    if user_resp == "A":
        user_resp = "Confirmed"
        about_clean = about

    if user_resp == "D":
        about_clean = "#X#"
        user_resp = "Discard"
        # print(f"\n===aboutChecker=> for Cia <{company}> user [D]iscard about_clean reset to #X#")

    if user_resp == "S":
        # user wants to stop scanning
        user_resp = "Stop"
        # print(f"\n===aboutUI_Rescue=> for Company <{company}> User asked for STOP")
        return user_resp, about_clean

    if marker == 0:
        about_clean = user_resp.replace("R/", "")
        user_resp = "Valid"
        # print(f"\n===aboutUI_Rescue=>==> For Company <{cia_name}> UI CiaAbout: <{ciaAbout}>  ")
    else:
        # print(f"\n===aboutUI_Rescue=> for Company <{company}>
        # UI user response Invalidates <{user_resp}>  ")
        user_resp = "Invalid"
    return user_resp, about_clean


def usr_rescue_cnpj(cia_name):
    """
    => askUser to manually rescue CNPJ
    :param cia_name:
    :return:
    """
    cia_cnpj = "#X#"
    user_cnpj = usr_cia_cnpj(cia_name)
    cnpj_marker = user_cnpj.find("A/")
    if user_cnpj == "I":
        cia_cnpj = "#X#"
        user_resp = "Ignore"
        print(
            f"\n===CNPJ_UI_Rescue=> for Company <{cia_name}> user [I]gnored cia_cnpj unchanged  "
        )
    if user_cnpj == "S":
        # user wants to stop scanning
        print(f"\n===CNPJ_UI_Rescue=> for Company <{cia_name}> User asked for STOP")
        user_resp = "Stop"
        return user_resp, cia_cnpj
    if cnpj_marker == 0:
        cia_cnpj = user_cnpj.replace("A/", "")
        user_resp = "Valid"
        # print(f"\n====V1-CNPJUI_Rescue=>==> For Company <{cia_name}> UI CiaCNPJ: <{cia_cnpj}>  ")
    else:
        print(
            f"\n===CNPJUI_Rescue=> for Company <{cia_name}> UI CiaCNPJ IGNORED <{user_cnpj}> "
        )
        user_resp = "Invalid"
        cia_cnpj = "#X#"  # the registered CNPJ is meaning less

        """
        # !! The instruction below is out of it´s context and must be re3moved
        # outputList[11] = cia_cnpj
        """
    return user_resp, cia_cnpj


print(f"\n===FixInc Module=> <User Interaction Routines 20230912-v3B> {date_stamp()}")
