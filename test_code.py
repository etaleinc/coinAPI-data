
# coding: utf-8

# In[4]:

import sys
sys.path.insert(0, '/Users/federicobuonerba/Downloads/')

from data_try_except import get_symbols, get_data

# In[11]:


unix_time= 1451606401
symbols=get_symbols()
get_data(unix_time, symbols[7])
