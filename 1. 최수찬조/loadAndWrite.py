#!/usr/bin/env python
# coding: utf-8

# In[2]:


import requests #Used to service API connection
from lxml import html #Used to parse XML
from bs4 import BeautifulSoup #Used to read XML table on webpage
import pandas as pd
# from common import cFunction as cf
import numpy as np
import wget

# get dataList from filesystem to load and write
#dataList = pd.read_excel("../../data/inbound/dataList.xlsx")

# get dataList from spreadsheet to load and write
dataList = pd.read_csv("https://docs.google.com/spreadsheets/d/1VngqG-m7G8k1587c21MZoheR1Fz3amp1mJtiBvA1Jb0/export?format=csv&gid=0")
print("### The total number of target data is " + str(len(dataList)))

# Filtering -> get dataList only defined url
dataList = dataList[   dataList['사이트'].notnull() ]
print(dataList[["사이트"]])
print("### The total number of filtered data is " + str(len(dataList)))

###################################################
# Filtering -> for your own object
# dataList = dataList[   dataList['번호'] == "339" ]
###################################################

# create folder to save result
outPath = "../../data/outbound/"
folderList = dataList["폴더명"].tolist()
for i in folderList:
    createFolder(outPath+i)

dataList = dataList.fillna("")
dataList = dataList.reset_index(drop=True)


# get dataList to load and write
for dataCount in range(0,len(dataList)):
    if dataCount == 4:
        inputUrl = dataList.loc[dataCount, "사이트"]
        inputKey = dataList.loc[dataCount, "서비스키"]
        inputParameter = dataList.loc[dataCount, "파라미터"]
        inputFolder = dataList.loc[dataCount, "폴더명"]
        inputFile = dataList.loc[dataCount, "서비스명"]
        inputFile = inputFile.split('&')
        inputDataType = dataList.loc[dataCount, "데이터타입"]
        inputRefUrl = dataList.loc[dataCount, "참고문서"]
        inputRefType = dataList.loc[dataCount, "참고문서타입"]
#     print(inputUrl)

print(inputFile)


# In[3]:


urlList = []
codeDF = pd.read_csv('../dataset/fuckingapi.csv', encoding='ms949')
codeDF['법정동코드'] = codeDF['법정동코드'].astype(str)
len(codeDF)


# In[4]:


#     paraList = []
#     for i in codeDF['법정동코드']:
#         sigunguCd = codeDF['법정동코드'].str[:5]
#         bjdongCd = codeDF['법정동코드'].str[5:]
#         paraList += [sigunguCd, bjdongCd]
# print(paraList)
# test = pd.DataFrame(paraList)
# test.head()
#     test.to_csv('./cut.csv')
for i in inputFile:
    for j in codeDF['법정동코드'].astype(str):
        a = j[:5]
        b = j[5:]
        url = makeURL(inputUrl,inputKey,inputParameter, i, a, b)
        urlList.append(url)
#         print("fullUrl is " + url)
print(urlList[1])
print(urlList[2])


# In[5]:


inputFile[0]


# In[6]:


# newDf = pd.DataFrame()
testList = []
for i in codeDF['법정동코드'].astype(str):
    a = i[:5]
    b = i[5:]
    url = makeURL(inputUrl,inputKey,inputParameter,inputFile[0], a, b)
    testList.append(url)
    
print(testList)    
    
    
# tempData1 = xmlProcess(urlList[1])
# tempData2 = xmlProcess(urlList[2])
    
# mergedata = pd.concat([tempData1,tempData2], axis=0)
    


# In[18]:


tempDF = pd.DataFrame()
for i in testList:
    try:
        temtem = xmlProcess(i)
        tempDF = pd.concat([tempDF, temtem], axis = 0)
    except Exception as e:
        print(i)
tempDF.head()


# In[22]:


tempDF.to_csv('./resultChoi.csv', encoding='ms949', index=False)


# In[ ]:


addName = []


# In[ ]:


for i in len(inputFile):
    addName[] = inputFile[i].astype(str)
    pd.to_csv('./test.csv')


# In[ ]:


for i in inputFile:
    resultName = '././' + i + '.csv'
    for j in paraList:
        
        
        
        to_csv(resultName, encoding='ms949')


# In[15]:


getApBasisOulnInfo


# In[ ]:


mergedata.reset_index(drop=True)


# In[ ]:


mergedata.to_csv('./resultTest.csv', encoding='ms949', index=False)


# In[ ]:


newDf

# newDF = pd.DataFrame()


# if (inputDataType == "xml"):
#     for i in urlList:
#         tempNewDF = xmlProcess(i)
#         newDF = pd.concat([newDF, tempNewDF], axis=0)

# elif(inputDataType == "json"):
#     newDF = cf.jsonProcess(url)
# elif(inputDataType == "csv"):
#     newDF = cf.csvProcess(url)

# fullOutPath = outPath+inputFolder+"/"+inputFolder+inputFile+".csv"
# print(fullOutPath)

# try:
#     newDF.to_csv(fullOutPath, index=False, encoding="ms949")
# except Exception as x:
#     print(x)

# fullOutRefPath = outPath + inputFolder + "/" + inputFolder + inputFile + "."+inputRefType
# try:
#     wget.download(inputRefUrl, fullOutRefPath)
# except Exception as e:
#     print(inputFolder+"참고문서 Error")
#     print(e)
#     pass


# In[8]:


tempNewDF.head()


# In[17]:


import os
import requests #Used to service API connection
from lxml import html #Used to parse XML
from bs4 import BeautifulSoup #Used to read XML table on webpage
import pandas as pd
from pandas.io.json import json_normalize

def makeURL(myUrl, myKey, myParameter , op, para1, para2):
    # myUrl = "http://192.168.1.120/index.php?"
    url = myUrl + '/'+op + "?ServiceKey=" + myKey + "&" + myParameter + 'sigunguCd=' + para1 + '&bjdongCd=' + para2

    url = url.rstrip('&')
    return url

def xmlProcess(url):
    response = requests.get(url)
    # Check if page is up
    if response.status_code == 200:
        # Convert webpage to %Data
        Data = BeautifulSoup(response.text, 'lxml-xml')
        result = []
        rows = 0
        columnName = []
        # search Item all item tag
        iterData = Data.find_all('item')
        for item in iterData:
            item_list = []
            # Fill the value in one row
            for tag in item.find_all():
                try:
                    tagname = tag.name
                    if rows == 0:
                        columnName.append(tagname)
                    item_list.append(item.find(tagname).text)
                except Exception as e:
                    print("This row will be ignored. ", item_list)
            rows = rows + 1
            result.append(item_list)
#             try:
#                 result.append(item_list)
#             except Exception as e:
#                 return pd.DataFrame()
    finalResult = pd.DataFrame(result)
    finalResult.columns = columnName
#     print(finalResult)
    return finalResult


def jsonProcess(url):

    # 정상 여부 확인 (200 정상)
    response = requests.get(url)
    # JSON 데이터 획득
    json = response.json()
    # PandasDataframe변환
    df = json_normalize(json)
    return df

def csvProcess(url):

    # 정상 여부 확인 (200 정상)
    response = requests.get(url)

    df = pd.read_csv(url, encoding="ms949")
    return df

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)


# In[ ]:


pd


# In[ ]:




