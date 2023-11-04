#!/usr/bin/env python
# coding: utf-8

# In[13]:


### Import Basic Modules + Horodateur


from datetime import datetime  # on veut tracer les executions
def date_stamp():
    now = datetime.now()
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    return date_time

import csv
# import datetime
from datetime import date, timedelta
import string
import os.path
import json


print(f"\n=== Initial Import <Horodateur + Basic Modules")


import os
import sys

# def install_module(module_name):
#     """Installs the specified module using pip."""
#     command = "pip install {}".format(module_name)
#     os.system(command)
#
# if __name__ == "__main__":
#     module_name = "bardapi"
#     install_module(module_name)
#
from bardapi import Bard
myToken = 'awh5YWTO8IrYw-mmk3qAFGi6T6X_XUo27w4b44wNu_T3gCzDOXyqzOdtBksLWj5O4mQu1A.'
bard = Bard(token = myToken)
response = bard.get_answer("Tell me about this Brazilian Company: 'Desktop Sigmanet Comunicação Multimidia'")
print(response)









