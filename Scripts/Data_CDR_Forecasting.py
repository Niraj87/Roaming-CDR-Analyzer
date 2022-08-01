#!/usr/bin/env python
# coding: utf-8

# In[20]:


import cx_Oracle
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline
from pandas_datareader import data
import statsmodels.tsa.stattools as sts
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.graphics.tsaplots as sgt


#ignore warning while runing
import warnings
warnings.filterwarnings('ignore')

#cx_Oracle.init_oracle_client(lib_dir= r"D:\Oracle\instantclient_19_9")


# In[39]:


#DB Connection

dsn_tns = cx_Oracle.makedsn('xxx.xx.xx.xx', 'xxxx', service_name='xxxx') 
conn1 = cx_Oracle.connect(user='xxxxx', password='xxxx', dsn=dsn_tns) 
#print(cx_Oracle.version)
c = conn1.cursor()

##df_full = pd.read_sql("""\select trunc(event_date) as EVENT_DATE , sum(VOICE_FILE_COUNT) AS VOICE_FILE_COUNT  from ROAMING_DAILY_STATS_VOICE where trunc(to_char(event_date, 'YYYY')) ='2046' group by  trunc(event_date) order by EVENT_DATE""", conn1)

sql1 = """select trunc(event_date) AS EVENT_DATE, sum(DATA_FILE_COUNT) as DATA_FILE_COUNT  from ROAMING_DAILY_STATS_DATA
where trunc(to_char(event_date, 'YYYY')) !='2046'
and event_date >= '01 JAN 2020'
group by  trunc(event_date)  
order by event_date"""

df_full = pd.read_sql(sql1, conn1)


# In[40]:


df_full.describe()


# In[41]:


df_full.tail()


# In[42]:


# Rename Column

df_full = df_full.rename(columns={'EVENT_DATE': 'ds','DATA_FILE_COUNT' : 'y'})


# In[43]:


# set index 

df_full['ds'] = pd.DatetimeIndex(df_full['ds'])


# In[44]:


df_full


# In[45]:


# Plot

ax = df_full.set_index('ds').plot(figsize=(24,8))
ax.set_ylabel('CDR_Count_Data')
ax.set_xlabel('Date')

#plt.show()


# In[46]:


# Data split to train & test

#train_df = df_full.head(int(len(df_full)*(98/100)))

#test_df = df_full.tail(int(len(df_full)*(2/100)))


train_df = df_full[0:-16]
test_df = df_full[-16:]


# In[47]:


#df = df_full.loc[(df_full['ds'] >= '2020-01-01 00:00:00')
               # & (df_full['ds'] <='2021-08-18 00:00:00')]

#test_df = df_full.loc[(df_full['ds'] >= '2021-08-18 00:00:00')
                #& (df_full['ds'] <='2021-09-07 00:00:00')]


# In[48]:


train_df


# In[49]:


test_df


# In[50]:


# Import prophet

from fbprophet import Prophet


# In[51]:


m = Prophet()


# In[52]:


# Fit model

m.fit(train_df)


# In[53]:



# Predict Future periods

future = m.make_future_dataframe(periods=20,
                            include_history = False)


# In[54]:


# Future value

forecast = m.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(20)


# In[55]:


# Plot

#fig1 = m.plot(forecast)


# In[58]:


# Overlap forecast value & actual value

figure = plt.figure(figsize=(24,8))
axes = figure.add_axes([0,0,1,1])

axes.plot(forecast[['ds']],forecast[['yhat']], color='red',label="Forcast")
axes.plot(test_df[['ds']],test_df[['y']], color='green',label="Test")
#axes.plot(df_full[['ds']],df_full[['y']], color='blue',label="Actual")

#plt.fill_between(x, y3, y4, color='grey', alpha='0.5')

axes.fill_between(forecast.ds,forecast.iloc[:, 2],forecast.iloc[:, 3], color='b', alpha=.20)
plt.legend(fontsize=21) 
plt.grid()
plt.title("DATA CDR File Count", size=30, color='Black')
plt.savefig(r'C:\Users\Vindhya_VIN071\Python\Roaming\CDR_Forecasting_Data.jpg',bbox_inches='tight', dpi=150)
axes.legend()


# In[57]:


# Components
m.plot_components(forecast);


# In[63]:


df_full


# In[ ]:





# In[ ]:




