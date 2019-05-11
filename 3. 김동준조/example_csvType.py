import pandas as pd

# 시험 데이터
# 389 한국감정원 / 지가지수(연도별, 용도지역별, 월별, 월별_읍면동별, 이용상황별)
url = 'https://www.data.go.kr/dataset/fileDownload.do?atchFileId=FILE_000000001420537&fileDetailSn=1&publicDataDetailPk=uddi:1187ad78-3933-43e9-92ae-9ed15c7096d8_201712281357'

data = pd.read_csv(url, encoding='ms949')


data.ti

print(data.head())