#!/usr/bin/env python
# coding: utf-8

"""
# => Module-General - Files Operations <2021030-v6>
def fpath(directory,filename): path => Creates path for directory/filename
def open_file_reader(file): okFlag, fi => Checks file - set reader utf8 newline '' delimiter ';'
def open_file_writer(file): okFlag, fo => Checks file - set writer utf8 newline '' delimiter ';'
def openFile_ReadWriter(path_file): okFlag, fio, win, wout => Set R/W utf8 newline '' delimiter ';'
def open_csv_reader(path_file): okFlag, fi, win => Checks file - set csv.reader utf-8 delimiter ';'
def open_csv_writer(path_file) => Checks file - set csv.writer utf-8 delimiter ';' newline = ''
def read_file(path): word_chain => read file considering utf8 encoding
def save_file_jason(index,path): => saves tp a JSON file with utf-8 encoding
def open_file_jason(path): index => open and read json file extension with encoding utf8
def restore_set_jason(path_file): okFlag, localSet => Checks file - Restore Set from a Jason file
def create_dict_json(newfile): okFlag, fd => Creates an empty dictionary and save into a jason file
def restore_dict_jason(path_file): okFlag, jasonDict => Checks file - Restore Dict from a Jason file
def save_dict_json(path_file, dict_2_save): flagOK => Save dictionary in Json file
def read_oneline(fr): one_line => read new one_line
def initialize_log_file (file,hdr): wout, fo => Setup Log file to write including header Line
def csv_2_scsv_converter(file):inFlag, outFlag => Transform CSV file into a ';' separator  text file
def csv_2_scsv_cia_record_converter(file): inFlag, outFlag =>  ',' to ';' about field preserved
"""

import os.path
import json
import csv
from modgen_timestamp import date_stamp
from modgen_manipulating_python_structures import pairlist_to_dict
from modgen_chain_manipulation import items_separator_converter


def file_path(directory, filename):
    """
    => Creates path for directory/filename
    :param directory:
    :param filename:
    :return: path
    """
    path = directory + "/" + filename
    return path


def open_file_reader(file):
    """
    => Checks file existence - set reader utf8 newline '' delimiter ';'
    :param file:
    :return: ok_flag, fi
    """
    # file contains the full path of the file
    ok_flag = "True"
    check_file = os.path.isfile(file)
    print(f"\n===open_file_reader=> Does File: <{file}> Exists? => {check_file}")
    if check_file:
        print(
            f"\n===open_file_reader=> check_file states that <{file}> EXISTS <{check_file}"
        )
        fi = open(file, "r", encoding="utf−8", newline="")
    else:
        print(
            f"\n===open_file_reader=> File  <{file}> DOES NOT EXIST => check_file: <{check_file}"
        )
        ok_flag = "False"
        fi = None
    return ok_flag, fi


def open_file_writer(file):
    """
    => Checks file existence - set writer utf8 newline '' delimiter ';'
    :param file:
    :return: ok_flag, fo
    """
    ok_flag = "True"
    fo = "False"
    check_file = os.path.isfile(file)
    print(f"\n===open_file_writer=> Does File: <{file}> Exists? => {check_file}")
    if check_file:
        # print(f"\n===open_file_writer=> check_file states that <{file}> EXISTS <{check_file}")
        fo = open(file, "a", encoding="utf−8", newline="")
    else:
        # print(
        # f"\n===open_file_writer=> check_file states that <{file}> DOES NOT EXIST:
        # <{check_file} => open new file"
        # )
        fo = open(file, "a", encoding="utf−8", newline="")
        ok_flag = "False"
    return ok_flag, fo


def open_file_reader_writer(path_file):
    """
    => Checks file existence - set R/W utf8 newline '' delimiter ';'
    :param path_file:
    :return:
    """
    input_file = path_file + ".txt"
    ok_flag = "True"
    win = "False"
    wout = "False"
    fio = "False"
    check_file = os.path.isfile(input_file)
    print(
        f"\n===open_file_reader_writer=> Does File: <{input_file}> Exists? => {check_file}"
    )
    if check_file:
        # print(
        # f"\n===open_file_reader_writer=> check_file states that
        # <{input_file}> EXISTS <{check_file}"
        # )
        fio = open(input_file, "r+", encoding="utf−8", newline="")
        win = csv.reader(fio, delimiter=";")
        wout = csv.writer(fio, delimiter=";")
    else:
        # print(
        # f"\n===open_file_reader_writer=> check_file states that
        # <{input_file}> DOES NOT EXIST: <{check_file}"
        # )
        ok_flag = "False"
    return ok_flag, fio, win, wout


def open_csv_reader(path_file):
    """
    => Checks file existence - set csv.reader utf-8 delimiter ';'
    :param path_file:
    :return:ok_flag, fo, wout
    """
    input_file = path_file + ".csv"
    ok_flag = "True"
    win = "False"
    fi = "False"
    check_file = os.path.isfile(input_file)
    print(f"\n===open_csv_reader=> Does File: <{input_file}> Exists? => {check_file}")
    if check_file:
        # print(
        # f"\n===open_csv_reader=> check_file states that <{input_file}> EXISTS <{check_file}"
        # )
        fi = open(input_file, "r", encoding="utf−8")
        win = csv.reader(fi, delimiter=";")
    else:
        # print(
        # f"\n===openLogFile_Reader=> check_file states that <{input_file}> DOES NOT EXIST:
        # <{check_file}"
        # )
        ok_flag = "False"
    return ok_flag, fi, win


def open_csv_writer(path_file):
    """
    Checks file existence - set csv.writer utf-8 delimiter ';' newline = ''
    :param path_file:
    :return:
    """
    output_file = path_file + ".csv"
    ok_flag = "True"
    wout = "False"
    fo = "False"
    check_file = os.path.isfile(output_file)
    print(f"\n===open_csv_reader=> Does File: <{output_file}> Exists? => {check_file}")
    if check_file:
        # print(f"\n===open_csv_reader=> check_file states that <{inputFile}> EXISTS <{check_file}")
        fo = open(output_file, "a", encoding="utf−8", newline="")
        wout = csv.writer(fo, delimiter=";")
    else:
        # print(
        # f"\n===openLogFile_Reader=> check_file states that <{inputFile}> DOES NOT EXIST:
        # <{check_file}"
        # )
        ok_flag = "False"
        fo = open(output_file, "a", encoding="utf−8", newline="")
        wout = csv.writer(fo, delimiter=";")

    return ok_flag, fo, wout


def read_file(path):
    """
    => Reads file encoding utf-8 - returns a chain of words
     :param path:
     :return: word_chain
    """
    with open(path, encoding="utf−8") as f:
        word_chain = f.read()
    return word_chain


def save_file_jason(index, path):
    """
    # 08 => Saves Python object into a Jason file
    :param index:
    :param path:
    :return:
    """
    filename = path + ".json"
    with open(filename, "w", encoding="utf8") as fp:
        json.dump(index, fp, ensure_ascii=False)
        fp.close()
        print(f"\n===save_file_jason=> Just dumped index to {filename}")
    # return


def open_file_jason(path):
    """
    # 09 => Open and reads Jason file - encoding utf-8
    :param path:
    :return: index
    """
    filename = path + ".json"
    index = {}
    with open(filename, "r", encoding="utf8") as fp:
        index = json.load(fp)
        fp.close()
        print(f"\n===open_file_jason=> Just loaded {filename} as returned index")
    return index


def restore_set_jason(path_file):
    """
    => Checks file existence - Restore Set stored in a Jason file
    :param path_file:
    :return: ok_flag, local_set
    """
    local_set = {}
    ok_flag = "False"
    out_file = path_file + ".json"
    check_file = os.path.isfile(out_file)
    print(
        f"\n===restoreAcronymSet_jason=> Does File: <{out_file}> Exists? => {check_file}"
    )
    if check_file:
        # print(f"\n===restoreAcronymSet_jason=> jason file <{out_file}> EXISTS: <{check_file}")
        local_list = open_file_jason(path_file)
        local_set = set(local_list)
        ok_flag = "True"
    return ok_flag, local_set


def create_dict_json(newfile):
    """
    => Creates an empty jason file open for write
    # !! This routine makes no sense should be discarded
    :param newfile:
    :return: check_file, fd

    If newfile does not exist Create a new file open for write -
    Returns
        > check_file 'True' if newfile already exists
        > fd : the file pointer

    Args:
    newfile: The path to the JSON file to create.
    """

    check_file = os.path.isfile(newfile)
    print(f"\n===createDict_jason=>  Does File <{newfile}> Exist?: <{check_file}>")
    fd = open(newfile, "w", encoding="utf8")
    return check_file, fd


def restore_dict_jason(path_file):
    """
    => Check file existence - Restore Dictionary stored in a Jason file
    :param path_file:
    :return: ok_flag, jason_dict
    """
    jason_dict = {}
    ok_flag = "False"
    jason_file = path_file + ".json"
    check_file = os.path.isfile(jason_file)
    print(
        f"\n===restore_dict_jason=>  Does File: <{jason_file}> Exist?: <{check_file}>"
    )
    if check_file:
        # print(
        # f"===restore_dict_jason=> os.path returned that jason file <{jason_file}>
        # EXISTS: <{check_file}"
        # )
        jason_list = open_file_jason(path_file)
        jason_dict = pairlist_to_dict(jason_list)
        ok_flag = "True"
    return ok_flag, jason_dict


def save_dict_json(path_file, dict_2_save):
    """
    => Save dictionary in a jason file - if jason file does not exists a new file will be created
    Args:    path_file: The path to the JSON file to save to.
    dictionary: The dictionary to save.
    Returns: ok_flag = 'True' if file already exited
    """
    jason_file = path_file + ".json"
    ok_flag, fd = create_dict_json(jason_file)
    # Save the dictionary to the JSON file.
    json.dump(dict_2_save, fd)
    # Close the JSON file.
    fd.close()

    return ok_flag


def read_oneline(fr):
    """
    => Reads one one_line in open file 'fr'
    :param fr:
    :return: one_line
    """
    line = fr.readline()
    return line


def initialize_log_file(file, hdr):
    """
    => setup Log file to write including header Line
    :param file:
    :param hdr:
    :return: wout, fo
    """
    check_file = os.path.isfile(file)
    print(f"\n===initialize_log_file=> Does File: <{file}> Exists?: <{check_file}>")
    fo = open(file, "a", encoding="utf−8", newline="")
    wout = csv.writer(fo, delimiter=";")
    if check_file != "True":
        # print(f"===initialize_log_file=> As <{file}> does not exists creating header Line")
        wout.writerow(hdr)
    return wout, fo


def csv_2_scsv_converter(file):
    """
    => Transform a csv comma delimited file into a semicolon delimited text file
    :param file:
    :return:
    """
    out_flag = "False"
    infile = file
    outfile = file.replace(".csv", ".txt")
    in_flag, fi = open_file_reader(infile)
    if not in_flag:
        print(
            f"\n===csv_2_scsv_converter=> Cannot convert problem with files:"
            f" in_flag:<{in_flag}> out_flag: <{out_flag}>"
        )
    else:
        out_flag, fo = open_file_writer(outfile)
        while input_line := fi.readline():
            input_list, _ = items_separator_converter(input_line, ",")
            output_line = ""
            for item in input_list:
                output_line = output_line + item + ";"
            output_line = output_line[:-1] + "\r\n"
            fo.write(output_line)
        out_flag = "True"
        fi.close()
        fo.close()
    return in_flag, out_flag


def csv_2_scsv_cia_record_converter(file):
    """
    => Transform a csv ',' delimited cia file into a ';' delimited text file preserving about field
    :param file:
    :return: in_flag, out_flag
    """
    out_flag = "False"
    outfile = file.replace(".csv", ".txt")
    in_flag, fi = open_file_reader(file)
    if not in_flag:
        print(
            f"\n===csv_2_scsv_converter=> Cannot convert problem with files: in_flag:<{in_flag}>"
            f"out_flag: <{out_flag}>"
        )
    else:
        out_flag, fo = open_file_writer(outfile)
        # let´s first read the header
        header_line = fi.readline()
        header_line = header_line.replace(",", ";")
        fo.write(header_line)
        while input_line := fi.readline():
            # we are going to extract the about column to preserve it's integrity
            about_pos = input_line.find('"')
            if about_pos < 0:  # the about field is empty and equal to '#X#'?
                about = "#X#"
                record = input_line[:-4]
            else:
                about = input_line[about_pos:]
                record = input_line[0:about_pos]
            record_list, _ = items_separator_converter(record, ",")
            output_line = ""
            for item in record_list:
                output_line = output_line + item + ";"
            # !! output_line = output_line + about + '\r\n' # '\r'\n' should not be added?
            output_line = output_line + about
            fo.write(output_line)
        out_flag = "True"
        fi.close()
        fo.close()
    return in_flag, out_flag


print(f"\n===FixInc Module=> <Files Operations 2021030-v6> exec@: {date_stamp()}")
