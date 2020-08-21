# DataCollector
- 머신러닝 기반 주가 예측 프로젝트의 데이터를 수집해오는 코드 입니다.


## create_DB_Collection.py
- azure cosmosdb에 Database를 생성하고 container를 생성하는 코드 입니다.


## daily_price_collector.py
- 코드를 돌린 날짜를 알아내어 그 당일의 KRX 종목 주가 데이터를 수집하여 CSV 파일로 변환하여 저장하는 코드 입니다.


## insert_daily_price.py
- daily_price_collector.py의 결과물인 CSV파일을 create_DB_Collection.py의 결과물인 azure cosmosdb의 database안 container에 적재하는 코드 입니다. 


## period_price_collector.py
- 기간을 입력하면 해당 기간 내의 KRX 종목 주가 데이터를 수집하여 CSV 파일로 변환하여 저장하는 코드 입니다.
