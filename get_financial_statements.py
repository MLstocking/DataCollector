import numpy as np
import OpenDartReader
import pandas as pd
import re
from azure.cosmos import CosmosClient
import json
import sys


# 여러 해의 분기별 보고서 concatenation
def concat_years_report(code, opt, start, end):
    # DART API key 입력
    api_key = ""
    dart = OpenDartReader(api_key)

    start_year = int(start[:4]) - 1
    end_year = int(end[:4])
    dividend = []
    for y in range(start_year, end_year + 1):
        dividend.append(dart.report(code, opt, y, '11013'))
        dividend.append(dart.report(code, opt, y, '11012'))
        dividend.append(dart.report(code, opt, y, '11014'))
        dividend.append(dart.report(code, opt, y, '11011'))

    print('Report loaded successfully.')
    return pd.concat(dividend)


# 여러 해의 분기별 재무 정보 concatenation
def concat_years_fs(code, start, end):
    # DART API key 입력
    api_key = ""
    dart = OpenDartReader(api_key)

    start_year = int(start[:4]) - 1
    end_year = int(end[:4])
    fs = []
    for y in range(start_year, end_year + 1):
        fs.append(dart.finstate_all(code, y, '11013'))
        fs.append(dart.finstate_all(code, y, '11012'))
        try:
            fs.append(dart.finstate_all(code, y, '11014'))
        except:
            pass
        try:
            fs.append(dart.finstate_all(code, y, '11011'))
        except:
            pass
    print('financial statement loaded successfully.')
    return pd.concat(fs)


# 가격 데이터의 타입을 float으로 변경
def dtype2float(val):
    if val == '-':
        return np.nan
    elif val == ' ':
        return np.nan
    elif val == '':
        return np.nan
    else:
        return float(re.sub(",", "", val))


# 보고서 번호를 날짜로 변경
def rcept_no2date(val):
    val = val[:8]
    return pd.to_datetime(val)

# DB에 있는 주가 데이터 가져오기
def get_stockprice(code, start, end):

    config = {
        "endpoint": "",
        "primarykey": ""
    }

    client = CosmosClient(config["endpoint"], config["primarykey"])

    database_name = 'MLStocking'
    database = client.get_database_client(database_name)
    container_name = 'daily_price'
    container = database.get_container_client(container_name)

    # Query
    q = f'''
    SELECT p.Date, p.code, p.Close
    FROM daily_price p
    WHERE p.code = @code
    AND (p.Date BETWEEN @start AND @end)
    '''

    # Get the number of items in daily_price container
    items = container.query_items(
        query=q,
        parameters=[
            {"name": "@code", "value": code},
            {"name": "@start", "value": start},
            {"name": "@end", "value": end}
        ],
        enable_cross_partition_query=True)

    json_list = []
    for item in items:
        json_list.append(item)

    stockprice = pd.DataFrame.from_records(json_list)

    print('Stock price loaded successfully.')
    return stockprice[['Date', 'code', 'Close']]


def insert_fs(df):
    for col in df.columns:
        df[col] = df[col].astype(str)

    config = {
        "endpoint": "",
        "primarykey": ""
    }

    client = CosmosClient(config["endpoint"], config["primarykey"])

    database_name = 'MLStocking'
    database = client.get_database_client(database_name)
    container_name = 'financial_statement'
    container = database.get_container_client(container_name)

    # Get the number of items in daily_price container
    continued_items = container.query_items(
        query='SELECT VALUE COUNT(1) FROM financial_statement',
        enable_cross_partition_query=True)

    for item in continued_items:
        records_cnt = json.dumps(item, indent=True)

    item_cnt = int(records_cnt)

    # Cosmos DB needs one column named 'id'.
    new_id = [x for x in range(item_cnt, item_cnt + len(df))]
    df['id'] = new_id

    # Convert the id column to a string - this is a document database.
    df['id'] = df['id'].astype(str)

    # Write rows of a pandas DataFrame as items to the Database Container
    for i in range(0, df.shape[0]):
        # create a dictionary for the selected row
        data_dict = dict(df.iloc[i, :])
        # convert the dictionary to a json object.
        data_dict = json.dumps(data_dict)
        insert_data = container.upsert_item(json.loads(data_dict))

    print('Records inserted successfully.')


# 발행주식수 계산
def calc_num_shares(fs, dividend):
    num_shares = pd.merge(fs[fs['account_nm'] == '보통주자본금'],
                          dividend[dividend['se'] == '주당액면가액(원)'],
                          on='rcept_no',
                          how='outer')
    num_shares = num_shares[['rcept_no', 'thstrm_nm', 'account_nm', 'thstrm_amount', 'se', 'thstrm']]
    capital = num_shares['thstrm_amount']
    price = num_shares['thstrm']
    num_shares['ns'] = capital / price
    return num_shares[['rcept_no', 'ns']]


# EPS 계산
def calc_EPS(fs, num_shares):
    fs_income = fs[fs['account_nm'] == '당기순이익'].drop_duplicates(['rcept_no'], keep='first')
    EPS = pd.merge(fs_income, num_shares, on='rcept_no', how='outer')
    income = EPS['thstrm_amount']
    ns = EPS['ns']
    EPS['EPS'] = income / ns

    return EPS[['rcept_no', 'EPS']]


# PER 계산
def calc_PER(EPS, stockprice):
    stockprice['Date'] = pd.to_datetime(stockprice['Date'])
    EPS.columns = ['Date', 'EPS']
    PER = pd.concat([EPS, stockprice])

    PER.sort_values(by='Date', ascending=True, inplace=True)
    PER['EPS'].fillna(method='ffill', inplace=True)
    PER.dropna(subset=['Close'], inplace=True)
    eps = PER['EPS']
    close = PER['Close']
    PER['PER'] = close / eps

    return PER[['Date', 'PER']]


# BPS 계산
def calc_BPS(fs, num_shares):
    captotal = fs[fs['account_nm'] == '자본총계']
    BPS = pd.merge(captotal, num_shares[['rcept_no', 'ns']], on='rcept_no', how='outer')
    amount = BPS['thstrm_amount']
    ns = BPS['ns']
    BPS['BPS'] = amount / ns

    return BPS[['rcept_no', 'BPS']]


# PBR 계산
def calc_PBR(BPS, stockprice):
    stockprice['Date'] = pd.to_datetime(stockprice['Date'])
    BPS.columns = ['Date', 'BPS']
    PBR = pd.concat([BPS, stockprice])

    PBR.sort_values(by='Date', ascending=True, inplace=True)
    PBR['BPS'].fillna(method='ffill', inplace=True)
    PBR.dropna(subset=['Close'], inplace=True)
    bps = PBR['BPS']
    close = PBR['Close']
    PBR['PBR'] = close / bps

    return PBR[['Date', 'code', 'PBR']]


def main(argv):
    code = argv[0]
    start = argv[1]
    end = argv[2]

    # 보고서 데이터 정제
    dividend = concat_years_report(code, '배당', start, end)
    dividend = dividend[['rcept_no', 'corp_name', 'se', 'thstrm', 'stock_knd']]
    dividend['thstrm'] = dividend['thstrm'].apply(dtype2float)
    dividend['rcept_no'] = dividend['rcept_no'].apply(rcept_no2date)

    # 재무 정보 데이터 정제
    fs = concat_years_fs(code, start, end)
    fs = fs[['rcept_no', 'reprt_code', 'account_nm', 'thstrm_nm', 'thstrm_amount']]
    fs['thstrm_amount'] = fs['thstrm_amount'].apply(dtype2float)
    fs['rcept_no'] = fs['rcept_no'].apply(rcept_no2date)

    # 주가 데이터 가져오기
    stockprice = get_stockprice(code, start, end)

    # 발행주식수 계산
    num_shares = calc_num_shares(fs, dividend)
    # EPS 계산
    EPS = calc_EPS(fs, num_shares)
    # PER 계산
    PER = calc_PER(EPS, stockprice)
    # BPS 계산
    BPS = calc_BPS(fs, num_shares)
    # PBR 계산
    PBR = calc_PBR(BPS, stockprice)

    # merge
    PBR['PER'] = PER['PER']
    # ROE 계산
    PBR['ROE'] = PBR['PBR'] / PER['PER']

    # DB에 적재
    insert_fs(PBR)


if __name__ == "__main__":
    # main("005930", "2019-07-01", "2019-12-31")
    main(sys.argv[1:])
