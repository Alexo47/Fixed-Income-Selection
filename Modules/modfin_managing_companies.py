#!/usr/bin/env python
# coding: utf-8


"""
=> Module-FixIncome - ManagingCompanies 20231020-v5
def match_cia_name(company): foundFlag,CompanyName => Scan Cia name to search Neo4j with UI
def test_acronym_token(token,limit): limitFlag,ciaMatchHits => checks if Neo4j Hits > user set limit
def adjust_cia_name(name): CompanyName => Adjusts auxiliary words that do not need Capital letters
def correct_spelling_company_name(cia_name): cia_name => Checks misspelled words in Company Names
def clean_company_name(cia_name): cia_name => Removes Companies registration status such as S.A.
def check_cnpj_format(cnpj): okFlag => checks if Cia CNPJ data looks like a CNPJ number
def search_cnpj(text): okFlag,ciaCNPJ =>
def find_marker_cnpj(clean_response,marker): cnpjFlag,ciaCNPJ => scan for cnpj format sequence
def init_acronyms_file(file,header): fio,win,wout => Launch csv readers/writers processing
def restore_acronym_set(file): acronymSet,len(acronymSet) => Process file with acronyms to a set
def open_acronyms_import_read(file): okFlag,fi,win => Checks file existence Open file csv.reader
def cleanReplyAbout(reply): cleanReply => Removes CR/NL and replaces - <'> by <^> ; <;> by <&>
"""

import re
import os
import csv
import spacy

# from ModFin_N4J import n4j_get_acr_match  #!! due to circular errors import at the function level
from modgen_timestamp import date_stamp
from modgen_user_interaction_routines import usr_hitlist_choice
from modgen_user_interaction_routines import usr_confirm_company
from modfin_global_definitions import FILES_DIR
from modgen_chain_manipulation import items_separator_converter

# Load the spaCy model.

nlp = spacy.load("en_core_web_sm")


def match_cia_name(company):
    """
    => Scan cia_name as tokens to search Neo4j + UI
    :param company:
    :return: found_flag,company_name
    """
    from modfin_n4j import n4j_get_acr_match

    company_name = company.strip()
    company_words = nlp(company)
    found_flag = "False"
    # print(f"\n===match_cia_name=> company_name: {company_words}")
    for token in company_words:
        if found_flag == "False":
            hits, hit_list = n4j_get_acr_match(token.text)
            # print(f"\n===match_cia_name=> For {token} Neo4j returned: {hits} hits")
            if hits >= 1:  # There are at least one match
                # print(
                # f"\n===match_cia_name=> Neo4j FOUND {hits} ENTRIES for acronym {token.text}"\
                # "in Company: {company_name}" \
                # ")"
                # print(f"\n===match_cia_name=>  The multiple entries found are: {hit_list}")
                found_flag, company_selected = usr_hitlist_choice(company_name, hit_list)
            else:
                # print(\
                # f"\n===match_cia_name=> Neo4j DID NOT MATCH the acronym <{token.text}>"\
                # "in Company: {company}"\
                # ")"
                found_flag = "False"

    if found_flag == "False":
        # !! usr_confirm_company replaced another function that was renamed  <= CHECK!
        found_flag, company_name = usr_confirm_company(company)
    # print(f"\n===match_cia_name=> returns: {company_name}")
    return found_flag, company_name


def test_acronym_token(token, limit):
    """
    => Checks if Neo4j Hits > than user set limit
    :param token:
    :param limit:
    :return: limit_flag,cia_match_hits
    """
    from modfin_n4j import n4j_get_acr_match

    limit_flag = "False"
    # print(f"\n===test_acronym_token=> Token: {token}")
    cia_match_hits, cia_match_list = n4j_get_acr_match(token)
    # print(f"\n===test_acronym_token=> For {token} Neo4j returned: {cia_match_hits} hits")
    if cia_match_hits > limit:
        limit_flag = "True"
        # print(f"\n===test_acronym_token=> For <{token}> overflow detected {cia_match_hits} hits")
    return limit_flag, cia_match_hits


def adjust_cia_name(name):
    """
    => Adjusts auxiliary words that do not need Capital letters
    :param name:
    :return: company_name
    """
    company_name = name
    company_name = company_name.replace(" De ", " de ")
    company_name = company_name.replace(" Do ", " do ")
    company_name = company_name.replace(" Da ", " da ")
    company_name = company_name.replace(" Das ", " das ")
    company_name = company_name.replace(" E ", " & ")
    return company_name


def correct_spelling_company_name(cia_name):
    """
    => Checks misspelled words in Company Names
    !! this version is clunky we need to manage with a dictionary and save/restore in JSON file
    :param cia_name:
    :return: cia_name
    """

    # adjustments
    # cia_name = cia_name.replace(',',' ' ) comma replacement must be done @Excel level
    # EXTENSION ACRONYMES
    cia_name = cia_name.replace(" ADM ", " ADMINISTRAÇÃO ")
    cia_name = cia_name.replace(" ART. ", " ARTIGOS ")
    cia_name = cia_name.replace(" BRA ", " BRASILEIRA ")
    cia_name = cia_name.replace("CIA ", "COMPANHIA  ")
    cia_name = cia_name.replace("CIA. ", "COMPANHIA  ")
    cia_name = cia_name.replace(" CRED. ", " CRÉDITO ")
    cia_name = cia_name.replace(" COM. ", " COMÉRCIO ")
    cia_name = cia_name.replace(" EMPREEND ", " EMPREENDIMENTOS ")
    cia_name = cia_name.replace(" EMPREENDS ", " EMPREENDIMENTOS ")
    cia_name = cia_name.replace(" EMPRS ", " EMPRESA ")
    cia_name = cia_name.replace(" ENERG ", " ENERGIA ")
    cia_name = cia_name.replace(" ENG. ", " ENERGIA ")
    cia_name = cia_name.replace(" EQUIP. ", " EQUIPAMENTOS ")
    cia_name = cia_name.replace(" FIN. ", " FINANCEIRO ")
    cia_name = cia_name.replace(" GER. ", " GERACÂO ")
    cia_name = cia_name.replace(" HOSP. ", " HOSPITALARES ")
    cia_name = cia_name.replace(" IND. ", " INDUSTRIA ")
    cia_name = cia_name.replace(" INDs ", " INDUSTRIAS ")
    cia_name = cia_name.replace(" INFRA ", " INFRAESTUTURA ")
    cia_name = cia_name.replace(" PARTICIP ", " PARTICIPAÇÕES ")
    cia_name = cia_name.replace(" PROP ", " PROPRIEDADES ")
    cia_name = cia_name.replace(" PUB ", " PUBLICA ")
    cia_name = cia_name.replace(" PARTS ", " PARTICIPAÇÕES ")
    cia_name = cia_name.replace(" TRANSM ", " TRANSMISSÃO ")

    # CORRECTIONS ORTHOGRAPHIES

    cia_name = cia_name.replace("ACO", "AÇO")
    cia_name = cia_name.replace("AGUAS", "ÁGUAS")
    cia_name = cia_name.replace("CONCESSIONARIA ", "CONCESSIONÁRIA ")
    cia_name = cia_name.replace("COMERCIO", "COMÉRCIO")
    cia_name = cia_name.replace("COSMETICO", "COSMÉTICOS")
    cia_name = cia_name.replace("EDUCACAO", "EDUCAÇÃO")
    cia_name = cia_name.replace("ELETRICA", "ELÉTRICA")
    cia_name = cia_name.replace("GAS", "GÁS")
    cia_name = cia_name.replace("GERACAO", "GERAÇÃO")
    cia_name = cia_name.replace("OLEO", "OLÉO")
    cia_name = cia_name.replace("PARTICIPAÇOES", "PARTICIPAÇÕES")
    cia_name = cia_name.replace("TRANSMISSAO", "TRANSMISSÃO")
    cia_name = cia_name.replace("TRANSMISSAO", "TRANSMISSÃO")
    cia_name = cia_name.strip()
    return cia_name


def clean_company_name(cia_name):
    """
    => Removes Companies registration status such as S.A., etc
    :param cia_name:
    :return: cia_name
    """
    cia_name = cia_name.strip()
    cia_name = cia_name.replace(" S/A.", "")
    cia_name = cia_name.replace(" S/A", "")
    cia_name = cia_name.replace(" S.A.", "")
    cia_name = cia_name.replace(" S.A.", "")
    cia_name = cia_name.replace(" S.A", "")
    cia_name = cia_name.replace(" Ltd.", "")
    token_sa = cia_name[-3:]
    if token_sa == " SA":
        cia_name = cia_name.replace(" SA", "")
    # we need to replace <'> by '^'
    cia_name = cia_name.replace("'", "^")
    return cia_name


def check_cnpj_format(cnpj):
    """
    => checks if Cia CNPJ data looks like a CNPJ number format such as  '20.223.016/0001-70'
    :param cnpj:
    :return: ok_flag
    """
    ok_flag = "False"
    pos1 = cnpj.find(".")
    cnpj2 = cnpj[pos1 + 1:]
    pos2 = cnpj2.find(".")
    pos3 = cnpj2.find("/")
    pos4 = cnpj2.find("-")
    # print(\
    # f"\n===check_cnpj_format=> pos1: {pos1} ; pos2: {pos2} ; pos3: {pos3} ;"\
    # pos4:{pos4} ; length: {len(cnpj)}"\
    # )
    if len(cnpj) == 18 and pos1 == 2 and pos2 == 3 and pos3 == 7 and pos4 == 12:
        ok_flag = "True"
    return ok_flag


def search_cnpj(text):
    """
    => search CNPJ pattern in a text
    :param text:
    :return: ok_flag,cia_cnpj
    """
    # cnpj format = 20.223.016/0001-70
    ok_flag = "False"
    cia_cnpj = "#X#"
    regex_cnpj = re.compile(r"\d\d.\d\d\d.\d\d\d/\d\d\d\d-\d\d")
    if regex_cnpj.search(text):
        cnpj = regex_cnpj.search(text)
        cia_cnpj = cnpj.group()
        ok_flag = "True"
    return ok_flag, cia_cnpj


def find_marker_cnpj(clean_response, marker):
    """
    =>scan a string to find a cnpj format sequence
    :param clean_response:
    :param marker:
    :return: cnpj_flag, cia_cnpj
    """
    cnpj_flag = "False"
    cia_cnpj = "#X#"
    pos1 = clean_response.find(marker)
    if pos1 > 0:
        clean_response_truncated = clean_response[pos1 + 2:]
        # print(f"n===find_marker_cnpj=> responseTruncated: {clean_response_truncated}")
        pos2 = clean_response_truncated.find(marker)
        if pos2 > 0:
            cia_cnpj = clean_response_truncated[:pos2]
            # print(f"n===find_marker_cnpj=> CNPJ selected: <{cia_cnpj}>")
            cnpj_flag = check_cnpj_format(cia_cnpj)
    return cnpj_flag, cia_cnpj


def init_acronyms_file(file, header):
    """
    => Sets the csv readers/writers to start acronym processing - !! needs review/upgrade
    :param file:
    :param header:
    :return:
    """
    file_path = FILES_DIR + "/" + file + ".txt"
    check_file = os.path.isfile(file_path)
    # print(f"\n===initAcronymFile=> for file <{file}> check_file gives: <{check_file}>")
    if check_file:
        print(
            f"\n===initAcronymFile=> check_file states that Acronym file"
            "<{path_file}> EXISTS: <{check_file}"
        )
        fio = open(file_path, "r+", encoding="utf−8", newline="")
        wout = csv.writer(fio, delimiter=";")
        win = csv.reader(fio, delimiter=";")
    else:
        print(
            f"\n===initAcronymFile=> CheckFile states that Acronym file"
            "<{path_file}> DOES NOT EXIST: <{check_file}"
        )
        fio = open(file_path, "a", encoding="utf−8", newline="")
        wout = csv.writer(fio, delimiter=";")
        win = "#X#"
        wout.writerow(header)
    return fio, win, wout


def restore_acronym_set(file):
    """
    => Process file containing acronyms to a set
    # The csv file has been replaced by a jason file with def restore_set_jason(filePath):
    :param file:
    :return: acronym_set, len(acronym_set)
    """
    ok_flag, fi, win = open_acronyms_import_read(file)
    if ok_flag == "True":
        # print(f"\n Return from open_AcronymsImport Reader After if ok_flag: {ok_flag} ")
        acronym_set = set()
        # we skip the input file header
        header_line = fi.readline()
        while input_line := fi.readline():
            input_list, input_list_len = items_separator_converter(input_line, ";")
            # print(\
            # f"\n InputList in: {inputLine} , has {input_list_len} items, namely:\n{input_list}"\
            # )
            acronym_set.add(input_list[2])
        fi.close()
    else:
        acronym_set = set()
        acronym_count = 0
    return acronym_set, len(acronym_set)


def open_acronyms_import_read(file):
    """
    => Checks file existence Open file csv.reader
    !! this routine can be replaced by def open_file_reader(filePath): return ok_flag,fi,win
    :param file:
    :return: ok_flag, fi,win
    """
    input_file_path = FILES_DIR + "/" + file + ".txt"
    ok_flag = "True"
    win = "False"
    fi = "False"
    check_file = os.path.isfile(input_file_path)
    # print(f"\n !!! Acronyms check_file: <{check_file}>")
    if check_file:
        print(
            f"\n===open_acronyms_import_read=> CheckFile states that ACRONYMS file\
             <{input_file_path}> EXISTS <{check_file}"
        )
        fi = open(input_file_path, "r", encoding="utf−8", newline="")
        win = csv.reader(fi, delimiter=";")
    else:
        print(
            f"\n===open_acronyms_import_read=> CheckFile states that ACRONYMS file\
            <{input_file_path}> DOES NOT EXIST: <{check_file}"
        )
        ok_flag = "False"
    return ok_flag, fi, win


def clean_about(reply):
    """
    => Removes CR/NL to make about in one one_line - replaces <'> by <^> and <;> by <&>
    :param reply:
    :return: clean_reply
    """
    clean_reply = reply.replace("\n", "")
    clean_reply = clean_reply.replace("'", "^")
    clean_reply = clean_reply.replace(";", "&")
    return clean_reply


print(f"\n===FixInc Module=> <ManagingCompanies 20231020-v5> exec@: {date_stamp()}")
