# DataCollector
- 머신러닝 기반 주가 예측 프로젝트의 데이터를 수집해옵니다.

- 파일 실행환경
1. Ubuntu Server 18.04 LTS version
2. Python 3.6.9 version

------------

### create_DB_Collection.py
 azure cosmosdb에 Database를 생성하고 container를 생성하는 코드 입니다.  
 
 
 본인의 end point값과 primary key 값을 넣어주면 azure cosmosdb에 Database와 container가 생성됩니다.
 
 - 사용법 
 1. 본인의 end point값과 primary key 값을 config에 넣습니다.
 2. 코드를 실행할 서버에서 cmd또는 terminal에 다음과 같은 명령어를 실행합니다.
 ```
 $python3 create_DB_Collection.py
 ``` 

------------

### daily_price_collector.py
 코드를 돌린 날짜를 알아내어 그 당일의 KRX 종목 주가 데이터를 수집하여 CSV 파일로 변환하여 저장하는 코드 입니다.

------------

### insert_daily_price.py
 daily_price_collector.py의 결과물인 CSV파일을 create_DB_Collection.py의 결과물인 azure cosmosdb의 database안 container에 적재하는 코드 입니다. 

------------

### period_price_collector.py
 기간을 입력하면 해당 기간 내의 KRX 종목 주가 데이터를 수집하여 CSV 파일로 변환하여 저장하는 코드 입니다.
