#!/usr/bin/env python
# coding: utf-8

# In[ ]:



# coding: utf-8

# In[8]:


import os #운영체제(OS)에서 제공되는 기본적인 기능들을 제공
import requests #Used to service API connection
from lxml import html #Used to parse XML
from bs4 import BeautifulSoup #Used to read XML table on webpage
import pandas as pd#데이터를 데이터프레임으로 바꿔서 보여주는 모듈
from pandas.io.json import json_normalize #json 형식의 데이터를 데이터프레임으로 변환하는 모듈
import tabula #table,표를 다룰 때 사용하는 모듈
from tabula import wrapper #pdf 에서 표를 읽을 때 필요한 모듈 / python 업 이후에는 wrapper.read_pdf 로 사용해야
from datetime import datetime #
import psycopg2
from sqlalchemy import create_engine
import re




def makeURL(myUrl, myKey, myParameter):
    # myUrl = "http://192.168.1.120/index.php?"
    url = myUrl + myKey + "&" + myParameter

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
    finalResult = pd.DataFrame(result)
    finalResult.columns = columnName
    print(finalResult)
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


def pdfProcess(inputFolder, url):
    #다른 사이트에서 pdf 데이터를 받을 때는 함수를 다시 만들어야 해요
    #html-parsing 작업_새로 업데이트된 pdf 파일의 일련번호를 가져와야 해요
    resp = requests.get("http://fsc.go.kr/info/trd_list.jsp?menu=7230000&bbsid=BBS0069")
    resp.encoding='utf-8'
    html = resp.text
    bs = BeautifulSoup(html, 'html.parser')
   
    #프로그램 실행시마다 최신데이터를 데이터를 가져오도록 하는 코드 
    #데이터 추출하기
    originalData  = bs.select("#contents > div.board > table > tbody > tr > td > a")
    convertedData = str(originalData[2])
    dailyUpdated = convertedData.split('"')[1].split('amp;')[1]

    url = url + "&" + dailyUpdated # & 를 안 써줘서 직업이 안됐었어....
    df2 = wrapper.read_pdf(url,
              multiple_tables=True,
              pages="all",
              pandas_options={"header":0})
    
    #컬럼 헤더에 특수문자 제거
    colName = df2[0].columns.tolist()
    for i in range(0, len(df2)):
        colName[i] = df2[i].columns.tolist()
        for j in range(0, len(colName)):
            clean = re.sub('[-=+,#/\?:^$.%@*\"※~&ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', colName[i][j])
            colName[i][j] = clean
        df2[i].columns = colName[i]

    #csv 파일로 저장하기 
    #파일이름에 반영할 현재 날짜 구하기 
    currentYear = datetime.today().year
    currentMonth = datetime.today().month
    currentDate = datetime.today().day

    currentYear = str(currentYear)[-2:]
    if (currentMonth < 10):
        currentMonth = "0" + str(currentMonth)
    else:
        currentMonth = str(currentMonth)

    if (currentDate < 10):
        currentDate = "0" + str(currentDate)
    else:
        currentDate = str(currentDate)


    today = currentYear + currentMonth + currentDate
    
    #각각의 표를 파일로 저장 (to DB : postgres)
    engine = create_engine('postgresql://kopo:kopo@192.168.110.111:5432/kopo')
    for i in range(0, len(df2)):
        fileName = inputFolder + "_" + today + "_" + str(i)
        df2[i].to_sql(fileName, engine, if_exists='replace', index=False)
        
        #
    #return
    
def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)