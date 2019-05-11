# 라이브러리 선언
import pandas as pd
import requests
from pandas.io.json import json_normalize

# 시험 데이터
# 1. 발주자/공종별 건설수주액(경상)

# 데이터 접속 주소 입력
url = 'http://kosis.kr/openapi/Param/statisticsParameterData.do?method=getList&apiKey=MjUzMTdiMjcyZjQwY2VkMWJkY2RkYTRmZDkwMWQ3ZGY=&itmId=T10+&objL1=0+&objL2=1+&objL3=&objL4=&objL5=&objL6=&objL7=&objL8=&format=json&jsonVD=Y&prdSe=M&newEstPrdCnt=3&loadGubun=1&orgId=101&tblId=DT_1G1B002'
# 정상 여부 확인 (200 정상)
response = requests.get(url)
response
# JSON 데이터 획득
json = response.json()
# PandasDataframe변환
df = json_normalize(json)
print(df.head())