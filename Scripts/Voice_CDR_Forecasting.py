#!/usr/bin/env python
# coding: utf-8

# In[1]:


import cx_Oracle
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline
from pandas_datareader import data
import IPython
#from IPython import get_ipython
#ignore warning while runing
import warnings
warnings.filterwarnings('ignore')

#cx_Oracle.init_oracle_client(lib_dir= r"D:\Oracle\instantclient_19_9")


# In[2]:


#DB Connection

dsn_tns = cx_Oracle.makedsn('xxx.xx.xx.xx', '1521', service_name='xxxx') 
conn1 = cx_Oracle.connect(user='xxxx', password='xxxx', dsn=dsn_tns) 
#print(cx_Oracle.version)
c = conn1.cursor()

##df_full = pd.read_sql("""\select trunc(event_date) as EVENT_DATE , sum(VOICE_FILE_COUNT) AS VOICE_FILE_COUNT  from ROAMING_DAILY_STATS_VOICE where trunc(to_char(event_date, 'YYYY')) ='2046' group by  trunc(event_date) order by EVENT_DATE""", conn1)

sql1 = """select trunc(event_date) AS EVENT_DATE, sum(VOICE_FILE_COUNT) as VOICE_FILE_COUNT  from ROAMING_DAILY_STATS_VOICE
where trunc(to_char(event_date, 'YYYY')) !='2046'
group by  trunc(event_date)  
order by event_date"""

df_full = pd.read_sql(sql1, conn1)


# In[3]:


df_full.describe()


# In[4]:


df_full.tail(10)


# In[5]:


# Rename Column

df_full = df_full.rename(columns={'EVENT_DATE': 'ds','VOICE_FILE_COUNT' : 'y'})


# In[6]:


# set index 

df_full['ds'] = pd.DatetimeIndex(df_full['ds'])


# In[7]:


df_full.tail(10)


# In[8]:


# Plot

ax = df_full.set_index('ds').plot(figsize=(24,8))
ax.set_ylabel('CDR_Count')
ax.set_xlabel('Date')

#plt.show()


# In[9]:


# Data split to train & test

train_df = df_full.head(int(len(df_full)*(90/100)))

test_df = df_full.tail(int(len(df_full)*(10/100)))


#train_df = df_full[0:-16]
#test_df = df_full[-16:]


# In[10]:


#df = df_full.loc[(df_full['ds'] >= '2020-01-01 00:00:00')
               # & (df_full['ds'] <='2021-08-18 00:00:00')]

#test_df = df_full.loc[(df_full['ds'] >= '2021-08-18 00:00:00')
                #& (df_full['ds'] <='2021-09-07 00:00:00')]


# In[11]:


train_df


# In[12]:


test_df


# In[13]:


# Import prophet

from fbprophet import Prophet


# In[14]:


m = Prophet()


# In[15]:


# Fit model

m.fit(train_df)


# In[16]:



# Predict Future periods

future = m.make_future_dataframe(periods=75,
                            include_history = False)


# In[17]:


# Future value

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(20)


# In[18]:


# Plot

#fig1 = m.plot(forecast)


# In[19]:


# Overlap forecast value & actual value

figure = plt.figure(figsize=(24,8))
axes = figure.add_axes([0,0,1,1])

axes.plot(forecast[['ds']],forecast[['yhat']], color='red',label="Forcast")
axes.plot(test_df[['ds']],test_df[['y']], color='green',label="Actual")

#plt.fill_between(x, y3, y4, color='grey', alpha='0.5')

axes.fill_between(forecast.ds,forecast.iloc[:, 2],forecast.iloc[:, 3], color='b', alpha=.20)
plt.legend(fontsize=21) 
plt.grid()
plt.title("Voice CDR File Count", size=30, color='Black')
plt.savefig(r'C:\Users\Vindhya_VIN071\Python\Roaming\CDR_Forecasting_Voice.jpg',bbox_inches='tight', dpi=150)
axes.legend()


# In[60]:


# Components
m.plot_components(forecast);


# In[ ]:





# In[ ]:





# In[ ]:




