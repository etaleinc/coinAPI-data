
# coding: utf-8

# In[4]:


#from test_functions import make_dataframe as mkdf
#from test_functions import make_csv as mk
import sys
sys.path.insert(0, '/Users/federicobuonerba/Downloads/')

from test_functions import download_json_simple_loop
from test_functions import make_csv


# In[11]:


unix_time= 1451606400
download_json_simple_loop(unix_time)
make_csv(unix_time)
