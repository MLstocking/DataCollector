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
 2. 코드를 실행할 서버에서 cmd또는 terminal에 다음과 같은 명령어를 입력합니다.
 ```
 $python3 create_DB_Collection.py
 ```   
 
 

------------

### daily_price_collector.py
 코드를 돌린 날짜를 알아내어 그 당일의 KRX 종목 주가 데이터를 수집하여 CSV 파일로 변환하여 저장하는 코드 입니다.  
 
 

### period_price_collector.py
 기간을 입력하면 해당 기간 내의 KRX 종목 주가 데이터를 수집하여 CSV 파일로 변환하여 저장하는 코드 입니다.
 

- 사용법
1. collector.py를 사용하려면 "finanacedatareader"라는 패키지를 설치하여야 합니다.  
자세한 내용은 링크를 타고 들어가셔서 확인하시기 바랍니다.  
> https://github.com/FinanceData/FinanceDataReader
 ```
 $pip install finance-datareader
 ```  

1-1. financedatareader를 설치한 후에도 패키지 관련 오류가 난다면 tqdm 패키지가 설치 되었는지 확인하시기 바랍니다.
 ```
 $pip install tqdm  
 ```  

2. 패키지 설치 후 cmd 또는 terminal에 다음과 같은 명령어를 입력합니다.
 ```
 $python3 daily_price_collector.py
 ```  

------------

### insert_daily_price.py
 daily_price_collector.py의 결과물인 CSV파일을 create_DB_Collection.py의 결과물인 azure cosmosdb의 database안 container에 적재하는 코드 입니다.  

본인의 end point값과 primary key 값을 넣어주면 azure cosmosdb container에 CSV파일 데이터가 적재됩니다.  
 
 - 사용법 
 1. 본인의 end point값과 primary key 값을 config에 넣습니다.
 2. 코드를 실행할 서버에서 cmd또는 terminal에 다음과 같은 명령어를 입력합니다.
 ```
 $python3 insert_daily_price.py
 ```   

