# !/usr/bin/env python
# coding: utf-8
# from IPython import get_ipython

# ###  ROB-CIA_N4J-SCSV_MergeUpload - SetUp - Imports

# ## General Imports
import Modules.ModHead
from Modules.ModHead import *

# ## Import Neo4j - Open Session
import ModFin_N4J as Mn4j
from ModGen_ManipulatingPythonStructures import split_csvrow_into_dict

print(f"\n===ROB-CIA_N4J-SCSV_MergeUpload=> <Setup Import>")


# ### ROB-CIA_N4J-SCSV_MergeUpload BEGINS HERE
# This routine interacts with Neo4j to Upload CIA Records stored in the input file
# Each line of the input SCSV file is a record containing the following columns (header structure)
#
# ###

print(f"\n===ROB-CIA_N4J-SCSV_MergeUpload=> <BEGINS HERE> exec@: {date_stamp()}")


# ###  ROB-CIA_N4J-SCSV_MergeUpload - Input/Output files


cia_file_name = 'CIA-SCSV_ReferenceData_201027-v2'
cia_file_path = Mgv.filesDir + "/" + cia_file_name
cia_file_csv = cia_file_path + '.csv'
cia_file_txt = cia_file_path + '.txt'

# ## we need to convert the .csv file into a semi-column separated text file with the same name
input_flag, output_flag = Mfil.CSV_2_SCSV_CiaRecord_Converter(cia_file_csv)


cia_flag, fi = Mfil.openFile_Reader(cia_file_txt)
if not cia_flag:
    print(f"\n===ROB-CIA_N4J-SCSV_MergeUpload=> Input file {cia_file_csv} Not Available - Fatal Error Code 1")
    exit(99)
    

# create new Jason file containing an empty dictionary
cia_renamed_dict = {}
dict_file_name = 'DICT-CVM_CiaRename_20231024-v3'
dict_file_path = Mgv.filesDir + "/" + dict_file_name
dict_file = dict_file_path + '.json'
# dictFlag = Mfil.saveDict_json(dict_file_path,cia_renamed_dict) # we will do this at the end entries in the dictionary
cia_renamed_dict_len = len(cia_renamed_dict)


log_file_name = 'RF$-LOG_CIA_N4j_UploadingRecords_20231027 -v1'
log_file_path = Mgv.filesDir + "/" + log_file_name
log_file = log_file_path + '.txt'
hdrLog = ['cvmcia_name', 'action']
wout_log, fo_log = Mfil.initializeLogFile(log_file, hdrLog)
logRecord = [None]*2

print(f"\n===ROB-CIA_N4J-SCSV_MergeUpload=> <Input/Output files> exec@: {date_stamp()}")

# ### ROB-CIA_N4J-SCSV_MergeUpload -  ENGINE Uploading Cia Records
#  Cia are directly uploaded to Neo4j FixInc database
### 

cia_record = [None]*11
cia_record_count = 0
add_count = 0
errorCount = 0
duplicate_count = 0
renamed_count = 0


cia_header = fi.readline()
cia_header = cia_header.replace('\r\n', '')
cia_header = cia_header.replace(',', ';')
print(f"\n===ROB-CIA_N4J-SCSV_MergeUpload=> Input File Header \n <{cia_header}> ")

# now we loop through records

# !! cia_reader = csv.DictReader(fi) this should be removed

while cia_record := fi.readline():
    cia_record_count += 1
    cia_record_list, cia_record_list_len = Mnlp.items_separator_converter(cia_record, ';')
    cia_name_original = cia_record_list[1]
    print('\n')
    print('x' * 120)
    print(f"======ROB-CIA_N4J-SCSV_MergeUpload=> Record#: {cia_record_count} - Processing:{cia_name_original}")
    cia_name_original_stripped = cia_name_original.strip()
    cia_name_clean = Mcia.adjustCiaName(cia_name_original_stripped)
    # ##
    # !! Below is an important decision all CiaNames will be stored in lowercase to avoid capitalization errors
    # ##
    cia_name_clean_lower = cia_name_clean.lower()
    if cia_name_clean_lower != cia_name_original:
        # print(f"\n===MergeUpload=> Looping cia_nameChanged {cia_name_original} adjusted to: {cia_name_clean_lower}")
        cia_record_list[1] = cia_name_clean_lower
        cia_renamed_dict[cia_name_original] = cia_name_clean_lower
        rename_flag = 'True'
        renamed_count += 1
        action = 'Renamed'
    # we need know to check if the Cia is not already in N4J Database
    cia_name = cia_record_list[1]
    n4jResp_len, n4jResp = Mn4j.N4J_checkCiaMatch(cia_name)
    # Let´s check if cia_name not in database
    if n4jResp_len > 0:
        print(f"\n===ROB-CIA_N4J-SCSV_MergeUpload=> cia_name <{cia_name}> already in database. N4j returned {n4jResp}")
        action = 'Duplicate'
        duplicate_count += 1
    else:
        query = Mn4j.N4J_buildQuery_MergeCia(cia_record_list)
        # print(f"===ROB-CIA_N4J-SCSV_MergeUpload=> Looping record {cia_record_list} translates into query: \n {query}")
        result = Mn4j.N4J_session.run(query)  # nodes_results contains nodes returned by neo4j following query
        result_list = [j[0] for j in result]  # register return as a list of nodes
        result_list_len = len(result_list)
        if result_list_len == 1:
            print(f"\n===ROB-CIA_N4J-SCSV_MergeUpload=> Looping Cia {cia_name} was ADDED to N4J> ")
            print('x' * 120)
            
            add_count += 1
            action = 'Added'
        else:
            print(f"\n===MergeUpload=> Looping Cia <{cia_record_list[1]}> N4J response is FISHY : {result_list} ")
            errorCount += 1
            action = 'Error'

    # Let's write the log line for this transaction
    log_line = cia_name_original + ';' + action + '\r\n'
    fo_log.write(log_line)

# ## we need now to close operations
# we need to save cia_renamed_dict
company_rename_list = Mpst.dict_to_pairlist(cia_renamed_dict)
Mfil.save_file_jason(company_rename_list, dict_file_path)

print(f"\n Processed:\n{cia_record_count} records;\n{renamed_count} renames;\n{add_count} Companies added;")
print(f" \n{duplicate_count} duplicates \n{errorCount} errors")

fi.close()
fo_log.close()

print(f"\n=== ROB-CIA_N4J_UploadAdditionalRecords  <ENGINE 20231024 - v1> exec@: {date_stamp()}")
