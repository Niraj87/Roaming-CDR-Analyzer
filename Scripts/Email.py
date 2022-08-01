#!/usr/bin/env python
# coding: utf-8

# In[14]:


import win32com.client
import pathlib


# In[15]:


path = pathlib.Path('CDR_Forecasting.jpg')


# In[16]:


path.absolute()


# In[17]:


path_absolute = str(path.absolute())


# In[18]:


#outlook = win32com.client.Dispatch('outlook.application')

outlook = win32com.client.Dispatch('outlook.application')
mail = outlook.CreateItem(0)


# In[ ]:


msg = outlook.CreateItem(0)


# In[ ]:


msg.To ="niraj.pushparaja@dialog.lk"
#msg.To ='Vindhya.Dissanayake@dialog.lk;Susudu.PaththiniGedara@dialog.lk'
msg.Subject ='Roaming Voice CDR File Stats'
msg.Body = 'CDR File Trend has Abnormal Behavior.Please refer attached'
#msg.Attachments.Add(path_absolute)
image = msg.Attachments.Add(path_absolute)
html_body ="""
    <div>   
    </div>
    <p style="color:black;">Dear All </p>
    
    <p1 style="color:black;">Please refer attached Roaming Voice CDR Forecasting Output. </p1>
    
    <br>
    
    
    <div>
    
    <br>
    
        <img src="cid:CDR_Forecasting-img" 
    </div>
    """
    
    # code for changing the content id of the image
image.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F", "CDR_Forecasting-img")

msg.HTMLBody = html_body

msg.Save()
msg.Send()


# In[ ]:





# In[ ]:


import numpy
numpy.version.version


# In[ ]:


import numpy
numpy.version.version


# In[ ]:


from fbprophet import Prophet
import logging
logger = logging.getLogger('fbprophet')
logger.setLevel(logging.DEBUG)

m = Prophet()
print(m.stan_backend)


# In[ ]:


import win32com.client


# In[ ]:



outlook = win32com.client.Dispatch('outlook.application')
mail = outlook.CreateItem(0)




mail.To = 'susudu.paththinigedara@dialog.lk'
mail.Subject = 'Test Mail'
mail.CC = 'niraj.pushparaja@dialog.lk'



mail.Send()


# In[ ]:




