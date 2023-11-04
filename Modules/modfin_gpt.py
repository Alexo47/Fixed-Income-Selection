#!/usr/bin/env python
# coding: utf-8

"""
=> Module-FixIncome - GPT related Routines  20231029-v2
# GPT_KEY_API => connection key to activate chatGPT API
# GPT_INOPERATIVE_LIST => List of useless sentences used by chatGPT
# GPT_INOPERATIVE_LIST_LEN = len(GPT_INOPERATIVE_LIST_LEN)
# def gpt_get_about(cia_name): about => Activates chatGPT prompting for an about
# def gpt_clean_about(reply): cleanReply => Replace characters + remove chatGPT boilerplate text
"""
# => Import Basic Modules + TimeStamp

# !pip install openai
from modgen_timestamp import date_stamp
import openai

# => connection key to activate chatGPT API

GPT_KEY_API = "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"
openai.api_key = GPT_KEY_API

"""
=> List of useless sentences used by chatGPT
"""
GPT_INOPERATIVE_LIST = [
    "It could be a small, local company that has not gained much visibility,",
    "or it could be a fictitious company.",
    "It would be appreciated if you could provide additional information about the company",
    "you are talking about",
    "However, upon conducting some research, ",
    "I could not find any information about a Brazilian company named",
    "is a lesser known company or a new company that has not yet established",
    "a significant online presence.",
    "Can you provide me with more information or context about the company",
    "you are referring to in order to",
    "I don^t have access to the latest ",
    "information or knowledge about Brazilian companies.",
    "current information, but as of my training data I can give you some information about",
    "verify the credibility of a company before investing or sharing personal information.",
    "context or specific information about the company or the question you have in mind?",
    "current or updated information beyond what is publicly available on the internet.",
    "current information about companies in Brazil, and there is no information about",
    "I do not have the ability to browse the internet to find the current information",
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
    "browse the internet and access information that",
    "current information, but here is what I found",
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

GPT_INOPERATIVE_LIST_LEN = len(GPT_INOPERATIVE_LIST)


# print
# (f"===chatGPT=> Boilerplate Sentences has <{len(GPT_INOPERATIVE_LIST)}> entries"\
# "namely:\n\n {GPT_INOPERATIVE_LIST}"\
# )


def gpt_get_about(cia_name):
    """
    => Activates chatGPT prompting for an about
    :param cia_name:
    :return: about
    """
    query_content = "content"
    query_about = "Tell me about this Brazilian company: "
    brz_cia_name = cia_name

    query_message = [{"role": "user", query_content: query_about + brz_cia_name}]

    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=query_message)
    about = chat.choices[0].message.content
    return about


def gpt_clean_about(reply):
    """
    => Replace some characters + remove chatGPT boilerplate text
    :param reply:
    :return: clean_reply
    """
    clean_reply = reply.replace("\r\n", "")
    clean_reply = clean_reply.replace("'", "^")
    clean_reply = clean_reply.replace("\\", "")

    # remove boiler plate statements
    for boilerplate in GPT_INOPERATIVE_LIST:
        clean_reply = clean_reply.replace(boilerplate, "")
        return clean_reply


print(f"\n===FixIncome=> <GPT related Routines 20231029-v2> exec@: {date_stamp()}")
