# import FinanceDataReader as fdr
# import pandas as pd
# pd.set_option('display.max_columns', 50)
#
# # KRX delisting stock data 상장폐지 종목 데이터 (상장일~상장폐지일)
# df = fdr.DataReader('036360', exchange='krx-delisting')
# print(df)
# # KRX stock delisting symbol list and names 상장폐지 종목 전체 리스트
# krx_delisting = fdr.StockListing('KRX-DELISTING')
# print(krx_delisting)
#
# tmp = fdr.DataReader('005930', '2020-01-01', '2020-01-03')
# print(tmp.head())
#
# tmp = fdr.StockListing('KRX')

from datetime import datetime, timedelta
from pytz import timezone
import pandas as pd
import FinanceDataReader as fdr

dateformat = '%Y-%m-%d'
today = datetime.now(timezone('Asia/Seoul'))
yesterday = today - timedelta(1)
today = today.strftime(dateformat)
yesterday = yesterday.strftime(dateformat)
print(today, yesterday)

daily_price = pd.read_csv("daily_price_2000.csv")
daily_price.to_csv("ttest_"+today+".csv", index=False)