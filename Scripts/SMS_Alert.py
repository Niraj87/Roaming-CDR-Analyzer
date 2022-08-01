#!/usr/bin/env python
# coding: utf-8

# In[1]:


#exec(open("Voice_CDR_Forecasting.py").read())

exec(open(r'C:\Users\Vindhya_VIN071\Python\Roaming\Data_CDR_Forecasting.py').read())


# In[2]:


import cx_Oracle
#DB Connection

dsn_tns = cx_Oracle.makedsn('xxxx', 'xxxx', service_name='cam') 
conn1 = cx_Oracle.connect(user='xxxx', password='xxxx', dsn=dsn_tns) 
#print(cx_Oracle.version)
c = conn1.cursor()


# In[3]:


# Test connection

print(cx_Oracle.version)


# In[4]:


# Sql query 

sql1 = """select * from API.KEY_SMS_MESSAGE_LIST_HP """


# In[5]:


# Make Dataframe

df = pd.read_sql(sql1, conn1)


# In[6]:


df


# In[7]:


test_df.tail(10)


# In[8]:


# Drop last Raw

#test_df = test_df.iloc[:-1 , :]


# In[9]:


test_df.tail(10)


# In[10]:


print(test_df.iloc[-1,1])


# In[11]:


#Actual value day -1 assign

Actual_value = test_df['y'].iloc[-1]


# In[12]:


# Actual value

Actual_value


# In[13]:


print(Actual_value)


# In[14]:


print(type(Actual_value))


# In[15]:


# Reset index


forecast.reset_index()

print(forecast)


# In[16]:


# Set index

forecast = forecast.set_index('ds')


# In[17]:


print(forecast)


# In[18]:


# Import

import datetime

import math


# In[19]:


# Logic 

ydDate = (datetime.date.today() - datetime.timedelta(1)).strftime('%m/%d/%Y')

Act_val = None
low_val = None
up_val =  None

for i in forecast.index:   
    if i.strftime('%m/%d/%Y') == ydDate:
        
        Actual_value = float(Actual_value)
        
        print(type(Actual_value))
        
        value = forecast.loc[i]['yhat_upper']
        print(value)
    
        
        value2 = forecast.loc[i]['yhat_lower']
         
        print (value2)
            
        if Actual_value > value or Actual_value < value2:  
            
           # print("Niraj")
            
            
            Act_val = str(math.floor(Actual_value * 100)/100.0)
            low_val = str(math.floor(value2 * 100)/100.0)
            up_val = str(math.floor(value * 100)/100.0)
            
            print(Act_val)
            
        
            msg_date = datetime.datetime.now().date()
            #event_date = (datetime.date.today() - datetime.timedelta(1)).strftime('%m/%d/%Y')
            msg_txt = 'Abnormal Behaviour in Roaming Daily CDR Count in Data \nDate: '+ydDate+' \nReceived Count: '+Act_val+'\nPredicted Range: '+low_val+' - '+up_val
            msg_date = datetime.datetime.now().date()
            # msg_values = [('VAS SMS','777694232', msg_txt,'N',msg_date),
            # ('VAS SMS','777337281', msg_txt,'N',msg_date),
            msg_values = [('VAS SMS','773339891', msg_txt,'N',msg_date),
            ('VAS SMS','777338024', msg_txt,'N',msg_date),
            ('VAS SMS','777333310', msg_txt,'N',msg_date),
            ('VAS SMS','777694232', msg_txt,'N',msg_date),
            ('VAS SMS','777337281', msg_txt,'N',msg_date),
            ('VAS SMS','777331494', msg_txt,'N',msg_date)]

            insert_stmt = """INSERT INTO API.KEY_SMS_MESSAGE_LIST_HP (MODULE_ID,PHONE_NO,MESSAGE,READ,ACTION_DATE) VALUES (:1, :2, :3, :4, :5)"""
            c.executemany(insert_stmt, msg_values)
            conn1.commit()


            
           # insert_table = "INSERT INTO API.KEY_SMS_MESSAGE_LIST_HP VALUES('VAS SMS','773339891','Abnormal Behavior','N',SYSDATE)"
                            
        
            #c.execute(insert_table)
            #conn1.commit()
            
            
        
        else:
            
            print("Normal Behavior")
            
                
        
          



# In[20]:


print(Actual_value)


# In[21]:


import win32com.client
import pathlib
path = pathlib.Path(r'C:\Users\Vindhya_VIN071\Python\Roaming\CDR_Forecasting_Data.jpg')
path.absolute()
path_absolute = str(path.absolute())
#outlook = win32com.client.Dispatch('outlook.application')


olMailItem = 0x0
outlook = win32com.client.Dispatch('outlook.application')
msg = outlook.CreateItem(olMailItem)
Act_val = str(Act_val)
low_val = str(low_val)
up_val = str(up_val)

#msg.To ='niraj.pushparaja@dialog.lk'
msg.To ='interconnectoperations@dialog.lk'
msg.CC='vindhya.dissanayake@dialog.lk;niraj.pushparaja@dialog.lk'
#msg.CC='susudu.paththinigedara@dialog.lk'
msg.Subject ='Roaming Data CDR File Stats'
#msg.Body = 'CDR File Trend has Abnormal Behavior.Please refer attached'
#msg.Attachments.Add(path_absolute)
image = msg.Attachments.Add(path_absolute)

if Act_val == 'None' or low_val == 'None' or up_val == 'None':

    
    html_body ="""
    <div>   
    </div>
    
    
    <p1 style="color:black;">Please refer Roaming Data stream CDR file stats.<br><br>
                             Date: """+ydDate+""" <br><br>
                             
                             
                             *************************************************

    
    <br>
    
    
    <div>
    
    <br>
    
        <img src="cid:CDR_Forecasting_Data-img" 
    </div>
    """

else:

    html_body ="""
        <div>   
        </div>
        <p style="color:Red;">System Alert!! </p>

        <p1 style="color:black;">Anomaly Detected in Roaming Data Stream.<br>
                                 Date: """+ydDate+""" <br>
                                 Recieved Count: """ +Act_val+""" <br>
                                 Predicted Range: """+low_val+""" - """+up_val+""" <br>

                                 ***************** Please Check ***************** 


        <br>


        <div>

        <br>

            <img src="cid:CDR_Forecasting_Data-img" 
        </div>
        """
    
    # code for changing the content id of the image
image.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "CDR_Forecasting_Data-img")

msg.HTMLBody = html_body

msg.Save()
msg.Send()
            


# In[ ]:





# In[ ]:





# In[ ]:




