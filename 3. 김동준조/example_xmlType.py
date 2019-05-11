# 라이브러리 선언
import requests #Used to service API connection
from lxml import html #Used to parse XML
from bs4 import BeautifulSoup #Used to read XML table on webpage
import pandas as pd

# 시험데이터
# 아파트 매매 실거래가 상세자료

baseUrl = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"

serviceKey = "AT33s775KYpJOkUBJu0dxkJuUeIfDIOJRzAH084EQS3JN%2BzFjErLHuk%2FGZa9L4gBTSGCzeA69tI9PwLp7B37IQ%3D%3D"

parameter = "pageNo=1&startPage=1&numOfRows=10&pageSize=10&LAWD_CD=11110&DEAL_YMD=201512"

# make url (example)
# developer can attach full url here
url = baseUrl+"?"+"serviceKey="+serviceKey+"&"+parameter

response = requests.get(url)
response

Data = BeautifulSoup(response.text, 'lxml-xml')
result = []
rows = 0
columnName = []
# search Item all item tag
iterData = Data.find_all('item')
iterData

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
                print("This row will be ignored. ",item_list)
        rows = rows + 1
        result.append(item_list)

result

finalResult = pd.DataFrame(result)
finalResult.columns = columnName
print(finalResult.head())
