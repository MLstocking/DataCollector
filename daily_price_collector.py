from datetime import datetime, timedelta
from pytz import timezone
import FinanceDataReader as fdr
import pandas as pd
from tqdm import tqdm

'''
KRX_list 함수
기능: 현재 KRX 종목 리스트를 반환합니다.
'''
def KRX_list():
    company_info = fdr.StockListing('KRX')
    company_info = company_info[['Symbol', 'Name']]
    company_info.rename(columns={'Symbol':'code', 'Name':'company'},inplace=True)

    # duplicate code(symbol) check
    if company_info.duplicated(['code']).sum() > 0:
        print("Duplicate value exists.")

    print(f'KRX_list shape:{company_info.shape}')
    company_info.to_csv("company_info.csv", index=False)
    print("KRX_list Download complete.")
    return company_info['code'].tolist()

'''
todayPrice2csv 함수
기능: 오늘 하루 동안의 KRX 종목 주가 데이터를 수집하여 csv파일로 저장합니다. 
'''
def todayPrice2csv():
    code = KRX_list()
    # 코드가 실행되는 당일과 작일(KST) 계산
    dateformat = '%Y-%m-%d'
    today = datetime.now(timezone('Asia/Seoul'))

    # weekday()함수: 요일 반환(0:월 1:화 2:수 3:목 4:금 5:토 6:일)
    if datetime.weekday(today) <= 4:
        yesterday = today - timedelta(1)
        today = today.strftime(dateformat)
        yesterday = yesterday.strftime(dateformat)
        # print(f'Today: {today} / Yesterday: {yesterday}')

        # 데이터 수집 및 전처리
        daily_price = []
        for cd in tqdm(code):
            tmp = fdr.DataReader(cd, yesterday, today)
            # insert code column
            tmp.insert(0, 'code', cd)
            daily_price.append(tmp)

        daily_price = pd.concat(daily_price)
        # drop 'Change' column
        daily_price.drop(columns=['Change'], axis=1, inplace=True)
        # 'Date' index to column
        daily_price.reset_index(inplace=True)
        daily_price.rename(columns={'index': 'Date'}, inplace=True)
        print(f'daily_price shape:{daily_price.shape}')

        # csv 파일로 저장
        # daily_price.to_csv("daily_price_" + today + ".csv", index=False)
        daily_price.to_csv("daily_price.csv", index=False)

    else:
        print("No data occurs on weekends.")

if __name__ == '__main__':
    todayPrice2csv()
