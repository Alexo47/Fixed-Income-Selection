#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# TEMPL A-0:Définitions Préliminaires : Horodateur


from datetime import datetime  # on veut tracer les executions
def date_stamp():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time


print(f"\n=== Cell A-0 <Définitions préliminaires> Executed")


# In[2]:


### hdr AppRF CDBs created from source AppRF HTML page
## 01: hdrSec_CBD, hdrSec_CBD_Record, hdrSec_CBD_len => Source AppRF
## 02: hdrSec_CVM_CSV. hdrSec_CVM_CSV_Record, hdrSec_CVM_CSV_len => AppRFsource file transformed in a csv database
## 03: hdrSec_XP,hdrSec_XP_Record,hdrSec_XP_len => Source XP manually grabbed from HTML page
## 04: hdrSec_XP_Offer, hdrSec_XP_Offer_Record, hdrSec_XP_Offer_len => XP Primary  UI Market HTML extraction
## 05: hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len => dictionnary of  CVM cia_name normalized,rough
## 06: hdrCia_MoodysRate, hdrCia_MoodysRate_Record, hdrCia_MoodysRate_len => Moodys Rating stuff
## 07: hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len => extracted/edited from CVM HTML page
## 08: hdrImpCia, hdrImpCia_Record, hdrImp_Record_len
## 09: hdrV1ImpCia, hdrV1ImpCia_Record, hdrV1Imp_Record_len

##01=> hdrSec_CBD, hdrSec_CBD_Record, hdrSec_CBD_len # AppRF HTML manually edited
hdrSec_CBD_Broker = "Nuinvest"
# Skip = "Investir" # this will removed
hdrSec_CBD_Category = 'CDB'
hdrSec_CBD_Rate = '0.27%'
hdrSec_CBD_Index = 'CDI'
hdrSec_CBD_Company = 'CARUANA FINANCEIRA'
hdrSec_CBD_MinInv =  1050
hdrSec_CBD_LastQuote = 1070.39
hdrSec_CBD_Yield = "1.94%"
hdrSec_CBD_Liquidity =  "No Vencimento"
hdrSec_CBD_RiskRate = "BBB"
hdrSec_CBD_Rater = 'Fitch'
hdrSec_CBD_ExpireDays = 60
hdrSec_CBD_ExpireDate = '2023-06-30'
hdrSec_CBD_KeyUniq =  '##' + hdrSec_CBD_Category +'#' + hdrSec_CBD_Rate + '#' + hdrSec_CBD_Index + '#' + hdrSec_CBD_Company + '#' + hdrSec_CBD_ExpireDate + '##'
hdrSec_CBD_EquivLabel= "LCI/LCA"
hdrSec_CBD_EquivRate = '96.88%'
hdrSec_CBD_EquivIndex ="CDI"
EOR = "#EOR#"

hdrSec_CBD = ['hdrSec_CBD_Broker','hdrSec_CBD_Category','hdrSec_CBD_Rate', 'hdrSec_CBD_Index', 'hdrSec_CBD_Company','hdrSec_CBD_MinInv','hdrSec_CBD_LastQuote','hdrSec_CBD_Yield', 'hdrSec_CBD_Liquidity','hdrSec_CBD_RiskRate','hdrSec_CBD_Rater','hdrSec_CBD_ExpireDays','hdrSec_CBD_ExpireDate','hdrSec_CBD_KeyUniq', 'hdrSec_CBD_EquivLabel', 'hdrSec_CBD_EquivRate','hdrSec_CBD_EquivIndex']
hdrSec_CBD_len = len(hdrSec_CBD)

hdrSec_CBD_Record = [hdrSec_CBD_Broker,hdrSec_CBD_Category,hdrSec_CBD_Rate,hdrSec_CBD_Index,hdrSec_CBD_Company,hdrSec_CBD_MinInv,hdrSec_CBD_LastQuote,hdrSec_CBD_Yield, hdrSec_CBD_Liquidity,hdrSec_CBD_RiskRate,hdrSec_CBD_Rater,hdrSec_CBD_ExpireDays,hdrSec_CBD_ExpireDate,hdrSec_CBD_KeyUniq,hdrSec_CBD_EquivLabel,hdrSec_CBD_EquivRate,hdrSec_CBD_EquivIndex]

##hdr 02: hdrSec_CVM_CSV. hdrSec_CVM_CSV_Record, hdrSec_CVM_CSV_len
hdrSec_CVM_CSV_CiaCode = '25224'
hdrSec_CVM_CSV_CiaCNPPJ = '08.773.135/0001-00'
hdrSec_CVM_CSV_CiaName = '2W Ecobank'
hdrSec_CVM_CSV_SubIndustryCode ='#X#'
hdrSec_CVM_CSV_IndustryCode = '#X#'
hdrSec_CVM_CSV_SectorCode = '#X#' 
hdrSec_CVM_CSV_InternalCode ='#X#'
hdrSec_CVM_CSV_Region ='BRZ'
hdrSec_CVM_CSV_Sym6C = '#X#'
hdrSec_CVM_CSV_Fitch = '#X#'
hdrSec_CVM_CSV_SP =  '#X#'
hdrSec_CVM_CSV_Moody = '#X#'
hdrSec_CVM_CSV_Group = '#X#'
hdrSec_CVM_CSV_About = '#X#'
hdrSec_CVM_CSV_cvmCiaName = '2W ECOBANK S.A.'
hdrSec_CVM_CSV_cvmCiaStatus = 'Open'
hdrSec_CVM_CSV_cvmCiaCode = '25224'
hdrSec_CVM_CSV_cvmRegistered = '29/10/2020'
hdrSec_CVM_CSV_neo4jStored = 'FALSE'

hdrSec_CVM_CSV = ['CiaCode','CiaCNPPJ','cia_name', 'SubIndustryCode', 'SectorCode', 'InternalCode' 'Region', 'Sym6C','Fitch', 'SP', 'Moody', 'Group', 'about', 'cvmCiaName', 'cvmCiaStatus' 'cvmCiaCode', 'cvmRegistered', 'neo4jStored']
hdrSec_CVM_CSV_len = len(hdrSec_CVM_CSV)

hdrSec_CVM_CSV_Record = [hdrSec_CVM_CSV_CiaCode,hdrSec_CVM_CSV_CiaCNPPJ,hdrSec_CVM_CSV_CiaName, hdrSec_CVM_CSV_SubIndustryCode, hdrSec_CVM_CSV_SectorCode, hdrSec_CVM_CSV_InternalCode, hdrSec_CVM_CSV_Region, hdrSec_CVM_CSV_Sym6C,hdrSec_CVM_CSV_Fitch,hdrSec_CVM_CSV_SP, hdrSec_CVM_CSV_Moody, hdrSec_CVM_CSV_Group, hdrSec_CVM_CSV_About, hdrSec_CVM_CSV_cvmCiaName, hdrSec_CVM_CSV_cvmCiaStatus, hdrSec_CVM_CSV_cvmCiaCode, hdrSec_CVM_CSV_cvmRegistered, hdrSec_CVM_CSV_neo4jStored]

##hdr 03 hdrSec_XP,hdrSec_XP_Record,hdrSec_XP_len
hdrSec_XP_CiaCode = 'ALSO'
hdrSec_XP_CiaName = 'Aliansce Sonae Shopping Center'
hdrSec_XP_Category = 'DEB'
hdrSec_XP_SecCode ='17J0000001'
hdrSec_XP_ExpireDate ='2023-04-05'
hdrSec_XP_Index = '%DI'
hdrSec_XP_Premium = '101%'
hdrSec_XP_Liquidity = '#X#'
hdrSec_XP_RiskRate =  'brAA+'
hdrSec_XP_Rater = 'S&P'
hdrSec_XP_RiskXP = '2'
hdrSec_XP_MinInv = '1000'
hdrSec_XP_KeyUniq = '##DEB#1.01#%DI#Aliansce Sonae Shopping Center#2023-4-5##'

hdrSec_XP = ['CiaCode','cia_name','Category','SecCode','ExpireDate','Index','Premium', 'Liquidity','RiskRate',                 'Rater','RiskXP', 'MinInv','KeyUniq']
hdrSec_XP_len = len(hdrSec_XP)

hdrSec_XP_Record = [hdrSec_XP_CiaCode,hdrSec_XP_CiaName,hdrSec_XP_Category,hdrSec_XP_SecCode, hdrSec_XP_ExpireDate, hdrSec_XP_Index,hdrSec_XP_Premium, hdrSec_XP_Liquidity, hdrSec_XP_RiskRate,hdrSec_XP_Rater,hdrSec_XP_RiskXP, hdrSec_XP_MinInv,hdrSec_XP_KeyUniq]


##hdr 04 hdrSec_XP_Offer, hdrSec_XP_Offer_Record, hdrSec_XP_Offer_len
hdrSec_XP_Offer_Category = 'CDB'
hdrSec_XP_Offer_Company = 'MASTER'
hdrSec_XP_Offer_Expiration = '15/05/2031'
hdrSec_XP_Offer_Premium = '14.00%'
hdrSec_XP_Offer_Liquidity = '15/05/2031'
hdrSec_XP_Offer_Interest = 'Mensal'
hdrSec_XP_Offer_PayBack = 'Vencimento'
hdrSec_XP_Offer_Rating = 'BBB'
hdrSec_XP_Offer_Qty = '18.103'
hdrSec_XP_Offer_MinInv = '1000'
hdrSec_XP_Offer_RiskXP = '27'
hdrSec_XP_Offer_Index = 'PRÉ'

hdrSec_XP_Offer = ['Category','Company','Expiration','Premium','Liquidity','Interest', 'PayBack','Rating', 'Qty','MinInv','RiskXP','Index']
hdrSec_XP_Offer_len = len (hdrSec_XP_Offer)

hdrSec_XP_Offer_Record = [hdrSec_XP_Offer_Category, hdrSec_XP_Offer_Company, hdrSec_XP_Offer_Expiration, hdrSec_XP_Offer_Premium, hdrSec_XP_Offer_Liquidity, hdrSec_XP_Offer_Interest, hdrSec_XP_Offer_PayBack, hdrSec_XP_Offer_Rating, hdrSec_XP_Offer_Qty,hdrSec_XP_Offer_MinInv, hdrSec_XP_Offer_RiskXP, hdrSec_XP_Offer_Index]


##hdr 05 hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len
hdrCia_CVM_CiaNameNormalized = '2W Ecobank'
hdrCia_CVM_CiaNameRough = '2W ECOBANK S.A.'

hdrCia_CVM = ['CiaNameNormalized','CiaNameRough']
hdrCia_CVM_Record = [hdrCia_CVM_CiaNameNormalized,hdrCia_CVM_CiaNameRough]
hdrCia_CVM__len =len(hdrCia_CVM)

##hdr 06 hdrCia_MoodysRate, hdrCia_MoodysRate_Record, hdrCia_MoodysRate_len
hdrCia_MoodysRate_CiaCode = 'AEGP'
hdrCia_MoodysRate_Emissor = 'Aegea Saneamento & Participações'
hdrCia_MoodysRate_TipoRating = 'Rating Corporativo'
hdrCia_MoodysRate_Rate = 'AA-'
hdrCia_MoodysRate_RateCode = '19'
hdrCia_MoodysRate_Outlook = 'Estável'
hdrCia_MoodysRate_Date = '06/01/2023'
hdrCia_MoodysRate_Analista = 'Nicole Salum'


hdrCia_MoodysRate = ['CiaCode', 'Emissor','TipoRating','Rate','RateCode', 'Outlook', 'Date', 'Analista' ]
hdrCia_MoodysRate_len = len (hdrCia_MoodysRate)

hdrCia_MoodysRate_Record = [hdrCia_MoodysRate_CiaCode, hdrCia_MoodysRate_Emissor, hdrCia_MoodysRate_TipoRating, hdrCia_MoodysRate_Rate, hdrCia_MoodysRate_RateCode, hdrCia_MoodysRate_Outlook, hdrCia_MoodysRate_Date, hdrCia_MoodysRate_Analista]


##hdr 07 hdrCia_CVM, hdrCia_CVM_Record, hdrCia_CVM_len
hdrCia_CVM_CiaName = '2W ECOBANK S.A.'
hdrCia_CVM_NPJ = '08.773.135/0001-00'
hdrCia_CVM_CiaStatus = 'Open'
hdrCia_CVM_CVM = '25224'
hdrCia_CVM_Registered = '29/10/2020'

hdrCia_CVM = ['cia_name', 'CNPJ', 'CiaStatus', 'CVM', 'Registered']
hdrCia_CVM_len = len(hdrCia_CVM)

hdrCia_CVM_Record = [hdrCia_CVM_CiaName, hdrCia_CVM_NPJ, hdrCia_CVM_CiaStatus, hdrCia_CVM_CVM, hdrCia_CVM_Registered]

##hdr 08 hdrImpCia, hdrImpCia_Record, hdrImp_Record_len
hdrImpCiaCode = 'RRRP'
hdrImpCiaCNPJ = '08.773.135/0001-00'
hdrImpCiaName = '3R Petroleum Oleo & Gas'
hdrImpSubIndustryCode = '10102010'
hdrImpIndustryCode = '101020'
hdrImpSectorCode = '10'
hdrImpInternalCode = '10,001'
hdrImpRegion = 'BRZ'
hdrImpSym6C = 'RRRP12'
hdrImpFitch = '#X#'
hdrImpSP = '#X#'
hdrImpMoody = '#X#'
hdrImpGroup = '#X#'
hdrImpAbout = '3R Petroleum Oleo & Gas is a Brazilian oil and gas company that operates in the...'

hdrImpCia = ['CiaCode','CiaCNPJ', 'cia_name', 'SubIndustryCode', 'IndustryCode', 'SectorCode', 'InternalCode', 'Region', 'Sym6C', 'Fitch', 'SP' ,'Moody', 'Group', 'about']
hdrImpCia_Record = [hdrImpCiaCode, hdrImpCiaCNPJ, hdrImpCiaName, hdrImpSubIndustryCode, hdrImpIndustryCode, hdrImpSectorCode, hdrImpInternalCode, hdrImpRegion, hdrImpSym6C, hdrImpFitch, hdrImpSP ,hdrImpMoody, hdrImpGroup, hdrImpAbout]
hdrImpCia_Record_len = len(hdrImpCia_Record)
# print(f"\n Neo4j Company Import header: {hdrImpCia}; has {hdrImpCia_Record_len} items ; sample Record: \n\n {hdrImpCia_Record}")

##hdr 09 hdrV1ImpCia, hdrV1ImpCia_Record, hdrV1Imp_Record_len
hdrV1ImpCiaCNPJ = '08.773.135/0001-00'
hdrV1ImpCiaName = '3R Petroleum Oleo & Gas'
hdrV1ImpSubIndustryCode = '10102010'
hdrV1ImpIndustryCode = '101020'
hdrV1ImpSectorCode = '10'
hdrV1ImpRegion = 'BRZ'
hdrV1ImpFitch = '#X#'
hdrV1ImpSP = '#X#'
hdrV1ImpMoody = '#X#'
hdrV1ImpGroup = '#X#'
hdrV1ImpAbout = '3R Petroleum Oleo & Gas is a Brazilian oil and gas company that operates in the...'


hdrV1ImpCia = ['CiaCNPJ', 'cia_name', 'SubIndustryCode', 'IndustryCode', 'SectorCode', 'Region', 'Fitch', 'SP' ,'Moody', 'Group', 'about']
hdrV1ImpCia_Record = [hdrV1ImpCiaCNPJ, hdrV1ImpCiaName, hdrV1ImpSubIndustryCode, hdrV1ImpIndustryCode,hdrV1ImpSectorCode, hdrV1ImpRegion, hdrV1ImpFitch, hdrV1ImpSP ,hdrV1ImpMoody, hdrV1ImpGroup, hdrV1ImpAbout]
hdrV1ImpCia_Record_len = len(hdrV1ImpCia_Record)
# print(f"\n Neo4j Cia V1 Import header: {hdrV1ImpCia} has <{hdrV1ImpCia_Record_len}> items ; sample:\n\n {hdrV1ImpCia_Record}")

print(f"\n===FixInc Module=> <Headers Definitions 20230804-v2>")


# In[ ]:




