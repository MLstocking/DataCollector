from datetime import datetime, timedelta
from pytz import timezone
import FinanceDataReader as fdr

'''
todayPrice2csv 함수 설명
기능: 오늘 하루 동안의 KRX 종목 주가 데이터를 수집하여 json파일로 저장한다. 
'''
def todayPrice2json():
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
        daily_price = fdr.DataReader('KRX', today, yesterday)
        print(daily_price.head())
        daily_price.drop(columns=['Change'], axis=1, inplace=True)
        daily_price.reset_index(inplace=True)
        daily_price.rename(columns={'index': 'Date'}, inplace=True)

        # csv 파일로 저장
        # daily_price.to_csv("daily_price_"+today+".csv", index=False)

        # json 파일로 저장
        daily_price.to_json("daily_price_" + today + ".json", orient='table')

    else:
        print("No data occurs on weekends.")

# def isChangeList():
#     company_info = fdr.StockListing('KRX')


if __name__ == '__main__':
    todayPrice2json()
