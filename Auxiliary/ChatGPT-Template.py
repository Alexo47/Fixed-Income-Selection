#!/usr/bin/env python
# coding: utf-

# TEMPL A-0:Définitions Préliminaires : Horodateur

from datetime import datetime # on veut tracer les executions
def date_stamp():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time


print(f"\n=== Cell A-0 <Définitions préliminaires> Executed")


# chatGPT #B-0 : Installation de Neo4j et chatGPT API key

# !pip install neo4j #requirement satisfied
# pip install openai

GPT_keyAPI = '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'
print(f"\n=== FixInc #B-0: <Installation de chatGPT> exec@: {date_stamp()}")



# chatGTP #B-1 : Ouverture Session chatGPT


import openai
openai.api_key = GPT_keyAPI

print(f"\n=== FixInc #B-1: <Ouverture Session chatGPT> exec@: {date_stamp()}")


# chatGTP #B-1 : Single Test on about Company


queryContent = "content"
queryAbout = "Tell me about this Brazilian company: "
brzCiaName = "Xp Investimentos"

queryMessage = [ {"role": "user", queryContent: queryAbout + brzCiaName} ]

chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = queryMessage)
reply = chat.choices[0].message.content

print(f" For query {queryMessage} , ChatGPT replies this: \n\n {reply}")

print(f"\n=== chatGTP #B-1: <Single test on About Company> exec@: {date_stamp()}")
