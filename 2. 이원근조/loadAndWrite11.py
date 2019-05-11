#!/usr/bin/env python
# coding: utf-8

# In[78]:


import requests #Used to service API connection
from lxml import html #Used to parse XML
from bs4 import BeautifulSoup #Used to read XML table on webpage
import pandas as pd
#from pandas import DataFrame
import numpy as np
import wget
from common import cFunction as cf
from sqlalchemy import create_engine

# get dataList from filesystem to load and write
#dataList = pd.read_excel("../../data/inbound/dataList.xlsx")


# In[79]:


# get dataList from spreadsheet to load and write
dataList = pd.read_csv("../../data/inbound/workSheet.csv")
print("### The total number of target data is " + str(len(dataList)))


# In[80]:


regionCdData = pd.read_csv("../../data/infomations/RegionCode.csv")
print(regionCdData)


# In[81]:


# Filtering -> get dataList only defined url
dataList = dataList[(dataList["제공항목(데이터셋)"] == '한국감정원 주택거래 현황') & (dataList["제공방식"] == 'OPENAPI')]
print("### The total number of filtered data is " + str(len(dataList)))
dataList


# In[82]:


###################################################
# Filtering -> for your own object
#dataList = dataList[   dataList['번호'] == "352" ]
###################################################

# create folder to save result
outPath = "../../data/outbound/"
folderList = dataList["폴더명"].tolist()


# In[83]:


for i in folderList:
    cf.createFolder(outPath+i)


# In[84]:


dataList = dataList.fillna("")
dataList = dataList.reset_index(drop=True)
dataList


# In[85]:


dataCount = 0


# In[86]:


# get dataList to load and write
inputUrl = dataList.loc[dataCount, "사이트"]
inputKey = dataList.loc[dataCount, "서비스키"]
inputParameter = dataList.loc[dataCount, "파라미터"]
inputFolder = dataList.loc[dataCount, "폴더명"]
inputFile = dataList.loc[dataCount, "서비스명"]
inputDataType = dataList.loc[dataCount, "데이터타입"]
inputRefUrl = dataList.loc[dataCount, "참고문서"]
inputRefType = dataList.loc[dataCount, "참고문서타입"]
inputbParameter = dataList.loc[dataCount, "비고_파라미터설명"]
len(inputbParameter)


# In[87]:


url = cf.makeURL(inputUrl,inputKey,inputParameter)
print("fullUrl is " + url)


# In[88]:


newDF = pd.DataFrame()
if (inputDataType == "xml"):
    newDF = cf.operatorXmlProcess(url, inputbParameter)
elif(inputDataType == "json"):
    newDF = cf.jsonProcess(url)
elif(inputDataType == "csv"):
    newDF = cf.csvProcess(url)        


# In[89]:


newDF


# In[90]:


fullOutPath = outPath+inputFolder+"/"+inputFolder+inputFile+".csv"
print(fullOutPath)


# In[91]:


# try:
#     newDF.to_csv(fullOutPath, index=False, encoding="utf-8")
# except Exception as x:
#     print(x)


# In[94]:


try:
    engine = create_engine('postgresql://postgres:postgres@192.168.110.23:5432/postgres')
    newDF.to_sql(inputFolder + inputFile + ".csv", engine, if_exists='replace', index = False)
except Exception as x:
    print(x)


# In[93]:


fullOutRefPath = outPath + inputFolder + "/" + inputFolder + inputFile + "."+inputRefType
try:
    wget.download(inputRefUrl, fullOutRefPath)
except Exception as e:
    print(inputFolder+"참고문서 Error")
    print(e)
    pass


# In[ ]:





# In[ ]:





# In[ ]:




