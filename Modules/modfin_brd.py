#!/usr/bin/env python
# coding: utf-8

"""
Module-FixIncome - BRD related Routines 220231028-v4 - Following PEP 8 recommendations

"""
# ### Import Basic Modules + TimeStamp

import re
from modgen_timestamp import date_stamp
from bardapi import Bard



# == Module-FixIncome - BRD related Routines 20230803 -v1
# BRD_KEY_API => BRD API key extracted form cookies
# brd_inoperative_list => BRD meaningless about responses
# brd_inoperative_list_len => len(brd_inoperative_list)
# brd_inoperative_set =>
# brd_inoperative_set_len =>
# brd_platitudes_list => BRD Platitudes about responses:
# brd_platitudes_list_len => len(brd_platitudes_list)
# def brd_cia_about(cia_name): troubleFlag,ciaAbout => Prompts BRD for a Cia about
# def brd_cleanReplyAbout(reply): cleanReply => Removes special characters + BRD Noise
# def brd_cia_cnpj(cia_name): troubleFlag,cnpjFlag,ciaCNPJ => Prompts BRD for a Cia CNPJ
# def find_marker_cnpj(clean_response,marker): cnpjFlag,ciaCNPJ => finds 'cnpj' in BARDs response
# def check_cnpj_format(cnpj): okFlag => try matches dd.ddd.ddd/dddd-dd  (20.223.016/0001-70)
# def brd_check_traffic_trouble(reply): troubleFlag => Checks BRD if is network accessible
# def brd_check_about_pertinence(about):okFlag => check if BRD reply is non operative
# def brd_filter_platitudes(about):  about => remove BRD boilerplate platitudes
# def brd_get_industry(cia_name): troubleFlag,response => requests BRD API Cia industry code
# def brd_get_industry_into_sector(cia_name,sector_code): trouble_flag,response.IBD.15104030
# def cia_search_sub_industry(text): ok_flag,cia_sector,cia_industry,cia_sub_industry
# ==


# BRD_KeyAPI = 'ZAh5YWaPE7QLc9Ymhbp8dxbv1QjnQKEeWs5RchFY4qMuiF3iWaJLyDIWUQzfRINEXghK0g.'
# BRD_KeyAPI = 'awh5YWTO8IrYw-mmk3qAFGi6T6X_XUo27w4b44wNu_T3gCzDOXyqzOdtBksLWj5O4mQu1A.'
# BRD_KEY_API = "bAh5YZa9CV1fancVHQZX6ayt-aX5S5FiLnE4XsKsR4Qt-uNq1z-CKeBfP0zykLxvbzhKeQ."
BRD_KEY_API = "cQh5Yb9ylfJXi5baOyNCGkE1ny7EhhCJhjFIkUgpTV4fVIEW5jDiZ_bVD86Gv753gSGwPA."
brd_bard = Bard(token=BRD_KEY_API)


brd_inoperative_list = [
    "It could be a small, local company that has not gained much visibility,"
    "or it could be a fictitious company.",
    "it would be appreciated if you could provide additional information about the company you"
    "are talking about"
    "However, upon conducting some research, I could not find any information"
    "about a Brazilian company named",
    "is a lesser known company or a new company that has not yet"
    "established a significant online presence.",
    "Can you provide me with more information or "
    "context about the company you are referring to in order to"
    "I don^t have access to the latest information or knowledge about Brazilian companies.",
    "current information, but as of my training data I can give you some information about",
    "verify the credibility of a company before investing or sharing personal information.",
    "context or specific information about the company or the question you have in mind?",
    "current or updated information beyond what is publicly available on the internet.",
    "current information about companies in Brazil, and there is no information about",
    "I do not have the ability to browse the internet to find the current information"
    "Furthermore, there are no results found on the internet about a company called",
    "some general information about the Brazilian agriculture and livestock sector.",
    "I don^t have access to the latest information - please note that the data",
    "this company may not exist, or it may have a different name or spelling.",
    "as it does not seem to be a legitimate financial institution in Brazil.",
    "I was not able to find any information on a Brazilian company called",
    "there is no information available about a Brazilian company called",
    "real-time database and updates about all Brazilian companies.",
    "Below is the available information on this Brazilian company",
    "Please provide accurate details for me to assist you better.",
    "I don^t have access to real-time information and databases.",
    "the current information and updates related to the company",
    "Without more information, this is as much as I can provide.",
    "the latest news and information about specific companies.",
    "is no longer in operation or is a small, local business.",
    "it is a small or local financial institution in Brazil.",
    "However, here is the information we could find online.",
    "I am not privy to the latest updates or news regarding",
    "you with some general information on the company.",
    "provided below may be out-of-date or inaccurate.",
    "any information about a Brazilian company named",
    "as it does not seem to be a well-known company.",
    "browse the internet and access information that current information, but here is what I found",
    "If you have any more information or details,",
    "I don^t have access to current information.",
    "real-time information on certain companies.",
    "to aid me in providing an accurate answer.",
    "and I would be happy to help you further.",
    "the latest information or current events.",
    "I^m sorry, but as an AI language model, ",
    "Unfortunately, as an AI language model,",
    "you with some general information about",
    "but I cannot provide information about",
    "I cannot provide information regarding",
    "There may be several reasons for this.",
    "However, here is a brief overview of",
    "However, to the best of my knowledge,",
    "up-to-date information on companies.",
    "Can I help you with anything else?",
    "I could not find a company named",
    "you some basic information about",
    "It^s possible that this company",
    "Sorry, as an AI language model,",
    "However, based on my research,",
    "about this Brazilian company,",
    "Can you please provide more ",
    "I have no information about",
    "is not publicly available.",
    "It is highly possible that",
    "as an AI language model, ",
    "As an AI language model,",
    "I do not have access to ",
    "However, I can provide ",
    "I don^t have access to ",
    "on the current state of",
    "real-time information.",
    "the latest information",
    "details or context?",
    "It is possible that",
    "please let me know ",
    "assist you better?",
    "It is important to",
    "I couldn^t find",
    "I^m sorry, but",
    "I am sorry, ",
]
brd_inoperative_list_len = len(brd_inoperative_list)


brd_inoperative_set = set()
for indx in range(brd_inoperative_list_len):
    brd_inoperative_set.add(brd_inoperative_list[indx])
brd_inoperative_set_len = len(brd_inoperative_set)
# print(f"\n===BRD API=> Inoperative  <{brd_inoperative_set_len}> entries:\n {brd_inoperative_set}")


brd_platitudes_list = [
    "Claro!",
    "Claro,  aqui está alguma informação sobre a ",
    "Claro.",
    "Claro. Aqui está alguma informação sobre a ",
    "Claro. Aqui está algumas informações sobre a ",
    "Claro., ''",
    "Do you have any other questions for me?",
    "Do you have any other questions for me?, ''",
    "Do you have other questions?",
    "Do you have other questions?, ''",
    "here is some information about ",
    "Here is some information about ",
    "Here are some additional details about",
    "Here^s what I found about",
    "Here is the merged text:",
    "I am still under development and learning to follow instructions carefully.",
    "I apologize for any inconvenience this may cause., ''",
    "I apologize for providing additional information in my previous response. ",
    "I don^t have any information about that company. ",
    "I hope this helps!",
    "I hope this information is helpful. ",
    "I will not provide any additional information about the company.",
    "Is there anything else I can help you with?",
    "Let me know if you have any other questions.",
    "Please let me know if you have any other questions.",
    "Sure! ",
    "Sure! Here is some information about ",
    "Sure,  I understand.",
    "Sure, ",
    "Sure. I can merge the two texts into a single non-redundantAbout",
    "without missing any key points",
    "without explicitly referencing the original text.",
]
brd_platitudes_list_len = len(brd_platitudes_list)


def brd_cia_about(cia_name):
    """
    => Prompts BRD for an about of a company
    :param cia_name:
    :return: trouble_flag, cia_about
    """
    query = "Tell me about this Brazilian company:" + cia_name + "? "
    response = brd_bard.get_answer(query)["content"]
    # print(f"===BRD_CiaAbout=> BRD Response to company {cia_name} is:\n{response}")
    trouble_flag = brd_check_traffic_trouble(response)
    cia_about = brd_clean_reply_about(response)
    return trouble_flag, cia_about


def brd_clean_reply_about(reply):
    """
    => Removes special characters + BRD Noise
    :param reply:
    :return: clean_reply
    """
    clean_reply = reply.replace("\r\n", "")
    clean_reply = clean_reply.replace("\n\n", "")
    clean_reply = clean_reply.replace("\r\n", "")
    clean_reply = clean_reply.replace("\n", "")
    clean_reply = clean_reply.replace("\r", "")
    clean_reply = clean_reply.replace("'", "^")
    clean_reply = clean_reply.replace(";", "&")

    # remove boiler plate statements
    for platitude in brd_platitudes_list:
        clean_reply = clean_reply.replace(platitude, "")
    clean_reply = clean_reply.strip()
    return clean_reply


def brd_cia_cnpj(cia_name):
    """
    => Prompts BRD for CNPJ of a company
    :param cia_name:
    :return: trouble_flag, cnpj_flag, cia_cnpj
    """
    two_stars = "**"

    query = (
        "Please do not provide any additional company information than the CNPJ number"
        "bracketed with '**':\n"
        "What is the CNPJ number for this Brazilian company:" + cia_name + "?"
    )
    response = brd_bard.get_answer(query)["content"]
    print(
        f"\n===BRD_CiaCNPJ=> For Cia: <{cia_name}> BRD CNPJ CRUDE response:\n{response}"
    )
    trouble_flag = brd_check_traffic_trouble(response)
    clean_response = brd_clean_reply_about(response)
    # print(f"\n===brd_cia_cnpj=> For Cia: <{cia_name}> CNPJ CLEANED response:\n{clean_response}" )
    star_flag, star_cnpj = find_marker_cnpj(clean_response, two_stars)
    if star_flag == "False":  # we are in the case BRD has not provided the ** mark
        posmark = clean_response.find(".")
        cia_cnpj = clean_response[posmark - 2 : posmark + 16]
        cnpj_flag = check_cnpj_format(cia_cnpj)
    else:
        cnpj_flag = star_flag
        cia_cnpj = star_cnpj
    return trouble_flag, cnpj_flag, cia_cnpj


def find_marker_cnpj(clean_response, marker):
    """
    => Finds cnpj string in BARDs response
    :param clean_response:
    :param marker:
    :return: cnpj_flag, cia_cnpj
    """
    cnpj_flag = "False"
    cia_cnpj = "#X#"
    pos1 = clean_response.find(marker)
    if pos1 > 0:
        clean_response_truncated = clean_response[pos1 + 2 :]
        # print(f"n===find_marker_cnpj=> responseTruncated: {clean_response_truncated}")
        pos2 = clean_response_truncated.find(marker)
        if pos2 > 0:
            cia_cnpj = clean_response_truncated[:pos2]
            # print(f"n===find_marker_cnpj=> CNPJ selected: <{cia_cnpj}>")
            cnpj_flag = check_cnpj_format(cia_cnpj)
    return cnpj_flag, cia_cnpj


def check_cnpj_format(cnpj):
    """
    => Checks if the cnpj data similar to format = 20.223.016/0001-70 (dd.ddd.ddd/dddd-dd)
    :param cnpj:
    :return: ok_flag
    """

    ok_flag = "False"
    pos1 = cnpj.find(".")
    cnpj2 = cnpj[pos1 + 1 :]
    pos2 = cnpj2.find(".")
    pos3 = cnpj2.find("/")
    pos4 = cnpj2.find("-")
    # print(f"\n===check_cnpj_format=> pos1: {pos1} ; pos2: {pos2} ;"
    # "pos3: {pos3} ; pos4:{pos4} ; length: {len(cnpj)}")
    if len(cnpj) == 18 and pos1 == 2 and pos2 == 3 and pos3 == 7 and pos4 == 12:
        ok_flag = "True"
    return ok_flag


def brd_check_traffic_trouble(reply):
    """
    => Checks if BRD is operational (network accessible)
    :param reply:
    :return: trouble_flag
    """
    trouble_flag = "False"
    error_mark = reply.find("Response Error:")
    network_mark = reply.find(
        "Temporarily unavailable due to traffic or an error in cookie values"
    )
    if error_mark >= 0 or network_mark >= 0:
        # print(f"\n===BRD_checkTrouble=> Flags raised: Error: {error_mark}"
        # "Traffic: {network_mark} in reply:\n {reply}" )
        trouble_flag = "True"
    return trouble_flag


def brd_check_about_pertinence(about):
    """
    => Checks if BRD reply is non-operative
    :param about:
    :return:
    """
    ok_flag = "True"
    if about in brd_inoperative_set:
        ok_flag = "False"
    return ok_flag


def brd_filter_platitudes(about):
    """
    => Remove BRD boilerplate platitudes
    :param about:
    :return:
    """
    for item in enumerate(brd_platitudes_list):
        about = about.replace(item, "")
    return about


def brd_get_industry(cia_name):
    """
    => Requests BRD API for the industry code of a company
    :param cia_name:
    :return: trouble_flag, response
    """
    query = (
        "Looking for Brazilian companies GICS Industry Code."
        "Provide the GICS code bracketed with the characters **'('(the format looks like this"
        "**.IBD.XXXXXXXX** where X is a digit - code MUST comprise 8 digits):"
        " ''' '')  What is the GICS Industry code for this Brazilian company:"
        + cia_name
        + " ?"
    )
    response = brd_bard.get_answer(query)["content"]
    trouble_flag = brd_check_traffic_trouble(response)
    return trouble_flag, response


def brd_get_industry_into_sector(cia_name, sector_code):
    """
    => Requests BRD API to regenerate response due to erroneous sector
    :param cia_name:
    :param sector_code:
    :return: trouble_flag, response
    """
    query = (
        " For brazilian company: " + cia_name + "you provided <" + sector_code + ">"
        "as GICS Sector Code: This is incorrect because GICS sector code must take on of "
        "the values in this entry_list: sectorList= [10,15,20,35,40,45,50,55,60,65]"
        "Provide the GICS code bracketed with the characters ** ."
        "Watch your regenerated response more carefully  "
        "What is the GICS Industry code for this Brazilian company:" + cia_name + " ?"
    )
    response = brd_bard.get_answer(query)["content"]
    trouble_flag = brd_check_traffic_trouble(response)
    return trouble_flag, response


def cia_search_sub_industry(text):
    """
    => SubIndustry pattern matching in a text string in format <.IBD.15104030>
    :param text:
    :return: ok_flag, cia_sector, cia_industry, cia_sub_industry
    """
    gics_sector_list = [
        "10",
        "15",
        "20",
        "25",
        "30",
        "35",
        "40",
        "45",
        "50",
        "55",
        "60",
    ]
    # industry format = .IBD.15104030
    ok_flag = "False"
    cia_sector = "#X#"
    cia_industry = "#X#"
    cia_sub_industry = "#X#"
    regex_sub_industry = re.compile(r".IBD.\d\d\d\d\d\d\d\d")
    if regex_sub_industry.search(text):
        result_sub_industry = regex_sub_industry.search(text)
        group_sub_industry = result_sub_industry.group()
        cia_sub_industry = group_sub_industry.replace(".IBD.", "")
        cia_sector = cia_sub_industry[0:2]
        if cia_sector in gics_sector_list:
            ok_flag = "SectorIncorrect"
            cia_industry = cia_sub_industry[0:6]
        else:
            ok_flag = "SectorIncorrect"
    else:  # Bard is not trustful and keeps missing the last digit
        regex_sub_industry = re.compile(r".IBD.\d\d\d\d\d\d\d")
        if regex_sub_industry.search(text):
            result_sub_industry = regex_sub_industry.search(text)
            group_sub_industry = result_sub_industry.group()
            # the last digit BRD is missing we need to add it
            cia_sub_industry = group_sub_industry.replace(".IBD.", "") + "0"
            cia_sector = cia_sub_industry[0:2]
            if cia_sector in gics_sector_list:
                cia_industry = cia_sub_industry[0:6]
                ok_flag = "Suspicious"
            else:
                ok_flag = "SectorIncorrect"
    return ok_flag, cia_sector, cia_industry, cia_sub_industry


print(
    f"\n===FixIncome Module=> <BRD Variable & Routines> 20231028-v4 exec@: {date_stamp()} "
)
